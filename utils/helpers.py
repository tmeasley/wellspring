import streamlit as st
from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple, Optional
import pandas as pd
import logging
from functools import wraps

def validate_email(email: str) -> bool:
    """Enhanced email validation with better pattern matching"""
    import re
    if not email or not isinstance(email, str):
        return False
    
    email = email.strip().lower()
    if len(email) > 254:  # Email length limit
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Enhanced phone validation with international support"""
    import re
    if not phone or not isinstance(phone, str):
        return False
    
    # Remove common phone formatting
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Check for valid phone patterns
    if cleaned.startswith('+1'):
        cleaned = cleaned[2:]  # Remove country code
    elif cleaned.startswith('1') and len(cleaned) == 11:
        cleaned = cleaned[1:]  # Remove leading 1
    
    return len(cleaned) >= 10 and len(cleaned) <= 15

def calculate_duration(check_in: date, check_out: date) -> int:
    """Calculate duration in days"""
    return (check_out - check_in).days

def validate_booking_duration(booking_type: str, duration: int) -> Tuple[bool, str]:
    """Enhanced booking duration validation with business rules"""
    if not booking_type or duration is None:
        return False, "Invalid booking type or duration"
    
    if duration <= 0:
        return False, "Duration must be at least 1 day"
    
    if duration > 365:
        return False, "Bookings cannot exceed 1 year"
    
    if booking_type == "refuge":
        if duration > 90:  # 3 months
            return False, "Refuge stays cannot exceed 3 months (90 days)"
        if duration < 7:
            return False, "Refuge stays require minimum 7 days"
    elif booking_type == "respite":
        if duration > 21:  # 3 weeks
            return False, "Respite stays cannot exceed 3 weeks (21 days)"
    elif booking_type == "retreat":
        if duration > 14:
            return False, "Retreat bookings cannot exceed 2 weeks (14 days)"
        if duration < 1:
            return False, "Retreat bookings require minimum 1 day"
    else:
        return False, f"Invalid booking type: {booking_type}"
    
    return True, ""

def format_date_range(check_in: date, check_out: date) -> str:
    """Format date range for display - nights = days duration"""
    duration = calculate_duration(check_in, check_out)
    nights = duration  # Number of nights = check_out - check_in
    night_text = "night" if nights == 1 else "nights"
    return f"{check_in.strftime('%b %d, %Y')} - {check_out.strftime('%b %d, %Y')} ({nights} {night_text})"

def get_booking_type_info() -> Dict[str, Dict]:
    """Get information about different booking types with full descriptions"""
    return {
        "respite": {
            "title": "🌿 Respite",
            "description": "A free nature-based refuge where you get a private room, access to a shared kitchen, trails, and a peaceful mountain setting for 3 days to 3 weeks.",
            "full_description": """
**What We Provide:**
- Private room in peaceful mountain setting
- Access to shared kitchen
- Trails and natural spaces
- One staff person on-site for logistics and practical needs
- Optional community activities (garden projects, crafts)
- Transportation help for trips to town

**What This Is:**
Space and time to direct your own healing and recovery. Other guests are around if you want company, but you control your own schedule and activities.

**What This Is NOT:**
- Not a peer respite with trained support staff
- We don't provide meals or structured activities
- Not therapeutic support or crisis intervention
- Staff keep things running smoothly but don't provide counseling

**Who This Works For:**
People dealing with burnout, depression, grief, life transitions, or needing space away from regular circumstances who can:
- Feed yourself and manage your own meals
- Take care of basic self-care needs
- Manage your own medications
- Ask for help when you need something practical

**Not Right If:**
You're in acute crisis and need active support (though we're working toward offering true peer respite in the future).

After submitting your inquiry, staff will connect with you to ensure we're a good fit.
            """,
            "max_duration": 21,
            "color": "#2196F3"
        },
        "refuge": {
            "title": "🏠 Refuge",
            "description": "Free temporary refuge for up to 3 months for those displaced by natural disasters or emergencies.",
            "full_description": """
**When Disaster Strikes:**
Wildfire, flood, hurricane, evacuation - you need a place to land while you figure out your next steps. We offer free temporary refuge in the North Carolina mountains.

