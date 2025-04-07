# Owaiken VM Deployment Guide

This guide will help you deploy the Owaiken application to a cloud VM. This approach ensures all dependencies are properly installed in a consistent environment.

## Step 1: Prepare Your VM

1. Create a new VM on your preferred cloud provider (AWS, Google Cloud, Azure, DigitalOcean, etc.)
2. Use Ubuntu 20.04 LTS or newer
3. Ensure the VM has at least:
   - 2 CPU cores
   - 4GB RAM
   - 20GB storage
4. Make sure ports 22 (SSH), 80 (HTTP), and 443 (HTTPS) are open in your firewall

## Step 2: Connect to Your VM

```bash
ssh username@your-vm-ip-address
```

## Step 3: Upload Your Code

Option 1: Use SCP to upload your code from your local machine:

```bash
# Run this on your local machine, not on the VM
cd /Users/aj/Downloads/Owaiken-main
scp -r ./* username@your-vm-ip-address:/tmp/owaiken/
```

Option 2: Clone directly from your Git repository (if you have one):

```bash
# Update the deploy_to_vm.sh script with your actual repository URL
```

## Step 4: Run the Deployment Script

```bash
# On your VM
cd /tmp/owaiken
chmod +x deploy_to_vm.sh
./deploy_to_vm.sh
```

## Step 5: Configure API Keys

After deployment, you need to set up your API keys:

```bash
# On your VM
sudo nano /opt/owaiken/.streamlit/secrets.toml
```

Add your API keys to this file:

```toml
# OpenAI API Key (for Whisper and other OpenAI services)
OPENAI_API_KEY = "your-openai-api-key"

# Other keys as needed...
```

Save the file (Ctrl+O, then Enter, then Ctrl+X)

## Step 6: Restart the Service

```bash
sudo systemctl restart owaiken
```

## Step 7: Access Your Application

Open a web browser and navigate to:

```
http://your-vm-ip-address
```

## Troubleshooting

If you encounter any issues, check the logs:

```bash
# View application logs
sudo journalctl -u owaiken -f

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

## Making Changes

To update your application after making changes:

```bash
# On your VM
cd /opt/owaiken
git pull  # If using git

# Or upload new files via SCP and copy them:
# cp -r /tmp/owaiken/* /opt/owaiken/

# Restart the service
sudo systemctl restart owaiken
```

## Security Recommendations

1. Set up HTTPS with Let's Encrypt:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

2. Use environment variables instead of the secrets.toml file:
   ```bash
   sudo nano /etc/systemd/system/owaiken.service
   # Add environment variables:
   # Environment=OPENAI_API_KEY=your-api-key
   sudo systemctl daemon-reload
   sudo systemctl restart owaiken
   ```

3. Keep your system updated:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```
