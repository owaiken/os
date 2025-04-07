"""
Prepared Statements Module for Owaiken
Implements secure database operations using prepared statements
"""
import os
import uuid
import json
import time
import streamlit as st
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime
from supabase import create_client, Client

class PreparedStatementManager:
    """
    Prepared Statement Manager for Supabase
    
    Implements secure database operations using prepared statements pattern
    with Supabase's RPC (Remote Procedure Call) functionality
    """
    
    def __init__(self, supabase_client: Optional[Client] = None):
        """
        Initialize the prepared statement manager
        
        Args:
            supabase_client: Supabase client instance
        """
        self.supabase = supabase_client
        
        if not self.supabase:
            # Try to get client from environment
            supabase_url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL", ""))
            supabase_key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY", ""))
            
            if supabase_url and supabase_key:
                try:
                    self.supabase = create_client(supabase_url, supabase_key)
                except Exception as e:
                    st.error(f"Error connecting to Supabase: {str(e)}")
                    self.supabase = None
    
    def _create_stored_procedures(self):
        """Create stored procedures in Supabase for prepared statements"""
        if not self.supabase:
            return False
        
        # Define stored procedures for common operations
        procedures = [
            # Get user subscription
            """
            CREATE OR REPLACE FUNCTION get_user_subscription(p_user_id TEXT)
            RETURNS SETOF subscriptions
            LANGUAGE plpgsql
            SECURITY DEFINER
            AS $$
            BEGIN
                RETURN QUERY
                SELECT *
                FROM subscriptions
                WHERE user_id = p_user_id
                ORDER BY created_at DESC
                LIMIT 1;
            END;
            $$;
            """,
            
            # Create user subscription
            """
            CREATE OR REPLACE FUNCTION create_user_subscription(
                p_user_id TEXT,
                p_plan TEXT,
                p_status TEXT,
                p_payment_id TEXT,
                p_amount INTEGER,
                p_expires_at TIMESTAMP
            )
            RETURNS subscriptions
            LANGUAGE plpgsql
            SECURITY DEFINER
            AS $$
            DECLARE
                v_subscription subscriptions;
            BEGIN
                INSERT INTO subscriptions (
                    user_id, plan, status, payment_id, amount, created_at, expires_at
                )
                VALUES (
                    p_user_id, p_plan, p_status, p_payment_id, p_amount, NOW(), p_expires_at
                )
                RETURNING * INTO v_subscription;
                
                RETURN v_subscription;
            END;
            $$;
            """,
            
            # Update user subscription
            """
            CREATE OR REPLACE FUNCTION update_user_subscription(
                p_subscription_id UUID,
                p_user_id TEXT,
                p_plan TEXT,
                p_status TEXT,
                p_expires_at TIMESTAMP
            )
            RETURNS subscriptions
            LANGUAGE plpgsql
            SECURITY DEFINER
            AS $$
            DECLARE
                v_subscription subscriptions;
            BEGIN
                -- Security check: only allow updating own subscriptions
                IF NOT EXISTS (
                    SELECT 1 FROM subscriptions 
                    WHERE id = p_subscription_id AND user_id = p_user_id
                ) THEN
                    RAISE EXCEPTION 'Unauthorized subscription update attempt';
                END IF;
                
                UPDATE subscriptions
                SET 
                    plan = p_plan,
                    status = p_status,
                    expires_at = p_expires_at
                WHERE id = p_subscription_id
                RETURNING * INTO v_subscription;
                
                RETURN v_subscription;
            END;
            $$;
            """,
            
            # Get active subscriptions
            """
            CREATE OR REPLACE FUNCTION get_active_subscriptions(p_user_id TEXT)
            RETURNS SETOF subscriptions
            LANGUAGE plpgsql
            SECURITY DEFINER
            AS $$
            BEGIN
                RETURN QUERY
                SELECT *
                FROM subscriptions
                WHERE 
                    user_id = p_user_id AND
                    status = 'active' AND
                    expires_at > NOW()
                ORDER BY created_at DESC;
            END;
            $$;
            """
        ]
        
        # Execute each procedure creation
        try:
            for procedure in procedures:
                self.supabase.rpc("exec_sql", {"sql": procedure}).execute()
            return True
        except Exception as e:
            st.error(f"Error creating stored procedures: {str(e)}")
            return False
    
    def initialize(self) -> bool:
        """Initialize the prepared statement manager"""
        if not self.supabase:
            return False
        
        return self._create_stored_procedures()
    
    def get_user_subscription(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user subscription using prepared statement
        
        Args:
            user_id: User ID
            
        Returns:
            Subscription data or None
        """
        if not self.supabase:
            return None
        
        try:
            response = self.supabase.rpc(
                "get_user_subscription", 
                {"p_user_id": user_id}
            ).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            st.error(f"Error getting user subscription: {str(e)}")
            return None
    
    def get_active_subscriptions(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get active subscriptions for a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of active subscriptions
        """
        if not self.supabase:
            return []
        
        try:
            response = self.supabase.rpc(
                "get_active_subscriptions", 
                {"p_user_id": user_id}
            ).execute()
            
            return response.data or []
        except Exception as e:
            st.error(f"Error getting active subscriptions: {str(e)}")
            return []
    
    def create_user_subscription(
        self, 
        user_id: str, 
        plan: str, 
        payment_id: str, 
        amount: int,
        status: str = "active",
        expires_at: Optional[datetime] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new subscription for a user
        
        Args:
            user_id: User ID
            plan: Subscription plan
            payment_id: Payment ID
            amount: Amount in cents
            status: Subscription status
            expires_at: Expiration date
            
        Returns:
            Created subscription or None
        """
        if not self.supabase:
            return None
        
        # Set default expiration if not provided
        if not expires_at:
            from datetime import datetime, timedelta
            expires_at = datetime.now() + timedelta(days=30)
        
        try:
            response = self.supabase.rpc(
                "create_user_subscription", 
                {
                    "p_user_id": user_id,
                    "p_plan": plan,
                    "p_status": status,
                    "p_payment_id": payment_id,
                    "p_amount": amount,
                    "p_expires_at": expires_at.isoformat()
                }
            ).execute()
            
            if response.data:
                return response.data
            return None
        except Exception as e:
            st.error(f"Error creating user subscription: {str(e)}")
            return None
    
    def update_user_subscription(
        self,
        subscription_id: str,
        user_id: str,
        plan: str,
        status: str,
        expires_at: datetime
    ) -> Optional[Dict[str, Any]]:
        """
        Update a user subscription
        
        Args:
            subscription_id: Subscription ID
            user_id: User ID (for authorization)
            plan: New subscription plan
            status: New subscription status
            expires_at: New expiration date
            
        Returns:
            Updated subscription or None
        """
        if not self.supabase:
            return None
        
        try:
            response = self.supabase.rpc(
                "update_user_subscription", 
                {
                    "p_subscription_id": subscription_id,
                    "p_user_id": user_id,
                    "p_plan": plan,
                    "p_status": status,
                    "p_expires_at": expires_at.isoformat()
                }
            ).execute()
            
            if response.data:
                return response.data
            return None
        except Exception as e:
            st.error(f"Error updating user subscription: {str(e)}")
            return None

# Get prepared statement manager instance
def get_prepared_statement_manager():
    """Get or create the prepared statement manager instance"""
    if "prepared_statement_manager" not in st.session_state:
        st.session_state.prepared_statement_manager = PreparedStatementManager()
        st.session_state.prepared_statement_manager.initialize()
    
    return st.session_state.prepared_statement_manager
