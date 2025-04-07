"""
OpenManus Integration for Owaiken
This module provides integration with OpenManus for AI agent capabilities
"""
import streamlit as st
import os
import subprocess
import json
import requests
import tempfile
import sys
from pathlib import Path
import toml
import time
from streamlit_pages.openmanus_dark_ui import apply_dark_theme, computer_svg, microphone_svg, reconnect_svg, fullscreen_svg
from streamlit_pages.magic_ai_voice import apply_magic_voice_styles, magic_ai_voice_input
from streamlit_pages.voice_chat import voice_recorder_component, init_voice_chat
from streamlit_pages.enhanced_voice_input import enhanced_voice_input
from streamlit_pages.enhanced_voice_input_simple import simplified_voice_input
from streamlit_pages.cloud_safe_voice import cloud_safe_voice_input

def openmanus_tab():
    """
    Tab for OpenManus integration with Owaiken
    """
    # Apply dark theme for OpenManus
    apply_dark_theme()
    
    # Apply Magic Design voice styles
    apply_magic_voice_styles()
    
    # Create a modern dark UI layout with two columns
    left_col, right_col = st.columns([1, 1])
    
    # Check if OpenManus is installed
    openmanus_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "openmanus")
    is_installed = os.path.exists(openmanus_path)
    
    with left_col:
        # Task history section
        st.markdown("### TASK HISTORY")
        st.info("Beta version task data on OpenManus' computer will be automatically deleted after one hour of inactivity.")
        
        # OpenManus section
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### OpenManus")
        with col2:
            st.markdown("<span style='background-color: #3a86ff; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;'>BETA</span>", unsafe_allow_html=True)
        
        st.markdown("👋 Welcome to GlobalGPT OpenManus!")
        
        # Task input area
        task_input = st.text_area("Type your task here...", height=150, key="task_input", label_visibility="collapsed")
        
        # Voice input options
        st.markdown("<p style='text-align: center; margin-bottom: 10px;'>Or use voice input:</p>", unsafe_allow_html=True)
        
        # Voice input options
        voice_option = st.radio(
            "Voice Input Method",
            ["Basic Voice", "Magic UI Voice", "Simple Voice", "Cloud-Safe Voice"],
            horizontal=True,
            key="voice_option",
            label_visibility="collapsed"
        )
        
        voice_container = st.container()
        with voice_container:
            if voice_option == "Basic Voice":
                # Initialize voice chat
                init_voice_chat()
                # Use the original voice recorder component
                transcription = voice_recorder_component()
                if transcription:
                    # If we got a transcription, update the task input
                    st.session_state.task_input = transcription
                    st.success(f"Voice input captured: {transcription}")
                    # Wait a moment to show the success message before rerunning
                    time.sleep(1)
                    st.experimental_rerun()
            elif voice_option == "Magic UI Voice":
                # Use the enhanced Magic UI voice component with demo mode enabled
                transcription = enhanced_voice_input(key_prefix="openmanus", demo_mode=True)
                if transcription:
                    # If we got a transcription, update the task input
                    st.session_state.task_input = transcription
                    st.success(f"Voice input captured: {transcription}")
                    # Wait a moment to show the success message before rerunning
                    time.sleep(1)
                    st.experimental_rerun()
            elif voice_option == "Simple Voice":
                # Use the simplified voice component with demo mode enabled
                transcription = simplified_voice_input(key_prefix="openmanus_simple", demo_mode=True)
                if transcription:
                    # If we got a transcription, update the task input
                    st.session_state.task_input = transcription
                    st.success(f"Voice input captured: {transcription}")
                    # Wait a moment to show the success message before rerunning
                    time.sleep(1)
                    st.experimental_rerun()
            else:  # Cloud-Safe Voice option
                # Use the cloud-safe voice component with demo mode enabled
                transcription = cloud_safe_voice_input(key_prefix="openmanus_cloud", demo_mode=True)
                if transcription:
                    # If we got a transcription, update the task input
                    st.session_state.task_input = transcription
                    st.success(f"Voice input captured: {transcription}")
                    # Wait a moment to show the success message before rerunning
                    time.sleep(1)
                    st.experimental_rerun()
        
        # Create task button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Create Task", use_container_width=True):
                if task_input:
                    st.session_state.current_task = task_input
                    st.session_state.task_running = True
                    st.experimental_rerun()
                else:
                    st.warning("Please enter a task description")
    
    with right_col:
        # OpenManus Computer section
        st.markdown("### OpenManus's Computer")
        
        # Computer display
        with st.container():
            st.image("https://raw.githubusercontent.com/YunQiAI/OpenManusWeb/main/public/computer.png", width=100)
            
            st.markdown("### OpenManus")
            st.markdown("<span style='background-color: #3a86ff; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;'>BETA</span>", unsafe_allow_html=True)
            
            st.markdown("Virtual Computer Environment Ready")
            
            status_col1, status_col2 = st.columns([1, 10])
            with status_col1:
                st.markdown("<div style='width: 10px; height: 10px; background-color: #3a86ff; border-radius: 50%; margin-top: 5px;'></div>", unsafe_allow_html=True)
            with status_col2:
                st.markdown("Standby mode - Waiting for task creation")
        
        # Instructions
        with st.container():
            st.markdown("### How to Start")
            st.markdown("1. This model handles complex tasks and may use many tokens. Use wisely.")
            st.markdown("2. Enter your task description in the input field on the left")
            st.markdown("3. Click \"Create Task\" to start the virtual computer")
            st.markdown("4. The computer will automatically perform the task")
            st.markdown("5. You can observe and interact with the computer in this window")
        
        # Footer buttons
        col1, col2 = st.columns(2)
        with col1:
            st.button("Reconnect", key="reconnect_button")
        with col2:
            st.button("Fullscreen", key="fullscreen_button")
        
        # Display computer output if task is running
        if hasattr(st.session_state, 'task_running') and st.session_state.task_running:
            task_output = display_task_output(openmanus_path, st.session_state.current_task)
            
            # Add buttons to control the task
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Stop Task"):
                    st.session_state.task_running = False
                    st.experimental_rerun()
            with col2:
                if st.button("Clear Output"):
                    st.session_state.task_output = ""
                    st.experimental_rerun()
    
    # Configuration and setup section (hidden in a collapsible section)
    with st.expander("Advanced Configuration", expanded=False):
        if not is_installed:
            st.warning("⚠️ OpenManus is not installed. Click the button below to install it.")
            if st.button("Install OpenManus", key="install_button"):
                with st.spinner("Installing OpenManus..."):
                    install_openmanus()
        else:
            st.success("✅ OpenManus is installed")
            
            # Create tabs for different OpenManus features
            tabs = st.tabs(["Configuration", "N8N Integration", "Workspace"])
            
            with tabs[0]:
                display_configuration_tab(openmanus_path)
                
            with tabs[1]:
                display_n8n_integration_tab(openmanus_path)
                
            with tabs[2]:
                display_workspace_tab(openmanus_path)

