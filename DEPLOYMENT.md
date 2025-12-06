# Deployment Guide for Render

This guide provides step-by-step instructions for deploying the CV-to-Job Matcher application on Render.

## Prerequisites

1. A GitHub account
2. A Render account (sign up at https://render.com - free tier available)
3. Git installed on your local machine

## Step-by-Step Deployment

### Step 1: Prepare Your Code

1. Make sure all files are in your project directory:
   ```
   SE Project/
   ├── app.py
   ├── requirements.txt
   ├── render.yaml
   ├── README.md
   ├── .gitignore
   └── src/
       ├── __init__.py
       ├── document_parser.py
       ├── skill_extractor.py
       ├── matcher.py
       ├── report_generator.py
       └── utils.py
   ```

### Step 2: Initialize Git Repository

If you haven't already:

```bash
cd "E:\SE Project"
git init
git add .
git commit -m "Initial commit - CV Job Matcher"
```

### Step 3: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `cv-job-matcher`)
3. **Do NOT** initialize with README, .gitignore, or license (we already have these)
4. Copy the repository URL

### Step 4: Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/cv-job-matcher.git
git branch -M main
git push -u origin main
```

### Step 5: Deploy on Render

#### Option A: Using render.yaml (Recommended)

1. Go to https://dashboard.render.com/
2. Click "New +" → "Blueprint"
3. Connect your GitHub account if not already connected
4. Select your repository (`cv-job-matcher`)
5. Render will automatically detect `render.yaml`
6. Review the configuration and click "Apply"
7. Wait for deployment (2-5 minutes)

#### Option B: Manual Configuration

1. Go to https://dashboard.render.com/
2. Click "New +" → "Web Service"
3. Connect your GitHub account if not already connected
4. Select your repository
5. Configure:
   - **Name**: `cv-job-matcher`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
6. Click "Create Web Service"

### Step 6: Wait for Deployment

- Render will:
  1. Install dependencies from `requirements.txt`
  2. Build your application
  3. Start the Streamlit server
  4. Provide you with a URL (e.g., `https://cv-job-matcher.onrender.com`)

### Step 7: Verify Deployment

1. Click on your service URL
2. You should see the CV-to-Job Matcher interface
3. Test by uploading a sample CV and JD

## Troubleshooting

### Build Fails

- Check the build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility

### App Doesn't Start

- Check the logs for errors
- Verify the start command is correct
- Ensure `app.py` is in the root directory

### Port Issues

- Render automatically sets `$PORT` environment variable
- Make sure your start command uses `$PORT`
- Streamlit should bind to `0.0.0.0` not `localhost`

### Memory Issues (Free Tier)

- Free tier has 512MB RAM limit
- If you hit memory limits, consider:
  - Optimizing code
  - Using Render's paid plans
  - Reducing model complexity

## Environment Variables

If you need to add environment variables:

1. Go to your service in Render dashboard
2. Navigate to "Environment" tab
3. Add variables as needed

## Updating Your App

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push
   ```
3. Render will automatically detect changes and redeploy

## Custom Domain (Optional)

1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain
4. Follow DNS configuration instructions

## Monitoring

- View logs in real-time in Render dashboard
- Check metrics (CPU, Memory, Requests)
- Set up alerts for errors

## Cost

- **Free Tier**: 
  - 750 hours/month
  - Services spin down after 15 minutes of inactivity
  - Good for demos and testing
  
- **Paid Plans**: 
  - Always-on services
  - More resources
  - Better performance

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- GitHub Issues: Open an issue in your repository

## Next Steps

After successful deployment:

1. Test all features thoroughly
2. Share the URL with users
3. Monitor usage and performance
4. Collect feedback for improvements
5. Consider adding:
   - User authentication
   - Database for storing results
   - Analytics
   - Custom domain

