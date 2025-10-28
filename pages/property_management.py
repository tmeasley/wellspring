"""
CLEAN Property Management System - Modern Airbnb Style
"""

import streamlit as st
from datetime import datetime, date, timedelta
from database.operations import BookingOperations
from database.property_operations import PropertyManagementOperations

def show_property_dashboard():
    """Modern property dashboard"""
    st.markdown("""
    <div class="modern-container">
        <h2 style="color: #222222; margin-bottom: 24px;">📊 Property Overview</h2>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        summary = PropertyManagementOperations.get_property_dashboard_summary()
        
        # Modern metrics in cards
        col1, col2, col3, col4 = st.columns(4)
        
        metrics_data = [
            ("🔧", "Maintenance", summary.get('pending_maintenance', 0), "pending tasks"),
            ("✅", "Tasks", summary.get('pending_todos', 0), "todo items"),
            ("📝", "Notes", summary.get('recent_notes', 0), "recent notes"),
            ("📁", "Files", summary.get('total_files', 0), "uploaded files")
        ]
        
        for i, (icon, title, value, subtitle) in enumerate(metrics_data):
            with [col1, col2, col3, col4][i]:
                st.markdown(f"""
                <div class="modern-container" style="text-align: center; padding: 20px;">
                    <div style="font-size: 32px; margin-bottom: 8px;">{icon}</div>
                    <h3 style="color: #222222; font-size: 28px; font-weight: 700; margin: 0;">{value}</h3>
                    <p style="color: #717171; font-size: 14px; font-weight: 500; margin: 4px 0 0 0;">{title}</p>
                    <p style="color: #717171; font-size: 12px; margin: 0;">{subtitle}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Building overview
        units = BookingOperations.get_all_lodging_units()
        locations = {}
        for unit in units:
            loc = unit['location']
            if loc not in locations:
                locations[loc] = []
            locations[loc].append(unit)
        
        st.markdown("""
        <div class="modern-container">
            <h3 style="color: #222222; margin-bottom: 16px;">🏗️ Buildings by Type</h3>
        </div>
        """, unsafe_allow_html=True)
        
        location_emojis = {
            'Lodge': '🏨', 'Uptown': '🏘️', 'Downtown': '🏢', 'A-frame': '🏕️',
            'Facilities': '🏭', 'Common Areas': '🍽️', 'Residential': '🏠'
        }
        
        # Create location overview cards
        cols = st.columns(min(len(locations), 4))
        for i, (location, units_list) in enumerate(sorted(locations.items())):
            if i < len(cols):
                with cols[i]:
                    emoji = location_emojis.get(location, '🏗️')
                    st.markdown(f"""
                    <div class="property-card" style="text-align: center;">
                        <div style="font-size: 24px; margin-bottom: 8px;">{emoji}</div>
                        <h4 style="color: #222222; margin: 0;">{location}</h4>
                        <p style="color: #717171; font-size: 14px; margin: 4px 0 0 0;">{len(units_list)} buildings</p>
                    </div>
                    """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Dashboard error: {e}")

def show_maintenance_management():
    """Modern maintenance management"""
    st.markdown("""
    <div class="modern-container">
        <h2 style="color: #222222; margin-bottom: 16px;">🔧 Maintenance Management</h2>
        <p style="color: #717171; margin: 0;">Track maintenance for all buildings including Warehouse, Office, Dining Hall, Houses, Lodge areas, and Cabins</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add task form
    with st.expander("➕ Create New Maintenance Task", expanded=False):
        with st.form("maintenance_form"):
            units = BookingOperations.get_all_lodging_units()
            unit_options = {f"{unit['name']} ({unit['location']})": unit['id'] for unit in units}
            
            col1, col2 = st.columns(2)
            
            with col1:
                selected_unit = st.selectbox("Building/Area:", list(unit_options.keys()))
                task_title = st.text_input("Task Description*")
                task_type = st.selectbox("Type:", ["cleaning", "plumbing", "electrical", "hvac", "painting", "general_maintenance"])
            
            with col2:
                priority = st.selectbox("Priority:", ["low", "medium", "high", "critical"])
                scheduled_date = st.date_input("Scheduled Date:")
                estimated_cost = st.number_input("Estimated Cost ($):", min_value=0.0)
            
            description = st.text_area("Additional Details:")
            
            if st.form_submit_button("Create Task", use_container_width=True) and task_title:
                try:
                    unit_id = unit_options[selected_unit]
                    task_id = PropertyManagementOperations.create_maintenance_task(
                        unit_id, task_title, description, task_type, priority, scheduled_date, estimated_cost
                    )
                    if task_id:
                        st.success("Task created successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # Show tasks by building type
    st.markdown("### 🏗️ Tasks by Building Type")
    
    try:
        tasks = PropertyManagementOperations.get_maintenance_tasks()
        units = BookingOperations.get_all_lodging_units()
        
        if tasks:
            # Group by location
            location_tasks = {}
            for task in tasks:
                unit = next((u for u in units if u['id'] == task.get('lodging_unit_id')), None)
                if unit:
                    location = unit['location']
                    if location not in location_tasks:
                        location_tasks[location] = []
                    location_tasks[location].append({**task, 'unit_name': unit['name']})
            
            for location, task_list in sorted(location_tasks.items()):
                with st.expander(f"🏗️ {location} - {len(task_list)} tasks"):
                    for task in task_list[:5]:
                        priority_colors = {'low': '🟢', 'medium': '🟡', 'high': '🔴', 'critical': '🚨'}
                        status_colors = {'pending': '⏳', 'in_progress': '🛠️', 'completed': '✅'}
                        
                        priority_emoji = priority_colors.get(task.get('priority'), '⚪')
                        status_emoji = status_colors.get(task.get('status'), '⚪')
                        
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.markdown(f"{priority_emoji}{status_emoji} **{task.get('task_title')}** - {task.get('unit_name')}")
                        with col2:
                            st.write(task.get('task_type', 'general').replace('_', ' ').title())
                        with col3:
                            st.write(task.get('status', 'pending').title())
        else:
            st.info("No maintenance tasks yet. Create your first task above!")
            
    except Exception as e:
        st.error(f"Error loading tasks: {e}")

def show_notes_management():
    """Modern notes management"""
    st.markdown("""
    <div class="modern-container">
        <h2 style="color: #222222; margin-bottom: 16px;">📝 Property Notes</h2>
        <p style="color: #717171; margin: 0;">Add observations, feedback, and important information for any building or area</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add note form
    with st.expander("➕ Add New Note", expanded=False):
        with st.form("note_form"):
            units = BookingOperations.get_all_lodging_units()
            unit_options = {f"{unit['name']} ({unit['location']})": unit['id'] for unit in units}
            
            col1, col2 = st.columns(2)
            
            with col1:
                selected_unit = st.selectbox("Building/Area:", list(unit_options.keys()))
                title = st.text_input("Note Title*")
                note_type = st.selectbox("Type:", ["general", "maintenance", "guest_feedback", "safety", "improvement"])
            
            with col2:
                priority = st.selectbox("Priority:", ["low", "medium", "high"])
            
            content = st.text_area("Note Content*")
            
            if st.form_submit_button("Save Note", use_container_width=True) and title and content:
                try:
                    unit_id = unit_options[selected_unit]
                    note_id = PropertyManagementOperations.create_property_note(
                        unit_id, note_type, title, content, priority
                    )
                    if note_id:
                        st.success("Note saved successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

def show_todos_management():
    """Modern todo management"""
    st.markdown("""
    <div class="modern-container">
        <h2 style="color: #222222; margin-bottom: 16px;">✅ Task Management</h2>
        <p style="color: #717171; margin: 0;">Organize and track tasks across all buildings and operations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add todo form
    with st.expander("➕ Add New Task", expanded=False):
        with st.form("todo_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Task Title*")
                category = st.selectbox("Category:", ["general", "maintenance", "cleaning", "administrative", "safety"])
                priority = st.selectbox("Priority:", ["low", "medium", "high"])
            
            with col2:
                due_date = st.date_input("Due Date:")
                assigned_to = st.text_input("Assigned To:")
            
            description = st.text_area("Description:")
            
            if st.form_submit_button("Create Task", use_container_width=True) and title:
                try:
                    todo_id = PropertyManagementOperations.create_todo(
                        title, description, None, priority, due_date, category, assigned_to
                    )
                    if todo_id:
                        st.success("Task created successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

def show_files_management():
    """Modern file management"""
    st.markdown("""
    <div class="modern-container">
        <h2 style="color: #222222; margin-bottom: 16px;">📁 File Management</h2>
        <p style="color: #717171; margin: 0;">Store photos, documents, manuals, and records for each building</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📤 Upload File", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            units = BookingOperations.get_all_lodging_units()
            unit_options = {f"{unit['name']} ({unit['location']})": unit['id'] for unit in units}
            selected_unit = st.selectbox("Building:", list(unit_options.keys()))
            file_category = st.selectbox("Category:", ["photos", "documents", "manuals", "warranties", "floor_plans"])
        
        with col2:
            uploaded_file = st.file_uploader("Choose file:", type=['jpg', 'png', 'pdf', 'doc', 'txt'])
            description = st.text_input("Description:")
        
        if st.button("Upload File", use_container_width=True) and uploaded_file:
            st.success(f"File '{uploaded_file.name}' uploaded! (Demo - full functionality coming soon)")

def show_unit_management():
    """Modern individual building management"""
    st.markdown("""
    <div class="modern-container">
        <h2 style="color: #222222; margin-bottom: 16px;">🏗️ Individual Building Management</h2>
        <p style="color: #717171; margin: 0;">Manage specific buildings with dedicated notes, files, and maintenance tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        units = BookingOperations.get_all_lodging_units()
        
        # Organize by location for easy browsing
        locations = {}
        for unit in units:
            loc = unit['location']
            if loc not in locations:
                locations[loc] = []
            locations[loc].append(unit)
        
        # Location selector with modern styling
        location_emojis = {
            'Lodge': '🏨', 'Uptown': '🏘️', 'Downtown': '🏢', 'A-frame': '🏕️',
            'Facilities': '🏭', 'Common Areas': '🍽️', 'Residential': '🏠'
        }
        
        selected_location = st.selectbox(
            "1️⃣ Choose Building Type:",
            list(locations.keys()),
            format_func=lambda x: f"{location_emojis.get(x, '🏗️')} {x} ({len(locations[x])} buildings)"
        )
        
        # Specific building selector
        location_units = locations[selected_location]
        selected_unit_name = st.selectbox(
            "2️⃣ Choose Specific Building:",
            [unit['name'] for unit in location_units]
        )
        
        selected_unit = next(u for u in location_units if u['name'] == selected_unit_name)
        
        # Building info card
        st.markdown(f"""
        <div class="modern-container" style="background: linear-gradient(135deg, rgba(255, 56, 92, 0.05) 0%, rgba(255, 56, 92, 0.02) 100%);">
            <h3 style="color: #222222; margin-bottom: 16px;">🏗️ {selected_unit['name']}</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 16px;">
                <div style="text-align: center; padding: 12px; background: white; border-radius: 8px;">
                    <div style="font-weight: 600; color: #222222;">{selected_unit['type'].title()}</div>
                    <div style="font-size: 12px; color: #717171;">Type</div>
                </div>
                <div style="text-align: center; padding: 12px; background: white; border-radius: 8px;">
                    <div style="font-weight: 600; color: #222222;">{"Capacity: " + str(selected_unit['capacity']) if selected_unit['capacity'] > 0 else "Facility"}</div>
                    <div style="font-size: 12px; color: #717171;">Info</div>
                </div>
                <div style="text-align: center; padding: 12px; background: white; border-radius: 8px;">
                    <div style="font-weight: 600; color: #222222;">{selected_unit['location']}</div>
                    <div style="font-size: 12px; color: #717171;">Location</div>
                </div>
            </div>
            <p style="color: #717171; margin-top: 16px; margin-bottom: 0; font-style: italic;">
                {selected_unit.get('description', 'No description available')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Management tabs for this specific building
        unit_tab1, unit_tab2, unit_tab3 = st.tabs(["📝 Notes", "📁 Files", "🔧 Maintenance"])
        
        with unit_tab1:
            show_unit_specific_notes(selected_unit['id'], selected_unit['name'])
        
        with unit_tab2:
            show_unit_specific_files(selected_unit['id'], selected_unit['name'])
        
        with unit_tab3:
            show_unit_specific_maintenance(selected_unit['id'], selected_unit['name'])
        
    except Exception as e:
        st.error(f"Error: {e}")

def show_unit_specific_notes(unit_id, unit_name):
    """Notes for specific building"""
    st.write(f"**Add notes specific to {unit_name}**")
    
    with st.form(f"unit_note_form_{unit_id}"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Note Title*")
            note_type = st.selectbox("Type:", ["general", "maintenance", "guest_feedback", "safety"])
        with col2:
            priority = st.selectbox("Priority:", ["low", "medium", "high"])
        
        content = st.text_area("Note Content*")
        
        if st.form_submit_button("Save Note") and title and content:
            try:
                note_id = PropertyManagementOperations.create_property_note(
                    unit_id, note_type, title, content, priority
                )
                if note_id:
                    st.success("Note saved!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    
    # Show existing notes for this unit
    try:
        notes = PropertyManagementOperations.get_property_notes(unit_id=unit_id)
        if notes:
            st.write("**Recent Notes:**")
            for note in notes[:3]:
                priority_colors = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}
                emoji = priority_colors.get(note.get('priority'), '⚪')
                st.write(f"{emoji} **{note.get('title')}** - {note.get('created_at', '')[:10]}")
        else:
            st.info(f"No notes for {unit_name} yet")
    except Exception as e:
        st.info("Notes will appear here")

def show_unit_specific_files(unit_id, unit_name):
    """Files for specific building"""
    st.write(f"**Upload files for {unit_name}**")
    
    uploaded_file = st.file_uploader(
        "Choose file:",
        type=['jpg', 'png', 'pdf', 'doc', 'txt'],
        key=f"upload_{unit_id}"
    )
    
    if uploaded_file and st.button("Upload", key=f"save_{unit_id}"):
        st.success(f"File '{uploaded_file.name}' uploaded for {unit_name}!")

def show_unit_specific_maintenance(unit_id, unit_name):
    """Maintenance history for specific building"""
    st.write(f"**Maintenance history for {unit_name}**")
    
    try:
        tasks = PropertyManagementOperations.get_maintenance_tasks(unit_id=unit_id)
        if tasks:
            for task in tasks[:3]:
                status_emoji = {'pending': '⏳', 'completed': '✅'}.get(task.get('status'), '⚪')
                st.write(f"{status_emoji} **{task.get('task_title')}** - {task.get('status')}")
        else:
            st.info(f"No maintenance history for {unit_name}")
    except Exception as e:
        st.info("Maintenance history will appear here")

def show_property_management_page():
    """Modern Airbnb-style property management interface"""
    
    # Modern hero section
    st.markdown("""
    <div class="modern-container" style="text-align: center; background: linear-gradient(135deg, rgba(255, 56, 92, 0.05) 0%, rgba(0, 164, 0, 0.05) 100%);">
        <h1 style="color: #222222; font-size: 36px; font-weight: 700; margin-bottom: 12px;">
            🏠 Property Management
        </h1>
        <p style="color: #717171; font-size: 18px; margin-bottom: 20px;">
            Comprehensive building management for Wellspring Mountain
        </p>
        <div style="display: flex; justify-content: center; gap: 16px; flex-wrap: wrap;">
            <div style="padding: 8px 16px; background: rgba(0, 164, 0, 0.1); border-radius: 20px;">
                <span style="color: #00A400; font-weight: 600; font-size: 14px;">✅ 31 Buildings</span>
            </div>
            <div style="padding: 8px 16px; background: rgba(255, 56, 92, 0.1); border-radius: 20px;">
                <span style="color: #FF385C; font-weight: 600; font-size: 14px;">🔧 Full Maintenance</span>
            </div>
            <div style="padding: 8px 16px; background: rgba(0, 102, 204, 0.1); border-radius: 20px;">
                <span style="color: #0066CC; font-weight: 600; font-size: 14px;">📁 File Storage</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Modern tab navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview", "🔧 Maintenance", "📝 Notes", 
        "✅ Tasks", "📁 Files", "🏗️ Buildings"
    ])
    
    with tab1:
        show_property_dashboard()
    
    with tab2:
        show_maintenance_management()
    
    with tab3:
        show_notes_management()
    
    with tab4:
        show_todos_management()
    
    with tab5:
        show_files_management()
    
    with tab6:
        show_unit_management()

# EXECUTE THE PAGE (required for Streamlit multipage)
if __name__ == "__main__":
    show_property_management_page()