def install_openmanus():
    """
    Install OpenManus from GitHub
    """
    try:
        # Create openmanus directory
        openmanus_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "openmanus")
        os.makedirs(openmanus_path, exist_ok=True)
        
        # Clone the repository
        subprocess.run(["git", "clone", "https://github.com/mannaandpoem/OpenManus.git", openmanus_path], check=True)
        
        # Install dependencies
        requirements_path = os.path.join(openmanus_path, "requirements.txt")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_path], check=True)
        
        # Clone the web repository
        openmanus_web_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "openmanus_web")
        os.makedirs(openmanus_web_path, exist_ok=True)
        subprocess.run(["git", "clone", "https://github.com/YunQiAI/OpenManusWeb.git", openmanus_web_path], check=True)
        
        # Install web dependencies
        web_requirements_path = os.path.join(openmanus_web_path, "requirements.txt")
        if os.path.exists(web_requirements_path):
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", web_requirements_path], check=True)
        
        st.success("✅ OpenManus installed successfully! Please restart the application.")
        
    except Exception as e:
        st.error(f"Error installing OpenManus: {str(e)}")

def display_configuration_tab(openmanus_path):
    """
    Display configuration options for OpenManus
    """
    st.markdown("### OpenManus Configuration")
    
    # Check if config file exists
    config_path = os.path.join(openmanus_path, "config", "config.toml")
    config_example_path = os.path.join(openmanus_path, "config", "config.example.toml")
    
    if not os.path.exists(os.path.dirname(config_path)):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    if not os.path.exists(config_path) and os.path.exists(config_example_path):
        # Copy example config
        with open(config_example_path, 'r') as f:
            example_config = f.read()
        with open(config_path, 'w') as f:
            f.write(example_config)
    
    if os.path.exists(config_path):
        try:
            # Load config
            config = toml.load(config_path)
            
            # Display and edit config
            st.markdown("#### LLM Configuration")
            
            # Global LLM settings
            llm_config = config.get('llm', {})
            model = st.text_input("Model", value=llm_config.get('model', 'gpt-4o'))
            base_url = st.text_input("Base URL", value=llm_config.get('base_url', 'https://api.openai.com/v1'))
            api_key = st.text_input("API Key", value=llm_config.get('api_key', ''), type="password")
            max_tokens = st.number_input("Max Tokens", value=llm_config.get('max_tokens', 4096))
            temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=llm_config.get('temperature', 0.0), step=0.1)
            
            # Save button
            if st.button("Save Configuration"):
                # Update config
                if 'llm' not in config:
                    config['llm'] = {}
                
                config['llm']['model'] = model
                config['llm']['base_url'] = base_url
                config['llm']['api_key'] = api_key
                config['llm']['max_tokens'] = max_tokens
                config['llm']['temperature'] = temperature
                
                # Save config
                with open(config_path, 'w') as f:
                    toml.dump(config, f)
                
                st.success("✅ Configuration saved successfully!")
        
        except Exception as e:
            st.error(f"Error loading configuration: {str(e)}")
    else:
        st.warning("⚠️ Configuration file not found. Please create a config.toml file in the config directory.")

