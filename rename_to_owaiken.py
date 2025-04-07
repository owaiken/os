#!/usr/bin/env python3
"""
Script to replace all instances of 'Archon' with 'Owaiken' throughout the codebase.
This script preserves case sensitivity where appropriate.
"""
import os
import re
import sys
from pathlib import Path

# Files and directories to exclude
EXCLUDE_DIRS = ['.git', '.streamlit', 'venv', '__pycache__', 'node_modules', 'temp']
EXCLUDE_FILES = ['.gitignore', 'rename_to_owaiken.py']
EXCLUDE_EXTENSIONS = ['.pyc', '.pyo', '.pyd', '.git', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.wav', '.mp3', '.m4a']

# File extensions to process
INCLUDE_EXTENSIONS = ['.py', '.md', '.txt', '.html', '.css', '.js', '.json', '.toml', '.yaml', '.yml']

def should_process_file(file_path):
    """Determine if a file should be processed based on exclusion rules."""
    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_name)[1].lower()
    
    # Check if file is in excluded list
    if file_name in EXCLUDE_FILES:
        return False
    
    # Check if extension is excluded
    if file_ext in EXCLUDE_EXTENSIONS:
        return False
    
    # Check if extension is included
    if file_ext not in INCLUDE_EXTENSIONS:
        return False
    
    return True

def should_process_dir(dir_path):
    """Determine if a directory should be processed based on exclusion rules."""
    dir_name = os.path.basename(dir_path)
    return dir_name not in EXCLUDE_DIRS

def replace_in_file(file_path):
    """Replace 'Archon' with 'Owaiken' in a file, preserving case sensitivity."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        
        # Replace different case variations
        new_content = content
        new_content = re.sub(r'Archon', 'Owaiken', new_content)
        new_content = re.sub(r'ARCHON', 'OWAIKEN', new_content)
        new_content = re.sub(r'archon', 'owaiken', new_content)
        
        # Only write if changes were made
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Updated: {file_path}")
            return 1
        return 0
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return 0

def process_directory(directory):
    """Process all files in a directory recursively."""
    changes_count = 0
    
    for root, dirs, files in os.walk(directory):
        # Filter directories
        dirs[:] = [d for d in dirs if should_process_dir(os.path.join(root, d))]
        
        # Process files
        for file in files:
            file_path = os.path.join(root, file)
            if should_process_file(file_path):
                changes_count += replace_in_file(file_path)
    
    return changes_count

if __name__ == "__main__":
    # Get the directory to process (default to current directory)
    directory = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Starting replacement of 'Archon' with 'Owaiken' in {directory}")
    changes = process_directory(directory)
    print(f"Completed with {changes} changes made.")
