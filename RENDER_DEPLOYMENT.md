# Deploying Owaiken to Render via GitHub

This guide will walk you through the process of pushing your Owaiken application to GitHub and then deploying it to Render.

## Step 1: Push Your Code to GitHub

1. **Create a new GitHub repository**:
   - Go to [GitHub](https://github.com) and sign in
   - Click the "+" icon in the top right and select "New repository"
   - Name your repository (e.g., "Owaiken")
   - Choose visibility (public or private)
   - Click "Create repository"

2. **Initialize your local repository and push to GitHub**:
   ```bash
   # Navigate to your Owaiken directory
   cd /Users/aj/Downloads/Owaiken-main

   # Initialize git repository (if not already done)
   git init

   # Add all files
   git add .

   # Commit the changes
   git commit -m "Initial commit for Owaiken"

   # Add your GitHub repository as a remote
   git remote add origin https://github.com/yourusername/Owaiken.git

   # Push to GitHub
   git push -u origin main
   ```

## Step 2: Deploy to Render

1. **Sign up for Render**:
   - Go to [Render](https://render.com) and sign up for an account if you don't have one

2. **Connect your GitHub account**:
   - In the Render dashboard, click on your profile in the top right
   - Select "Account Settings"
   - Go to "GitHub" tab
   - Click "Connect GitHub" and follow the instructions

3. **Create a new Web Service**:
   - From the Render dashboard, click "New +" and select "Web Service"
   - Select "Connect GitHub repo"
   - Find and select your Owaiken repository
   - Click "Connect"

4. **Configure your Web Service**:
   - Name: "owaiken" (or your preferred name)
   - Region: Choose the region closest to your users
   - Branch: "main" (or your default branch)
   - Runtime: "Python 3"
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run streamlit_ui.py`
   - Instance Type: "Free" (to start, you can upgrade later)
   - Click "Advanced" and add the following environment variables:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - Any other API keys your application needs

5. **Create Web Service**:
   - Click "Create Web Service"
   - Render will now build and deploy your application (this may take a few minutes)

6. **Access Your Application**:
   - Once deployment is complete, Render will provide a URL (e.g., `https://owaiken.onrender.com`)
   - Click the URL to access your application

## Step 3: Configure Streamlit Secrets (Optional)

If your application requires secrets, you can set them up in Render:

1. **Add Environment Variables**:
   - In your Render dashboard, select your Owaiken service
   - Go to the "Environment" tab
   - Add each secret as a key-value pair
   - Click "Save Changes"

2. **Update Your Code**:
   - Make sure your code reads secrets from environment variables:
   ```python
   import os
   api_key = os.environ.get("OPENAI_API_KEY")
   ```

## Step 4: Set Up Automatic Deployments

Render automatically deploys when you push changes to your GitHub repository. To update your application:

1. **Make changes to your code locally**
2. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Update description here"
   git push
   ```
3. **Render will automatically detect the changes and redeploy**

## Troubleshooting

If you encounter issues with your deployment:

1. **Check the Render logs**:
   - In your Render dashboard, select your Owaiken service
   - Go to the "Logs" tab to see what's happening

2. **Verify environment variables**:
   - Make sure all required API keys and secrets are set correctly

3. **Check for missing dependencies**:
   - Ensure all required packages are in your requirements.txt file

4. **Memory/CPU issues**:
   - If your application is slow or crashes, consider upgrading from the free tier

## Additional Tips

1. **Custom Domain**:
   - In your Render dashboard, select your Owaiken service
   - Go to the "Settings" tab
   - Under "Custom Domain", click "Add Custom Domain"
   - Follow the instructions to set up your domain

2. **Performance Monitoring**:
   - Render provides basic metrics in the "Metrics" tab
   - Consider adding application-level monitoring

3. **Scaling**:
   - As your needs grow, you can easily upgrade your instance type in the "Settings" tab
