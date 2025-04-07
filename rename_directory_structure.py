#!/usr/bin/env python3
"""
Script to rename the directory structure from 'archon' to 'owaiken'
and update all import statements accordingly.
"""
import os
import re
import shutil
import sys
from pathlib import Path

def rename_directory():
    """Rename the archon directory to owaiken and copy all files."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    archon_dir = os.path.join(root_dir, 'archon')
    owaiken_dir = os.path.join(root_dir, 'owaiken')
    
    # Create owaiken directory if it doesn't exist
    if not os.path.exists(owaiken_dir):
        os.makedirs(owaiken_dir)
    
    # Copy all files from archon to owaiken
    for item in os.listdir(archon_dir):
        src = os.path.join(archon_dir, item)
        dst = os.path.join(owaiken_dir, item.replace('archon', 'owaiken'))
        
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    
    print(f"Copied files from {archon_dir} to {owaiken_dir}")
    
    # Rename files with 'archon' in their name
    for root, dirs, files in os.walk(owaiken_dir):
        for file in files:
            if 'archon' in file and file.endswith('.py'):
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, file.replace('archon', 'owaiken'))
                os.rename(old_path, new_path)
                print(f"Renamed {old_path} to {new_path}")

def update_imports_in_file(file_path):
    """Update import statements in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace import statements
        updated_content = re.sub(r'from\s+archon\.', 'from owaiken.', content)
        updated_content = re.sub(r'import\s+archon\.', 'import owaiken.', updated_content)
        
        # Only write if changes were made
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            return True
        return False
    except Exception as e:
        print(f"Error updating imports in {file_path}: {str(e)}")
        return False

def update_imports():
    """Update import statements in all Python files."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    count = 0
    
    for root, dirs, files in os.walk(root_dir):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if update_imports_in_file(file_path):
                    count += 1
                    print(f"Updated imports in {file_path}")
    
    print(f"Updated imports in {count} files")

if __name__ == "__main__":
    print("Starting directory structure rename...")
    rename_directory()
    print("\nUpdating import statements...")
    update_imports()
    print("\nDone!")
