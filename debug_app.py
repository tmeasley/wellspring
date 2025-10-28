#!/usr/bin/env python3
"""
Debug version of the app to isolate the property management issue
"""

import streamlit as st

def debug_property_page():
    st.title("🏠 DEBUG: Property Management")
    st.write("This is a debug version to test if the property management page renders at all")
    
    st.success("✅ If you can see this, the page is working!")
    
    # Test basic functionality
    if st.button("Test Button"):
        st.success("Button works!")
    
    # Test selectbox
    option = st.selectbox("Test selector:", ["Option 1", "Option 2", "Option 3"])
    st.write(f"You selected: {option}")
    
    # Test metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Test Metric 1", 5)
    with col2:
        st.metric("Test Metric 2", 10)
    with col3:
        st.metric("Test Metric 3", 15)

def debug_staff_page():
    st.title("🏢 DEBUG: Staff Dashboard")
    
    # Simple navigation without authentication
    page = st.selectbox("Select view:", ["Overview", "Property Management Debug"])
    
    if page == "Overview":
        st.subheader("📊 Overview")
        st.write("This is the overview page")
        
    elif page == "Property Management Debug":
        debug_property_page()

def main():
    st.set_page_config(
        page_title="DEBUG: Wellspring Mountain",
        page_icon="🏔️",
        layout="wide"
    )
    
    st.sidebar.title("🏔️ DEBUG MODE")
    access_level = st.sidebar.radio("Select Access:", ["Public Booking", "Staff Dashboard (No Auth)"])
    
    if access_level == "Staff Dashboard (No Auth)":
        debug_staff_page()
    else:
        st.title("🏠 Public Booking")
        st.write("Public booking would be here")

if __name__ == "__main__":
    main()