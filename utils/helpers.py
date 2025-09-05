import streamlit as st
from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple
import pandas as pd

def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Basic phone validation"""
    import re
    # Remove common phone formatting
    cleaned = re.sub(r'[^\d]', '', phone)
    return len(cleaned) >= 10

def calculate_duration(check_in: date, check_out: date) -> int:
    """Calculate duration in days"""
    return (check_out - check_in).days

def validate_booking_duration(booking_type: str, duration: int) -> Tuple[bool, str]:
    """Validate booking duration based on type"""
    if booking_type == "refuge" and duration > 90:  # 3 months
        return False, "Refuge stays cannot exceed 3 months (90 days)"
    elif booking_type == "respite" and duration > 21:  # 3 weeks
        return False, "Respite stays cannot exceed 3 weeks (21 days)"
    elif duration <= 0:
        return False, "Duration must be at least 1 day"
    return True, ""

def format_date_range(check_in: date, check_out: date) -> str:
    """Format date range for display"""
    duration = calculate_duration(check_in, check_out)
    return f"{check_in.strftime('%b %d, %Y')} - {check_out.strftime('%b %d, %Y')} ({duration} days)"

def get_booking_type_info() -> Dict[str, Dict]:
    """Get information about different booking types"""
    return {
        "refuge": {
            "title": "🏠 Refuge",
            "description": "Longer-term stays up to 3 months for those seeking temporary housing",
            "max_duration": 90,
            "color": "#4CAF50"
        },
        "respite": {
            "title": "🌿 Respite", 
            "description": "Short-term stays up to 3 weeks for rest and recovery",
            "max_duration": 21,
            "color": "#2196F3"
        },
        "retreat": {
            "title": "👥 Retreat",
            "description": "Group bookings for nonprofits, corporations, and organizations",
            "max_duration": None,
            "color": "#FF9800"
        }
    }

def display_lodging_unit_card(unit: Dict, show_capacity: bool = True):
    """Display a lodging unit as a card"""
    with st.container():
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 8px 0;">
            <h4>{unit['name']}</h4>
            <p><strong>Location:</strong> {unit['location']}</p>
            <p><strong>Type:</strong> {unit['type'].title()}</p>
            {'<p><strong>Capacity:</strong> ' + str(unit['capacity']) + ' guests</p>' if show_capacity else ''}
            {'<p><em>' + unit['description'] + '</em></p>' if unit.get('description') else ''}
        </div>
        """, unsafe_allow_html=True)

def create_availability_calendar(units: List[Dict], bookings: List[Dict]) -> pd.DataFrame:
    """Create availability calendar data"""
    # This is a placeholder - would need more complex logic for a full calendar
    today = date.today()
    dates = [today + timedelta(days=i) for i in range(30)]
    
    calendar_data = []
    for unit in units:
        for date_item in dates:
            # Simple availability check (would be more complex in practice)
            is_available = True
            for booking in bookings:
                if (booking['lodging_unit_id'] == unit['id'] and 
                    booking['status'] == 'confirmed' and
                    booking['check_in'] <= date_item < booking['check_out']):
                    is_available = False
                    break
            
            calendar_data.append({
                'unit_name': unit['name'],
                'date': date_item,
                'available': is_available
            })
    
    return pd.DataFrame(calendar_data)

def format_booking_status(status: str) -> str:
    """Format booking status with colors"""
    status_colors = {
        'pending': '#FFA726',
        'confirmed': '#4CAF50', 
        'cancelled': '#F44336',
        'rejected': '#9E9E9E'
    }
    
    color = status_colors.get(status, '#9E9E9E')
    return f'<span style="color: {color}; font-weight: bold;">{status.upper()}</span>'

def get_location_emoji(location: str) -> str:
    """Get emoji for location"""
    location_emojis = {
        'Lodge': '🏠',
        'Uptown': '🏘️',
        'Downtown': '🏢',
        'A-frame': '🏕️'
    }
    return location_emojis.get(location, '📍')

def create_summary_metric(title: str, value: int, delta: int = None):
    """Create a metric display"""
    if delta is not None:
        st.metric(title, value, delta)
    else:
        st.metric(title, value)