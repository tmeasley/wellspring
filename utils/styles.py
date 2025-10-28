"""
Custom styling and CSS for Wellspring Mountain Booking System
"""
import streamlit as st

def inject_custom_css():
    """Inject modern Airbnb-style CSS styling into the Streamlit app"""
    st.markdown("""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    html, body, [class*="css"]  {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main app styling */
    .main-header {
        background: linear-gradient(135deg, #FF5A5F 0%, #FF385C 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(255, 56, 92, 0.15);
    }
    
    /* Step progress indicator */
    .step-progress {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
    
    .step-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #e0e0e0;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 0.5rem;
        font-weight: bold;
    }
    
    .step-circle.active {
        background: #4CAF50;
        color: white;
    }
    
    .step-circle.completed {
        background: #2196F3;
        color: white;
    }
    
    /* Modern Airbnb-style booking cards */
    .booking-card {
        border: 1px solid #EBEBEB;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        text-align: left;
        transition: all 0.2s ease;
        cursor: pointer;
        background: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
    }
    
    .booking-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(0,0,0,0.12);
        border-color: #FF385C;
    }
    
    .booking-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #FF385C, #FF5A5F);
    }
    
    .booking-card h3 {
        font-size: 22px;
        font-weight: 600;
        color: #222222;
        margin-bottom: 8px;
    }
    
    .booking-card p {
        font-size: 16px;
        color: #717171;
        line-height: 1.4;
        margin-bottom: 12px;
    }
    
    .booking-card small {
        font-size: 14px;
        color: #717171;
        font-weight: 500;
    }
    
    /* Lodging unit cards */
    .lodging-card {
        border: 1px solid #ddd;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .lodging-card:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Status badges */
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        text-transform: uppercase;
    }
    
    .status-pending {
        background-color: #FFF3E0;
        color: #F57C00;
        border: 1px solid #FFB74D;
    }
    
    .status-confirmed {
        background-color: #E8F5E8;
        color: #2E7D32;
        border: 1px solid #81C784;
    }
    
    .status-cancelled {
        background-color: #FFEBEE;
        color: #C62828;
        border: 1px solid #EF5350;
    }
    
    /* Form enhancements */
    .form-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #4CAF50;
    }
    
    /* Metrics styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #2196F3;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Calendar styling */
    .calendar-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    /* Success/Error message styling */
    .success-banner {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .error-banner {
        background: linear-gradient(90deg, #F44336, #FF5722);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Modern Airbnb-style buttons */
    .stButton > button {
        background: #FF385C !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 14px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.2s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton > button:hover {
        background: #E31C5F !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(255, 56, 92, 0.3) !important;
    }
    
    /* Secondary button style */
    .stButton > button[kind="secondary"] {
        background: white !important;
        color: #FF385C !important;
        border: 2px solid #FF385C !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #FF385C !important;
        color: white !important;
    }
    
    /* Modern sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: #FAFAFA !important;
        border-right: 1px solid #EBEBEB !important;
    }
    
    /* Sidebar navigation items */
    .css-1d391kg .stRadio > label {
        background: white;
        padding: 12px 16px;
        border-radius: 12px;
        margin: 4px 0;
        border: 1px solid #EBEBEB;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .css-1d391kg .stRadio > label:hover {
        border-color: #FF385C;
        box-shadow: 0 2px 8px rgba(255, 56, 92, 0.1);
    }
    
    /* Modern data table styling */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border: 1px solid #EBEBEB;
    }
    
    /* Modern metric cards */
    .metric-container {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #F0F0F0;
        transition: all 0.2s ease;
    }
    
    .metric-container:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    
    /* Modern form styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        border-radius: 8px !important;
        border: 2px solid #EBEBEB !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        transition: all 0.2s ease !important;
    }

    /* Increase dropdown menu height */
    .stSelectbox [data-baseweb="popover"] {
        max-height: 500px !important;
    }

    .stSelectbox [role="listbox"] {
        max-height: 500px !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        max-height: 500px !important;
    }

    /* Make individual dropdown items taller and more readable */
    .stSelectbox [role="option"] {
        min-height: 48px !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > div:focus {
        border-color: #FF385C !important;
        box-shadow: 0 0 0 3px rgba(255, 56, 92, 0.1) !important;
        outline: none !important;
    }
    
    /* Modern tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 12px;
        padding: 12px 20px;
        border: 2px solid #EBEBEB;
        color: #717171;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: #FF385C !important;
        border-color: #FF385C !important;
        color: white !important;
    }
    
    /* Modern headers */
    h1, h2, h3 {
        color: #222222 !important;
        font-weight: 600 !important;
    }
    
    h1 {
        font-size: 32px !important;
        font-weight: 700 !important;
    }
    
    /* Modern containers */
    .modern-container {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.08);
        border: 1px solid #F0F0F0;
        margin: 16px 0;
    }
    
    /* Property card styling */
    .property-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border: 1px solid #EBEBEB;
        transition: all 0.2s ease;
        margin: 12px 0;
    }
    
    .property-card:hover {
        box-shadow: 0 6px 24px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Modern success/error styling */
    .stSuccess {
        background: #F7FDF0 !important;
        border: 1px solid #00A400 !important;
        border-radius: 12px !important;
        color: #00A400 !important;
    }
    
    .stError {
        background: #FFF8F6 !important;
        border: 1px solid #FF385C !important;
        border-radius: 12px !important;
        color: #FF385C !important;
    }
    
    .stInfo {
        background: #F0F9FF !important;
        border: 1px solid #0066CC !important;
        border-radius: 12px !important;
        color: #0066CC !important;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    </style>
    """, unsafe_allow_html=True)

