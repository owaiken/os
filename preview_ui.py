import streamlit as st
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set page config
st.set_page_config(
    page_title="Owaiken UI Preview",
    page_icon="🎨",
    layout="wide",
)

# Custom CSS to simulate Shadcn UI styles
st.markdown("""
<style>
:root {
    --primary: #000000;
    --primary-foreground: #ffffff;
    --secondary: #444444;
    --secondary-foreground: #ffffff;
    --background: #ffffff;
    --foreground: #000000;
    --muted: #f1f5f9;
    --muted-foreground: #64748b;
    --accent: #f1f5f9;
    --accent-foreground: #0f172a;
    --destructive: #ef4444;
    --destructive-foreground: #ffffff;
    --border: #e2e8f0;
    --input: #e2e8f0;
    --ring: #000000;
    --radius: 0.5rem;
}

/* Dark mode */
.dark {
    --background: #020817;
    --foreground: #ffffff;
    --muted: #1e293b;
    --muted-foreground: #94a3b8;
    --accent: #1e293b;
    --accent-foreground: #ffffff;
    --border: #1e293b;
    --input: #1e293b;
}

/* Button styles */
.shadcn-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius);
    font-weight: 500;
    padding: 0.5rem 1rem;
    transition: all 0.2s ease;
    cursor: pointer;
    margin: 0.25rem;
}

.shadcn-button.primary {
    background-color: var(--primary);
    color: var(--primary-foreground);
    border: none;
}

.shadcn-button.secondary {
    background-color: var(--secondary);
    color: var(--secondary-foreground);
    border: none;
}

.shadcn-button.destructive {
    background-color: var(--destructive);
    color: var(--destructive-foreground);
    border: none;
}

.shadcn-button.outline {
    background-color: transparent;
    color: var(--foreground);
    border: 1px solid var(--border);
}

.shadcn-button.ghost {
    background-color: transparent;
    color: var(--foreground);
    border: none;
}

.shadcn-button:hover {
    opacity: 0.9;
}

/* Card styles */
.shadcn-card {
    background-color: var(--background);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}

.shadcn-card-header {
    margin-bottom: 1rem;
}

.shadcn-card-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
}

.shadcn-card-description {
    color: var(--muted-foreground);
    font-size: 0.875rem;
}

.shadcn-card-content {
    margin-bottom: 1rem;
}

.shadcn-card-footer {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
}

/* Input styles */
.shadcn-input {
    width: 100%;
    border-radius: var(--radius);
    border: 1px solid var(--input);
    background-color: transparent;
    padding: 0.5rem;
    font-size: 0.875rem;
    margin-bottom: 1rem;
}

.shadcn-input:focus {
    outline: none;
    border-color: var(--ring);
    box-shadow: 0 0 0 1px var(--ring);
}

/* Badge styles */
.shadcn-badge {
    display: inline-flex;
    align-items: center;
    border-radius: 9999px;
    padding: 0.125rem 0.5rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin-right: 0.5rem;
}

.shadcn-badge.default {
    background-color: var(--primary);
    color: var(--primary-foreground);
}

.shadcn-badge.secondary {
    background-color: var(--secondary);
    color: var(--secondary-foreground);
}

.shadcn-badge.outline {
    background-color: transparent;
    border: 1px solid var(--border);
    color: var(--foreground);
}

.shadcn-badge.destructive {
    background-color: var(--destructive);
    color: var(--destructive-foreground);
}

/* Alert styles */
.shadcn-alert {
    border-radius: var(--radius);
    padding: 1rem;
    margin-bottom: 1rem;
    border-left: 4px solid;
}

.shadcn-alert.default {
    background-color: var(--muted);
    border-left-color: var(--primary);
}

.shadcn-alert.success {
    background-color: #dcfce7;
    border-left-color: #22c55e;
}

.shadcn-alert.warning {
    background-color: #fef9c3;
    border-left-color: #eab308;
}

.shadcn-alert.destructive {
    background-color: #fee2e2;
    border-left-color: var(--destructive);
}

/* Switch styles */
.shadcn-switch {
    position: relative;
    display: inline-block;
    width: 36px;
    height: 20px;
    margin-right: 0.5rem;
}

.shadcn-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.shadcn-switch-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--muted);
    transition: .4s;
    border-radius: 34px;
}

.shadcn-switch-slider:before {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 2px;
    bottom: 2px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
}

input:checked + .shadcn-switch-slider {
    background-color: var(--primary);
}

input:checked + .shadcn-switch-slider:before {
    transform: translateX(16px);
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("Owaiken UI with Shadcn Components")
st.markdown("This is a preview of how Shadcn UI components will look in your Owaiken application.")

# Create tabs for different component categories
tabs = st.tabs(["Overview", "Basic Components", "Form Elements", "Layout Components"])

with tabs[0]:
    st.header("Overview")
    st.markdown("""
    Shadcn UI provides a set of accessible, reusable, and composable components that can be used to build modern web applications.
    These components are designed to be:
    
    - **Accessible**: All components follow WAI-ARIA guidelines
    - **Responsive**: Components adapt to different screen sizes
    - **Customizable**: Easy to customize with CSS variables
    - **Consistent**: Uniform design language across all components
    """)
    
    # Show a card with key features
    st.markdown("""
    <div class="shadcn-card">
        <div class="shadcn-card-header">
            <div class="shadcn-card-title">Key Features</div>
            <div class="shadcn-card-description">What makes Shadcn UI special</div>
        </div>
        <div class="shadcn-card-content">
            <ul>
                <li>Modern design with clean aesthetics</li>
                <li>Dark and light mode support</li>
                <li>Keyboard navigation support</li>
                <li>Responsive and mobile-friendly</li>
                <li>Seamless integration with Streamlit</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tabs[1]:
    st.header("Basic Components")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Buttons")
        st.markdown("""
        <button class="shadcn-button primary">Primary Button</button>
        <button class="shadcn-button secondary">Secondary Button</button>
        <button class="shadcn-button destructive">Destructive Button</button>
        <button class="shadcn-button outline">Outline Button</button>
        <button class="shadcn-button ghost">Ghost Button</button>
        """, unsafe_allow_html=True)
        
        st.subheader("Badges")
        st.markdown("""
        <span class="shadcn-badge default">Default</span>
        <span class="shadcn-badge secondary">Secondary</span>
        <span class="shadcn-badge outline">Outline</span>
        <span class="shadcn-badge destructive">Destructive</span>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Alerts")
        st.markdown("""
        <div class="shadcn-alert default">
            <strong>Information:</strong> This is an informational alert.
        </div>
        <div class="shadcn-alert success">
            <strong>Success:</strong> Operation completed successfully.
        </div>
        <div class="shadcn-alert warning">
            <strong>Warning:</strong> This action cannot be undone.
        </div>
        <div class="shadcn-alert destructive">
            <strong>Error:</strong> Something went wrong.
        </div>
        """, unsafe_allow_html=True)

with tabs[2]:
    st.header("Form Elements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Fields")
        st.markdown("""
        <label for="username">Username</label>
        <input class="shadcn-input" id="username" placeholder="Enter your username" />
        
        <label for="email">Email</label>
        <input class="shadcn-input" id="email" type="email" placeholder="Enter your email" />
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Switches")
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <label class="shadcn-switch">
                <input type="checkbox" checked>
                <span class="shadcn-switch-slider"></span>
            </label>
            <span>Notifications</span>
        </div>
        
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <label class="shadcn-switch">
                <input type="checkbox">
                <span class="shadcn-switch-slider"></span>
            </label>
            <span>Dark Mode</span>
        </div>
        """, unsafe_allow_html=True)

with tabs[3]:
    st.header("Layout Components")
    
    st.subheader("Cards")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="shadcn-card">
            <div class="shadcn-card-header">
                <div class="shadcn-card-title">Feature Card</div>
                <div class="shadcn-card-description">A card showcasing a feature</div>
            </div>
            <div class="shadcn-card-content">
                <p>This card contains information about a feature. Cards are useful for organizing related content and actions.</p>
            </div>
            <div class="shadcn-card-footer">
                <button class="shadcn-button outline">Learn More</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="shadcn-card">
            <div class="shadcn-card-header">
                <div class="shadcn-card-title">Pricing Card</div>
                <div class="shadcn-card-description">A card showing pricing information</div>
            </div>
            <div class="shadcn-card-content">
                <h3>$99/month</h3>
                <p>All features included</p>
                <ul>
                    <li>Feature 1</li>
                    <li>Feature 2</li>
                    <li>Feature 3</li>
                </ul>
            </div>
            <div class="shadcn-card-footer">
                <button class="shadcn-button primary">Subscribe</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center;">
    <div>Owaiken UI Preview</div>
    <div>
        <button class="shadcn-button outline">Light</button>
        <button class="shadcn-button primary">Dark</button>
    </div>
</div>
""", unsafe_allow_html=True)
