"""
Rate Limiting Module for Owaiken
Implements advanced rate limiting to prevent abuse and ensure fair usage
"""
import time
import threading
import hashlib
import redis
import os
import streamlit as st
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, Any, List, Optional, Union, Callable

# Rate limiting algorithms
class TokenBucket:
    """
    Token Bucket Algorithm Implementation
    - More flexible than fixed window
    - Allows for bursts within limits
    - Industry standard for API rate limiting
    """
    def __init__(self, rate: float, capacity: float):
        """
        Initialize a token bucket
        
        Args:
            rate: Token refill rate (tokens/second)
            capacity: Maximum bucket capacity
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = threading.RLock()
    
    def consume(self, tokens: float = 1.0) -> bool:
        """
        Consume tokens from the bucket
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            bool: True if tokens were consumed, False if not enough tokens
        """
        with self.lock:
            # Refill tokens based on time elapsed
            now = time.time()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_refill = now
            
            # Check if enough tokens and consume
            if tokens <= self.tokens:
                self.tokens -= tokens
                return True
            return False

class SlidingWindowCounter:
    """
    Sliding Window Counter Algorithm
    - More accurate than fixed window
    - Prevents edge-case bursts
    - Used by major API providers like GitHub
    """
    def __init__(self, window_size: int, max_requests: int):
        """
        Initialize a sliding window counter
        
        Args:
            window_size: Window size in seconds
            max_requests: Maximum requests allowed in window
        """
        self.window_size = window_size
        self.max_requests = max_requests
        self.requests = []
        self.lock = threading.RLock()
    
    def check_and_record(self) -> bool:
        """
        Check if request is allowed and record it
        
        Returns:
            bool: True if request is allowed, False if rate limit exceeded
        """
        with self.lock:
            now = time.time()
            
            # Remove expired timestamps
            self.requests = [ts for ts in self.requests if now - ts < self.window_size]
            
            # Check if under limit
            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True
            return False

# Redis-backed rate limiters for distributed environments
class RedisRateLimiter:
    """
    Redis-backed rate limiter for distributed environments
    - Scales across multiple servers
    - Persistent across application restarts
    - Used by enterprise applications
    """
    def __init__(self, redis_url: Optional[str] = None, prefix: str = "rate_limit"):
        """
        Initialize Redis rate limiter
        
        Args:
            redis_url: Redis connection URL
            prefix: Key prefix for Redis
        """
        self.prefix = prefix
        self.redis_url = redis_url or os.environ.get("REDIS_URL") or st.secrets.get("REDIS_URL")
        
        if self.redis_url:
            try:
                self.redis = redis.from_url(self.redis_url)
                self.enabled = True
            except Exception as e:
                print(f"Redis connection error: {str(e)}")
                self.enabled = False
        else:
            self.enabled = False
            print("Redis URL not provided, falling back to in-memory rate limiting")
    
    def _get_key(self, identifier: str, window: str) -> str:
        """Get Redis key for rate limiting"""
        return f"{self.prefix}:{identifier}:{window}"
    
    def is_rate_limited(self, identifier: str, max_requests: int, window_seconds: int) -> bool:
        """
        Check if identifier is rate limited
        
        Args:
            identifier: User identifier (IP, user ID, etc.)
            max_requests: Maximum requests allowed
            window_seconds: Time window in seconds
            
        Returns:
            bool: True if rate limited, False otherwise
        """
        if not self.enabled:
            # Fall back to in-memory rate limiting
            if not hasattr(self, '_in_memory_limiters'):
                self._in_memory_limiters = {}
            
            key = f"{identifier}:{window_seconds}"
            if key not in self._in_memory_limiters:
                self._in_memory_limiters[key] = SlidingWindowCounter(window_seconds, max_requests)
            
            return not self._in_memory_limiters[key].check_and_record()
        
        # Use Redis for distributed rate limiting
        key = self._get_key(identifier, f"{window_seconds}s")
        current = self.redis.incr(key)
        
        # Set expiration if this is the first request in window
        if current == 1:
            self.redis.expire(key, window_seconds)
        
        return current > max_requests

# Rate limiting decorators
def rate_limit(
    requests_per_minute: int = 60,
    requests_per_hour: int = 1000,
    requests_per_day: int = 10000,
    identifier_func: Optional[Callable] = None,
    redis_url: Optional[str] = None
):
    """
    Rate limiting decorator for API endpoints
    
    Args:
        requests_per_minute: Maximum requests per minute
        requests_per_hour: Maximum requests per hour
        requests_per_day: Maximum requests per day
        identifier_func: Function to get identifier (defaults to IP)
        redis_url: Redis URL for distributed rate limiting
        
    Returns:
        Decorator function
    """
    limiter = RedisRateLimiter(redis_url)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get identifier (IP address or user ID)
            if identifier_func:
                identifier = identifier_func(*args, **kwargs)
            else:
                # Default to session ID or IP-based identifier
                identifier = st.session_state.get("clerk_token", "anonymous")
                if identifier == "anonymous":
                    # Try to get IP from request headers
                    if hasattr(st, "request"):
                        identifier = st.request.headers.get("X-Forwarded-For", "unknown")
            
            # Hash the identifier for privacy
            hashed_id = hashlib.md5(identifier.encode()).hexdigest()
            
            # Check rate limits at different time scales
            minute_limited = limiter.is_rate_limited(f"{hashed_id}:minute", requests_per_minute, 60)
            hour_limited = limiter.is_rate_limited(f"{hashed_id}:hour", requests_per_hour, 3600)
            day_limited = limiter.is_rate_limited(f"{hashed_id}:day", requests_per_day, 86400)
            
            if minute_limited:
                st.error("Rate limit exceeded. Please try again in a minute.")
                return None
            elif hour_limited:
                st.error("Hourly rate limit exceeded. Please try again later.")
                return None
            elif day_limited:
                st.error("Daily rate limit exceeded. Please try again tomorrow.")
                return None
            
            # Execute the function if not rate limited
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator

# Application-specific rate limiters
class OwaikanRateLimiter:
    """
    Owaikan-specific rate limiter with tiered limits based on subscription
    """
    def __init__(self, redis_url: Optional[str] = None):
        """Initialize with optional Redis URL"""
        self.limiter = RedisRateLimiter(redis_url)
        
        # Define tier limits
        self.tier_limits = {
            "free": {
                "minute": 30,
                "hour": 300,
                "day": 1000
            },
            "basic": {
                "minute": 60,
                "hour": 1000,
                "day": 5000
            },
            "premium": {
                "minute": 120,
                "hour": 3000,
                "day": 10000
            },
            "enterprise": {
                "minute": 300,
                "hour": 10000,
                "day": 50000
            }
        }
    
    def check_rate_limit(self, user_id: str, tier: str = "free") -> Dict[str, bool]:
        """
        Check rate limits for a user based on their subscription tier
        
        Args:
            user_id: User ID
            tier: Subscription tier (free, basic, premium, enterprise)
            
        Returns:
            Dict with rate limit status for different time windows
        """
        # Get limits for tier (default to free)
        limits = self.tier_limits.get(tier, self.tier_limits["free"])
        
        # Hash the user ID
        hashed_id = hashlib.md5(user_id.encode()).hexdigest()
        
        # Check rate limits
        minute_limited = self.limiter.is_rate_limited(
            f"{hashed_id}:minute", limits["minute"], 60
        )
        hour_limited = self.limiter.is_rate_limited(
            f"{hashed_id}:hour", limits["hour"], 3600
        )
        day_limited = self.limiter.is_rate_limited(
            f"{hashed_id}:day", limits["day"], 86400
        )
        
        return {
            "minute_limited": minute_limited,
            "hour_limited": hour_limited,
            "day_limited": day_limited,
            "is_limited": minute_limited or hour_limited or day_limited
        }

# Get the rate limiter instance
def get_rate_limiter():
    """Get or create the rate limiter instance"""
    if "rate_limiter" not in st.session_state:
        redis_url = st.secrets.get("REDIS_URL", os.environ.get("REDIS_URL"))
        st.session_state.rate_limiter = OwaikanRateLimiter(redis_url)
    
    return st.session_state.rate_limiter