def create_step_progress(current_step: int, total_steps: int = 5):
    """Create a visual step progress indicator"""
    steps = ["Type", "Dates", "Info", "Room", "Confirm"]
    
    progress_html = '<div class="step-progress">'
    for i in range(total_steps):
        step_class = "step-circle"
        if i + 1 < current_step:
            step_class += " completed"
        elif i + 1 == current_step:
            step_class += " active"
        
        progress_html += f'<div class="{step_class}">{i + 1}</div>'
        if i < total_steps - 1:
            progress_html += '<div style="flex: 1; height: 2px; background: #e0e0e0; align-self: center; margin: 0 0.5rem;"></div>'
    
    progress_html += '</div>'
    
    # Add step labels
    progress_html += '<div style="display: flex; justify-content: center; margin-top: 0.5rem;">'
    for i, step in enumerate(steps):
        color = "#4CAF50" if i + 1 <= current_step else "#999"
        progress_html += f'<div style="margin: 0 1rem; color: {color}; font-size: 0.8rem; text-align: center;">{step}</div>'
    progress_html += '</div>'
    
    st.markdown(progress_html, unsafe_allow_html=True)

def create_booking_type_card(booking_type: str, info: dict, key: str):
    """Create an enhanced booking type selection card"""
    card_html = f'''
    <div class="booking-card {booking_type}" onclick="selectBookingType('{booking_type}')">
        <h3 style="margin: 0; color: {info['color']};">{info['title']}</h3>
        <p style="margin: 1rem 0;">{info['description']}</p>
        {f"<small><strong>Max duration:</strong> {info['max_duration']} days</small>" if info['max_duration'] else "<small>Flexible duration</small>"}
    </div>
    '''
    return card_html

def create_metric_card(title: str, value: str, delta: str = None):
    """Create a styled metric card"""
    delta_html = ""
    if delta:
        delta_color = "#4CAF50" if delta.startswith("+") else "#F44336"
        delta_html = f'<div style="color: {delta_color}; font-size: 0.9rem; margin-top: 0.5rem;">{delta}</div>'
    
    return f'''
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{title}</div>
        {delta_html}
    </div>
    '''

def create_status_badge(status: str):
    """Create a styled status badge"""
    return f'<span class="status-badge status-{status}">{status}</span>'

def show_success_message(message: str):
    """Display a styled success message"""
    st.markdown(f'<div class="success-banner">✅ {message}</div>', unsafe_allow_html=True)

def show_error_message(message: str):
    """Display a styled error message"""
    st.markdown(f'<div class="error-banner">❌ {message}</div>', unsafe_allow_html=True)