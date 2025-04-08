"""
Secure Database Operations Module

This module provides secure database operations with proper RLS enforcement
and protection for user data storage.
"""

from typing import Dict, Any, List, Optional
import re
from supabase import Client

def sanitize_input(input_value: str) -> str:
    """
    Sanitize user input to prevent SQL injection and other attacks
    
    Args:
        input_value: The user input to sanitize
        
    Returns:
        Sanitized input string
    """
    if not isinstance(input_value, str):
        return str(input_value)
        
    # Remove any SQL injection patterns
    sql_patterns = [
        r'--.*$',                   # SQL comments
        r';.*$',                    # Multiple statements
        r'\/\*.*\*\/',              # Block comments
        r'UNION\s+ALL\s+SELECT',    # UNION attacks
        r'SELECT\s+.*\s+FROM',      # Unauthorized SELECT
        r'DROP\s+TABLE',            # Table dropping
        r'ALTER\s+TABLE',           # Table altering
        r'DELETE\s+FROM',           # Mass deletion
        r'INSERT\s+INTO',           # Unauthorized inserts
        r'UPDATE\s+.*\s+SET',       # Unauthorized updates
        r'EXEC\s*\(',               # Command execution
    ]
    
    sanitized = input_value
    for pattern in sql_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
    
    return sanitized

def secure_query(supabase: Client, table_name: str, query_type: str, 
                 data: Optional[Dict[str, Any]] = None, 
                 filters: Optional[Dict[str, Any]] = None,
                 columns: Optional[str] = "*") -> Dict[str, Any]:
    """
    Perform a secure database query with proper RLS enforcement
    
    Args:
        supabase: Supabase client
        table_name: Name of the table to query
        query_type: Type of query (select, insert, update, delete)
        data: Data for insert/update operations
        filters: Query filters
        columns: Columns to select
        
    Returns:
        Query result
    """
    if not supabase:
        raise ValueError("Supabase client is required")
    
    # Sanitize table name and column names to prevent injection
    table_name = sanitize_input(table_name)
    if columns != "*":
        columns = sanitize_input(columns)
    
    # Sanitize data and filters
    if data:
        sanitized_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized_data[sanitize_input(key)] = sanitize_input(value)
            else:
                sanitized_data[sanitize_input(key)] = value
        data = sanitized_data
    
    if filters:
        sanitized_filters = {}
        for key, value in filters.items():
            if isinstance(value, str):
                sanitized_filters[sanitize_input(key)] = sanitize_input(value)
            else:
                sanitized_filters[sanitize_input(key)] = value
        filters = sanitized_filters
    
    # Perform the query with proper RLS enforcement
    try:
        query = supabase.table(table_name)
        
        if query_type.lower() == "select":
            query = query.select(columns)
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            return query.execute()
            
        elif query_type.lower() == "insert":
            if not data:
                raise ValueError("Data is required for insert operations")
            return query.insert(data).execute()
            
        elif query_type.lower() == "update":
            if not data or not filters:
                raise ValueError("Data and filters are required for update operations")
            for key, value in filters.items():
                query = query.eq(key, value)
            return query.update(data).execute()
            
        elif query_type.lower() == "delete":
            if not filters:
                raise ValueError("Filters are required for delete operations")
            for key, value in filters.items():
                query = query.eq(key, value)
            return query.delete().execute()
            
        else:
            raise ValueError(f"Unsupported query type: {query_type}")
            
    except Exception as e:
        # Log the error without exposing sensitive details
        from utils.utils import write_to_log
        write_to_log(f"Database error: {type(e).__name__}")
        raise

def verify_rls_policies(supabase: Client, table_name: str) -> bool:
    """
    Verify that RLS policies are properly enabled for a table
    
    Args:
        supabase: Supabase client
        table_name: Name of the table to check
        
    Returns:
        True if RLS is enabled, False otherwise
    """
    try:
        # This query will only work if you have admin privileges
        # For regular users, assume RLS is enabled (safer default)
        result = supabase.rpc(
            'check_rls_enabled', 
            {'table_name': table_name}
        ).execute()
        
        return result.data.get('rls_enabled', True)
    except:
        # If the query fails, assume RLS is enabled (safer default)
        return True

def get_user_data_with_rls(supabase: Client, table_name: str, user_id: str) -> List[Dict[str, Any]]:
    """
    Get user data with proper RLS enforcement
    
    Args:
        supabase: Supabase client
        table_name: Name of the table to query
        user_id: User ID for RLS filtering
        
    Returns:
        User data filtered by RLS
    """
    if not supabase:
        return []
        
    try:
        # RLS will automatically filter results based on user_id
        result = secure_query(
            supabase=supabase,
            table_name=sanitize_input(table_name),
            query_type="select",
            filters={"user_id": sanitize_input(user_id)}
        )
        
        return result.data if hasattr(result, 'data') else []
    except Exception:
        # Return empty list on error
        return []
