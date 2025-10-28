import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

DATABASE_PATH = "wellspring_bookings.db"

def get_db_connection():
    """Create and return database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
    return conn

def initialize_database():
    """Create database tables if they don't exist"""
    conn = get_db_connection()
    
    # Create lodging_units table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS lodging_units (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            location VARCHAR(50) NOT NULL,
            type VARCHAR(50) NOT NULL,
            capacity INTEGER NOT NULL,
            description TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create booking_requests table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS booking_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_name VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL,
            phone VARCHAR(20),
            booking_type VARCHAR(20) NOT NULL,
            check_in DATE NOT NULL,
            check_out DATE NOT NULL,
            guests INTEGER NOT NULL,
            lodging_unit_id INTEGER,
            status VARCHAR(20) DEFAULT 'pending',
            notes TEXT,
            special_requests TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lodging_unit_id) REFERENCES lodging_units (id)
        )
    """)
    
    # Create availability_calendar table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS availability_calendar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lodging_unit_id INTEGER NOT NULL,
            date DATE NOT NULL,
            is_available BOOLEAN DEFAULT 1,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lodging_unit_id) REFERENCES lodging_units (id),
            UNIQUE(lodging_unit_id, date)
        )
    """)
    
    # Property management tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS property_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lodging_unit_id INTEGER NOT NULL,
            note_type VARCHAR(50) NOT NULL,
            title VARCHAR(200) NOT NULL,
            content TEXT NOT NULL,
            priority VARCHAR(20) DEFAULT 'medium',
            created_by VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lodging_unit_id) REFERENCES lodging_units (id)
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lodging_unit_id INTEGER NOT NULL,
            task_title VARCHAR(200) NOT NULL,
            description TEXT,
            task_type VARCHAR(50) NOT NULL,
            priority VARCHAR(20) DEFAULT 'medium',
            status VARCHAR(20) DEFAULT 'pending',
            scheduled_date DATE,
            completed_date DATE,
            assigned_to VARCHAR(100),
            estimated_cost DECIMAL(10,2),
            actual_cost DECIMAL(10,2),
            created_by VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lodging_unit_id) REFERENCES lodging_units (id)
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS property_todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lodging_unit_id INTEGER,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            priority VARCHAR(20) DEFAULT 'medium',
            status VARCHAR(20) DEFAULT 'pending',
            due_date DATE,
            assigned_to VARCHAR(100),
            category VARCHAR(50),
            created_by VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (lodging_unit_id) REFERENCES lodging_units (id)
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS property_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lodging_unit_id INTEGER NOT NULL,
            file_name VARCHAR(255) NOT NULL,
            file_type VARCHAR(50) NOT NULL,
            file_category VARCHAR(50) NOT NULL,
            file_path VARCHAR(500) NOT NULL,
            file_size INTEGER,
            description TEXT,
            uploaded_by VARCHAR(100),
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lodging_unit_id) REFERENCES lodging_units (id)
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS property_inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lodging_unit_id INTEGER NOT NULL,
            inspection_type VARCHAR(50) NOT NULL,
            inspection_date DATE NOT NULL,
            inspector_name VARCHAR(100),
            overall_rating INTEGER CHECK(overall_rating BETWEEN 1 AND 5),
            checklist_data TEXT,
            issues_found TEXT,
            recommendations TEXT,
            next_inspection_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lodging_unit_id) REFERENCES lodging_units (id)
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lodging_unit_id INTEGER NOT NULL,
            schedule_name VARCHAR(200) NOT NULL,
            task_type VARCHAR(50) NOT NULL,
            frequency VARCHAR(50) NOT NULL,
            next_due_date DATE NOT NULL,
            last_completed DATE,
            description TEXT,
            estimated_cost DECIMAL(10,2),
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lodging_unit_id) REFERENCES lodging_units (id)
        )
    """)
    
    conn.commit()
    conn.close()

def seed_initial_data():
    """Add initial lodging units to the database"""
    conn = get_db_connection()
    
    # Check if data already exists
    cursor = conn.execute("SELECT COUNT(*) FROM lodging_units")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return  # Data already seeded
    
    # Lodge accommodations
    lodge_units = [
        # Downstairs
        ("Lodge Room 1", "Lodge", "private", 1, "Private room downstairs"),
        ("Lodge Room 2", "Lodge", "private", 1, "Private room downstairs"),
        ("Lodge Room 3", "Lodge", "private", 1, "Private room downstairs"),
        ("Lodge Room 4", "Lodge", "private", 1, "Private room downstairs"),
        ("Lodge Dormroom", "Lodge", "dorm", 6, "Dormroom with 3 bunkbeds downstairs"),
        # Upstairs
        ("Lodge Room 5", "Lodge", "private", 1, "Private room upstairs"),
        ("Lodge Room 6", "Lodge", "private", 1, "Private room upstairs"),
        ("Lodge Room 7", "Lodge", "private", 1, "Private room upstairs"),
        ("Lodge Shared Room", "Lodge", "shared", 4, "Shared room with 2 bunkbeds upstairs"),
    ]
    
    # Uptown cabins
    uptown_cabins = [
        (f"Uptown Cabin {i}", "Uptown", "private", 1, f"Private cabin {i} in Uptown area")
        for i in range(1, 6)
    ]
    
    # Downtown cabins
    downtown_cabins = [
        (f"Downtown Cabin {i}", "Downtown", "private", 1, f"Private cabin {i} in Downtown area")
        for i in range(1, 4)
    ]
    
    # A-frame camping cabins
    aframe_cabins = [
        (f"A-frame Cabin {i}", "A-frame", "camping", 3, f"Camping cabin {i} with 3 beds")
        for i in range(1, 5)
    ]
    
    # A-frame classroom
    classroom = [("A-frame Classroom", "A-frame", "classroom", 15, "Classroom space for up to 15 with instructor/guest loft")]
    
    # Combine all units
    all_units = lodge_units + uptown_cabins + downtown_cabins + aframe_cabins + classroom
    
    # Insert all units
    conn.executemany("""
        INSERT INTO lodging_units (name, location, type, capacity, description)
        VALUES (?, ?, ?, ?, ?)
    """, all_units)
    
    conn.commit()
    conn.close()

# Initialize database when module is imported
if __name__ == "__main__":
    initialize_database()
    seed_initial_data()
    print("Database initialized and seeded with initial data.")