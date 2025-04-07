#!/usr/bin/env python3
"""
N8N Setup Script for Owaiken
This script helps manage the N8N instance for Owaiken.
"""
import os
import subprocess
import sys
import time
import requests
import json

def check_docker_installed():
    """Check if Docker is installed and running."""
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        subprocess.run(["docker-compose", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def start_n8n():
    """Start N8N using Docker Compose."""
    print("Starting N8N and PostgreSQL containers...")
    subprocess.run(["docker-compose", "up", "-d"], check=True)
    
    # Wait for N8N to start
    print("Waiting for N8N to start (this may take a minute)...")
    for _ in range(30):  # Try for 30 seconds
        try:
            response = requests.get("http://localhost:5678/")
            if response.status_code == 200:
                print("N8N is now running!")
                print("Access the N8N editor at: http://localhost:5678/")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    
    print("N8N didn't start properly. Check the logs with 'docker-compose logs n8n'")
    return False

def stop_n8n():
    """Stop N8N containers."""
    print("Stopping N8N and PostgreSQL containers...")
    subprocess.run(["docker-compose", "down"], check=True)
    print("Containers stopped.")

def get_n8n_api_key():
    """Get or create an N8N API key."""
    try:
        # First, check if we can access the REST API without auth
        response = requests.get("http://localhost:5678/rest/settings")
        
        if response.status_code == 401:
            print("N8N requires authentication. Please create an API key manually:")
            print("1. Go to http://localhost:5678/")
            print("2. Click on your user icon in the top right")
            print("3. Go to 'Settings' -> 'API' -> 'Create API Key'")
            print("4. Copy the API key and use it in Owaiken's N8N Integration settings")
        else:
            print("N8N API is accessible. You can use Owaiken's N8N Integration without an API key.")
    except requests.exceptions.ConnectionError:
        print("Cannot connect to N8N. Make sure it's running with 'python setup_n8n.py start'")

def create_test_workflow():
    """Create a simple test workflow in N8N."""
    print("Creating a test workflow in N8N...")
    
    # Simple workflow that pings a website and sends the result to a Webhook
    workflow = {
        "name": "Test Workflow",
        "nodes": [
            {
                "parameters": {
                    "url": "https://example.com",
                    "authentication": "none",
                    "method": "GET",
                    "sendHeaders": True,
                    "headerParameters": {
                        "parameters": [
                            {
                                "name": "User-Agent",
                                "value": "Owaiken"
                            }
                        ]
                    }
                },
                "name": "HTTP Request",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 3,
                "position": [
                    580,
                    300
                ]
            }
        ],
        "connections": {},
        "active": False,
        "settings": {},
        "tags": ["test", "owaiken"],
        "pinData": {}
    }
    
    try:
        # Try to create the workflow
        response = requests.post(
            "http://localhost:5678/rest/workflows",
            json=workflow
        )
        
        if response.status_code in (200, 201):
            print("Test workflow created successfully!")
            print("You can view it in the N8N editor at http://localhost:5678/")
        else:
            print(f"Failed to create test workflow. Status code: {response.status_code}")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("Cannot connect to N8N. Make sure it's running with 'python setup_n8n.py start'")

def show_help():
    """Show help information."""
    print("N8N Setup Script for Owaiken")
    print("Usage: python setup_n8n.py [command]")
    print("\nCommands:")
    print("  start       - Start N8N and PostgreSQL containers")
    print("  stop        - Stop N8N and PostgreSQL containers")
    print("  restart     - Restart N8N and PostgreSQL containers")
    print("  status      - Check if N8N is running")
    print("  api-key     - Get information about N8N API key")
    print("  test        - Create a test workflow in N8N")
    print("  help        - Show this help information")

def check_status():
    """Check if N8N is running."""
    try:
        response = requests.get("http://localhost:5678/")
        if response.status_code == 200:
            print("N8N is running at http://localhost:5678/")
            return True
        else:
            print(f"N8N returned unexpected status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("N8N is not running")
        return False

def main():
    """Main function to handle command line arguments."""
    if not check_docker_installed():
        print("Error: Docker and/or Docker Compose are not installed or not running.")
        print("Please install Docker Desktop from https://www.docker.com/products/docker-desktop/")
        return
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        start_n8n()
    elif command == "stop":
        stop_n8n()
    elif command == "restart":
        stop_n8n()
        start_n8n()
    elif command == "status":
        check_status()
    elif command == "api-key":
        get_n8n_api_key()
    elif command == "test":
        create_test_workflow()
    elif command == "help":
        show_help()
    else:
        print(f"Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()
