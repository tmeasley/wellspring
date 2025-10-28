#!/usr/bin/env python3
"""
Migrate local SQLite database to Turso cloud database

IMPORTANT: Set environment variables before running:
  export USE_TURSO=true
  export TURSO_DATABASE_URL="your-turso-database-url"
  export TURSO_AUTH_TOKEN="your-turso-auth-token"

Or create a .env file with these variables.
"""

import os
import sys

# Check if Turso credentials are set
if not os.getenv("TURSO_DATABASE_URL") or not os.getenv("TURSO_AUTH_TOKEN"):
    print("ERROR: Turso credentials not found!")
    print("\nPlease set the following environment variables:")
    print("  TURSO_DATABASE_URL")
    print("  TURSO_AUTH_TOKEN")
    print("\nYou can either:")
    print("  1. Export them in your shell")
    print("  2. Create a .env file with these variables")
    print("  3. Pass them directly: TURSO_DATABASE_URL='...' TURSO_AUTH_TOKEN='...' python migrate_to_turso.py")
    sys.exit(1)

# Enable Turso mode
os.environ["USE_TURSO"] = "true"

from database.models import initialize_database, seed_initial_data
from database.connection import get_db_connection
import sqlite3

def migrate_data():
    """Migrate data from local SQLite to Turso"""

    print("=" * 80)
    print("MIGRATING TO TURSO CLOUD DATABASE")
    print("=" * 80)

    # Step 1: Initialize Turso database (create all tables)
    print("\nStep 1: Creating tables in Turso...")
    initialize_database()
    print("[OK] Tables created")

    # Step 2: Check if local database exists and has data
    local_db = "wellspring_bookings.db"
    if not os.path.exists(local_db):
        print(f"\n[INFO] No local database found at {local_db}")
        print("[INFO] Seeding initial data...")
        seed_initial_data()
        print("[OK] Initial data seeded")
        print("\n[SUCCESS] Turso database is ready!")
        return

    print(f"\nStep 2: Reading from local database: {local_db}")

    # Connect to local database
    local_conn = sqlite3.connect(local_db)
    local_conn.row_factory = sqlite3.Row

    # Connect to Turso database
    turso_conn = get_db_connection()

    # Tables to migrate (in order due to foreign keys)
    tables = [
        "lodging_units",
        "booking_requests",
        "property_notes",
        "maintenance_tasks",
        "property_todos",
        "property_files",
        "property_inspections",
        "maintenance_schedules"
    ]

    for table in tables:
        print(f"\n  Migrating table: {table}")

        try:
            # Get all rows from local table
            local_cursor = local_conn.execute(f"SELECT * FROM {table}")
            rows = local_cursor.fetchall()

            if not rows:
                print(f"    [SKIP] No data in {table}")
                continue

            # Get column names
            columns = [desc[0] for desc in local_cursor.description]

            # Prepare INSERT statement
            placeholders = ", ".join(["?" for _ in columns])
            column_names = ", ".join(columns)
            insert_sql = f"INSERT OR REPLACE INTO {table} ({column_names}) VALUES ({placeholders})"

            # Insert each row into Turso
            count = 0
            for row in rows:
                values = tuple(row[col] for col in columns)
                turso_conn.execute(insert_sql, values)
                count += 1

            turso_conn.commit()
            print(f"    [OK] Migrated {count} rows")

        except Exception as e:
            print(f"    [ERROR] Failed to migrate {table}: {e}")
            continue

    local_conn.close()
    turso_conn.close()

    print("\n" + "=" * 80)
    print("[SUCCESS] Migration complete!")
    print("=" * 80)
    print("\nYour Turso database is now populated with all data.")
    print("You can now deploy to Streamlit Cloud!")

if __name__ == "__main__":
    try:
        migrate_data()
    except Exception as e:
        print(f"\n[ERROR] Migration failed: {e}")
        sys.exit(1)