def display_task_output(openmanus_path, task):
    """
    Display task output in a computer terminal style
    """
    # Initialize task output in session state if not present
    if 'task_output' not in st.session_state:
        st.session_state.task_output = ""
    
    # Create a terminal-like output area
    st.markdown("### OpenManus Terminal")
    st.markdown("Task Running...")
    
    # If this is a new task, initialize the output
    if not st.session_state.task_output:
        st.session_state.task_output = f">> Task received: {task}\n>> Initializing OpenManus agent...\n"
    
    # Simulate agent thinking and processing
    if hasattr(st.session_state, 'last_update_time'):
        time_since_update = time.time() - st.session_state.last_update_time
        if time_since_update > 2:  # Add new output every 2 seconds
            # Generate some simulated output
            next_output = generate_simulated_output()
            st.session_state.task_output += next_output
            st.session_state.last_update_time = time.time()
    else:
        st.session_state.last_update_time = time.time()
    
    # Display the current output in a code block
    st.code(st.session_state.task_output, language="bash")
    
    return st.session_state.task_output

def generate_simulated_output():
    """
    Generate simulated agent output for demonstration purposes
    """
    import random
    
    outputs = [
        ">> Analyzing task requirements...\n",
        ">> Searching for relevant information...\n",
        ">> Planning solution approach...\n",
        ">> Generating code for implementation...\n",
        ">> Testing solution components...\n",
        ">> Refining approach based on feedback...\n",
        ">> Integrating components into final solution...\n",
        ">> Documenting solution for user reference...\n",
        ">> Preparing final output...\n"
    ]
    
    return random.choice(outputs)

