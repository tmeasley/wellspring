"""
Update Wellspring Mountain facilities with correct information
"""
import sqlite3
from database.models import get_db_connection

def update_facilities():
    """Update all facilities with correct names and information"""
    conn = get_db_connection()
    cursor = conn.cursor()

    print("Updating Wellspring Mountain facilities...")

    # First, clear existing data
    cursor.execute("DELETE FROM lodging_units")
    print("[OK] Cleared old data")

    # RESIDENTIAL HOUSES (bookable)
    houses = [
        ("House 1 (Neighbor House)", "Residential", "house", 4, "Neighbor house residential unit"),
        ("House 2 (Easley House)", "Residential", "house", 4, "Easley house residential unit"),
    ]

    # LODGE - Bookable rooms
    lodge_rooms = [
        # Downstairs
        ("Lodge Room 1", "Lodge", "private", 1, "Private room downstairs"),
        ("Lodge Room 2", "Lodge", "private", 1, "Private room downstairs"),
        ("Lodge Room 3", "Lodge", "private", 1, "Private room downstairs"),
        ("Lodge Room 4", "Lodge", "private", 1, "Private room downstairs"),
        ("Lodge Dormroom", "Lodge", "dorm", 6, "Dormroom with space for 6 people (3 bunkbeds) downstairs"),
        # Upstairs
        ("Lodge Room 5", "Lodge", "private", 1, "Private room upstairs"),
        ("Lodge Room 6", "Lodge", "private", 1, "Private room upstairs"),
        ("Lodge Room 7", "Lodge", "private", 1, "Private room upstairs"),
        ("Lodge Shared Room", "Lodge", "shared", 4, "Shared room with 2 bunkbeds (4 people) upstairs"),
    ]

    # LODGE - Facilities (non-bookable)
    lodge_facilities = [
        ("Lodge Upstairs (Facilities)", "Lodge", "facility", 0, "Lodge upstairs common area and facilities"),
        ("Lodge Downstairs (Facilities)", "Lodge", "facility", 0, "Lodge downstairs common area and facilities"),
    ]

    # UPTOWN CABINS
    uptown_cabins = [
        (f"Uptown Cabin {i}", "Uptown", "private", 1, f"Private cabin {i} in Uptown area")
        for i in range(1, 6)
    ]
    uptown_facilities = [
        ("Uptown Cabins Area (Facilities)", "Uptown", "facility", 0, "Uptown cabins common area and facilities"),
    ]

    # DOWNTOWN CABINS - with correct names
    downtown_cabins = [
        ("Downtown Cabin 1 (Woodshed)", "Downtown", "private", 1, "Woodshed cabin"),
        ("Downtown Cabin 2 (Craft)", "Downtown", "private", 1, "Craft cabin"),
        ("Downtown Cabin 3 (Caboose)", "Downtown", "private", 1, "Caboose cabin"),
        ("Downtown Cabin 4 (Woodshop)", "Downtown", "private", 1, "Woodshop cabin"),
    ]

    # A-FRAME CAMPING CABINS
    aframe_cabins = [
        (f"A-frame Cabin {i}", "A-frame", "camping", 3, f"Camping cabin {i} with 3 beds")
        for i in range(1, 5)
    ]

    # FACILITIES - All shared spaces
    facilities = [
        ("A-frame Classroom", "Facilities", "classroom", 15, "Classroom space for up to 15 with instructor/guest loft"),
        ("Artist Studio", "Facilities", "studio", 1, "Artist studio with 1 bed"),
        ("Showerhouse (Facilities)", "Facilities", "facility", 0, "Community shower facilities"),
        ("Community Kitchen", "Facilities", "kitchen", 0, "Shared community kitchen"),
        ("Dining Hall (Facilities)", "Facilities", "facility", 0, "Community dining hall"),
        ("Laundry Room", "Facilities", "facility", 0, "Shared laundry facilities"),
        ("Apothecary", "Facilities", "facility", 0, "Apothecary and wellness space"),
        ("Shop", "Facilities", "facility", 0, "General shop and workspace"),
        ("Road Maintenance", "Facilities", "maintenance", 0, "Road maintenance and infrastructure"),
    ]

    # Combine all units
    all_units = (
        houses +
        lodge_rooms +
        lodge_facilities +
        uptown_cabins +
        uptown_facilities +
        downtown_cabins +
        aframe_cabins +
        facilities
    )

    # Insert all units
    cursor.executemany("""
        INSERT INTO lodging_units (name, location, type, capacity, description)
        VALUES (?, ?, ?, ?, ?)
    """, all_units)

    conn.commit()

    # Print summary
    print(f"\n[OK] Added {len(all_units)} total units:")
    print(f"  - {len(houses)} Residential Houses")
    print(f"  - {len(lodge_rooms)} Lodge Rooms (bookable)")
    print(f"  - {len(lodge_facilities)} Lodge Facilities")
    print(f"  - {len(uptown_cabins)} Uptown Cabins")
    print(f"  - {len(uptown_facilities)} Uptown Facilities")
    print(f"  - {len(downtown_cabins)} Downtown Cabins")
    print(f"  - {len(aframe_cabins)} A-frame Cabins")
    print(f"  - {len(facilities)} Common Facilities")

    # Verify
    cursor.execute("SELECT COUNT(*) FROM lodging_units")
    total = cursor.fetchone()[0]
    print(f"\n[OK] Total units in database: {total}")

    # Show breakdown by type
    cursor.execute("""
        SELECT type, COUNT(*) as count
        FROM lodging_units
        GROUP BY type
        ORDER BY count DESC
    """)
    print("\nBreakdown by type:")
    for row in cursor.fetchall():
        print(f"  - {row[0]}: {row[1]}")

    conn.close()
    print("\n[OK] Database updated successfully!")

if __name__ == "__main__":
    update_facilities()
