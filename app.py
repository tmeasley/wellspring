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
    
    # Clean sidebar header
    st.sidebar.title("🏔️ Wellspring Mountain")
    st.sidebar.caption("Mountain Retreat Management")
    
    # Clean navigation menu
    page = st.sidebar.radio(
        "Choose your access:",
        ["🏠 Public Booking", "🏢 Staff Dashboard"],
        key="main_navigation"
    )
    
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
        📞 **Phone:** (555) 123-4567  
        📧 **Email:** info@wellspringmountain.org
        """)
    
    # Route to appropriate page
    if page == "🏠 Public Booking":
        show_booking_page()
    elif page == "🏢 Staff Dashboard":
        show_staff_page()

if __name__ == "__main__":
    main()