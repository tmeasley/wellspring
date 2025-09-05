import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from utils.auth import require_auth, create_logout_button
from utils.helpers import (
    format_booking_status, get_location_emoji, create_summary_metric,
    format_date_range, get_booking_type_info
)
from database.operations import BookingOperations

def show_staff_page():
    """Main staff dashboard"""
    require_auth("staff")
    create_logout_button("staff")
    
    st.title("🏢 Staff Dashboard - Wellspring Mountain")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("📋 Dashboard Menu")
        page = st.radio(
            "Select view:",
            ["Overview", "Booking Requests", "Manage Bookings", "Availability", "Reports"],
            key="staff_page_selection"
        )
    
    if page == "Overview":
        show_overview()
    elif page == "Booking Requests":
        show_booking_requests()
    elif page == "Manage Bookings":
        show_manage_bookings()
    elif page == "Availability":
        show_availability_management()
    elif page == "Reports":
        show_reports()

def show_overview():
    """Dashboard overview with key metrics"""
    st.header("📊 Dashboard Overview")
    
    # Get summary statistics
    summary = BookingOperations.get_booking_summary()
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_summary_metric("Total Units", summary['total_units'])
    
    with col2:
        create_summary_metric("Pending Requests", summary['pending_requests'])
    
    with col3:
        create_summary_metric("Current Occupancy", summary['current_occupancy'])
    
    with col4:
        create_summary_metric("Confirmed This Month", summary['confirmed_this_month'])
    
    # Recent booking requests
    st.subheader("🔔 Recent Booking Requests")
    recent_bookings = BookingOperations.get_all_booking_requests()[:10]
    
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
                    st.markdown(f"📍 {booking['lodging_name']} ({booking['lodging_location']})")
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
    """Manage unit availability"""
    st.header("📅 Availability Management")
    
    # Get all lodging units
    units = BookingOperations.get_all_lodging_units()
    
    if not units:
        st.error("No lodging units found. Please initialize the database.")
        return
    
    # Unit selection
    unit_options = {f"{unit['name']} ({unit['location']})": unit for unit in units}
    selected_unit_name = st.selectbox("Select Unit:", list(unit_options.keys()))
    selected_unit = unit_options[selected_unit_name]
    
    st.info(f"Managing: **{selected_unit['name']}** - {selected_unit['description']}")
    
    # Date range for blocking
    st.subheader("Block Dates")
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Start Date:",
            value=date.today(),
            min_value=date.today()
        )
    
    with col2:
        end_date = st.date_input(
            "End Date:",
            value=date.today() + timedelta(days=1),
            min_value=start_date + timedelta(days=1)
        )
    
    notes = st.text_area("Reason for blocking:", placeholder="Maintenance, cleaning, etc.")
    
    if st.button("Block Dates"):
        success = BookingOperations.block_dates(selected_unit['id'], start_date, end_date, notes)
        if success:
            st.success(f"Dates blocked for {selected_unit['name']}")
        else:
            st.error("Failed to block dates")
    
    # Show upcoming bookings for this unit
    st.subheader(f"Upcoming Bookings - {selected_unit['name']}")
    unit_bookings = [
        b for b in BookingOperations.get_all_booking_requests('confirmed')
        if b.get('lodging_unit_id') == selected_unit['id']
    ]
    
    if unit_bookings:
        for booking in unit_bookings:
            check_in_date = datetime.strptime(booking['check_in'], '%Y-%m-%d').date()
            check_out_date = datetime.strptime(booking['check_out'], '%Y-%m-%d').date()
            
            if check_out_date >= date.today():
                st.write(f"• **{booking['guest_name']}** - {format_date_range(check_in_date, check_out_date)}")
    else:
        st.info("No confirmed bookings for this unit.")

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