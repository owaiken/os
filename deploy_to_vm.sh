#!/bin/bash
# Owaiken Cloud Deployment Script
# This script sets up the Owaiken application on a fresh Ubuntu VM

# Exit on any error
set -e

echo "===== Starting Owaiken Deployment ====="

# Update system packages
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install required system dependencies
echo "Installing system dependencies..."
sudo apt install -y python3-pip python3-venv git nginx

# Create application directory
echo "Setting up application directory..."
APP_DIR="/opt/owaiken"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Clone the repository (replace with your actual repository URL)
echo "Cloning the repository..."
git clone https://github.com/yourusername/Owaiken.git $APP_DIR || cp -r /tmp/owaiken/* $APP_DIR/

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt || pip install streamlit openai python-dotenv logfire

# Create secrets directory with proper permissions
echo "Setting up secrets configuration..."
mkdir -p .streamlit
touch .streamlit/secrets.toml
chmod 700 .streamlit
chmod 600 .streamlit/secrets.toml

# Configure secrets (you'll need to edit this file manually)
cat > .streamlit/secrets.toml << EOF
# Owaiken Secrets Configuration
# SECURITY WARNING: Store actual API keys in environment variables for production

# OpenAI API Key (for Whisper and other OpenAI services)
OPENAI_API_KEY = ""

# Supabase Configuration (if needed)
SUPABASE_URL = ""
SUPABASE_KEY = ""

# Keygen License Configuration
KEYGEN_ACCOUNT_ID = ""
KEYGEN_PRODUCT_ID = ""

# Security settings
COOKIE_PASSWORD = "$(openssl rand -hex 32)"
EOF

# Set up systemd service
echo "Setting up systemd service..."
sudo bash -c "cat > /etc/systemd/system/owaiken.service << EOF
[Unit]
Description=Owaiken Streamlit Application
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/streamlit run streamlit_ui.py
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF"

# Set up Nginx as a reverse proxy
echo "Setting up Nginx reverse proxy..."
sudo bash -c "cat > /etc/nginx/sites-available/owaiken << EOF
server {
    listen 80;
    server_name \$host;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF"

# Enable the Nginx site
sudo ln -sf /etc/nginx/sites-available/owaiken /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Enable and start the service
echo "Starting the Owaiken service..."
sudo systemctl enable owaiken
sudo systemctl start owaiken

echo "===== Owaiken Deployment Complete ====="
echo "You can now access your application at http://your-server-ip"
echo "Check the service status with: sudo systemctl status owaiken"
echo "View logs with: sudo journalctl -u owaiken -f"
