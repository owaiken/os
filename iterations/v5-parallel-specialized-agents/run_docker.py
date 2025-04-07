#!/usr/bin/env python
"""
Simple script to build and run Owaiken Docker containers.
"""

import os
import subprocess
import platform
import time
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and print output in real-time."""
    print(f"Running: {' '.join(command)}")
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=False,  
        cwd=cwd
    )
    
    for line in process.stdout:
        try:
            decoded_line = line.decode('utf-8', errors='replace')
            print(decoded_line.strip())
        except Exception as e:
            print(f"Error processing output: {e}")
    
    process.wait()
    return process.returncode

def check_docker():
    """Check if Docker is installed and running."""
    try:
        subprocess.run(
            ["docker", "--version"], 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Error: Docker is not installed or not in PATH")
        return False

def main():
    """Main function to build and run Owaiken containers."""
    # Check if Docker is available
    if not check_docker():
        return 1
    
    # Get the base directory
    base_dir = Path(__file__).parent.absolute()
    
    # Check for .env file
    env_file = base_dir / ".env"
    env_args = []
    if env_file.exists():
        print(f"Using environment file: {env_file}")
        env_args = ["--env-file", str(env_file)]
    else:
        print("No .env file found. Continuing without environment variables.")
    
    # Build the MCP container
    print("\n=== Building Owaiken MCP container ===")
    mcp_dir = base_dir / "mcp"
    if run_command(["docker", "build", "-t", "owaiken-mcp:latest", "."], cwd=mcp_dir) != 0:
        print("Error building MCP container")
        return 1
    
    # Build the main Owaiken container
    print("\n=== Building main Owaiken container ===")
    if run_command(["docker", "build", "-t", "owaiken:latest", "."], cwd=base_dir) != 0:
        print("Error building main Owaiken container")
        return 1
    
    # Check if the container exists (running or stopped)
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "-q", "--filter", "name=owaiken-container"],
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print("\n=== Removing existing Owaiken container ===")
            container_id = result.stdout.strip()
            print(f"Found container with ID: {container_id}")
            
            # Check if the container is running
            running_check = subprocess.run(
                ["docker", "ps", "-q", "--filter", "id=" + container_id],
                check=True,
                capture_output=True,
                text=True
            )
            
            # If running, stop it first
            if running_check.stdout.strip():
                print("Container is running. Stopping it first...")
                stop_result = run_command(["docker", "stop", container_id])
                if stop_result != 0:
                    print("Warning: Failed to stop container gracefully, will try force removal")
            
            # Remove the container with force flag to ensure it's removed
            print("Removing container...")
            rm_result = run_command(["docker", "rm", "-f", container_id])
            if rm_result != 0:
                print("Error: Failed to remove container. Please remove it manually with:")
                print(f"  docker rm -f {container_id}")
                return 1
            
            print("Container successfully removed")
    except subprocess.SubprocessError as e:
        print(f"Error checking for existing containers: {e}")
        pass
    
    # Run the Owaiken container
    print("\n=== Starting Owaiken container ===")
    cmd = [
        "docker", "run", "-d",
        "--name", "owaiken-container",
        "-p", "8501:8501",
        "-p", "8100:8100",
        "--add-host", "host.docker.internal:host-gateway"
    ]
    
    # Add environment variables if .env exists
    if env_args:
        cmd.extend(env_args)
    
    # Add image name
    cmd.append("owaiken:latest")
    
    if run_command(cmd) != 0:
        print("Error starting Owaiken container")
        return 1
    
    # Wait a moment for the container to start
    time.sleep(2)
    
    # Print success message
    print("\n=== Owaiken is now running! ===")
    print("-> Access the Streamlit UI at: http://localhost:8501")
    print("-> MCP container is ready to use - see the MCP tab in the UI.")
    print("\nTo stop Owaiken, run: docker stop owaiken-container && docker rm owaiken-container")
    
    return 0

if __name__ == "__main__":
    exit(main())