def display_n8n_integration_tab(openmanus_path):
    """
    Display N8N integration options for OpenManus
    """
    st.markdown("### OpenManus + N8N Integration")
    
    # N8N connection settings
    st.markdown("#### N8N Connection")
    n8n_url = st.text_input("N8N URL", value="http://localhost:5678")
    n8n_api_key = st.text_input("N8N API Key (if required)", type="password")
    
    # Test connection
    if st.button("Test N8N Connection"):
        try:
            headers = {}
            if n8n_api_key:
                headers["X-N8N-API-KEY"] = n8n_api_key
            
            response = requests.get(f"{n8n_url}/healthz", headers=headers)
            
            if response.status_code == 200:
                st.success("✅ Successfully connected to N8N!")
            else:
                st.error(f"❌ Failed to connect to N8N. Status code: {response.status_code}")
        
        except Exception as e:
            st.error(f"❌ Error connecting to N8N: {str(e)}")
    
    # Workflow creation
    st.markdown("#### Create N8N Workflow from OpenManus")
    
    workflow_name = st.text_input("Workflow Name", value="OpenManus_Workflow")
    
    workflow_description = st.text_area("Workflow Description", 
                                       placeholder="This workflow integrates with OpenManus to...",
                                       height=100)
    
    # Workflow type
    workflow_type = st.selectbox("Workflow Type", [
        "Agent to N8N (Send agent results to N8N)",
        "N8N to Agent (Trigger agent from N8N)",
        "Bidirectional (Full integration)"
    ])
    
    # Create workflow button
    if st.button("Create N8N Workflow"):
        if not workflow_name:
            st.warning("⚠️ Please enter a workflow name.")
            return
        
        with st.spinner("Creating N8N workflow..."):
            try:
                # Generate workflow JSON based on type
                workflow_json = generate_n8n_workflow(workflow_name, workflow_description, workflow_type, n8n_url)
                
                # Create workflow in N8N
                headers = {"Content-Type": "application/json"}
                if n8n_api_key:
                    headers["X-N8N-API-KEY"] = n8n_api_key
                
                response = requests.post(
                    f"{n8n_url}/rest/workflows",
                    headers=headers,
                    json=workflow_json
                )
                
                if response.status_code in (200, 201):
                    workflow_id = response.json().get("id")
                    st.success(f"✅ Workflow created successfully! Workflow ID: {workflow_id}")
                    
                    # Show link to workflow
                    st.markdown(f"[Open workflow in N8N]({n8n_url}/workflow/{workflow_id})")
                else:
                    st.error(f"❌ Failed to create workflow. Status code: {response.status_code}")
                    st.error(f"Response: {response.text}")
            
            except Exception as e:
                st.error(f"❌ Error creating workflow: {str(e)}")