**What We Provide:**
- Cabins with electricity (shower house nearby - no bathroom/water in cabins)
- Camping areas (no RV hookups available)
- Access to shared kitchen facilities
- One staff person on-site for practical support
- Time and space to plan your next move

**What You Need:**
- Working vehicle (we're rural - you'll need transportation for supplies, work, appointments)
- Ability to manage in rustic conditions
- Handle your own food/cooking
- Basic self-sufficiency

**Who This Is For:**
Individuals and families displaced by natural disasters, climate events, or other emergencies who need temporary housing while they rebuild, relocate, or sort out longer-term plans.

**This Is:**
Crisis infrastructure - a bridge between losing your home and finding your footing again.

After submitting your inquiry, staff will connect with you to make sure we're a good fit and answer questions about the space.
            """,
            "max_duration": 90,
            "color": "#4CAF50"
        },
        "retreat": {
            "title": "👥 Retreat",
            "description": "Mountain property rentals for weekend to week-long retreats for nonprofits, corporations, and organizations.",
            "full_description": """
**Group Bookings:**
We offer our mountain property for retreats that bring teams and communities together away from daily distractions.

**What We Provide:**
- Lodging in our cabins and facilities
- Meal service
- Meeting and gathering spaces
- Access to trails, gardens, and natural setting
- Support staff to help your retreat run smoothly

**Who This Is For:**
Organizations looking for a peaceful mountain setting for:
- Team retreats
- Strategic planning sessions
- Training intensives
- Community gatherings
- Nonprofit events
- Corporate off-sites

**Pricing & Availability:**
Contact us to discuss your group's specific needs, capacity requirements, dates, and pricing.

After submitting your inquiry, staff will work with you to plan the perfect retreat for your organization.
            """,
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

def create_availability_calendar(units: List[Dict], bookings: List[Dict], days_ahead: int = 30) -> pd.DataFrame:
    """Create availability calendar data with enhanced booking conflict detection"""
    today = date.today()
    dates = [today + timedelta(days=i) for i in range(days_ahead)]
    
    calendar_data = []
    for unit in units:
        for date_item in dates:
            # Enhanced availability check
            is_available = True
            booking_info = None
            
            for booking in bookings:
                if (booking.get('lodging_unit_id') == unit['id'] and 
                    booking.get('status') in ['confirmed', 'pending'] and
                    booking.get('check_in') and booking.get('check_out')):
                    
                    # Convert string dates to date objects if needed
                    check_in = booking['check_in']
                    check_out = booking['check_out']
                    if isinstance(check_in, str):
                        check_in = datetime.strptime(check_in, '%Y-%m-%d').date()
                    if isinstance(check_out, str):
                        check_out = datetime.strptime(check_out, '%Y-%m-%d').date()
                    
                    if check_in <= date_item < check_out:
                        is_available = False
                        booking_info = {
                            'guest_name': booking.get('guest_name', 'Reserved'),
                            'status': booking.get('status', 'unknown'),
                            'booking_type': booking.get('booking_type', '')
                        }
                        break
            
            calendar_data.append({
                'unit_id': unit['id'],
                'unit_name': unit['name'],
                'location': unit['location'],
                'capacity': unit['capacity'],
                'date': date_item,
                'available': is_available,
                'booking_info': booking_info
            })
    
    return pd.DataFrame(calendar_data)

def create_visual_calendar(availability_df: pd.DataFrame, selected_location: str = None) -> None:
    """Create a visual calendar display for availability"""
    # Filter by location if specified
    if selected_location:
        availability_df = availability_df[availability_df['location'] == selected_location]
    
    if availability_df.empty:
        st.warning("No availability data to display")
        return
    
    # Get unique dates and units
    dates = sorted(availability_df['date'].unique())
    units = availability_df[['unit_id', 'unit_name', 'location']].drop_duplicates()
    
    # Create calendar grid
    st.subheader(f"Availability Calendar - {selected_location or 'All Locations'}")
    
    # Date header
    cols = st.columns([2] + [1] * min(len(dates), 14))  # Show up to 14 days
    cols[0].write("**Unit**")
    
    for i, date_item in enumerate(dates[:14]):  # Limit to first 14 days for display
        cols[i+1].write(f"**{date_item.strftime('%m/%d')}**")
    
    # Unit rows
    for _, unit in units.iterrows():
        cols = st.columns([2] + [1] * 14)
        cols[0].write(f"{unit['unit_name']} ({unit['location']})")
        
        unit_availability = availability_df[availability_df['unit_id'] == unit['unit_id']]
        
        for i, date_item in enumerate(dates[:14]):
            day_data = unit_availability[unit_availability['date'] == date_item]
            
            if not day_data.empty:
                is_available = day_data.iloc[0]['available']
                if is_available:
                    cols[i+1].success("✓")
                else:
                    booking_info = day_data.iloc[0]['booking_info']
                    if booking_info and booking_info['status'] == 'pending':
                        cols[i+1].warning("⏳")
                    else:
                        cols[i+1].error("✗")
            else:
                cols[i+1].write("-")
    
    # Legend
    st.markdown("""
    **Legend:** ✓ Available | ✗ Booked | ⏳ Pending | - No data
    """)

def format_booking_status(status: str) -> str:
    """Format booking status with emoji (no HTML)"""
    status_map = {
        'pending': '⏳ PENDING',
        'confirmed': '✅ CONFIRMED',
        'cancelled': '❌ CANCELLED',
        'rejected': '🚫 REJECTED'
    }

    return status_map.get(status.lower(), status.upper())

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

def validate_guest_count(guests: int, unit_capacity: int = None) -> Tuple[bool, str]:
    """Validate guest count against unit capacity and business rules"""
    if not isinstance(guests, int) or guests <= 0:
        return False, "Guest count must be a positive number"
    
    if guests > 15:  # Maximum group size
        return False, "Maximum group size is 15 guests"
    
    if unit_capacity and guests > unit_capacity:
        return False, f"Guest count exceeds unit capacity of {unit_capacity}"
    
    return True, ""

def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize text input to prevent issues"""
    if not text or not isinstance(text, str):
        return ""
    
    # Remove potential HTML/script content
    import re
    text = re.sub(r'<[^>]+>', '', text)
    text = text.strip()
    
    if len(text) > max_length:
        text = text[:max_length]
    
    return text

