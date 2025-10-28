#!/usr/bin/env python3
"""
Fix facility names and make non-bookable facilities inactive for booking
"""

import sqlite3
import sys

def fix_facilities():
    """Fix duplicate location names and make facilities non-bookable"""

    conn = sqlite3.connect('wellspring_bookings.db')
    cursor = conn.cursor()

    print("Fixing facility names and bookability...")
    print("=" * 80)

    # 1. Remove duplicate location from cabin names
    # The location is already in the "location" column, so names like
    # "Downtown Cabin 1 (Woodshed)" showing as "... (Downtown)" is redundant
    name_fixes = {
        # These names are fine - they have descriptive names in parens, not locations
        # We just need to make sure facilities aren't bookable
    }

    # 2. Make facilities (capacity = 0) non-bookable by setting is_active = 0
    # Keep them in the system for property management, but not for guest booking

    print("\n1. Deactivating facilities (capacity 0) from guest booking...")
    print("-" * 80)

    # Get all capacity 0 units
    cursor.execute("""
        SELECT id, name, location, type
        FROM lodging_units
        WHERE capacity = 0 AND is_active = 1
    """)

    facilities = cursor.fetchall()

    if facilities:
        print(f"Found {len(facilities)} facilities to deactivate from guest booking:")
        for fac_id, name, location, fac_type in facilities:
            print(f"  - {name} ({location})")

        # Deactivate them
        cursor.execute("""
            UPDATE lodging_units
            SET is_active = 0
            WHERE capacity = 0
        """)

        print(f"\n[OK] Deactivated {len(facilities)} facilities from guest booking")
        print("    (They remain in property management)")
    else:
        print("No facilities need deactivation")

    # 3. Remove "(Facilities)" suffix from names as it's redundant with location
    print("\n2. Cleaning up facility name suffixes...")
    print("-" * 80)

    name_cleanups = [
        ("Showerhouse (Facilities)", "Showerhouse"),
        ("Dining Hall (Facilities)", "Dining Hall"),
        ("Lodge Upstairs (Facilities)", "Lodge Upstairs"),
        ("Lodge Downstairs (Facilities)", "Lodge Downstairs"),
        ("Uptown Cabins Area (Facilities)", "Uptown Common Area"),
    ]

    for old_name, new_name in name_cleanups:
        cursor.execute("""
            UPDATE lodging_units
            SET name = ?
            WHERE name = ?
        """, (new_name, old_name))

        if cursor.rowcount > 0:
            print(f"  - Renamed: '{old_name}' -> '{new_name}'")

    # 4. Verify Artist Studio stays bookable (it has capacity 1)
    print("\n3. Verifying bookable units with capacity > 0...")
    print("-" * 80)

    cursor.execute("""
        SELECT COUNT(*)
        FROM lodging_units
        WHERE capacity > 0 AND is_active = 1
    """)
    bookable_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT name, location, capacity
        FROM lodging_units
        WHERE capacity > 0 AND is_active = 1 AND location = 'Facilities'
    """)

    bookable_facilities = cursor.fetchall()
    if bookable_facilities:
        print(f"Bookable units in Facilities location:")
        for name, location, capacity in bookable_facilities:
            print(f"  - {name}: capacity {capacity}")

    print(f"\nTotal bookable units: {bookable_count}")

    # Commit changes
    conn.commit()

    # Show final summary
    print("\n" + "=" * 80)
    print("SUMMARY OF ALL UNITS")
    print("=" * 80)

    cursor.execute("""
        SELECT location,
               COUNT(*) as total,
               SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) as bookable,
               SUM(CASE WHEN is_active = 0 THEN 1 ELSE 0 END) as facility_only
        FROM lodging_units
        GROUP BY location
        ORDER BY location
    """)

    print(f"\n{'Location':<20} {'Total':<8} {'Bookable':<10} {'Facility Only':<15}")
    print("-" * 80)

    for location, total, bookable, facility_only in cursor.fetchall():
        print(f"{location:<20} {total:<8} {bookable:<10} {facility_only:<15}")

    cursor.execute("SELECT COUNT(*) FROM lodging_units WHERE is_active = 1")
    total_bookable = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM lodging_units WHERE is_active = 0")
    total_facilities = cursor.fetchone()[0]

    print("-" * 80)
    print(f"{'TOTAL':<20} {total_bookable + total_facilities:<8} {total_bookable:<10} {total_facilities:<15}")

    conn.close()

    print("\n[OK] All fixes applied successfully!")
    return True

if __name__ == "__main__":
    try:
        fix_facilities()
    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
