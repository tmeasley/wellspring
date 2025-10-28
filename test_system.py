"""
Wellspring Mountain Booking System - Test Suite
Run basic functionality tests on the system
"""

import sys
import os
from datetime import date, timedelta

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_initialization():
    """Test database initialization"""
    print("\n[TEST] Database Initialization...")
    try:
        from database.models import initialize_database, seed_initial_data
        initialize_database()
        seed_initial_data()
        print("  [PASS] Database initialized successfully")
        return True
    except Exception as e:
        print(f"  [FAIL] Database initialization failed: {e}")
        return False

def test_lodging_units():
    """Test lodging units retrieval"""
    print("\n[TEST] Lodging Units Operations...")
    try:
        from database.operations import BookingOperations
        units = BookingOperations.get_all_lodging_units()
        assert len(units) > 0, "No lodging units found"
        assert all('id' in unit and 'name' in unit for unit in units), "Missing required fields"
        print(f"  [PASS] Found {len(units)} lodging units")
        return True
    except Exception as e:
        print(f"  [FAIL] Lodging units test failed: {e}")
        return False

def test_booking_operations():
    """Test booking operations"""
    print("\n[TEST] Booking Operations...")
    try:
        from database.operations import BookingOperations

        # Test booking summary
        summary = BookingOperations.get_booking_summary()
        assert 'total_units' in summary, "Missing total_units in summary"
        assert 'pending_bookings' in summary, "Missing pending_bookings in summary"
        print(f"  [PASS] Booking summary: {summary}")

        # Test creating a booking
        test_booking = {
            'guest_name': 'Test User',
            'email': 'test@example.com',
            'phone': '555-1234',
            'booking_type': 'respite',
            'check_in': date.today() + timedelta(days=7),
            'check_out': date.today() + timedelta(days=10),
            'guests': 2,
            'lodging_unit_id': 1,
            'special_requests': 'Test booking',
            'notes': 'Automated test'
        }

        booking_id = BookingOperations.create_booking_request(test_booking)
        assert booking_id > 0, "Failed to create booking"
        print(f"  [PASS] Created test booking ID: {booking_id}")

        # Test retrieving bookings
        bookings = BookingOperations.get_all_booking_requests()
        assert len(bookings) > 0, "No bookings found"
        print(f"  [PASS] Retrieved {len(bookings)} bookings")

        # Test updating booking status
        success = BookingOperations.update_booking_status(booking_id, 'confirmed', 'Test confirmation')
        assert success, "Failed to update booking status"
        print(f"  [PASS] Updated booking status")

        # Clean up test booking
        BookingOperations.update_booking_status(booking_id, 'cancelled', 'Test cleanup')
        print(f"  [PASS] Cleaned up test booking")

        return True
    except Exception as e:
        print(f"  [FAIL] Booking operations test failed: {e}")
        return False

def test_property_management():
    """Test property management operations"""
    print("\n[TEST] Property Management Operations...")
    try:
        from database.property_operations import PropertyManagementOperations

        # Test dashboard summary
        summary = PropertyManagementOperations.get_property_dashboard_summary()
        assert isinstance(summary, dict), "Dashboard summary should be a dict"
        print(f"  [PASS] Property dashboard summary: {summary}")

        # Test creating a note
        note_id = PropertyManagementOperations.create_property_note(
            unit_id=1,
            note_type='general',
            title='Test Note',
            content='This is a test note',
            priority='low'
        )
        assert note_id > 0, "Failed to create property note"
        print(f"  [PASS] Created test property note ID: {note_id}")

        # Test creating a maintenance task
        task_id = PropertyManagementOperations.create_maintenance_task(
            unit_id=1,
            title='Test Maintenance',
            description='Test maintenance task',
            task_type='general_maintenance',
            priority='low',
            scheduled_date=date.today() + timedelta(days=7)
        )
        assert task_id > 0, "Failed to create maintenance task"
        print(f"  [PASS] Created test maintenance task ID: {task_id}")

        # Test retrieving tasks
        tasks = PropertyManagementOperations.get_maintenance_tasks()
        assert len(tasks) > 0, "No maintenance tasks found"
        print(f"  [PASS] Retrieved {len(tasks)} maintenance tasks")

        # Test creating a todo
        todo_id = PropertyManagementOperations.create_todo(
            title='Test Todo',
            description='Test todo item',
            priority='low',
            category='general'
        )
        assert todo_id > 0, "Failed to create todo"
        print(f"  [PASS] Created test todo ID: {todo_id}")

        return True
    except Exception as e:
        print(f"  [FAIL] Property management test failed: {e}")
        return False

def test_configuration():
    """Test configuration and environment"""
    print("\n[TEST] Configuration...")
    try:
        from config import Config

        # Test that config can be loaded
        assert hasattr(Config, 'PUBLIC_PASSWORD'), "Missing PUBLIC_PASSWORD"
        assert hasattr(Config, 'STAFF_PASSWORD'), "Missing STAFF_PASSWORD"
        print(f"  [PASS] Configuration loaded successfully")

        # Test validation (should not fail if defaults are used)
        is_valid = Config.validate()
        if is_valid:
            print(f"  [PASS] Configuration is valid")
        else:
            print(f"  [WARN] Configuration using defaults")

        return True
    except Exception as e:
        print(f"  [FAIL] Configuration test failed: {e}")
        return False

def test_helpers():
    """Test helper functions"""
    print("\n[TEST] Helper Functions...")
    try:
        from utils.helpers import sanitize_input, format_booking_status, format_date_range

        # Test sanitize_input
        test_input = "Test <script>alert('xss')</script>"
        sanitized = sanitize_input(test_input, 100)
        assert '<script>' not in sanitized, "XSS not sanitized"
        print(f"  [PASS] Input sanitization working")

        # Test format_booking_status
        status_html = format_booking_status('confirmed')
        assert 'confirmed' in status_html.lower(), "Status formatting failed"
        print(f"  [PASS] Status formatting working")

        # Test format_date_range
        start = date(2024, 1, 1)
        end = date(2024, 1, 5)
        date_range = format_date_range(start, end)
        # Jan 1 to Jan 5 is 4 nights (4 days duration)
        assert '4 nights' in date_range or '4 night' in date_range, f"Date range calculation failed: got '{date_range}'"
        print(f"  [PASS] Date range formatting working: {date_range}")

        return True
    except Exception as e:
        print(f"  [FAIL] Helper functions test failed: {e}")
        return False

def test_availability():
    """Test availability checking"""
    print("\n[TEST] Availability Checking...")
    try:
        from database.operations import BookingOperations

        # Test with a unit that should be available
        check_in = date.today() + timedelta(days=30)
        check_out = date.today() + timedelta(days=33)

        is_available = BookingOperations.check_availability(1, check_in, check_out)
        print(f"  [INFO] Availability check result: {is_available}")
        print(f"  [PASS] Availability checking functional")

        return True
    except Exception as e:
        print(f"  [FAIL] Availability test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Wellspring Mountain Booking System - Test Suite")
    print("=" * 60)

    tests = [
        test_database_initialization,
        test_configuration,
        test_lodging_units,
        test_booking_operations,
        test_property_management,
        test_helpers,
        test_availability
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n[ERROR] Test crashed: {e}")
            results.append(False)

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Tests Failed: {total - passed}/{total}")

    if passed == total:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print("\n[FAILURE] Some tests failed.")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
