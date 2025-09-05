import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_password(password_type: str) -> bool:
    """Check if the entered password is correct"""
    if password_type == "public":
        correct_password = os.getenv("PUBLIC_PASSWORD", "public123")
    elif password_type == "staff":
        correct_password = os.getenv("STAFF_PASSWORD", "staff123")
    else:
        return False
    
    # Initialize session state
    if f"{password_type}_authenticated" not in st.session_state:
        st.session_state[f"{password_type}_authenticated"] = False
    
    # If already authenticated, return True
    if st.session_state[f"{password_type}_authenticated"]:
        return True
    
    # Create password input
    st.title("🏔️ Wellspring Mountain")
    st.subheader(f"{'Public Booking' if password_type == 'public' else 'Staff Dashboard'} Access")
    
    password = st.text_input(
        "Enter Password:", 
        type="password",
        key=f"{password_type}_password"
    )
    
    if st.button(f"Access {'Booking System' if password_type == 'public' else 'Staff Dashboard'}"):
        if password == correct_password:
            st.session_state[f"{password_type}_authenticated"] = True
            st.success("Access granted!")
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")
    
    return False

def logout(password_type: str):
    """Logout function"""
    st.session_state[f"{password_type}_authenticated"] = False
    st.rerun()

def is_authenticated(password_type: str) -> bool:
    """Check if user is authenticated"""
    return st.session_state.get(f"{password_type}_authenticated", False)

def require_auth(password_type: str):
    """Decorator-like function to require authentication"""
    if not is_authenticated(password_type):
        check_password(password_type)
        st.stop()

def create_logout_button(password_type: str):
    """Create a logout button in the sidebar"""
    with st.sidebar:
        st.write("---")
        if st.button(f"🚪 Logout", key=f"{password_type}_logout"):
            logout(password_type)