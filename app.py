import streamlit as st
import os
from database.models import initialize_database, seed_initial_data
from pages.booking import show_booking_page
from pages.staff import show_staff_page
from utils.styles import inject_custom_css

# Configure Streamlit page
st.set_page_config(
    page_title="Wellspring Mountain Booking",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def init_database():
    """Initialize database and seed initial data"""
    initialize_database()
    seed_initial_data()
    return True

def main():
    """Main application entry point"""

    # Inject custom CSS
    inject_custom_css()

    # Initialize database
    init_database()

    # Mobile-friendly navigation at top of page (always visible)
    st.title("🏔️ Wellspring Mountain")
    st.caption("Mountain Retreat Management")

    # Main navigation - visible on all devices
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Public Booking", use_container_width=True, type="primary" if st.session_state.get('page', 'public') == 'public' else "secondary"):
            st.session_state.page = 'public'
            st.rerun()
    with col2:
        if st.button("🏢 Staff Dashboard", use_container_width=True, type="primary" if st.session_state.get('page', 'public') == 'staff' else "secondary"):
            st.session_state.page = 'staff'
            st.rerun()

    st.markdown("---")

    # Get current page
    page = st.session_state.get('page', 'public')

    # Also keep sidebar navigation for desktop
    st.sidebar.title("🏔️ Wellspring Mountain")
    st.sidebar.caption("Mountain Retreat Management")

    # Sidebar navigation (for desktop)
    sidebar_page = st.sidebar.radio(
        "Choose your access:",
        ["🏠 Public Booking", "🏢 Staff Dashboard"],
        index=0 if page == 'public' else 1,
        key="sidebar_navigation"
    )

    # Sync sidebar selection with main navigation
    if sidebar_page == "🏠 Public Booking" and page != 'public':
        st.session_state.page = 'public'
        st.rerun()
    elif sidebar_page == "🏢 Staff Dashboard" and page != 'staff':
        st.session_state.page = 'staff'
        st.rerun()
    
    # Modern information section
    with st.sidebar:
        st.markdown("---")
        
        # Clean sidebar content without complex HTML
        st.markdown("---")
        st.markdown("**About Wellspring Mountain**")
        st.markdown("""
        🏠 **Refuge:** Long-term stays (up to 3 months)  
        🌿 **Respite:** Short stays (up to 3 weeks)  
        👥 **Retreats:** Group bookings
        """)
        
        st.markdown("---")
        st.markdown("**Contact Information**")
        st.markdown("""
        📞 **Phone:** 743-241-6310
        📧 **Email:** SpringMountainWellness@proton.me
        """)
    
    # Route to appropriate page based on session state
    if page == 'staff':
        show_staff_page()
    else:
        show_booking_page()

if __name__ == "__main__":
    main()