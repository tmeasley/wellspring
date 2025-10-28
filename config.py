"""
Configuration and environment validation for Wellspring Mountain Booking System
"""
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

class Config:
    """Application configuration with validation"""

    # Required environment variables
    PUBLIC_PASSWORD = os.getenv("PUBLIC_PASSWORD")
    STAFF_PASSWORD = os.getenv("STAFF_PASSWORD")

    # Optional configuration
    DATABASE_PATH = os.getenv("DATABASE_PATH", "wellspring_bookings.db")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

    # Streamlit configuration
    APP_TITLE = "Wellspring Mountain Booking System"
    APP_ICON = "🏔️"

    @classmethod
    def validate(cls) -> bool:
        """Validate that all required environment variables are set"""
        errors = []

        if not cls.PUBLIC_PASSWORD:
            errors.append("PUBLIC_PASSWORD is not set in .env file")

        if not cls.STAFF_PASSWORD:
            errors.append("STAFF_PASSWORD is not set in .env file")

        if errors:
            print("\n[ERROR] Configuration Error:")
            for error in errors:
                print(f"  - {error}")
            print("\nPlease create a .env file with the required variables.")
            print("See .env.example for reference.\n")
            return False

        return True

    @classmethod
    def display_config_info(cls):
        """Display configuration information (for debugging)"""
        if cls.DEBUG_MODE:
            print("=" * 50)
            print("Configuration Info:")
            print(f"  Database Path: {cls.DATABASE_PATH}")
            print(f"  Debug Mode: {cls.DEBUG_MODE}")
            print(f"  Public Password Set: {'YES' if cls.PUBLIC_PASSWORD else 'NO'}")
            print(f"  Staff Password Set: {'YES' if cls.STAFF_PASSWORD else 'NO'}")
            print("=" * 50)

# Validate configuration on import (only in production mode)
if __name__ != "__main__":
    if not Config.validate():
        print("\nStarting with default passwords. Please set up your .env file.")
        print("Default passwords:")
        print("  PUBLIC_PASSWORD: public123")
        print("  STAFF_PASSWORD: staff123\n")

def check_environment():
    """Check and report environment status"""
    is_valid = Config.validate()
    Config.display_config_info()
    return is_valid

if __name__ == "__main__":
    print("Wellspring Mountain - Configuration Check")
    print("=" * 50)
    if check_environment():
        print("\n[SUCCESS] All environment variables are properly configured!")
    else:
        print("\n[WARNING] Some configuration issues detected.")
        print("The application will use default values where possible.")
    print("=" * 50)
