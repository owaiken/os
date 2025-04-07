"""
Security Configuration for Owaiken
Implements row-level security policies and SQL injection prevention
"""
import streamlit as st
import os
import re
from supabase import create_client, Client
from typing import Dict, Any, List, Optional, Union

# Initialize Supabase client with security focus
def get_secure_supabase_client():
    """Get Supabase client with security configurations"""
    supabase_url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL", ""))
    supabase_key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY", ""))
    
    if not supabase_url or not supabase_key:
        st.warning("Supabase credentials not found. Running in demo mode.")
        return None
    
    try:
        # Create client with secure timeout settings
        return create_client(
            supabase_url, 
            supabase_key,
            options={
                "schema": "public",
                "autoRefreshToken": True,
                "persistSession": True,
                "detectSessionInUrl": False,
                "headers": {"X-Client-Info": "owaiken-app"}
            }
        )
    except Exception as e:
        st.error(f"Error connecting to Supabase: {str(e)}")
        return None

# SQL Injection Prevention
def sanitize_input(input_string: str) -> str:
    """Sanitize input to prevent SQL injection"""
    if not isinstance(input_string, str):
        return str(input_string)
    
    # Remove any SQL injection patterns
    patterns = [
        r"--",              # SQL comment
        r";",               # Statement terminator
        r"\/\*.*?\*\/",     # Block comment
        r"DROP\s+TABLE",    # Drop table
        r"DELETE\s+FROM",   # Delete from
        r"INSERT\s+INTO",   # Insert into
        r"UPDATE\s+",       # Update
        r"UNION\s+SELECT",  # Union select
        r"SELECT\s+",       # Select
        r"ALTER\s+TABLE",   # Alter table
        r"EXEC\s+",         # Exec
        r"EXECUTE\s+",      # Execute
    ]
    
    sanitized = input_string
    for pattern in patterns:
        sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)
    
    return sanitized

# Secure query builder for Supabase
class SecureQueryBuilder:
    """Secure query builder to prevent SQL injection"""
    
    def __init__(self, supabase: Client, table: str):
        self.supabase = supabase
        self.table = table
        self.query = supabase.table(table)
    
    def select(self, columns: Union[str, List[str]] = "*") -> "SecureQueryBuilder":
        """Secure select operation"""
        if isinstance(columns, list):
            # Sanitize each column name
            columns = [sanitize_input(col) for col in columns]
        elif columns != "*":
            columns = sanitize_input(columns)
        
        self.query = self.query.select(columns)
        return self
    
    def insert(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Secure insert operation"""
        # Sanitize all keys and string values
        sanitized_data = {}
        for key, value in data.items():
            sanitized_key = sanitize_input(key)
            sanitized_value = sanitize_input(value) if isinstance(value, str) else value
            sanitized_data[sanitized_key] = sanitized_value
        
        response = self.query.insert(sanitized_data).execute()
        return response.data[0] if response.data else None
    
    def update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Secure update operation"""
        # Sanitize all keys and string values
        sanitized_data = {}
        for key, value in data.items():
            sanitized_key = sanitize_input(key)
            sanitized_value = sanitize_input(value) if isinstance(value, str) else value
            sanitized_data[sanitized_key] = sanitized_value
        
        response = self.query.update(sanitized_data).execute()
        return response.data[0] if response.data else None
    
    def eq(self, column: str, value: Any) -> "SecureQueryBuilder":
        """Secure equals filter"""
        sanitized_column = sanitize_input(column)
        sanitized_value = sanitize_input(value) if isinstance(value, str) else value
        
        self.query = self.query.eq(sanitized_column, sanitized_value)
        return self
    
    def neq(self, column: str, value: Any) -> "SecureQueryBuilder":
        """Secure not equals filter"""
        sanitized_column = sanitize_input(column)
        sanitized_value = sanitize_input(value) if isinstance(value, str) else value
        
        self.query = self.query.neq(sanitized_column, sanitized_value)
        return self
    
    def gt(self, column: str, value: Any) -> "SecureQueryBuilder":
        """Secure greater than filter"""
        sanitized_column = sanitize_input(column)
        
        self.query = self.query.gt(sanitized_column, value)
        return self
    
    def lt(self, column: str, value: Any) -> "SecureQueryBuilder":
        """Secure less than filter"""
        sanitized_column = sanitize_input(column)
        
        self.query = self.query.lt(sanitized_column, value)
        return self
    
    def limit(self, count: int) -> "SecureQueryBuilder":
        """Secure limit operation"""
        self.query = self.query.limit(count)
        return self
    
    def order(self, column: str, ascending: bool = True) -> "SecureQueryBuilder":
        """Secure order operation"""
        sanitized_column = sanitize_input(column)
        
        self.query = self.query.order(sanitized_column, ascending=ascending)
        return self
    
    def execute(self) -> Dict[str, Any]:
        """Execute the query"""
        return self.query.execute()

# Setup Row Level Security
def setup_row_level_security(supabase: Client) -> bool:
    """Set up Row Level Security policies for all tables"""
    if not supabase:
        return False
    
    try:
        # Create RLS policies for subscriptions table
        supabase.rpc(
            "setup_rls_policies",
            {
                "table_name": "subscriptions",
                "enable_rls": True
            }
        ).execute()
        
        # Create policy to allow users to only see their own subscriptions
        supabase.rpc(
            "create_policy",
            {
                "table_name": "subscriptions",
                "policy_name": "users_can_see_own_subscriptions",
                "policy_definition": "auth.uid()::text = user_id",
                "policy_operation": "SELECT"
            }
        ).execute()
        
        # Create policy to allow users to only update their own subscriptions
        supabase.rpc(
            "create_policy",
            {
                "table_name": "subscriptions",
                "policy_name": "users_can_update_own_subscriptions",
                "policy_definition": "auth.uid()::text = user_id",
                "policy_operation": "UPDATE"
            }
        ).execute()
        
        # Create policy to allow users to only insert their own subscriptions
        supabase.rpc(
            "create_policy",
            {
                "table_name": "subscriptions",
                "policy_name": "users_can_insert_own_subscriptions",
                "policy_definition": "auth.uid()::text = user_id",
                "policy_operation": "INSERT"
            }
        ).execute()
        
        # Create policy to prevent deletion of subscriptions
        supabase.rpc(
            "create_policy",
            {
                "table_name": "subscriptions",
                "policy_name": "prevent_subscription_deletion",
                "policy_definition": "false",  # No one can delete
                "policy_operation": "DELETE"
            }
        ).execute()
        
        return True
    except Exception as e:
        print(f"Error setting up RLS: {str(e)}")
        return False

# Initialize security for Supabase
def initialize_database_security():
    """Initialize all security features for the database"""
    supabase = get_secure_supabase_client()
    
    if not supabase:
        return False
    
    # Set up RLS policies
    setup_row_level_security(supabase)
    
    # Create secure query builder for subscriptions
    subscriptions = SecureQueryBuilder(supabase, "subscriptions")
    
    # Store in session state for reuse
    st.session_state.secure_subscriptions = subscriptions
    
    return True
