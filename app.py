import streamlit as st
import os
from database.models import initialize_database, seed_initial_data
from pages.booking import show_booking_page
from pages.staff import show_staff_page

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
    
    # Initialize database
    init_database()
    
    # Main navigation
    st.sidebar.title("🏔️ Wellspring Mountain")
    st.sidebar.markdown("---")
    
    # Navigation menu
    page = st.sidebar.radio(
        "Select Access Level:",
        ["🏠 Public Booking", "🏢 Staff Dashboard"],
        key="main_navigation"
    )
    
    # Add information section
    with st.sidebar:
        st.markdown("---")
        st.markdown("""
        ### ℹ️ About
        
        **Wellspring Mountain** offers:
        - 🏠 Refuge (up to 3 months)
        - 🌿 Respite (up to 3 weeks)  
        - 👥 Group Retreats
        
        Contact us for more information or assistance with your booking.
        """)
        
        # Contact information (you can customize this)
        st.markdown("""
        ### 📞 Contact
        - **Phone:** (555) 123-4567
        - **Email:** info@wellspringmountain.org
        """)
    
    # Route to appropriate page
    if page == "🏠 Public Booking":
        show_booking_page()
    elif page == "🏢 Staff Dashboard":
        show_staff_page()

if __name__ == "__main__":
    main()