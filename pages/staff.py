import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from utils.auth import require_auth, create_logout_button
from utils.helpers import (
    format_booking_status, get_location_emoji, create_summary_metric,
    format_date_range, get_booking_type_info, create_availability_calendar,
    create_visual_calendar, get_availability_summary, format_lodging_display
)
from utils.styles import show_success_message, show_error_message
from database.operations import BookingOperations
from database.property_operations import PropertyManagementOperations
from pages.property_management import show_property_management_page

def show_staff_page():
    """Main staff dashboard"""
    require_auth("staff")
    create_logout_button("staff")

    st.title("🏢 Staff Dashboard - Wellspring Mountain")

    # Mobile-friendly navigation (always visible at top)
    st.markdown("### 📋 Quick Navigation")

    # Get current page from session state
    if 'staff_page' not in st.session_state:
        st.session_state.staff_page = "Overview"

    # Create mobile-friendly tabs/selectbox
    mobile_page = st.selectbox(
        "Choose a view:",
        ["Overview", "Booking Requests", "Active Stays", "Assign Rooms", "Manage Bookings", "Availability", "Property Management", "Reports"],
        index=["Overview", "Booking Requests", "Active Stays", "Assign Rooms", "Manage Bookings", "Availability", "Property Management", "Reports"].index(st.session_state.staff_page),
        key="mobile_staff_nav"
    )

    # Update session state if selection changed
    if mobile_page != st.session_state.staff_page:
        st.session_state.staff_page = mobile_page
        st.rerun()

    st.markdown("---")

    # Sidebar navigation (for desktop)
    with st.sidebar:
        st.header("📋 Dashboard Menu")
        sidebar_page = st.radio(
            "Select view:",
            ["Overview", "Booking Requests", "Active Stays", "Assign Rooms", "Manage Bookings", "Availability", "Property Management", "Reports"],
            index=["Overview", "Booking Requests", "Active Stays", "Assign Rooms", "Manage Bookings", "Availability", "Property Management", "Reports"].index(st.session_state.staff_page),
            key="staff_page_selection"
        )

        # Sync sidebar with mobile navigation
        if sidebar_page != st.session_state.staff_page:
            st.session_state.staff_page = sidebar_page
            st.rerun()

    # Use the session state page
    page = st.session_state.staff_page

    if page == "Overview":
        show_overview()
    elif page == "Booking Requests":
        show_booking_requests()
    elif page == "Active Stays":
        show_active_stays()
    elif page == "Assign Rooms":
        show_room_assignment()
    elif page == "Manage Bookings":
        show_manage_bookings()
    elif page == "Availability":
        show_availability_management()
    elif page == "Property Management":
        show_property_management_page()
    elif page == "Reports":
        show_reports()

def show_overview():
    """Enhanced dashboard overview with key metrics and quick calendar"""
    st.header("📊 Dashboard Overview")
    
    # Get summary statistics
    summary = BookingOperations.get_booking_summary()
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Units", summary.get('total_units', 0))
    with col2:
        st.metric("Pending Requests", summary.get('pending_bookings', 0))
    with col3:
        st.metric("Confirmed Bookings", summary.get('confirmed_bookings', 0))
    with col4:
        st.metric("Today's Check-ins", summary.get('todays_checkins', 0))
    
    st.markdown("---")
    
    # Quick availability overview
    st.subheader("🗓️ Quick Availability (Next 7 Days)")
    
    units = BookingOperations.get_all_lodging_units()
    bookings = BookingOperations.get_all_booking_requests()
    
    if units and bookings is not None:
        availability_df = create_availability_calendar(units, bookings, days_ahead=7)
        
        if not availability_df.empty:
            create_visual_calendar(availability_df)
        else:
            st.info("No availability data for the next 7 days")
    else:
        st.warning("Unable to load availability data")
    
    st.markdown("---")
    
    # Recent booking requests
    st.subheader("📋 Recent Booking Requests")
    recent_bookings = BookingOperations.get_all_booking_requests(limit=5)
    
    if recent_bookings:
        for booking in recent_bookings:
            with st.expander(
                f"{booking['guest_name']} - {booking['booking_type'].title()} - {format_booking_status(booking['status'])}", 
                expanded=False
            ):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Email:** {booking['email']}")
                    st.write(f"**Phone:** {booking.get('phone', 'Not provided')}")
                    st.write(f"**Check-in:** {booking['check_in']}")
                    st.write(f"**Check-out:** {booking['check_out']}")
                
                with col2:
                    st.write(f"**Guests:** {booking['guests']}")
                    st.write(f"**Lodging:** {booking.get('lodging_name', 'Staff will assign')}")
                    st.write(f"**Created:** {booking['created_at']}")
                
                if booking.get('special_requests'):
                    st.write(f"**Special Requests:** {booking['special_requests']}")
                
                if booking.get('notes'):
                    st.write(f"**Notes:** {booking['notes']}")
    else:
        st.info("No recent booking requests.")

