"""
Property Management Operations for Wellspring Mountain
Comprehensive property management functionality including maintenance, notes, todos, and files
"""

import sqlite3
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
import logging
import os
import json
from database.models import get_db_connection
from utils.helpers import safe_database_operation, sanitize_input

class PropertyManagementOperations:
    """Operations for comprehensive property management"""
    
    # NOTES OPERATIONS
    @staticmethod
    @safe_database_operation
    def create_property_note(unit_id: int, note_type: str, title: str, content: str, 
                           priority: str = 'medium', created_by: str = 'staff') -> int:
        """Create a new property note"""
        conn = get_db_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO property_notes 
                (lodging_unit_id, note_type, title, content, priority, created_by)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (unit_id, note_type, sanitize_input(title, 200), 
                  sanitize_input(content, 5000), priority, created_by))
            
            note_id = cursor.lastrowid
            conn.commit()
            return note_id
        finally:
            conn.close()
    
    @staticmethod
    @safe_database_operation
    def get_property_notes(unit_id: Optional[int] = None, note_type: Optional[str] = None) -> List[Dict]:
        """Get property notes with optional filtering"""
        conn = get_db_connection()
        try:
            query = "SELECT * FROM property_notes"
            params = []
            conditions = []
            
            if unit_id:
                conditions.append("lodging_unit_id = ?")
                params.append(unit_id)
            
            if note_type:
                conditions.append("note_type = ?")
                params.append(note_type)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY created_at DESC"
            
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    # MAINTENANCE OPERATIONS
    @staticmethod
    @safe_database_operation
    def create_maintenance_task(unit_id: int, title: str, description: str, task_type: str,
                              priority: str = 'medium', scheduled_date: date = None,
                              estimated_cost: float = None, assigned_to: str = None) -> int:
        """Create a new maintenance task"""
        conn = get_db_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO maintenance_tasks 
                (lodging_unit_id, task_title, description, task_type, priority, 
                 scheduled_date, estimated_cost, assigned_to)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (unit_id, sanitize_input(title, 200), sanitize_input(description, 2000),
                  task_type, priority, scheduled_date, estimated_cost, assigned_to))
            
            task_id = cursor.lastrowid
            conn.commit()
            return task_id
        finally:
            conn.close()
    
    @staticmethod
    @safe_database_operation
    def get_maintenance_tasks(unit_id: Optional[int] = None, status: Optional[str] = None,
                            overdue_only: bool = False) -> List[Dict]:
        """Get maintenance tasks with optional filtering"""
        conn = get_db_connection()
        try:
            query = """
                SELECT mt.*, lu.name as unit_name, lu.location
                FROM maintenance_tasks mt
                LEFT JOIN lodging_units lu ON mt.lodging_unit_id = lu.id
            """
            params = []
            conditions = []
            
            if unit_id:
                conditions.append("mt.lodging_unit_id = ?")
                params.append(unit_id)
            
            if status:
                conditions.append("mt.status = ?")
                params.append(status)
            
            if overdue_only:
                conditions.append("mt.scheduled_date < ? AND mt.status != 'completed'")
                params.append(date.today())
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY mt.scheduled_date ASC, mt.priority DESC"
            
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    @staticmethod
    @safe_database_operation
    def update_maintenance_task(task_id: int, status: str = None, actual_cost: float = None,
                              completed_date: date = None, notes: str = None) -> bool:
        """Update maintenance task status and details"""
        conn = get_db_connection()
        try:
            updates = []
            params = []
            
            if status:
                updates.append("status = ?")
                params.append(status)
            
            if actual_cost is not None:
                updates.append("actual_cost = ?")
                params.append(actual_cost)
            
            if completed_date:
                updates.append("completed_date = ?")
                params.append(completed_date)
            
            updates.append("updated_at = CURRENT_TIMESTAMP")
            
            if updates:
                query = f"UPDATE maintenance_tasks SET {', '.join(updates)} WHERE id = ?"
                params.append(task_id)
                
                cursor = conn.execute(query, params)
                success = cursor.rowcount > 0
                conn.commit()
                return success
            
            return False
        finally:
            conn.close()
    
    # TODO OPERATIONS
    @staticmethod
    @safe_database_operation
    def create_todo(title: str, description: str = '', unit_id: Optional[int] = None,
                   priority: str = 'medium', due_date: Optional[date] = None,
                   category: str = 'general', assigned_to: str = None) -> int:
        """Create a new todo item"""
        conn = get_db_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO property_todos 
                (lodging_unit_id, title, description, priority, due_date, category, assigned_to)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (unit_id, sanitize_input(title, 200), sanitize_input(description, 1000),
                  priority, due_date, category, assigned_to))
            
            todo_id = cursor.lastrowid
            conn.commit()
            return todo_id
        finally:
            conn.close()
    
    @staticmethod
    @safe_database_operation
    def get_todos(unit_id: Optional[int] = None, status: str = 'pending',
                 category: Optional[str] = None, overdue_only: bool = False) -> List[Dict]:
        """Get todos with optional filtering"""
        conn = get_db_connection()
        try:
            query = """
                SELECT pt.*, lu.name as unit_name, lu.location
                FROM property_todos pt
                LEFT JOIN lodging_units lu ON pt.lodging_unit_id = lu.id
            """
            params = []
            conditions = []
            
            if unit_id:
                conditions.append("pt.lodging_unit_id = ?")
                params.append(unit_id)
            
            if status:
                conditions.append("pt.status = ?")
                params.append(status)
            
            if category:
                conditions.append("pt.category = ?")
                params.append(category)
            
            if overdue_only:
                conditions.append("pt.due_date < ? AND pt.status = 'pending'")
                params.append(date.today())
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY pt.due_date ASC, pt.priority DESC"
            
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    @staticmethod
    @safe_database_operation
    def update_todo(todo_id: int, status: str = None, completed_at: datetime = None) -> bool:
        """Update todo status"""
        conn = get_db_connection()
        try:
            updates = []
            params = []
            
            if status:
                updates.append("status = ?")
                params.append(status)
            
            if completed_at:
                updates.append("completed_at = ?")
                params.append(completed_at)
            
            updates.append("updated_at = CURRENT_TIMESTAMP")
            
            if updates:
                query = f"UPDATE property_todos SET {', '.join(updates)} WHERE id = ?"
                params.append(todo_id)
                
                cursor = conn.execute(query, params)
                success = cursor.rowcount > 0
                conn.commit()
                return success
            
            return False
        finally:
            conn.close()
    
    # FILE OPERATIONS
    @staticmethod
    @safe_database_operation
    def save_file_record(unit_id: int, file_name: str, file_type: str, file_category: str,
                        file_path: str, file_size: int = None, description: str = '',
                        uploaded_by: str = 'staff') -> int:
        """Save file record to database"""
        conn = get_db_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO property_files 
                (lodging_unit_id, file_name, file_type, file_category, file_path, 
                 file_size, description, uploaded_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (unit_id, file_name, file_type, file_category, file_path,
                  file_size, sanitize_input(description, 500), uploaded_by))
            
            file_id = cursor.lastrowid
            conn.commit()
            return file_id
        finally:
            conn.close()
    
    @staticmethod
    @safe_database_operation
    def get_property_files(unit_id: Optional[int] = None, file_category: Optional[str] = None) -> List[Dict]:
        """Get property files with optional filtering"""
        conn = get_db_connection()
        try:
            query = """
                SELECT pf.*, lu.name as unit_name, lu.location
                FROM property_files pf
                LEFT JOIN lodging_units lu ON pf.lodging_unit_id = lu.id
            """
            params = []
            conditions = []
            
            if unit_id:
                conditions.append("pf.lodging_unit_id = ?")
                params.append(unit_id)
            
            if file_category:
                conditions.append("pf.file_category = ?")
                params.append(file_category)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY pf.uploaded_at DESC"
            
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    # INSPECTION OPERATIONS
    @staticmethod
    @safe_database_operation
    def create_inspection(unit_id: int, inspection_type: str, inspection_date: date,
                         inspector_name: str, overall_rating: int, checklist_data: Dict,
                         issues_found: str = '', recommendations: str = '',
                         next_inspection_date: date = None) -> int:
        """Create a property inspection record"""
        conn = get_db_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO property_inspections 
                (lodging_unit_id, inspection_type, inspection_date, inspector_name, 
                 overall_rating, checklist_data, issues_found, recommendations, next_inspection_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (unit_id, inspection_type, inspection_date, inspector_name, overall_rating,
                  json.dumps(checklist_data), sanitize_input(issues_found, 2000),
                  sanitize_input(recommendations, 2000), next_inspection_date))
            
            inspection_id = cursor.lastrowid
            conn.commit()
            return inspection_id
        finally:
            conn.close()
    
    @staticmethod
    @safe_database_operation
    def get_inspections(unit_id: Optional[int] = None, inspection_type: Optional[str] = None) -> List[Dict]:
        """Get property inspections"""
        conn = get_db_connection()
        try:
            query = """
                SELECT pi.*, lu.name as unit_name, lu.location
                FROM property_inspections pi
                LEFT JOIN lodging_units lu ON pi.lodging_unit_id = lu.id
            """
            params = []
            conditions = []
            
            if unit_id:
                conditions.append("pi.lodging_unit_id = ?")
                params.append(unit_id)
            
            if inspection_type:
                conditions.append("pi.inspection_type = ?")
                params.append(inspection_type)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY pi.inspection_date DESC"
            
            cursor = conn.execute(query, params)
            inspections = [dict(row) for row in cursor.fetchall()]
            
            # Parse JSON checklist data
            for inspection in inspections:
                if inspection['checklist_data']:
                    try:
                        inspection['checklist_data'] = json.loads(inspection['checklist_data'])
                    except json.JSONDecodeError:
                        inspection['checklist_data'] = {}
            
            return inspections
        finally:
            conn.close()
    
    # MAINTENANCE SCHEDULE OPERATIONS
    @staticmethod
    @safe_database_operation
    def create_maintenance_schedule(unit_id: int, schedule_name: str, task_type: str,
                                  frequency: str, next_due_date: date, description: str = '',
                                  estimated_cost: float = None) -> int:
        """Create a recurring maintenance schedule"""
        conn = get_db_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO maintenance_schedules 
                (lodging_unit_id, schedule_name, task_type, frequency, next_due_date, 
                 description, estimated_cost)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (unit_id, sanitize_input(schedule_name, 200), task_type, frequency,
                  next_due_date, sanitize_input(description, 1000), estimated_cost))
            
            schedule_id = cursor.lastrowid
            conn.commit()
            return schedule_id
        finally:
            conn.close()
    
    @staticmethod
    @safe_database_operation
    def get_maintenance_schedules(unit_id: Optional[int] = None, overdue_only: bool = False) -> List[Dict]:
        """Get maintenance schedules"""
        conn = get_db_connection()
        try:
            query = """
                SELECT ms.*, lu.name as unit_name, lu.location
                FROM maintenance_schedules ms
                LEFT JOIN lodging_units lu ON ms.lodging_unit_id = lu.id
                WHERE ms.is_active = 1
            """
            params = []
            
            if unit_id:
                query += " AND ms.lodging_unit_id = ?"
                params.append(unit_id)
            
            if overdue_only:
                query += " AND ms.next_due_date < ?"
                params.append(date.today())
            
            query += " ORDER BY ms.next_due_date ASC"
            
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    # DASHBOARD OPERATIONS
    @staticmethod
    @safe_database_operation
    def get_property_dashboard_summary() -> Dict:
        """Get comprehensive property management dashboard summary"""
        conn = get_db_connection()
        try:
            summary = {}
            
            # Pending maintenance tasks
            cursor = conn.execute("SELECT COUNT(*) FROM maintenance_tasks WHERE status = 'pending'")
            summary['pending_maintenance'] = cursor.fetchone()[0]
            
            # Overdue maintenance
            cursor = conn.execute("SELECT COUNT(*) FROM maintenance_tasks WHERE scheduled_date < ? AND status = 'pending'", (date.today(),))
            summary['overdue_maintenance'] = cursor.fetchone()[0]
            
            # Pending todos
            cursor = conn.execute("SELECT COUNT(*) FROM property_todos WHERE status = 'pending'")
            summary['pending_todos'] = cursor.fetchone()[0]
            
            # Overdue todos
            cursor = conn.execute("SELECT COUNT(*) FROM property_todos WHERE due_date < ? AND status = 'pending'", (date.today(),))
            summary['overdue_todos'] = cursor.fetchone()[0]
            
            # Recent notes
            cursor = conn.execute("SELECT COUNT(*) FROM property_notes WHERE created_at >= ?", (datetime.now() - timedelta(days=7),))
            summary['recent_notes'] = cursor.fetchone()[0]
            
            # Total property files
            cursor = conn.execute("SELECT COUNT(*) FROM property_files")
            summary['total_files'] = cursor.fetchone()[0]
            
            # Inspections due soon (next 30 days)
            cursor = conn.execute("SELECT COUNT(*) FROM property_inspections WHERE next_inspection_date BETWEEN ? AND ?", 
                                (date.today(), date.today() + timedelta(days=30)))
            summary['inspections_due_soon'] = cursor.fetchone()[0]
            
            return summary
        finally:
            conn.close()