def generate_n8n_workflow(name, description, workflow_type, n8n_url):
    """
    Generate N8N workflow JSON based on the selected type
    """
    # Basic workflow structure
    workflow = {
        "name": name,
        "nodes": [],
        "connections": {},
        "active": False,
        "settings": {
            "saveManualExecutions": True,
            "callerPolicy": "workflowsFromSameOwner"
        },
        "tags": ["OpenManus", "AI", "Automation"],
        "pinData": {}
    }
    
    if description:
        workflow["description"] = description
    
    # Add nodes based on workflow type
    if workflow_type == "Agent to N8N (Send agent results to N8N)":
        # Webhook node to receive data from OpenManus
        webhook_node = {
            "id": "webhook",
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 1,
            "position": [250, 300],
            "parameters": {
                "path": f"openmanus/{name.lower().replace(' ', '_')}",
                "responseMode": "lastNode",
                "options": {}
            }
        }
        
        # JSON node to parse the incoming data
        json_node = {
            "id": "json",
            "name": "JSON Parse",
            "type": "n8n-nodes-base.functionItem",
            "typeVersion": 1,
            "position": [450, 300],
            "parameters": {
                "functionCode": "return JSON.parse(JSON.stringify(items[0].json));"
            }
        }
        
        # Set node to prepare data for further processing
        set_node = {
            "id": "set",
            "name": "Set",
            "type": "n8n-nodes-base.set",
            "typeVersion": 1,
            "position": [650, 300],
            "parameters": {
                "values": {
                    "string": [
                        {
                            "name": "agentResult",
                            "value": "={{ $json.result }}"
                        },
                        {
                            "name": "taskId",
                            "value": "={{ $json.taskId }}"
                        }
                    ]
                },
                "options": {}
            }
        }
        
        # Add nodes to workflow
        workflow["nodes"] = [webhook_node, json_node, set_node]
        
        # Add connections
        workflow["connections"] = {
            "Webhook": {
                "main": [
                    [
                        {
                            "node": "JSON Parse",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "JSON Parse": {
                "main": [
                    [
                        {
                            "node": "Set",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        }
        
    elif workflow_type == "N8N to Agent (Trigger agent from N8N)":
        # Manual trigger node
        trigger_node = {
            "id": "trigger",
            "name": "Manual Trigger",
            "type": "n8n-nodes-base.manualTrigger",
            "typeVersion": 1,
            "position": [250, 300],
            "parameters": {}
        }
        
        # HTTP Request node to call OpenManus API
        http_node = {
            "id": "http",
            "name": "HTTP Request",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 3,
            "position": [450, 300],
            "parameters": {
                "url": "http://localhost:8000/api/tasks",
                "method": "POST",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {
                            "name": "Content-Type",
                            "value": "application/json"
                        }
                    ]
                },
                "sendBody": True,
                "bodyParameters": {
                    "parameters": [
                        {
                            "name": "task",
                            "value": "={{ $json.task }}"
                        }
                    ]
                },
                "options": {}
            }
        }
        
        # Add nodes to workflow
        workflow["nodes"] = [trigger_node, http_node]
        
        # Add connections
        workflow["connections"] = {
            "Manual Trigger": {
                "main": [
                    [
                        {
                            "node": "HTTP Request",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        }
        
    else:  # Bidirectional
        # Webhook node to receive data from OpenManus
        webhook_node = {
            "id": "webhook",
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 1,
            "position": [250, 300],
            "parameters": {
                "path": f"openmanus/{name.lower().replace(' ', '_')}",
                "responseMode": "lastNode",
                "options": {}
            }
        }
        
        # HTTP Request node to call OpenManus API
        http_node = {
            "id": "http",
            "name": "HTTP Request",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 3,
            "position": [450, 300],
            "parameters": {
                "url": "http://localhost:8000/api/tasks",
                "method": "POST",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {
                            "name": "Content-Type",
                            "value": "application/json"
                        }
                    ]
                },
                "sendBody": True,
                "bodyParameters": {
                    "parameters": [
                        {
                            "name": "task",
                            "value": "={{ $json.task }}"
                        }
                    ]
                },
                "options": {}
            }
        }
        
        # Add nodes to workflow
        workflow["nodes"] = [webhook_node, http_node]
        
        # Add connections
        workflow["connections"] = {
            "Webhook": {
                "main": [
                    [
                        {
                            "node": "HTTP Request",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        }
    
    return workflow

def display_workspace_tab(openmanus_path):
    """
    Display workspace files from OpenManus
    """
    st.markdown("### OpenManus Workspace")
    
    # Path to workspace
    workspace_path = os.path.join(openmanus_path, "workspace")
    
    # Check if workspace exists
    if not os.path.exists(workspace_path):
        os.makedirs(workspace_path, exist_ok=True)
        st.info("Workspace directory created. No files yet.")
        return
    
    # List files in workspace
    files = []
    for root, dirs, filenames in os.walk(workspace_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            rel_path = os.path.relpath(file_path, workspace_path)
            files.append({
                "name": filename,
                "path": rel_path,
                "full_path": file_path,
                "size": os.path.getsize(file_path),
                "modified": os.path.getmtime(file_path)
            })
    
    if not files:
        st.info("No files in workspace yet.")
        return
    
    # Sort files by modification time (newest first)
    files.sort(key=lambda x: x["modified"], reverse=True)
    
    # Display files
    st.markdown("#### Workspace Files")
    
    for file in files:
        with st.expander(f"{file['path']} ({format_size(file['size'])})"):
            # Display file content based on extension
            ext = os.path.splitext(file['name'])[1].lower()
            
            if ext in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv']:
                try:
                    with open(file['full_path'], 'r') as f:
                        content = f.read()
                    
                    if ext == '.py':
                        st.code(content, language='python')
                    elif ext == '.js':
                        st.code(content, language='javascript')
                    elif ext == '.html':
                        st.code(content, language='html')
                    elif ext == '.css':
                        st.code(content, language='css')
                    elif ext == '.json':
                        st.code(content, language='json')
                    elif ext == '.md':
                        st.markdown(content)
                    else:
                        st.text(content)
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
            elif ext in ['.png', '.jpg', '.jpeg', '.gif']:
                try:
                    st.image(file['full_path'])
                except Exception as e:
                    st.error(f"Error displaying image: {str(e)}")
            else:
                st.info(f"File type {ext} cannot be previewed.")
            
            # Download button
            with open(file['full_path'], 'rb') as f:
                st.download_button(
                    label="Download File",
                    data=f,
                    file_name=file['name'],
                    mime="application/octet-stream"
                )

def format_size(size_bytes):
    """
    Format file size in a human-readable format
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"