def safe_database_operation(func):
    """Decorator for safe database operations with error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Database operation failed: {str(e)}")
            st.error("A database error occurred. Please try again or contact support.")
            return None
    return wrapper

def validate_date_range(check_in: date, check_out: date, booking_type: str = None) -> Tuple[bool, str]:
    """Enhanced date range validation"""
    if not check_in or not check_out:
        return False, "Both check-in and check-out dates are required"
    
    if check_in >= check_out:
        return False, "Check-out date must be after check-in date"
    
    if check_in < date.today():
        return False, "Check-in date cannot be in the past"
    
    # Check for reasonable advance booking limits
    max_advance_days = 365
    if check_in > date.today() + timedelta(days=max_advance_days):
        return False, f"Bookings can only be made up to {max_advance_days} days in advance"
    
    duration = calculate_duration(check_in, check_out)
    
    if booking_type:
        is_valid, error_msg = validate_booking_duration(booking_type, duration)
        if not is_valid:
            return False, error_msg
    
    return True, ""

def format_error_message(error: str, context: str = None) -> str:
    """Format error messages consistently"""
    if context:
        return f"❌ {context}: {error}"
    return f"❌ {error}"

def get_availability_summary(availability_df: pd.DataFrame) -> Dict[str, int]:
    """Get availability summary statistics"""
    if availability_df.empty:
        return {}
    
    total_slots = len(availability_df)
    available_slots = len(availability_df[availability_df['available'] == True])
    occupied_slots = total_slots - available_slots
    
    return {
        'total_slots': total_slots,
        'available_slots': available_slots,
        'occupied_slots': occupied_slots,
        'occupancy_rate': round((occupied_slots / total_slots) * 100, 1) if total_slots > 0 else 0
    }