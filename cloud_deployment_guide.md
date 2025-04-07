# Owaiken Cloud Deployment Guide

This guide provides instructions for deploying the Owaiken application to a cloud VM.

## Prerequisites

- A cloud VM with Ubuntu 20.04 or later
- Python 3.8 or later installed
- Git installed
- Sufficient permissions to install packages and run services

## Deployment Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Owaiken.git
cd Owaiken
```

### 2. Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.streamlit` directory and set up the secrets file:

```bash
mkdir -p .streamlit
touch .streamlit/secrets.toml
chmod 700 .streamlit
chmod 600 .streamlit/secrets.toml
```

Edit the secrets file to include your API keys:

```toml
# Owaiken Secrets Configuration
# SECURITY WARNING: Store actual API keys in environment variables for production

# OpenAI API Key (for Whisper and other OpenAI services)
OPENAI_API_KEY = "your-api-key"

# Supabase Configuration (if needed)
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-key"

# Keygen License Configuration
KEYGEN_ACCOUNT_ID = "your-keygen-account-id"
KEYGEN_PRODUCT_ID = "your-keygen-product-id"

# Security settings
COOKIE_PASSWORD = "generate-a-random-string-here"
```

Alternatively, set environment variables directly:

```bash
export OPENAI_API_KEY="your-api-key"
export SUPABASE_URL="your-supabase-url"
export SUPABASE_KEY="your-supabase-key"
export KEYGEN_ACCOUNT_ID="your-keygen-account-id"
export KEYGEN_PRODUCT_ID="your-keygen-product-id"
```

### 5. Run the Application

For development/testing:

```bash
streamlit run streamlit_ui.py
```

For production, set up a systemd service:

Create a service file:

```bash
sudo nano /etc/systemd/system/owaiken.service
```

Add the following content:

```
[Unit]
Description=Owaiken Streamlit Application
After=network.target

[Service]
User=yourusername
WorkingDirectory=/path/to/Owaiken
ExecStart=/path/to/Owaiken/venv/bin/streamlit run streamlit_ui.py
Restart=always
Environment=PYTHONUNBUFFERED=1
Environment=OPENAI_API_KEY=your-api-key
Environment=SUPABASE_URL=your-supabase-url
Environment=SUPABASE_KEY=your-supabase-key

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable owaiken
sudo systemctl start owaiken
```

### 6. Set Up Nginx as a Reverse Proxy (Optional)

Install Nginx:

```bash
sudo apt update
sudo apt install nginx
```

Create a configuration file:

```bash
sudo nano /etc/nginx/sites-available/owaiken
```

Add the following content:

```
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable the site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/owaiken /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 7. Set Up SSL with Let's Encrypt (Optional)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Troubleshooting

### Application Crashes

Check the logs:

```bash
sudo journalctl -u owaiken.service -f
```

### Permission Issues

Make sure the application has the right permissions:

```bash
sudo chown -R yourusername:yourusername /path/to/Owaiken
```

### API Key Issues

Verify your API keys are correctly set:

```bash
grep -r "API_KEY" .streamlit/secrets.toml
```

## Security Recommendations

1. Use environment variables instead of the secrets.toml file for production
2. Set up a firewall to restrict access to your server
3. Keep your system and dependencies updated
4. Use strong, unique passwords for all services
5. Regularly back up your data

## Monitoring

Consider setting up basic monitoring for your application:

```bash
sudo apt install prometheus node-exporter
```

## Backup Strategy

Regularly back up your application data:

```bash
# Create a backup script
mkdir -p /backups/owaiken
tar -czf /backups/owaiken/backup-$(date +%Y%m%d).tar.gz /path/to/Owaiken
```
