"""
Fix Render Startup Issues

This script provides a more robust initialization for both Supabase and OpenAI connections
that will prevent 502 errors and authentication errors on Render.
"""

import os
import sys
import json
from supabase import create_client, Client
import time
from openai import OpenAI, AsyncOpenAI

def fix_render_startup():
    """Fix Render startup issues by ensuring environment variables are properly set"""
    print("Starting Render startup fix...")
    print(f"Current environment variables: {json.dumps({k: '***' if 'key' in k.lower() or 'secret' in k.lower() else v for k, v in os.environ.items() if k.startswith(('SUPABASE_', 'OPENAI_', 'EMBEDDING_'))})}")
    
    # ===== SUPABASE CONNECTION FIX =====
    print("\n=== Checking Supabase Configuration ===")
    
    # Set fallback Supabase URL if empty
    if not os.environ.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL").strip() == "":
        os.environ["SUPABASE_URL"] = "https://effhhuuhualzawjtnczv.supabase.co"
        print("Set fallback SUPABASE_URL to https://effhhuuhualzawjtnczv.supabase.co")
    
    # Check if service key is available
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not supabase_key:
        # Try other keys
        supabase_key = os.environ.get("SUPABASE_KEY")
        if supabase_key:
            print("Using SUPABASE_KEY instead of SUPABASE_SERVICE_KEY")
        else:
            supabase_key = os.environ.get("SUPABASE_ANON_KEY")
            if supabase_key:
                print("Using SUPABASE_ANON_KEY as fallback")
    
    # Check for SUPABASE_ANON_KEY but don't automatically set it for security reasons
    if not os.environ.get("SUPABASE_ANON_KEY") and supabase_key:
        print("Note: SUPABASE_ANON_KEY not found - you may need to set this explicitly in your environment")
    
    # Validate we have a key
    if not supabase_key:
        print("⚠️ ERROR: No Supabase key found in environment variables")
        print("Please set SUPABASE_SERVICE_KEY in your Render environment variables")
        # Don't exit - we'll continue in demo mode
    
    # Test Supabase connection
    supabase_success = False
    if supabase_key and os.environ.get("SUPABASE_URL"):
        try:
            print(f"Testing connection to Supabase at {os.environ.get('SUPABASE_URL')}")
            supabase = create_client(os.environ.get("SUPABASE_URL"), supabase_key)
            # Simple query to test connection
            response = supabase.table("subscriptions").select("count").execute()
            print(f"✅ Successfully connected to Supabase: {response.data}")
            supabase_success = True
        except Exception as e:
            print(f"❌ Error connecting to Supabase: {type(e).__name__} - {str(e)}")
            print("Application will continue in demo mode for Supabase features")
    
    # ===== API KEYS CHECK =====
    print("\n=== Checking API Configurations ===")
    
    # Check for OpenAI API key (used for embeddings)
    print("\n--- Checking OpenAI API (for embeddings) ---")
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key:
        openai_key = os.environ.get("EMBEDDING_API_KEY")
        if openai_key:
            print("Using EMBEDDING_API_KEY for OpenAI API")
    
    # Validate we have an OpenAI key for embeddings
    if not openai_key:
        print("⚠️ WARNING: No OpenAI API key found for embeddings")
        print("Please set OPENAI_API_KEY in your Render environment variables")
    elif openai_key.startswith(("no-", "sk-dummy", "placeholder", "your-")):
        print(f"⚠️ WARNING: OpenAI API key appears to be a placeholder: {openai_key[:7]}***")
    
    # Check for OpenRouter API key
    print("\n--- Checking OpenRouter API ---")
    openrouter_key = os.environ.get("LLM_API_KEY")
    if not openrouter_key:
        print("⚠️ WARNING: No OpenRouter API key found")
        print("Please set LLM_API_KEY in your Render environment variables")
    elif openrouter_key.startswith(("no-", "sk-dummy", "placeholder", "your-")):
        print(f"⚠️ WARNING: OpenRouter API key appears to be a placeholder: {openrouter_key[:7]}***")
    
    # Check for BASE_URL
    base_url = os.environ.get("BASE_URL")
    if not base_url:
        print("Setting BASE_URL to OpenRouter API endpoint")
        os.environ["BASE_URL"] = "https://openrouter.ai/api/v1"
    
    # Check for model settings
    if not os.environ.get("PRIMARY_MODEL"):
        print("Setting PRIMARY_MODEL to claude-3-7-sonnet")
        os.environ["PRIMARY_MODEL"] = "anthropic/claude-3-7-sonnet"
    
    if not os.environ.get("REASONER_MODEL"):
        print("Setting REASONER_MODEL to quasar-alpha")
        os.environ["REASONER_MODEL"] = "openrouter/quasar-alpha"
    
    # Check for embedding model settings
    if not os.environ.get("EMBEDDING_BASE_URL"):
        print("Setting EMBEDDING_BASE_URL to OpenAI API endpoint")
        os.environ["EMBEDDING_BASE_URL"] = "https://api.openai.com/v1"
    
    if not os.environ.get("EMBEDDING_MODEL"):
        print("Setting EMBEDDING_MODEL to text-embedding-3-small")
        os.environ["EMBEDDING_MODEL"] = "text-embedding-3-small"
    
    # Test API connections
    openai_success = False
    if openai_key and not openai_key.startswith(("no-", "sk-dummy", "placeholder", "your-")):
        try:
            print("\nTesting connection to OpenAI API for embeddings...")
            client = OpenAI(api_key=openai_key, base_url="https://api.openai.com/v1")
            models = client.models.list()
            print(f"✅ Successfully connected to OpenAI API")
            openai_success = True
        except Exception as e:
            print(f"❌ Error connecting to OpenAI API: {type(e).__name__} - {str(e)}")
            if "authentication" in str(e).lower() or "invalid_api_key" in str(e).lower():
                print("Authentication error: Please check your OpenAI API key")
    
    # We don't test OpenRouter connection here to avoid unnecessary token usage
    openrouter_success = openrouter_key is not None and not openrouter_key.startswith(("no-", "sk-dummy", "placeholder", "your-"))
    
    # ===== LICENSE CHECK =====
    print("\n=== Checking License Configuration ===")
    keygen_account_id = os.environ.get("KEYGEN_ACCOUNT_ID")
    keygen_product_id = os.environ.get("KEYGEN_PRODUCT_ID")
    
    if not keygen_account_id or not keygen_product_id:
        print("⚠️ WARNING: License configuration not found")
        print("You are running in evaluation mode")
        print("To activate your license, set KEYGEN_ACCOUNT_ID and KEYGEN_PRODUCT_ID")
    else:
        print("✅ License configuration found")
    
    # ===== SUMMARY =====
    print("\n=== Startup Fix Summary ===")
    print(f"Supabase Connection: {'✅ SUCCESS' if supabase_success else '❌ FAILED'}")
    print(f"OpenAI API (Embeddings): {'✅ SUCCESS' if openai_success else '❌ FAILED'}")
    print(f"OpenRouter (LLM Models): {'✅ CONFIGURED' if openrouter_success else '❌ NOT CONFIGURED'}")
    print(f"License Configuration: {'✅ FOUND' if keygen_account_id and keygen_product_id else '⚠️ NOT FOUND'}")
    
    if not supabase_success or not openai_success or not openrouter_success or not keygen_account_id or not keygen_product_id:
        print("\n=== INSTRUCTIONS FOR FIXING RENDER DEPLOYMENT ===")
        print("1. Go to your Render dashboard: https://dashboard.render.com")
        print("2. Select your web service for Owaiken")
        print("3. Click on 'Environment' in the left sidebar")
        print("4. Add or update the following environment variables:")
        if not supabase_success:
            print("   - SUPABASE_URL: https://effhhuuhualzawjtnczv.supabase.co")
            print("   - SUPABASE_SERVICE_KEY: your-service-key-here")
            print("   - SUPABASE_ANON_KEY: your-anon-key-here (same as service key if you don't have a separate anon key)")
        if not openai_success:
            print("   - OPENAI_API_KEY: your-openai-api-key-here (for embeddings)")
        if not openrouter_success:
            print("   - LLM_API_KEY: your-openrouter-api-key (for multiple LLM models)")
            print("   - BASE_URL: https://openrouter.ai/api/v1 (for OpenRouter)")
            print("   - PRIMARY_MODEL: anthropic/claude-3-7-sonnet (or your preferred main model)")
            print("   - REASONER_MODEL: openrouter/quasar-alpha (or your preferred reasoning model)")
        if not keygen_account_id or not keygen_product_id:
            print("   - KEYGEN_ACCOUNT_ID: your-keygen-account-id (to activate license)")
            print("   - KEYGEN_PRODUCT_ID: your-keygen-product-id (to activate license)")
        print("5. Click 'Save Changes'")
        print("6. Restart your service by clicking 'Manual Deploy' > 'Deploy latest commit'")
    
    print("\nRender startup fix completed")

if __name__ == "__main__":
    fix_render_startup()
