"""
Production-ready database connection module
Supports both local SQLite and Turso cloud database
"""

import sqlite3
import os
import logging
from typing import Optional

# Try to import Turso client (optional for local development)
try:
    import libsql_client
    TURSO_AVAILABLE = True
except ImportError:
    TURSO_AVAILABLE = False
    logging.warning("libsql-client not installed. Turso support disabled.")

# Try to use Streamlit secrets, fall back to env vars
try:
    import streamlit as st
    USE_STREAMLIT = True
except ImportError:
    USE_STREAMLIT = False

class DatabaseConfig:
    """Database configuration from environment or Streamlit secrets"""

    @staticmethod
    def get(key: str, default: Optional[str] = None) -> Optional[str]:
        """Get config value from Streamlit secrets or environment"""
        if USE_STREAMLIT and hasattr(st, 'secrets'):
            try:
                return st.secrets.get(key, os.getenv(key, default))
            except:
                return os.getenv(key, default)
        return os.getenv(key, default)

    @property
    def use_turso(self) -> bool:
        """Check if Turso should be used"""
        return self.get("USE_TURSO", "false").lower() == "true" and TURSO_AVAILABLE

    @property
    def turso_url(self) -> Optional[str]:
        """Get Turso database URL"""
        return self.get("TURSO_DATABASE_URL")

    @property
    def turso_auth_token(self) -> Optional[str]:
        """Get Turso auth token"""
        return self.get("TURSO_AUTH_TOKEN")

    @property
    def local_db_path(self) -> str:
        """Get local database path"""
        return self.get("DATABASE_PATH", "wellspring_bookings.db")


# Global config instance
config = DatabaseConfig()


def get_db_connection():
    """
    Create and return database connection

    Automatically chooses between:
    - Turso cloud database (production)
    - Local SQLite database (development)

    Returns:
        Connection object with Row factory enabled
    """

    if config.use_turso:
        # Use Turso cloud database
        logging.info("Connecting to Turso cloud database")

        if not config.turso_url or not config.turso_auth_token:
            raise ValueError(
                "Turso credentials missing. Set TURSO_DATABASE_URL and TURSO_AUTH_TOKEN"
            )

        try:
            # Use HTTP URL instead of WebSocket for reliability
            http_url = config.turso_url.replace("libsql://", "https://")

            client = libsql_client.create_client_sync(
                url=http_url,
                auth_token=config.turso_auth_token
            )

            # Wrap Turso client to be compatible with sqlite3.Connection interface
            return TursoConnectionWrapper(client)

        except Exception as e:
            logging.error(f"Failed to connect to Turso: {e}")
            logging.warning("Falling back to local SQLite database")
            # Fall through to local database

    # Use local SQLite database
    logging.debug(f"Connecting to local SQLite database: {config.local_db_path}")
    conn = sqlite3.connect(config.local_db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


class TursoConnectionWrapper:
    """
    Wrapper to make Turso client compatible with sqlite3.Connection interface
    """

    def __init__(self, client):
        self.client = client
        self._row_factory = None

    @property
    def row_factory(self):
        return self._row_factory

    @row_factory.setter
    def row_factory(self, factory):
        self._row_factory = factory

    def execute(self, sql: str, parameters=None):
        """Execute SQL query"""
        try:
            if parameters:
                # Convert parameters tuple to list for Turso
                params = list(parameters) if isinstance(parameters, tuple) else parameters
                result = self.client.execute(sql, params)
            else:
                result = self.client.execute(sql)

            return TursoCursorWrapper(result, self._row_factory)
        except Exception as e:
            # Log the error for debugging
            logging.error(f"Turso execute error: {e}")
            # Return empty cursor on error
            class EmptyResult:
                rows = []
                columns = []
                rows_affected = 0
            return TursoCursorWrapper(EmptyResult(), self._row_factory)

    def executemany(self, sql: str, seq_of_parameters):
        """Execute SQL query multiple times with different parameters"""
        try:
            total_affected = 0
            for parameters in seq_of_parameters:
                # Convert parameters tuple to list for Turso
                params = list(parameters) if isinstance(parameters, tuple) else parameters
                result = self.client.execute(sql, params)
                # Track rows affected
                if hasattr(result, 'rows_affected'):
                    total_affected += result.rows_affected
                elif hasattr(result, '__dict__') and 'rows_affected' in result.__dict__:
                    total_affected += result.__dict__['rows_affected']

            # Return a cursor with the total rows affected
            class BatchResult:
                rows = []
                columns = []
                rows_affected = total_affected

            return TursoCursorWrapper(BatchResult(), self._row_factory)
        except Exception as e:
            logging.error(f"Turso executemany error: {e}")
            # Return empty cursor on error
            class EmptyResult:
                rows = []
                columns = []
                rows_affected = 0
            return TursoCursorWrapper(EmptyResult(), self._row_factory)

    def commit(self):
        """Commit transaction (Turso auto-commits)"""
        pass

    def close(self):
        """Close connection"""
        try:
            self.client.close()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class TursoCursorWrapper:
    """
    Wrapper to make Turso result compatible with sqlite3.Cursor interface
    """

    def __init__(self, result, row_factory=None):
        self.result = result
        self._row_factory = row_factory
        self._rows = None
        self._index = 0

        # Extract rows from result - handle different result formats
        if hasattr(result, 'rows'):
            self._rows = result.rows
        elif hasattr(result, '__dict__') and 'rows' in result.__dict__:
            self._rows = result.__dict__['rows']
        elif isinstance(result, dict) and 'rows' in result:
            self._rows = result['rows']
        else:
            self._rows = []

    @property
    def rowcount(self):
        """Number of rows affected"""
        if hasattr(self.result, 'rows_affected'):
            return self.result.rows_affected
        elif hasattr(self.result, '__dict__') and 'rows_affected' in self.result.__dict__:
            return self.result.__dict__['rows_affected']
        elif isinstance(self.result, dict) and 'rows_affected' in self.result:
            return self.result['rows_affected']
        return len(self._rows) if self._rows else 0

    def fetchone(self):
        """Fetch one row"""
        if self._index < len(self._rows):
            row = self._rows[self._index]
            self._index += 1

            if self._row_factory == sqlite3.Row:
                # Convert to dict-like Row object
                columns = self._get_columns()
                return DictRow(dict(zip(columns, row)))
            return row

        return None

    def fetchall(self):
        """Fetch all rows"""
        if self._row_factory == sqlite3.Row:
            columns = self._get_columns()
            return [DictRow(dict(zip(columns, row))) for row in self._rows]

        return self._rows

    def _get_columns(self):
        """Get column names from result"""
        if hasattr(self.result, 'columns'):
            return self.result.columns
        elif hasattr(self.result, '__dict__') and 'columns' in self.result.__dict__:
            return self.result.__dict__['columns']
        elif isinstance(self.result, dict) and 'columns' in self.result:
            return self.result['columns']
        return []


class DictRow(dict):
    """
    Dictionary that also supports attribute access
    Compatible with sqlite3.Row interface
    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        self[key] = value
