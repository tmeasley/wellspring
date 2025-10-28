#!/usr/bin/env python3
"""
Remove Lodge Shared Room and reorganize room display order
"""

import sqlite3
import sys

def reorganize_rooms():
    """Remove Lodge Shared Room and set display order"""

    conn = sqlite3.connect('wellspring_bookings.db')
    cursor = conn.cursor()

    print("Reorganizing rooms...")
    print("=" * 80)

    # 1. Remove Lodge Shared Room
    print("\n1. Removing Lodge Shared Room...")
    print("-" * 80)

    cursor.execute("SELECT id, name FROM lodging_units WHERE name = 'Lodge Shared Room'")
    shared_room = cursor.fetchone()

    if shared_room:
        room_id, room_name = shared_room
        print(f"Found: {room_name} (ID: {room_id})")

        # Check if it has any bookings
        cursor.execute("""
            SELECT COUNT(*) FROM booking_requests
            WHERE lodging_unit_id = ? AND status IN ('pending', 'confirmed')
        """, (room_id,))
        booking_count = cursor.fetchone()[0]

        if booking_count > 0:
            print(f"WARNING: This room has {booking_count} active bookings!")
            print("Setting to inactive instead of deleting...")
            cursor.execute("UPDATE lodging_units SET is_active = 0 WHERE id = ?", (room_id,))
        else:
            print("No active bookings - safe to delete")
            cursor.execute("DELETE FROM lodging_units WHERE id = ?", (room_id,))

        print(f"[OK] Lodge Shared Room removed")
    else:
        print("Lodge Shared Room not found - already removed")

    # 2. Check if display_order column exists, if not add it
    print("\n2. Adding display_order column if needed...")
    print("-" * 80)

    cursor.execute("PRAGMA table_info(lodging_units)")
    columns = [col[1] for col in cursor.fetchall()]

    if 'display_order' not in columns:
        print("Adding display_order column...")
        cursor.execute("ALTER TABLE lodging_units ADD COLUMN display_order INTEGER DEFAULT 999")
        print("[OK] Column added")
    else:
        print("display_order column already exists")

    # 3. Set display order: Lodge rooms/dorm first, then Uptown cabins, then others
    print("\n3. Setting display order...")
    print("-" * 80)

    # Order:
    # 1-10: Lodge rooms and dorm
    # 11-15: Uptown cabins (5 cabins)
    # 100+: Everything else (let them sort alphabetically within location)

    display_order_map = {
        # Lodge - priority 1-10
        "Lodge Room 1": 1,
        "Lodge Room 2": 2,
        "Lodge Room 3": 3,
        "Lodge Room 4": 4,
        "Lodge Room 5": 5,
        "Lodge Room 6": 6,
        "Lodge Room 7": 7,
        "Lodge Dormroom": 8,

        # Uptown - priority 11-15
        "Uptown Cabin 1": 11,
        "Uptown Cabin 2": 12,
        "Uptown Cabin 3": 13,
        "Uptown Cabin 4": 14,
        "Uptown Cabin 5": 15,
    }

    for name, order in display_order_map.items():
        cursor.execute("""
            UPDATE lodging_units
            SET display_order = ?
            WHERE name = ?
        """, (order, name))

        if cursor.rowcount > 0:
            print(f"  {order:3d}. {name}")

    # 4. Update get_available_units and similar queries to use display_order
    print("\n4. Current room listing (ordered)...")
    print("-" * 80)

    cursor.execute("""
        SELECT name, location, capacity, display_order, is_active
        FROM lodging_units
        WHERE is_active = 1
        ORDER BY display_order, location, name
    """)

    bookable_rooms = cursor.fetchall()

    print(f"\n{'Order':<8} {'Name':<40} {'Location':<15} {'Capacity':<10}")
    print("-" * 80)

    for name, location, capacity, order, active in bookable_rooms:
        print(f"{order:<8} {name:<40} {location:<15} {capacity:<10}")

    print(f"\nTotal bookable rooms: {len(bookable_rooms)}")

    # Commit changes
    conn.commit()
    conn.close()

    print("\n[OK] All reorganization complete!")
    return True

if __name__ == "__main__":
    try:
        reorganize_rooms()
    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
