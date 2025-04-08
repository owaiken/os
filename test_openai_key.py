#!/usr/bin/env python3
"""
API Key Validator for OpenAI and OpenRouter

This script tests if your API key is valid by making a minimal API call.
It supports both OpenAI and OpenRouter API keys.
"""

import os
import sys
import json
import argparse
import requests
from openai import OpenAI, APIError, AuthenticationError

def detect_key_type(api_key):
    """Detect if the key is for OpenAI or OpenRouter"""
    if api_key.startswith("sk-org-"):
        return "openai"
    elif api_key.startswith("sk-proj-"):
        return "openrouter"
    elif api_key.startswith("sk-"):
        return "openai"  # Standard OpenAI key
    else:
        return "unknown"

def test_openrouter_key(api_key=None):
    """Test if an OpenRouter API key is valid"""
    print("\n=== OpenRouter API Key Validator ===")
    
    # Get API key if not provided
    if not api_key:
        api_key = os.environ.get("LLM_API_KEY")
        
    if not api_key:
        api_key = input("Enter your OpenRouter API key to test: ").strip()
    
    # Validate key format
    if not api_key.startswith("sk-"):
        print("❌ Invalid key format. OpenRouter API keys should start with 'sk-'")
        return False
        
    print(f"Testing OpenRouter API key: {api_key[:7]}***{api_key[-4:]}")
    
    # Use direct HTTP request to test OpenRouter key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Just get the models list - minimal API call
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers
        )
        
        if response.status_code == 200:
            models = response.json()
            print("✅ API key is valid! Successfully connected to OpenRouter API.")
            if models and len(models.get('data', [])) > 0:
                print(f"Available models: {len(models.get('data', []))} models found")
                # Print a few example models
                for model in models.get('data', [])[:3]:
                    print(f"  - {model.get('id')}")
            return True
        else:
            print(f"❌ API Error: Status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected Error: {type(e).__name__} - {str(e)}")
        return False

def test_openai_key(api_key=None):
    """Test if an OpenAI API key is valid"""
    print("\n=== OpenAI API Key Validator ===")
    
    # Get API key if not provided
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY")
        
    if not api_key:
        api_key = input("Enter your OpenAI API key to test: ").strip()
    
    # Validate key format
    if not api_key.startswith("sk-"):
        print("❌ Invalid key format. OpenAI API keys should start with 'sk-'")
        return False
        
    print(f"Testing OpenAI API key: {api_key[:7]}***{api_key[-4:]}")
    
    # Create a client with the key
    client = OpenAI(api_key=api_key)
    
    try:
        # Make a minimal API call that uses the least tokens
        # Just listing models is the cheapest operation
        response = client.models.list()
        
        print("✅ API key is valid! Successfully connected to OpenAI API.")
        if hasattr(response, 'data') and len(response.data) > 0:
            print(f"Available model: {response.data[0].id}")
        return True
        
    except AuthenticationError as e:
        print(f"❌ Authentication Error: {str(e)}")
        print("Your API key is invalid or has been revoked.")
        return False
        
    except APIError as e:
        print(f"❌ API Error: {str(e)}")
        if "rate limit" in str(e).lower():
            print("Your API key is valid but you've hit a rate limit.")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {type(e).__name__} - {str(e)}")
        return False

def test_api_key(api_key=None):
    """Test if an API key is valid (OpenAI or OpenRouter)"""
    # Get API key from argument, environment, or prompt
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("LLM_API_KEY")
        
    if not api_key:
        api_key = input("Enter your API key to test: ").strip()
    
    # Validate key format
    if not api_key.startswith("sk-"):
        print("❌ Invalid key format. API keys should start with 'sk-'")
        return False
    
    # Detect key type
    key_type = detect_key_type(api_key)
    
    if key_type == "openrouter":
        return test_openrouter_key(api_key)
    elif key_type == "openai":
        return test_openai_key(api_key)
    else:
        print("❌ Unknown API key format")
        print("Trying both OpenAI and OpenRouter...")
        
        # Try both services
        openai_success = test_openai_key(api_key)
        if openai_success:
            return True
            
        print("\nTrying OpenRouter instead...")
        return test_openrouter_key(api_key)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test if an API key is valid (OpenAI or OpenRouter)")
    parser.add_argument("--key", help="API key to test")
    parser.add_argument("--service", choices=["openai", "openrouter"], help="Force testing with a specific service")
    args = parser.parse_args()
    
    if args.service == "openai":
        success = test_openai_key(args.key)
    elif args.service == "openrouter":
        success = test_openrouter_key(args.key)
    else:
        success = test_api_key(args.key)
    
    if success:
        print("\nYour API key is valid and working correctly.")
        print("You can use this key in your Render environment variables.")
    else:
        print("\nYour API key appears to be invalid.")
        print("Please check your key and try again, or generate a new key at:")
        print("OpenAI: https://platform.openai.com/account/api-keys")
        print("OpenRouter: https://openrouter.ai/keys")
    
    sys.exit(0 if success else 1)
