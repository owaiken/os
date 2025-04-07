"""
N8N Integration for Owaiken.
This module provides integration with N8N for workflow automation.
"""
import streamlit as st
import requests
import json
import os
from utils.utils import get_clients

def n8n_integration_tab():
    """
    N8N integration tab for managing and creating workflows.
    """
    st.markdown("## N8N Workflow Integration")
    
    # Get OpenAI client for workflow generation
    openai_client, _ = get_clients()
    
    # N8N Connection Settings
    with st.expander("N8N Connection Settings"):
        n8n_url = st.text_input(
            "N8N URL", 
            value=st.session_state.get("n8n_url", "http://localhost:5678"),
            help="URL of your N8N instance"
        )
        
        n8n_api_key = st.text_input(
            "N8N API Key", 
            value=st.session_state.get("n8n_api_key", ""),
            type="password",
            help="API key for your N8N instance"
        )
        
        if st.button("Save Connection Settings"):
            st.session_state.n8n_url = n8n_url
            st.session_state.n8n_api_key = n8n_api_key
            st.success("Connection settings saved!")
    
    # Create tabs for different N8N features
    n8n_tabs = st.tabs(["Workflow Generator", "Workflow Library", "My Workflows"])
    
    with n8n_tabs[0]:
        st.markdown("### AI Workflow Generator")
        st.markdown("""
        Describe the workflow you want to create in natural language, and Owaiken will 
        generate an N8N workflow for you.
        """)
        
        workflow_description = st.text_area(
            "Workflow Description",
            placeholder="Example: When a new lead is added to my CRM, send me an email and create a task in Asana",
            height=150
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            include_error_handling = st.checkbox("Include error handling", value=True)
        
        with col2:
            workflow_complexity = st.select_slider(
                "Workflow Complexity",
                options=["Simple", "Moderate", "Complex"]
            )
        
        preferred_services = st.multiselect(
            "Preferred services (optional)",
            options=[
                "Gmail", "Slack", "Trello", "Asana", "GitHub", "Airtable", 
                "Notion", "Google Sheets", "HubSpot", "Salesforce", "Zapier"
            ]
        )
        
        if st.button("Generate Workflow"):
            if not workflow_description:
                st.error("Please provide a workflow description")
            else:
                with st.spinner("Generating your N8N workflow..."):
                    try:
                        # Prepare the prompt for workflow generation
                        system_prompt = """You are an expert N8N workflow designer. 
                        Create a complete N8N workflow based on the user's description.
                        Return ONLY valid JSON that can be imported into N8N.
                        The JSON should include nodes, connections, and all necessary configuration.
                        """
                        
                        user_prompt = f"""
                        Create an N8N workflow based on this description:
                        "{workflow_description}"
                        
                        Additional requirements:
                        - Complexity level: {workflow_complexity}
                        - {"Include error handling nodes" if include_error_handling else "No error handling needed"}
                        - {"Preferred services: " + ", ".join(preferred_services) if preferred_services else "No service preferences"}
                        
                        Return ONLY the complete workflow JSON that can be imported into N8N.
                        """
                        
                        # Call OpenAI to generate the workflow
                        response = openai_client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_prompt}
                            ],
                            response_format={"type": "json_object"}
                        )
                        
                        # Extract the workflow JSON
                        workflow_json = json.loads(response.choices[0].message.content)
                        
                        # Save the workflow to session state
                        if "generated_workflows" not in st.session_state:
                            st.session_state.generated_workflows = []
                        
                        workflow_name = f"Generated Workflow: {workflow_description[:30]}..."
                        st.session_state.generated_workflows.append({
                            "name": workflow_name,
                            "data": workflow_json
                        })
                        
                        # Display success message
                        st.success("Workflow generated successfully!")
                        
                        # Display the workflow JSON
                        with st.expander("View Workflow JSON"):
                            st.json(workflow_json)
                        
                        # Provide download option
                        workflow_str = json.dumps(workflow_json, indent=2)
                        st.download_button(
                            label="Download Workflow JSON",
                            data=workflow_str,
                            file_name="n8n_workflow.json",
                            mime="application/json"
                        )
                        
                        # Show deployment option
                        if st.button("Deploy to N8N"):
                            if not n8n_url or not n8n_api_key:
                                st.error("Please configure your N8N connection settings first")
                            else:
                                try:
                                    # This would need to be implemented based on N8N's API
                                    st.info("Deployment to N8N would happen here")
                                    # In a real implementation, you would make an API call to N8N
                                    # to import the workflow
                                except Exception as e:
                                    st.error(f"Error deploying workflow: {str(e)}")
                    
                    except Exception as e:
                        st.error(f"Error generating workflow: {str(e)}")
    
    with n8n_tabs[1]:
        st.markdown("### Workflow Library")
        st.markdown("""
        Browse and use pre-built workflow templates for common automation scenarios.
        """)
        
        # Categories for workflow templates
        categories = [
            "All Templates",
            "Marketing Automation",
            "Sales & CRM",
            "Customer Support",
            "Data Processing",
            "Social Media",
            "Project Management"
        ]
        
        selected_category = st.selectbox("Filter by category", categories)
        
        # Sample workflow templates (in a real implementation, these would come from a database)
        templates = [
            {
                "name": "Lead Nurturing Workflow",
                "description": "Automatically nurture leads with personalized emails based on their behavior",
                "category": "Marketing Automation",
                "complexity": "Moderate",
                "services": ["HubSpot", "Gmail", "Slack"]
            },
            {
                "name": "Social Media Monitoring",
                "description": "Monitor social media mentions and send alerts to Slack",
                "category": "Social Media",
                "complexity": "Simple",
                "services": ["Twitter", "Slack"]
            },
            {
                "name": "Customer Ticket Processing",
                "description": "Automatically categorize and assign customer support tickets",
                "category": "Customer Support",
                "complexity": "Complex",
                "services": ["Zendesk", "Slack", "Airtable"]
            }
        ]
        
        # Filter templates by category
        if selected_category != "All Templates":
            filtered_templates = [t for t in templates if t["category"] == selected_category]
        else:
            filtered_templates = templates
        
        # Display templates
        for template in filtered_templates:
            with st.expander(f"{template['name']} ({template['complexity']})"):
                st.write(template["description"])
                st.write(f"**Services:** {', '.join(template['services'])}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"View {template['name']}", key=f"view_{template['name']}"):
                        st.info(f"This would show the details of the {template['name']} workflow")
                
                with col2:
                    if st.button(f"Use {template['name']}", key=f"use_{template['name']}"):
                        st.info(f"This would import the {template['name']} workflow template")
    
    with n8n_tabs[2]:
        st.markdown("### My Workflows")
        st.markdown("""
        View and manage your N8N workflows.
        """)
        
        if st.button("Refresh Workflows"):
            if not n8n_url or not n8n_api_key:
                st.error("Please configure your N8N connection settings first")
            else:
                with st.spinner("Fetching your workflows..."):
                    # In a real implementation, you would make an API call to N8N
                    # to get the user's workflows
                    st.info("This would fetch workflows from your N8N instance")
        
        # Display generated workflows from session state
        if "generated_workflows" in st.session_state and st.session_state.generated_workflows:
            st.markdown("#### Generated Workflows")
            
            for i, workflow in enumerate(st.session_state.generated_workflows):
                with st.expander(workflow["name"]):
                    st.json(workflow["data"])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("Deploy", key=f"deploy_{i}"):
                            st.info("This would deploy the workflow to N8N")
                    
                    with col2:
                        workflow_str = json.dumps(workflow["data"], indent=2)
                        st.download_button(
                            label="Download",
                            data=workflow_str,
                            file_name=f"{workflow['name']}.json",
                            mime="application/json",
                            key=f"download_{i}"
                        )
                    
                    with col3:
                        if st.button("Delete", key=f"delete_{i}"):
                            st.session_state.generated_workflows.pop(i)
                            st.rerun()
        else:
            st.info("No workflows generated yet. Use the Workflow Generator to create workflows.")

def n8n_knowledge_base():
    """
    Knowledge base for N8N workflows and automation best practices.
    """
    st.markdown("## N8N Knowledge Base")
    
    # Create tabs for different knowledge areas
    kb_tabs = st.tabs(["Getting Started", "Best Practices", "Common Patterns", "Troubleshooting"])
    
    with kb_tabs[0]:
        st.markdown("### Getting Started with N8N")
        st.markdown("""
        N8N is a powerful workflow automation tool that allows you to connect different services and automate tasks.
        
        #### Key Concepts
        
        - **Nodes**: Building blocks that represent actions or triggers
        - **Connections**: Links between nodes that define the flow of data
        - **Workflows**: Complete automation sequences made up of nodes and connections
        
        #### Basic Workflow Structure
        
        1. **Trigger Node**: Starts the workflow (e.g., webhook, schedule, database)
        2. **Processing Nodes**: Transform and manipulate data
        3. **Action Nodes**: Perform actions in external services
        
        #### Example: Simple Email Notification Workflow
        
        ```
        [Schedule] → [HTTP Request] → [Filter] → [Send Email]
        ```
        
        This workflow periodically checks a website, filters the results, and sends an email notification.
        """)
        
        st.markdown("#### Video Tutorial")
        st.video("https://www.youtube.com/watch?v=1MwSoB0gnM4")
    
    with kb_tabs[1]:
        st.markdown("### N8N Best Practices")
        st.markdown("""
        #### Workflow Design
        
        1. **Start Simple**: Begin with basic workflows and add complexity gradually
        2. **Use Error Handling**: Add error nodes to handle failures gracefully
        3. **Document Your Workflows**: Add notes to explain complex logic
        4. **Test Thoroughly**: Test with sample data before deploying
        
        #### Performance Optimization
        
        1. **Batch Processing**: Use batch operations when possible
        2. **Minimize API Calls**: Combine operations to reduce external API calls
        3. **Use Caching**: Cache results when appropriate
        4. **Schedule Wisely**: Choose appropriate intervals for scheduled workflows
        
        #### Security Considerations
        
        1. **Protect Credentials**: Use environment variables for sensitive information
        2. **Validate Inputs**: Always validate incoming data
        3. **Limit Permissions**: Use the principle of least privilege
        4. **Audit Regularly**: Review workflows and access permissions
        """)
    
    with kb_tabs[2]:
        st.markdown("### Common Workflow Patterns")
        
        patterns = [
            {
                "name": "Data Transformation",
                "description": "Extract, transform, and load data between systems",
                "example": "[Database] → [Function] → [Spreadsheet]"
            },
            {
                "name": "Notification System",
                "description": "Monitor events and send notifications",
                "example": "[Webhook] → [Filter] → [Slack/Email/SMS]"
            },
            {
                "name": "Content Publishing",
                "description": "Create and publish content across platforms",
                "example": "[RSS Feed] → [Function] → [Social Media Posts]"
            },
            {
                "name": "Lead Processing",
                "description": "Qualify and route leads to the right teams",
                "example": "[Form Submission] → [Scoring] → [CRM] → [Notification]"
            }
        ]
        
        for pattern in patterns:
            with st.expander(pattern["name"]):
                st.write(pattern["description"])
                st.code(pattern["example"], language="text")
                st.markdown("#### When to Use")
                st.write(f"Use this pattern when you need to {pattern['description'].lower()}.")
    
    with kb_tabs[3]:
        st.markdown("### Troubleshooting N8N Workflows")
        
        issues = [
            {
                "problem": "Workflow Not Triggering",
                "solutions": [
                    "Check if the trigger node is properly configured",
                    "Verify that the webhook URL is accessible",
                    "Check for any authentication issues",
                    "Ensure the workflow is activated"
                ]
            },
            {
                "problem": "Data Not Processing Correctly",
                "solutions": [
                    "Use the debug panel to inspect data at each step",
                    "Check for data format mismatches",
                    "Verify that all required fields are present",
                    "Add a Function node to transform data if needed"
                ]
            },
            {
                "problem": "API Connection Failures",
                "solutions": [
                    "Verify API credentials are correct",
                    "Check if you've reached API rate limits",
                    "Test the API endpoint separately",
                    "Add retry logic for transient failures"
                ]
            }
        ]
        
        for issue in issues:
            with st.expander(issue["problem"]):
                st.markdown("#### Solutions")
                for i, solution in enumerate(issue["solutions"]):
                    st.markdown(f"{i+1}. {solution}")

# Add this to your streamlit_ui.py to include the N8N tab
