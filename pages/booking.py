import streamlit as st
from datetime import datetime, date, timedelta
from utils.auth import require_auth, create_logout_button
from utils.helpers import (
    validate_email, validate_phone, calculate_duration, 
    validate_booking_duration, get_booking_type_info,
    display_lodging_unit_card, get_location_emoji,
    validate_guest_count, sanitize_input, validate_date_range,
    format_error_message
)
from utils.styles import show_success_message, show_error_message
from database.operations import BookingOperations

def show_booking_page():
    """Main booking page for public users"""
    require_auth("public")
    create_logout_button("public")
    
    # Clean hero section using Streamlit components
    st.title("🏔️ Wellspring Mountain Booking")
    st.markdown(
        "<p style='text-align: center; color: #717171; font-size: 18px; margin-bottom: 32px;'>" +
        "Find your perfect stay in our mountain retreat</p>", 
        unsafe_allow_html=True
    )
    
    # Initialize session state for multi-step form
    if 'booking_step' not in st.session_state:
        st.session_state.booking_step = 1
    
    # Modern breadcrumb navigation
    steps = ["Type", "Dates", "Details", "Room", "Confirm"]
    current_step = st.session_state.booking_step
    
    breadcrumb_html = "<div style='display: flex; justify-content: center; align-items: center; margin: 24px 0;'>"
    
    for i, step in enumerate(steps):
        step_num = i + 1
        is_current = step_num == current_step
        is_completed = step_num < current_step
        
        # Step circle
        if is_completed:
            circle_style = "background: #00A400; color: white;"
            icon = "✓"
        elif is_current:
            circle_style = "background: #FF385C; color: white;"
            icon = str(step_num)
        else:
            circle_style = "background: #F7F7F7; color: #717171;"
            icon = str(step_num)
        
        breadcrumb_html += f"""
        <div style="display: flex; flex-direction: column; align-items: center; margin: 0 16px;">
            <div style="
                width: 40px; height: 40px; border-radius: 50%; 
                display: flex; align-items: center; justify-content: center;
                font-weight: 600; font-size: 14px; {circle_style}
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            ">{icon}</div>
            <span style="font-size: 12px; color: {'#222222' if is_current else '#717171'}; 
                        font-weight: {'600' if is_current else '400'}; margin-top: 8px;">
                {step}
            </span>
        </div>
        """
        
        # Add connector line (except for last step)
        if i < len(steps) - 1:
            line_color = "#00A400" if step_num < current_step else "#EBEBEB"
            breadcrumb_html += f"""
            <div style="flex: 1; height: 2px; background: {line_color}; margin: 0 8px; margin-top: -16px;"></div>
            """
    
    breadcrumb_html += "</div>"
    st.markdown(breadcrumb_html, unsafe_allow_html=True)
    
    if st.session_state.booking_step == 1:
        show_booking_type_selection()
    elif st.session_state.booking_step == 2:
        show_date_selection()
    elif st.session_state.booking_step == 3:
        show_guest_info()
    elif st.session_state.booking_step == 4:
        show_lodging_selection()
    elif st.session_state.booking_step == 5:
        show_confirmation()