def show_booking_requests():
    """Show and manage pending booking requests"""
    st.header("📝 Booking Requests")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "Filter by Status:",
            ["All", "pending", "confirmed", "cancelled", "rejected"]
        )
    
    with col2:
        booking_type_filter = st.selectbox(
            "Filter by Type:",
            ["All", "refuge", "respite", "retreat"]
        )
    
    with col3:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Get filtered bookings
    status = None if status_filter == "All" else status_filter
    all_bookings = BookingOperations.get_all_booking_requests(status)
    
    if booking_type_filter != "All":
        all_bookings = [b for b in all_bookings if b['booking_type'] == booking_type_filter]
    
    if not all_bookings:
        st.info("No booking requests match your filters.")
        return
    
    # Display bookings
    for booking in all_bookings:
        with st.container():
            st.markdown("---")
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"### {booking['guest_name']}")
                st.markdown(f"**{booking['booking_type'].title()}** • {format_date_range(datetime.strptime(booking['check_in'], '%Y-%m-%d').date(), datetime.strptime(booking['check_out'], '%Y-%m-%d').date())}")
                
                if booking.get('lodging_name'):
                    st.markdown(f"📍 {format_lodging_display(booking['lodging_name'], booking['lodging_location'])}")
                else:
                    st.markdown("📍 *Staff will assign accommodation*")
            
            with col2:
                st.markdown(f"**Status:** {format_booking_status(booking['status'])}", unsafe_allow_html=True)
                st.markdown(f"**Guests:** {booking['guests']}")
                st.markdown(f"**Contact:** {booking['email']}")
            
            with col3:
                st.markdown(f"**Created:** {booking['created_at'][:10]}")
                
                # Action buttons for pending requests
                if booking['status'] == 'pending':
                    col_confirm, col_reject = st.columns(2)
                    
                    with col_confirm:
                        if st.button("✅ Confirm", key=f"confirm_{booking['id']}"):
                            BookingOperations.update_booking_status(booking['id'], 'confirmed')
                            st.success("Booking confirmed!")
                            st.rerun()
                    
                    with col_reject:
                        if st.button("❌ Reject", key=f"reject_{booking['id']}"):
                            BookingOperations.update_booking_status(booking['id'], 'rejected')
                            st.warning("Booking rejected!")
                            st.rerun()
            
            # Expandable details
            with st.expander("View Details", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Phone:** {booking.get('phone', 'Not provided')}")
                    if booking.get('special_requests'):
                        st.write(f"**Special Requests:**")
                        st.write(booking['special_requests'])
                
                with col2:
                    if booking.get('notes'):
                        st.write(f"**Additional Notes:**")
                        st.write(booking['notes'])
                
                # Update status and notes
                st.write("**Update Booking:**")
                new_status = st.selectbox(
                    "Change Status:",
                    ["pending", "confirmed", "cancelled", "rejected"],
                    index=["pending", "confirmed", "cancelled", "rejected"].index(booking['status']),
                    key=f"status_{booking['id']}"
                )
                
                staff_notes = st.text_area(
                    "Staff Notes:",
                    value=booking.get('notes', ''),
                    key=f"notes_{booking['id']}"
                )
                
                if st.button(f"Update Booking #{booking['id']}", key=f"update_{booking['id']}"):
                    BookingOperations.update_booking_status(booking['id'], new_status, staff_notes)
                    st.success("Booking updated!")
                    st.rerun()

def show_manage_bookings():
    """Manage all bookings"""
    st.header("🗂️ Manage All Bookings")
    
    bookings = BookingOperations.get_all_booking_requests()
    
    if not bookings:
        st.info("No bookings found.")
        return
    
    # Convert to DataFrame for better display
    df_data = []
    for booking in bookings:
        df_data.append({
            'ID': booking['id'],
            'Guest': booking['guest_name'],
            'Type': booking['booking_type'].title(),
            'Check-in': booking['check_in'],
            'Check-out': booking['check_out'],
            'Guests': booking['guests'],
            'Lodging': booking.get('lodging_name', 'TBA'),
            'Status': booking['status'],
            'Created': booking['created_at'][:10]
        })
    
    df = pd.DataFrame(df_data)
    
    # Display as interactive dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Bulk operations
    st.subheader("Bulk Operations")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("Select booking IDs for bulk operations (coming soon)")
    
    with col2:
        if st.button("Export to CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"bookings_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

def show_availability_management():
    """Enhanced availability management page with upfront calendar view"""
    st.header("🗓️ Availability Management")
    
    # Get data for calendar
    units = BookingOperations.get_all_lodging_units()
    bookings = BookingOperations.get_all_booking_requests()
    
    if not units:
        st.warning("No lodging units found")
        return
    
    # Location filter
    locations = list(set(unit['location'] for unit in units))
    selected_location = st.selectbox(
        "Filter by location (optional):",
        ["All Locations"] + locations,
        key="availability_location_filter"
    )
    
    location_filter = None if selected_location == "All Locations" else selected_location
    
    # Create availability calendar
    availability_df = create_availability_calendar(units, bookings, days_ahead=21)
    
    if availability_df.empty:
        st.warning("No availability data to display")
        return
    
    # Show summary statistics
    summary = get_availability_summary(availability_df)
    if summary:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Capacity", f"{len(units)} units")
        with col2:
            st.metric("Available Slots", summary.get('available_slots', 0))
        with col3:
            st.metric("Occupied Slots", summary.get('occupied_slots', 0))
        with col4:
            st.metric("Occupancy Rate", f"{summary.get('occupancy_rate', 0)}%")
    
    st.markdown("---")
    
    # Visual calendar display
    create_visual_calendar(availability_df, location_filter)
    
    # Detailed availability table
    st.subheader("Detailed Availability")
    
    # Filter dataframe by location if selected
    display_df = availability_df.copy()
    if location_filter:
        display_df = display_df[display_df['location'] == location_filter]
    
    # Group by unit and show next 7 days
    unique_units = display_df[['unit_id', 'unit_name', 'location', 'capacity']].drop_duplicates()
    
    for _, unit in unique_units.iterrows():
        with st.expander(f"{get_location_emoji(unit['location'])} {unit['unit_name']} (Capacity: {unit['capacity']})"):
            unit_data = display_df[display_df['unit_id'] == unit['unit_id']].head(7)
            
            for _, day in unit_data.iterrows():
                col1, col2, col3 = st.columns([2, 1, 3])
                
                with col1:
                    st.write(day['date'].strftime('%A, %B %d'))
                
                with col2:
                    if day['available']:
                        st.success("Available")
                    else:
                        if day['booking_info'] and day['booking_info']['status'] == 'pending':
                            st.warning("Pending")
                        else:
                            st.error("Booked")
                
                with col3:
                    if not day['available'] and day['booking_info']:
                        info = day['booking_info']
                        st.write(f"Guest: {info.get('guest_name', 'Unknown')} ({info.get('booking_type', 'N/A')})")


def show_active_stays():
    """Show all currently active stays"""
    st.header("🏠 Active Stays")

    # Get active stays
    active_stays = BookingOperations.get_active_stays()

    if not active_stays:
        st.info("No active stays currently. This shows confirmed bookings where guests are currently checked in (today is between check-in and check-out dates).")
        return

    st.success(f"Currently {len(active_stays)} active {'stay' if len(active_stays) == 1 else 'stays'}")

    # Display each active stay
    for stay in active_stays:
        with st.container():
            st.markdown("---")

            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(f"### {stay['guest_name']}")
                if stay.get('lodging_name'):
                    st.markdown(f"📍 **Room:** {format_lodging_display(stay['lodging_name'], stay['lodging_location'])}")
                else:
                    st.warning("⚠️ No room assigned yet")
                st.markdown(f"**Type:** {stay['booking_type'].title()}")

            with col2:
                check_in = datetime.strptime(stay['check_in'], '%Y-%m-%d').date()
                check_out = datetime.strptime(stay['check_out'], '%Y-%m-%d').date()
                days_in = (date.today() - check_in).days
                days_remaining = (check_out - date.today()).days

                st.markdown(f"**Checked in:** {check_in.strftime('%b %d')}")
                st.markdown(f"**Check out:** {check_out.strftime('%b %d')}")
                st.markdown(f"**Days in:** {days_in}")
                st.markdown(f"**Days remaining:** {days_remaining}")

            with col3:
                st.markdown(f"**Guests:** {stay['guests']}")
                st.markdown(f"**Email:** {stay['email']}")
                if stay.get('phone'):
                    st.markdown(f"**Phone:** {stay['phone']}")

            # Expandable details
            with st.expander("View Details & Update"):
                if stay.get('special_requests'):
                    st.write(f"**Special Requests:** {stay['special_requests']}")

                if stay.get('notes'):
                    st.write(f"**Notes:** {stay['notes']}")

                # Quick actions
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"End Stay Early", key=f"cancel_{stay['id']}"):
                        if BookingOperations.update_booking_status(stay['id'], 'cancelled', "Stay ended early by staff"):
                            st.success("Stay ended")
                            st.rerun()

                with col2:
                    new_notes = st.text_area("Add/Update Notes:", value=stay.get('notes', ''), key=f"notes_{stay['id']}")
                    if st.button(f"Update Notes", key=f"update_notes_{stay['id']}"):
                        if BookingOperations.update_booking_status(stay['id'], 'confirmed', new_notes):
                            st.success("Notes updated")
                            st.rerun()


def show_room_assignment():
    """Interface for assigning rooms to pending booking requests"""
    st.header("🔑 Room Assignment & Direct Booking")

    # Create tabs for different actions
    tab1, tab2 = st.tabs(["📋 Assign to Inquiries", "➕ Create Direct Booking"])

    with tab1:
        st.info("Assign specific rooms to pending booking inquiries. Remember: staff always assigns rooms, guests never self-book.")
        show_inquiry_assignment()

    with tab2:
        st.info("Create a direct booking for family, friends, staff, or to block off a room - without going through the inquiry system.")
        show_direct_booking_form()


def show_inquiry_assignment():
    """Show the inquiry assignment interface"""
    # Get pending bookings (inquiries without room assignments)
    pending_bookings = BookingOperations.get_all_booking_requests(status='pending')

    if not pending_bookings:
        st.success("✅ No pending inquiries need room assignment!")
        st.info("All current inquiries either have rooms assigned or are not yet confirmed. Check 'Booking Requests' to review and confirm pending inquiries.")
        return

    # Filter to show only those without room assignment
    unassigned = [b for b in pending_bookings if not b.get('lodging_unit_id')]
    assigned_pending = [b for b in pending_bookings if b.get('lodging_unit_id')]

    if unassigned:
        st.warning(f"⏳ {len(unassigned)} {'inquiry needs' if len(unassigned) == 1 else 'inquiries need'} room assignment")

        for booking in unassigned:
            with st.container():
                st.markdown("---")

                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"### {booking['guest_name']}")
                    check_in = datetime.strptime(booking['check_in'], '%Y-%m-%d').date()
                    check_out = datetime.strptime(booking['check_out'], '%Y-%m-%d').date()
                    st.markdown(f"**Dates:** {format_date_range(check_in, check_out)}")
                    st.markdown(f"**Type:** {booking['booking_type'].title()}")
                    st.markdown(f"**Guests:** {booking['guests']}")

                with col2:
                    st.markdown(f"**Email:** {booking['email']}")
                    if booking.get('phone'):
                        st.markdown(f"**Phone:** {booking['phone']}")
                    st.markdown(f"**Created:** {booking['created_at'][:10]}")

                # Show special requests if any
                if booking.get('special_requests'):
                    st.info(f"**Special Requests:** {booking['special_requests']}")

                # Get available units for these dates
                available_units = BookingOperations.get_available_units(
                    check_in,
                    check_out,
                    booking['guests']
                )

                if not available_units:
                    st.error("❌ No available accommodations for these dates and guest count")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Contact Guest", key=f"contact_{booking['id']}"):
                            st.info(f"Contact {booking['guest_name']} at {booking['email']}")
                    with col2:
                        if st.button(f"Reject Inquiry", key=f"reject_assign_{booking['id']}"):
                            if BookingOperations.update_booking_status(booking['id'], 'rejected', "No availability for requested dates"):
                                st.warning("Inquiry rejected")
                                st.rerun()
                else:
                    st.success(f"✅ {len(available_units)} available accommodations found")

                    # Group by location for easier selection
                    locations = {}
                    for unit in available_units:
                        location = unit['location']
                        if location not in locations:
                            locations[location] = []
                        locations[location].append(unit)

                    # Room selection
                    selected_unit_id = None

                    for location, units in locations.items():
                        st.markdown(f"**{get_location_emoji(location)} {location}**")

                        for unit in units:
                            col1, col2, col3 = st.columns([2, 1, 1])

                            with col1:
                                st.write(f"• {unit['name']}")
                                if unit.get('description'):
                                    st.caption(unit['description'])

                            with col2:
                                st.write(f"Capacity: {unit['capacity']}")

                            with col3:
                                if st.button(f"Assign", key=f"assign_{booking['id']}_{unit['id']}"):
                                    try:
                                        if BookingOperations.assign_room_to_booking(booking['id'], unit['id']):
                                            st.success(f"✅ Assigned {unit['name']} to {booking['guest_name']}")
                                            st.balloons()
                                            st.rerun()
                                    except ValueError as e:
                                        st.error(f"Failed to assign room: {str(e)}")

    if assigned_pending:
        st.markdown("---")
        st.subheader("📋 Pending Inquiries with Rooms Assigned")
        st.info(f"{len(assigned_pending)} {'inquiry has' if len(assigned_pending) == 1 else 'inquiries have'} rooms assigned and awaiting confirmation")

        for booking in assigned_pending:
            with st.expander(f"{booking['guest_name']} - {booking.get('lodging_name', 'Unknown')}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Room:** {format_lodging_display(booking.get('lodging_name', 'Unknown'), booking.get('lodging_location', 'Unknown'))}")
                    st.write(f"**Dates:** {booking['check_in']} to {booking['check_out']}")
                    st.write(f"**Guests:** {booking['guests']}")

                with col2:
                    st.write(f"**Email:** {booking['email']}")
                    if booking.get('phone'):
                        st.write(f"**Phone:** {booking['phone']}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Confirm Booking", key=f"confirm_assign_{booking['id']}"):
                        if BookingOperations.update_booking_status(booking['id'], 'confirmed'):
                            st.success("Booking confirmed!")
                            st.rerun()

                with col2:
                    if st.button(f"Change Room", key=f"change_{booking['id']}"):
                        # Clear the assignment to allow re-assignment
                        if BookingOperations.assign_room_to_booking(booking['id'], booking['lodging_unit_id']):
                            st.info("You can now assign a different room above")


