import sqlite3
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from database.models import get_db_connection

class BookingOperations:
    @staticmethod
    def get_all_lodging_units(active_only: bool = True) -> List[Dict]:
        """Get all lodging units"""
        conn = get_db_connection()
        query = "SELECT * FROM lodging_units"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY location, name"
        
        cursor = conn.execute(query)
        units = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return units
    
    @staticmethod
    def get_lodging_units_by_location(location: str) -> List[Dict]:
        """Get lodging units by location"""
        conn = get_db_connection()
        cursor = conn.execute(
            "SELECT * FROM lodging_units WHERE location = ? AND is_active = 1 ORDER BY name",
            (location,)
        )
        units = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return units
    
    @staticmethod
    def create_booking_request(booking_data: Dict) -> int:
        """Create a new booking request"""
        conn = get_db_connection()
        cursor = conn.execute("""
            INSERT INTO booking_requests 
            (guest_name, email, phone, booking_type, check_in, check_out, 
             guests, lodging_unit_id, notes, special_requests)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            booking_data['guest_name'],
            booking_data['email'],
            booking_data.get('phone', ''),
            booking_data['booking_type'],
            booking_data['check_in'],
            booking_data['check_out'],
            booking_data['guests'],
            booking_data.get('lodging_unit_id'),
            booking_data.get('notes', ''),
            booking_data.get('special_requests', '')
        ))
        
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return booking_id
    
    @staticmethod
    def get_all_booking_requests(status: Optional[str] = None) -> List[Dict]:
        """Get all booking requests, optionally filtered by status"""
        conn = get_db_connection()
        
        query = """
            SELECT br.*, lu.name as lodging_name, lu.location as lodging_location
            FROM booking_requests br
            LEFT JOIN lodging_units lu ON br.lodging_unit_id = lu.id
        """
        params = []
        
        if status:
            query += " WHERE br.status = ?"
            params.append(status)
            
        query += " ORDER BY br.created_at DESC"
        
        cursor = conn.execute(query, params)
        bookings = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return bookings
    
    @staticmethod
    def update_booking_status(booking_id: int, status: str, notes: str = "") -> bool:
        """Update booking request status"""
        conn = get_db_connection()
        cursor = conn.execute("""
            UPDATE booking_requests 
            SET status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, notes, booking_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    @staticmethod
    def check_availability(lodging_unit_id: int, check_in: date, check_out: date) -> bool:
        """Check if a lodging unit is available for given dates"""
        conn = get_db_connection()
        
        # Check for confirmed bookings that overlap
        cursor = conn.execute("""
            SELECT COUNT(*) FROM booking_requests
            WHERE lodging_unit_id = ? 
            AND status = 'confirmed'
            AND NOT (check_out <= ? OR check_in >= ?)
        """, (lodging_unit_id, check_in.isoformat(), check_out.isoformat()))
        
        overlapping_bookings = cursor.fetchone()[0]
        
        # Check availability calendar for blocked dates
        cursor = conn.execute("""
            SELECT COUNT(*) FROM availability_calendar
            WHERE lodging_unit_id = ?
            AND date >= ? AND date < ?
            AND is_available = 0
        """, (lodging_unit_id, check_in.isoformat(), check_out.isoformat()))
        
        blocked_dates = cursor.fetchone()[0]
        
        conn.close()
        return overlapping_bookings == 0 and blocked_dates == 0
    
    @staticmethod
    def get_available_units(check_in: date, check_out: date, min_capacity: int = 1) -> List[Dict]:
        """Get all available units for given dates and capacity"""
        units = BookingOperations.get_all_lodging_units()
        available_units = []
        
        for unit in units:
            if unit['capacity'] >= min_capacity:
                if BookingOperations.check_availability(unit['id'], check_in, check_out):
                    available_units.append(unit)
        
        return available_units
    
    @staticmethod
    def block_dates(lodging_unit_id: int, start_date: date, end_date: date, notes: str = "") -> bool:
        """Block dates for a lodging unit"""
        conn = get_db_connection()
        
        current_date = start_date
        while current_date < end_date:
            conn.execute("""
                INSERT OR REPLACE INTO availability_calendar
                (lodging_unit_id, date, is_available, notes)
                VALUES (?, ?, 0, ?)
            """, (lodging_unit_id, current_date.isoformat(), notes))
            
            # Move to next day
            from datetime import timedelta
            current_date += timedelta(days=1)
        
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def get_booking_summary() -> Dict:
        """Get summary statistics for dashboard"""
        conn = get_db_connection()
        
        # Total units
        cursor = conn.execute("SELECT COUNT(*) FROM lodging_units WHERE is_active = 1")
        total_units = cursor.fetchone()[0]
        
        # Pending requests
        cursor = conn.execute("SELECT COUNT(*) FROM booking_requests WHERE status = 'pending'")
        pending_requests = cursor.fetchone()[0]
        
        # Confirmed bookings this month
        cursor = conn.execute("""
            SELECT COUNT(*) FROM booking_requests 
            WHERE status = 'confirmed' 
            AND strftime('%Y-%m', check_in) = strftime('%Y-%m', 'now')
        """)
        confirmed_this_month = cursor.fetchone()[0]
        
        # Current occupancy (active bookings today)
        cursor = conn.execute("""
            SELECT COUNT(*) FROM booking_requests 
            WHERE status = 'confirmed'
            AND date('now') >= check_in 
            AND date('now') < check_out
        """)
        current_occupancy = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_units': total_units,
            'pending_requests': pending_requests,
            'confirmed_this_month': confirmed_this_month,
            'current_occupancy': current_occupancy
        }