def show_booking_type_selection():
    """Step 1: Booking type selection with consistent sizing"""
    st.header("Step 1: What type of stay are you looking for?")
    
    booking_types = get_booking_type_info()
    
    # Create columns for booking type cards with consistent height
    cols = st.columns(3)
    
    for i, (key, info) in enumerate(booking_types.items()):
        with cols[i]:
            # Simple clean card using Streamlit components
            with st.container():
                # Create a clean card-like layout
                st.markdown(f"<div style='text-align: center; padding: 20px; background: #f8f9fa; border-radius: 12px; border: 1px solid #e9ecef; margin: 10px 0;'>", unsafe_allow_html=True)
                
                # Emoji and title
                emoji = info['title'].split()[0]
                title = info['title'].split(' ', 1)[1] if len(info['title'].split()) > 1 else info['title']
                
                st.markdown(f"<div style='font-size: 48px; margin-bottom: 16px;'>{emoji}</div>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='color: #333; margin: 0 0 12px 0;'>{title}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #666; font-size: 14px; margin-bottom: 16px;'>{info['description']}</p>", unsafe_allow_html=True)
                
                # Duration info
                duration_text = f"Max: {info['max_duration']} days" if info['max_duration'] else "Flexible duration"
                st.markdown(f"<small style='color: #888; font-weight: 500;'>{duration_text}</small>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Modern button
            if st.button(f"Choose {info['title'].split(' ', 1)[1] if len(info['title'].split()) > 1 else info['title']}", 
                        key=f"select_{key}", use_container_width=True):
                st.session_state.booking_type = key
                st.session_state.booking_step = 2
                st.rerun()

def show_date_selection():
    """Step 2: Date and duration selection with enhanced validation"""
    st.header("Step 2: When would you like to stay?")
    
    booking_types = get_booking_type_info()
    selected_type = st.session_state.booking_type
    type_info = booking_types[selected_type]
    
    # Enhanced info display with booking rules
    with st.expander(f"ℹ️ {type_info['title']} Details", expanded=True):
        st.markdown(f"""
        **{type_info['description']}**
        
        - Maximum duration: {type_info['max_duration']} days
        - {"Minimum 7 days required" if selected_type == "refuge" else ""}
        - Perfect for: {"Long-term housing assistance" if selected_type == "refuge" else "Short breaks and recovery" if selected_type == "respite" else "Group events and workshops"}
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        check_in = st.date_input(
            "Check-in Date:",
            min_value=date.today(),
            value=date.today() + timedelta(days=1),
            help="Select your arrival date"
        )
    
    with col2:
        # Set intelligent defaults based on booking type
        default_days = {
            "refuge": 14,  # Start with 2 weeks for refuge
            "respite": 7,  # 1 week for respite
            "retreat": 3   # 3 days for retreat
        }
        default_checkout = check_in + timedelta(days=default_days.get(selected_type, 7))
        
        check_out = st.date_input(
            "Check-out Date:",
            min_value=check_in + timedelta(days=1),
            value=default_checkout,
            help="Select your departure date"
        )
    
    # Enhanced date validation
    is_valid_dates, date_error = validate_date_range(check_in, check_out, selected_type)
    
    if not is_valid_dates:
        st.error(format_error_message(date_error, "Date Selection"))
        return
    
    duration = calculate_duration(check_in, check_out)
    
    # Success message with helpful information
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"✅ Duration: {duration} days")
    with col2:
        # Show cost estimate (placeholder)
        st.info(f"💡 Estimated stay: {duration} nights")
    
    # Enhanced guest count input
    max_guests = 15 if selected_type == "retreat" else 8
    
    guests = st.number_input(
        "Number of guests:",
        min_value=1,
        max_value=max_guests,
        value=1,
        help=f"Maximum {max_guests} guests for {selected_type} bookings"
    )
    
    # Validate guest count
    is_valid_guests, guest_error = validate_guest_count(guests)
    if not is_valid_guests:
        st.error(format_error_message(guest_error, "Guest Count"))
        return
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.booking_step = 1
            st.rerun()
    
    with col2:
        if st.button("Next →"):
            st.session_state.check_in = check_in
            st.session_state.check_out = check_out
            st.session_state.guests = guests
            st.session_state.booking_step = 3
            st.rerun()

def show_guest_info():
    """Step 3: Guest information"""
    st.header("Step 3: Your information")
    
    # Display booking summary
    st.info(f"""
    **Booking Summary:**
    - Type: {get_booking_type_info()[st.session_state.booking_type]['title']}
    - Dates: {st.session_state.check_in} to {st.session_state.check_out}
    - Duration: {calculate_duration(st.session_state.check_in, st.session_state.check_out)} days
    - Guests: {st.session_state.guests}
    """)
    
    # Guest information form
    with st.form("guest_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            guest_name = st.text_input("Full Name*", placeholder="Your full name")
            email = st.text_input("Email Address*", placeholder="your.email@example.com")
        
        with col2:
            phone = st.text_input("Phone Number", placeholder="(555) 123-4567")
            organization = st.text_input("Organization (if applicable)", placeholder="Company/Nonprofit name")
        
        special_requests = st.text_area(
            "Special Requests or Accessibility Needs:",
            placeholder="Please describe any special accommodations needed..."
        )
        
        notes = st.text_area(
            "Additional Information:",
            placeholder="Tell us more about your stay, group size, purpose of visit, etc."
        )
        
        submitted = st.form_submit_button("Continue →")
        
        if submitted:
            # Enhanced validation with better error handling
            errors = []
            
            # Name validation
            sanitized_name = sanitize_input(guest_name, 100)
            if not sanitized_name:
                errors.append("Full name is required")
            elif len(sanitized_name) < 2:
                errors.append("Name must be at least 2 characters long")
            
            # Email validation
            if not email.strip():
                errors.append("Email address is required")
            elif not validate_email(email):
                errors.append("Please enter a valid email address (e.g., name@example.com)")
            
            # Phone validation (if provided)
            if phone and not validate_phone(phone):
                errors.append("Please enter a valid phone number (10+ digits)")
            
            # Organization validation
            sanitized_org = sanitize_input(organization, 200)
            
            # Special requests validation
            sanitized_requests = sanitize_input(special_requests, 1000)
            sanitized_notes = sanitize_input(notes, 2000)
            
            if errors:
                st.error("Please fix the following issues:")
                for error in errors:
                    st.error(f"• {error}")
            else:
                # Save sanitized data to session state
                st.session_state.guest_name = sanitized_name
                st.session_state.email = email.strip().lower()
                st.session_state.phone = phone.strip() if phone else ""
                st.session_state.organization = sanitized_org
                st.session_state.special_requests = sanitized_requests
                st.session_state.notes = sanitized_notes
                st.session_state.booking_step = 4
                st.rerun()
    
    if st.button("← Back"):
        st.session_state.booking_step = 2
        st.rerun()

def show_lodging_selection():
    """Step 4: Lodging selection"""
    st.header("Step 4: Choose your accommodation")
    
    # Get available units
    available_units = BookingOperations.get_available_units(
        st.session_state.check_in,
        st.session_state.check_out,
        st.session_state.guests
    )
    
    if not available_units:
        st.warning("No accommodations are available for your selected dates. Please try different dates or contact us directly.")
        if st.button("← Back to change dates"):
            st.session_state.booking_step = 2
            st.rerun()
        return
    
    # Group units by location
    locations = {}
    for unit in available_units:
        location = unit['location']
        if location not in locations:
            locations[location] = []
        locations[location].append(unit)
    
    st.success(f"Found {len(available_units)} available accommodations for your dates!")
    
    # Display available units by location
    selected_unit_id = None
    
    for location, units in locations.items():
        st.subheader(f"{get_location_emoji(location)} {location}")
        
        for unit in units:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                display_lodging_unit_card(unit)
            
            with col2:
                st.write("")  # Spacer
                if st.button(f"Select", key=f"select_unit_{unit['id']}"):
                    selected_unit_id = unit['id']
                    st.session_state.selected_unit = unit
                    st.session_state.booking_step = 5
                    st.rerun()
    
    # Option to proceed without specific unit selection
    st.markdown("---")
    st.markdown("**Not sure which accommodation to choose?**")
    if st.button("Let staff choose the best option for me"):
        st.session_state.selected_unit = None
        st.session_state.booking_step = 5
        st.rerun()
    
    if st.button("← Back"):
        st.session_state.booking_step = 3
        st.rerun()

def show_confirmation():
    """Step 5: Confirmation and submission"""
    st.header("Step 5: Confirm your booking request")
    
    # Display complete booking summary
    booking_type_info = get_booking_type_info()[st.session_state.booking_type]
    
    st.markdown(f"""
    ### 📋 Booking Summary
    
    **Guest Information:**
    - Name: {st.session_state.guest_name}
    - Email: {st.session_state.email}
    - Phone: {st.session_state.get('phone', 'Not provided')}
    - Organization: {st.session_state.get('organization', 'Not provided')}
    
    **Stay Details:**
    - Type: {booking_type_info['title']}
    - Check-in: {st.session_state.check_in.strftime('%B %d, %Y')}
    - Check-out: {st.session_state.check_out.strftime('%B %d, %Y')}
    - Duration: {calculate_duration(st.session_state.check_in, st.session_state.check_out)} days
    - Guests: {st.session_state.guests}
    
    **Accommodation:**
    {f"- {st.session_state.selected_unit['name']} ({st.session_state.selected_unit['location']})" if st.session_state.get('selected_unit') else "- Staff will assign best available option"}
    
    **Special Requests:**
    {st.session_state.get('special_requests', 'None')}
    
    **Additional Notes:**
    {st.session_state.get('notes', 'None')}
    """)
    
    with st.container():
        st.markdown("### What happens next?")
        st.markdown("""
        • We'll review your booking request  
        • A staff member will contact you within 24-48 hours  
        • We'll discuss your needs and confirm availability  
        • Once confirmed, you'll receive booking details and check-in instructions
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back to edit"):
            st.session_state.booking_step = 4
            st.rerun()
    
    with col2:
        if st.button("Submit Booking Request", type="primary"):
            # Create booking request
            booking_data = {
                'guest_name': st.session_state.guest_name,
                'email': st.session_state.email,
                'phone': st.session_state.get('phone', ''),
                'booking_type': st.session_state.booking_type,
                'check_in': st.session_state.check_in,
                'check_out': st.session_state.check_out,
                'guests': st.session_state.guests,
                'lodging_unit_id': st.session_state.selected_unit['id'] if st.session_state.get('selected_unit') else None,
                'special_requests': st.session_state.get('special_requests', ''),
                'notes': st.session_state.get('notes', '')
            }
            
            try:
                booking_id = BookingOperations.create_booking_request(booking_data)
                
                # Clear session state
                for key in ['booking_step', 'booking_type', 'check_in', 'check_out', 'guests',
                           'guest_name', 'email', 'phone', 'organization', 'special_requests', 
                           'notes', 'selected_unit']:
                    if key in st.session_state:
                        del st.session_state[key]
                
                st.balloons()
                st.success("✅ **Booking request submitted successfully!**")
                st.info(f"**Your booking request ID is: {booking_id}**")
                st.markdown(f"""
                We'll contact you at **{booking_data['email']}** within 24-48 hours to confirm your stay.
                
                Thank you for choosing Wellspring Mountain!
                """)
                
                if st.button("Submit Another Booking"):
                    st.session_state.booking_step = 1
                    st.rerun()
                    
            except Exception as e:
                st.error(f"An error occurred while submitting your request: {str(e)}")
                st.error("Please try again or contact us directly.")

# EXECUTE THE PAGE (required for Streamlit multipage)
if __name__ == "__main__":
    show_booking_page()