def show_direct_booking_form():
    """Form for staff to create direct bookings"""
    st.markdown("### Create New Booking")

    with st.form("direct_booking_form"):
        col1, col2 = st.columns(2)

        with col1:
            guest_name = st.text_input("Guest Name *", help="Full name of guest or 'BLOCKED' to block off room")
            email = st.text_input("Email", help="Optional for room blocks")
            phone = st.text_input("Phone", help="Optional")

            booking_type = st.selectbox(
                "Booking Type *",
                ["respite", "refuge", "retreat", "staff", "family", "blocked"],
                format_func=lambda x: x.title()
            )

        with col2:
            check_in = st.date_input("Check-in Date *", value=date.today())
            check_out = st.date_input("Check-out Date *", value=date.today() + timedelta(days=3))
            guests = st.number_input("Number of Guests *", min_value=1, max_value=20, value=1)

        # Room selection
        st.markdown("### Select Room")

        # Get available units for the selected dates
        if check_in and check_out and check_in < check_out:
            available_units = BookingOperations.get_available_units(
                check_in,
                check_out,
                guests
            )

            if available_units:
                # Group by location
                locations = {}
                for unit in available_units:
                    location = unit['location']
                    if location not in locations:
                        locations[location] = []
                    locations[location].append(unit)

                selected_unit_id = None
                for location, units in locations.items():
                    st.markdown(f"**{get_location_emoji(location)} {location}**")

                    unit_options = {f"{unit['name']} (Capacity: {unit['capacity']})": unit['id'] for unit in units}

                    if unit_options:
                        selected = st.selectbox(
                            f"Choose unit in {location}:",
                            options=["-- Select --"] + list(unit_options.keys()),
                            key=f"select_{location}"
                        )

                        if selected != "-- Select --":
                            selected_unit_id = unit_options[selected]
                            break

                # Store selected unit in form
                if 'selected_unit_id' not in locals():
                    selected_unit_id = None
            else:
                st.warning("No available units for these dates and guest count. Try different dates or guest count.")
                selected_unit_id = None
        else:
            st.warning("Please select valid check-in and check-out dates")
            selected_unit_id = None

        special_requests = st.text_area("Special Requests/Notes", help="Any notes about this booking")

        submitted = st.form_submit_button("Create Booking", type="primary")

        if submitted:
            # Validation
            if not guest_name:
                st.error("Guest name is required")
            elif not check_in or not check_out:
                st.error("Check-in and check-out dates are required")
            elif check_in >= check_out:
                st.error("Check-out must be after check-in")
            elif not selected_unit_id:
                st.error("Please select a room")
            else:
                # Create the booking
                try:
                    booking_data = {
                        'guest_name': guest_name,
                        'email': email if email else f"staff-booking-{datetime.now().timestamp()}@wellspring.local",
                        'phone': phone,
                        'booking_type': booking_type,
                        'check_in': check_in,
                        'check_out': check_out,
                        'guests': guests,
                        'lodging_unit_id': selected_unit_id,
                        'special_requests': special_requests,
                        'notes': f"Direct booking created by staff on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    }

                    booking_id = BookingOperations.create_booking_request(booking_data)

                    if booking_id:
                        # Auto-confirm the booking
                        BookingOperations.update_booking_status(booking_id, 'confirmed', booking_data['notes'])

                        st.success(f"✅ Booking created and confirmed! Booking ID: {booking_id}")
                        st.balloons()
                        st.info("The booking has been automatically confirmed. You can view it in 'Manage Bookings' or 'Active Stays'.")

                        # Provide a button to create another
                        if st.button("Create Another Booking"):
                            st.rerun()
                    else:
                        st.error("Failed to create booking")

                except Exception as e:
                    st.error(f"Error creating booking: {str(e)}")


def show_reports():
    """Show various reports"""
    st.header("📈 Reports")
    
    # Date range for reports
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Report Start Date:", value=date.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("Report End Date:", value=date.today())
    
    # Get bookings in date range
    all_bookings = BookingOperations.get_all_booking_requests()
    
    # Filter by date range
    filtered_bookings = []
    for booking in all_bookings:
        booking_date = datetime.strptime(booking['created_at'][:10], '%Y-%m-%d').date()
        if start_date <= booking_date <= end_date:
            filtered_bookings.append(booking)
    
    if not filtered_bookings:
        st.info("No bookings found in the selected date range.")
        return
    
    # Booking statistics
    st.subheader("📊 Booking Statistics")
    
    # Status distribution
    status_counts = {}
    for booking in filtered_bookings:
        status = booking['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Status Distribution:**")
        for status, count in status_counts.items():
            st.write(f"• {status.title()}: {count}")
    
    # Booking type distribution
    type_counts = {}
    for booking in filtered_bookings:
        btype = booking['booking_type']
        type_counts[btype] = type_counts.get(btype, 0) + 1
    
    with col2:
        st.write("**Booking Type Distribution:**")
        for btype, count in type_counts.items():
            st.write(f"• {btype.title()}: {count}")
    
    # Location popularity
    st.subheader("🏠 Location Popularity")
    
    location_counts = {}
    for booking in filtered_bookings:
        location = booking.get('lodging_location', 'Unknown')
        location_counts[location] = location_counts.get(location, 0) + 1
    
    for location, count in location_counts.items():
        st.write(f"• {location}: {count} bookings")
    
    # Export functionality
    st.markdown("---")
    st.subheader("📥 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export Filtered Bookings"):
            try:
                df = pd.DataFrame(filtered_bookings)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"bookings_report_{start_date}_to_{end_date}.csv",
                    mime="text/csv"
                )
                show_success_message("Export ready for download!")
            except Exception as e:
                show_error_message(f"Export failed: {str(e)}")
    
    with col2:
        if st.button("Export All Data"):
            try:
                all_data = BookingOperations.get_all_booking_requests(limit=1000)
                df = pd.DataFrame(all_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download All Bookings CSV",
                    data=csv,
                    file_name=f"all_bookings_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key="download_all"
                )
                show_success_message("Full export ready for download!")
            except Exception as e:
                show_error_message(f"Export failed: {str(e)}")
    
    # Property Management Summary (if available)
    try:
        property_summary = PropertyManagementOperations.get_property_dashboard_summary()
        if property_summary:
            st.markdown("---")
            st.subheader("🏠 Property Management Summary")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Pending Maintenance", property_summary.get('pending_maintenance', 0))
            with col2:
                st.metric("Pending Todos", property_summary.get('pending_todos', 0))
            with col3:
                st.metric("Property Files", property_summary.get('total_files', 0))
    except Exception as e:
        st.info("Property management data not available yet")
    location_counts = {}
    for booking in filtered_bookings:
        if booking.get('lodging_location'):
            loc = booking['lodging_location']
            location_counts[loc] = location_counts.get(loc, 0) + 1
    
    if location_counts:
        for location, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True):
            st.write(f"• {get_location_emoji(location)} {location}: {count} bookings")
    
    # Export report
    st.subheader("📤 Export Report")
    if st.button("Generate Full Report"):
        # Create comprehensive report data
        report_data = []
        for booking in filtered_bookings:
            report_data.append({
                'Booking ID': booking['id'],
                'Guest Name': booking['guest_name'],
                'Email': booking['email'],
                'Phone': booking.get('phone', ''),
                'Booking Type': booking['booking_type'],
                'Check In': booking['check_in'],
                'Check Out': booking['check_out'],
                'Guests': booking['guests'],
                'Lodging': booking.get('lodging_name', ''),
                'Location': booking.get('lodging_location', ''),
                'Status': booking['status'],
                'Created Date': booking['created_at'][:10],
                'Special Requests': booking.get('special_requests', ''),
                'Notes': booking.get('notes', '')
            })
        
        df = pd.DataFrame(report_data)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="Download Report CSV",
            data=csv,
            file_name=f"booking_report_{start_date}_to_{end_date}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    show_staff_page()