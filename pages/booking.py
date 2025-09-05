import streamlit as st
from datetime import datetime, date, timedelta
from utils.auth import require_auth, create_logout_button
from utils.helpers import (
    validate_email, validate_phone, calculate_duration, 
    validate_booking_duration, get_booking_type_info,
    display_lodging_unit_card, get_location_emoji
)
from database.operations import BookingOperations

def show_booking_page():
    """Main booking page for public users"""
    require_auth("public")
    create_logout_button("public")
    
    st.title("🏔️ Wellspring Mountain Booking")
    st.markdown("Welcome to our booking system. Please fill out the form below to request your stay.")
    
    # Initialize session state for multi-step form
    if 'booking_step' not in st.session_state:
        st.session_state.booking_step = 1
    
    # Progress bar
    progress = st.session_state.booking_step / 5
    st.progress(progress)
    
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
    """Step 1: Booking type selection"""
    st.header("Step 1: What type of stay are you looking for?")
    
    booking_types = get_booking_type_info()
    
    # Create columns for booking type cards
    cols = st.columns(3)
    
    for i, (key, info) in enumerate(booking_types.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="
                border: 2px solid {info['color']}; 
                border-radius: 10px; 
                padding: 20px; 
                margin: 10px 0;
                text-align: center;
                background-color: {info['color']}20;
            ">
                <h3>{info['title']}</h3>
                <p>{info['description']}</p>
                {f"<p><small>Max duration: {info['max_duration']} days</small></p>" if info['max_duration'] else ""}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Select {info['title']}", key=f"select_{key}"):
                st.session_state.booking_type = key
                st.session_state.booking_step = 2
                st.rerun()

def show_date_selection():
    """Step 2: Date and duration selection"""
    st.header("Step 2: When would you like to stay?")
    
    booking_types = get_booking_type_info()
    selected_type = st.session_state.booking_type
    type_info = booking_types[selected_type]
    
    st.info(f"Selected: {type_info['title']} - {type_info['description']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        check_in = st.date_input(
            "Check-in Date:",
            min_value=date.today(),
            value=date.today() + timedelta(days=1)
        )
    
    with col2:
        # Set default check-out based on booking type
        default_checkout = check_in + timedelta(days=7 if selected_type == "respite" else 30)
        check_out = st.date_input(
            "Check-out Date:",
            min_value=check_in + timedelta(days=1),
            value=default_checkout
        )
    
    if check_out <= check_in:
        st.error("Check-out date must be after check-in date.")
        return
    
    duration = calculate_duration(check_in, check_out)
    is_valid, error_msg = validate_booking_duration(selected_type, duration)
    
    if not is_valid:
        st.error(error_msg)
        return
    
    st.success(f"Duration: {duration} days")
    
    # Number of guests
    guests = st.number_input(
        "Number of guests:",
        min_value=1,
        max_value=15 if selected_type == "retreat" else 6,
        value=1
    )
    
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
            # Validation
            errors = []
            if not guest_name.strip():
                errors.append("Full name is required")
            if not email.strip():
                errors.append("Email address is required")
            elif not validate_email(email):
                errors.append("Please enter a valid email address")
            if phone and not validate_phone(phone):
                errors.append("Please enter a valid phone number")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Save to session state
                st.session_state.guest_name = guest_name
                st.session_state.email = email
                st.session_state.phone = phone
                st.session_state.organization = organization
                st.session_state.special_requests = special_requests
                st.session_state.notes = notes
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
    
    st.info("""
    **What happens next?**
    1. We'll review your booking request
    2. A staff member will contact you within 24-48 hours
    3. We'll discuss your needs and confirm availability
    4. Once confirmed, you'll receive booking details and check-in instructions
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
                
                st.success(f"""
                ✅ **Booking request submitted successfully!**
                
                Your booking request ID is: **{booking_id}**
                
                We'll contact you at {st.session_state.email} within 24-48 hours to confirm your stay.
                
                Thank you for choosing Wellspring Mountain!
                """)
                
                if st.button("Submit Another Booking"):
                    st.session_state.booking_step = 1
                    st.rerun()
                    
            except Exception as e:
                st.error(f"An error occurred while submitting your request: {str(e)}")
                st.error("Please try again or contact us directly.")

if __name__ == "__main__":
    show_booking_page()