import sqlite3
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
import logging
from database.models import get_db_connection
from utils.helpers import safe_database_operation, sanitize_input

class BookingOperations:
    @staticmethod
    @safe_database_operation
    def get_all_lodging_units(active_only: bool = True) -> List[Dict]:
        """Get all lodging units with error handling"""
        conn = get_db_connection()
        try:
            query = "SELECT * FROM lodging_units"
            if active_only:
                query += " WHERE is_active = 1"
            query += " ORDER BY location, name"
            
            cursor = conn.execute(query)
            units = [dict(row) for row in cursor.fetchall()]
            return units
        finally:
            conn.close()
    
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
    @safe_database_operation
    def create_booking_request(booking_data: Dict) -> int:
        """Create a new booking request with enhanced validation and sanitization"""
        # Input sanitization
        sanitized_data = {
            'guest_name': sanitize_input(booking_data.get('guest_name', ''), 100),
            'email': booking_data.get('email', '').strip().lower(),
            'phone': sanitize_input(booking_data.get('phone', ''), 20),
            'booking_type': booking_data.get('booking_type', ''),
            'check_in': booking_data.get('check_in'),
            'check_out': booking_data.get('check_out'),
            'guests': booking_data.get('guests', 1),
            'lodging_unit_id': booking_data.get('lodging_unit_id'),
            'notes': sanitize_input(booking_data.get('notes', ''), 2000),
            'special_requests': sanitize_input(booking_data.get('special_requests', ''), 1000)
        }
        
        # Validate required fields
        if not sanitized_data['guest_name']:
            raise ValueError("Guest name is required")
        if not sanitized_data['email']:
            raise ValueError("Email is required")
        if not sanitized_data['check_in'] or not sanitized_data['check_out']:
            raise ValueError("Check-in and check-out dates are required")
        
        conn = get_db_connection()
        try:
            # Check for potential conflicts
            if sanitized_data['lodging_unit_id']:
                if not BookingOperations.check_availability(
                    sanitized_data['lodging_unit_id'], 
                    sanitized_data['check_in'], 
                    sanitized_data['check_out']
                ):
                    raise ValueError("Selected accommodation is not available for those dates")
            
            cursor = conn.execute("""
                INSERT INTO booking_requests 
                (guest_name, email, phone, booking_type, check_in, check_out, 
                 guests, lodging_unit_id, notes, special_requests)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sanitized_data['guest_name'],
                sanitized_data['email'],
                sanitized_data['phone'],
                sanitized_data['booking_type'],
                sanitized_data['check_in'],
                sanitized_data['check_out'],
                sanitized_data['guests'],
                sanitized_data['lodging_unit_id'],
                sanitized_data['notes'],
                sanitized_data['special_requests']
            ))
            
            booking_id = cursor.lastrowid
            conn.commit()
            logging.info(f"Created booking request {booking_id} for {sanitized_data['guest_name']}")
            return booking_id
        finally:
            conn.close()
    
    @staticmethod
    @safe_database_operation
    def get_all_booking_requests(status: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Get all booking requests with pagination and filtering"""
        conn = get_db_connection()
        try:
            query = """
                SELECT br.*, lu.name as lodging_name, lu.location as lodging_location
                FROM booking_requests br
                LEFT JOIN lodging_units lu ON br.lodging_unit_id = lu.id
            """
            params = []
            
            if status:
                query += " WHERE br.status = ?"
                params.append(status)
                
            query += " ORDER BY br.created_at DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            bookings = [dict(row) for row in cursor.fetchall()]
            return bookings
        finally:
            conn.close()
    
    @staticmethod
    @safe_database_operation
    def update_booking_status(booking_id: int, status: str, notes: str = "") -> bool:
        """Update booking request status with validation"""
        if not booking_id or booking_id <= 0:
            raise ValueError("Invalid booking ID")
        
        valid_statuses = ['pending', 'confirmed', 'cancelled', 'rejected']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        sanitized_notes = sanitize_input(notes, 2000)
        
        conn = get_db_connection()
        try:
            cursor = conn.execute("""
                UPDATE booking_requests 
                SET status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (status, sanitized_notes, booking_id))
            
            success = cursor.rowcount > 0
            conn.commit()
            
            if success:
                logging.info(f"Updated booking {booking_id} status to {status}")
            else:
                logging.warning(f"Failed to update booking {booking_id} - not found")
            
            return success
        finally:
            conn.close()
    
    @staticmethod
    @safe_database_operation
    def check_availability(lodging_unit_id: int, check_in: date, check_out: date) -> bool:
        """Check if a lodging unit is available for given dates"""
        conn = get_db_connection()
        try:
            cursor = conn.execute("""
                SELECT COUNT(*) FROM booking_requests 
                WHERE lodging_unit_id = ? 
                AND status IN ('confirmed', 'pending')
                AND (
                    (check_in <= ? AND check_out > ?) OR
                    (check_in < ? AND check_out >= ?) OR
                    (check_in >= ? AND check_out <= ?)
                )
            """, (lodging_unit_id, check_in, check_in, check_out, check_out, check_in, check_out))
            
            count = cursor.fetchone()[0]
            return count == 0
        finally:
            conn.close()
    
    @staticmethod
    @safe_database_operation
    def get_available_units(check_in: date, check_out: date, guests: int = 1) -> List[Dict]:
        """Get units available for given dates and guest count"""
        conn = get_db_connection()
        try:
            query = """
                SELECT * FROM lodging_units
                WHERE is_active = 1 AND capacity >= ?
                AND id NOT IN (
                    SELECT lodging_unit_id FROM booking_requests
                    WHERE lodging_unit_id IS NOT NULL
                    AND status IN ('confirmed', 'pending')
                    AND (
                        (check_in <= ? AND check_out > ?) OR
                        (check_in < ? AND check_out >= ?) OR
                        (check_in >= ? AND check_out <= ?)
                    )
                )
                ORDER BY location, name
            """
            
            cursor = conn.execute(query, (
                guests, check_in, check_in, check_out, check_out, check_in, check_out
            ))
            
            units = [dict(row) for row in cursor.fetchall()]
            return units
        finally:
            conn.close()
    
    @staticmethod
    @safe_database_operation
    def get_booking_summary() -> Dict[str, int]:
        """Get booking summary statistics"""
        conn = get_db_connection()
        try:
            # Get total units
            cursor = conn.execute("SELECT COUNT(*) FROM lodging_units WHERE is_active = 1")
            total_units = cursor.fetchone()[0]

            # Get pending bookings/requests
            cursor = conn.execute("SELECT COUNT(*) FROM booking_requests WHERE status = 'pending'")
            pending_bookings = cursor.fetchone()[0]

            # Get confirmed bookings
            cursor = conn.execute("SELECT COUNT(*) FROM booking_requests WHERE status = 'confirmed'")
            confirmed_bookings = cursor.fetchone()[0]

            # Get today's check-ins
            today = date.today()
            cursor = conn.execute("SELECT COUNT(*) FROM booking_requests WHERE check_in = ? AND status = 'confirmed'", (today,))
            todays_checkins = cursor.fetchone()[0]

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

            return {
                'total_units': total_units,
                'pending_bookings': pending_bookings,
                'pending_requests': pending_bookings,  # Alias for compatibility
                'confirmed_bookings': confirmed_bookings,
                'todays_checkins': todays_checkins,
                'confirmed_this_month': confirmed_this_month,
                'current_occupancy': current_occupancy
            }
        finally:
            conn.close()
    
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
    
