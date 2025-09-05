#!/usr/bin/env python3
"""
Database initialization script for Wellspring Mountain Booking System

Run this script to initialize the database and seed it with initial lodging data.
This is useful for initial setup or resetting the database.
"""

from database.models import initialize_database, seed_initial_data

def main():
    print("Initializing Wellspring Mountain Booking Database...")
    
    try:
        # Initialize database schema
        print("Creating database tables...")
        initialize_database()
        print("✅ Database tables created successfully")
        
        # Seed initial data
        print("Seeding initial lodging data...")
        seed_initial_data()
        print("✅ Initial data seeded successfully")
        
        print("\n🎉 Database initialization complete!")
        print("\nYou can now run the application with: streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())