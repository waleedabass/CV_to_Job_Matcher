# Deploying to Hugging Face Spaces

This guide will help you deploy the CV-to-Job Matcher application to Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account (sign up at https://huggingface.co/join)
2. Your code pushed to a Git repository (GitHub, GitLab, etc.)
3. Google AI API key (optional, for AI features)

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

Make sure your repository has:
- `app.py` in the root directory
- `requirements.txt` in the root directory
- `README.md` (will be used as Space description)
- `src/` directory with all modules

### Step 2: Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Fill in the details:
   - **Space name**: `cv-job-matcher` (or your preferred name)
   - **SDK**: Select **"Streamlit"**
   - **Visibility**: Choose **Public** (free) or **Private** (requires paid plan)
   - **Hardware**: Select **CPU Basic** (free) or upgrade if needed
4. Click **"Create Space"**

### Step 3: Connect Your Repository

You have two options:

#### Option A: Direct Git Push (Recommended)

1. **Get your access token**:
   - Go to https://huggingface.co/settings/tokens
   - Click "New token"
   - Select "Write" permissions
   - Copy the token

2. **Add remote and push**:
   ```bash
   # Method 1: Include token in URL (easiest)
   git remote add huggingface https://YOUR_USERNAME:YOUR_TOKEN@huggingface.co/spaces/YOUR_USERNAME/cv-job-matcher
   git push huggingface main
   
   # Method 2: Use credential helper (more secure)
   git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/cv-job-matcher
   git config --global credential.helper wincred  # Windows
   # or: git config --global credential.helper store  # Linux/Mac
   git push huggingface main
   # When prompted: Username = YOUR_USERNAME, Password = YOUR_TOKEN
   ```

**Important**: Use your **access token** as the password, NOT your Hugging Face account password!

#### Option B: GitHub Integration

1. In your Space settings, go to **"Repository"** tab
2. Connect your GitHub repository
3. Select the branch (usually `main`)
4. Hugging Face will automatically sync

### Step 4: Configure Environment Variables

1. In your Space, go to **"Settings"** → **"Variables and secrets"**
2. Add the following environment variable:
   - **Key**: `GOOGLE_AI_API_KEY`
   - **Value**: Your Google AI API key (get it from https://aistudio.google.com/apikey)
   - **Secret**: ✅ Check this box (hides the value)

3. Click **"Save"**

### Step 5: Wait for Build

- Hugging Face will automatically:
  1. Install dependencies from `requirements.txt`
  2. Build your application
  3. Start the Streamlit server

- This usually takes 2-5 minutes
- You can monitor progress in the **"Logs"** tab

### Step 6: Access Your App

Once built, your app will be available at:
```
https://huggingface.co/spaces/YOUR_USERNAME/cv-job-matcher
```

## File Structure for Hugging Face

Your repository should have this structure:
```
.
├── app.py                 # Main Streamlit app (required)
├── requirements.txt       # Python dependencies (required)
├── README.md             # Space description (optional but recommended)
├── .gitignore            # Git ignore rules
├── src/                  # Source code modules
│   ├── __init__.py
│   ├── document_parser.py
│   ├── skill_extractor.py
│   ├── matcher.py
│   ├── gemini_client.py
│   ├── report_generator.py
│   └── utils.py
└── .streamlit/           # Streamlit config (optional)
    └── config.toml
```

## Updating Your Deployment

### Method 1: Git Push
```bash
git add .
git commit -m "Update app"
git push huggingface main
```

### Method 2: GitHub Integration
- Just push to your connected GitHub repository
- Hugging Face will automatically rebuild

## Hardware Options

### Free Tier (CPU Basic)
- ✅ Sufficient for testing and demos
- ✅ 2 CPU cores
- ✅ 16 GB RAM
- ⚠️ Apps sleep after 48 hours of inactivity

### Paid Tiers
- **CPU Upgrade**: Better performance, no sleep
- **GPU**: For heavy ML workloads (not needed for this app)

## Troubleshooting

### Build Fails

1. **Check Logs**: Go to **"Logs"** tab in your Space
2. **Common Issues**:
   - Missing dependencies in `requirements.txt`
   - Syntax errors in code
   - Import errors

3. **Fix and Push Again**:
   ```bash
   git add .
   git commit -m "Fix build issues"
   git push huggingface main
   ```

### App Doesn't Start

1. Check that `app.py` is in the root directory
2. Verify Streamlit SDK is selected
3. Check logs for error messages

### Environment Variables Not Working

1. Make sure variable name is exactly `GOOGLE_AI_API_KEY`
2. Verify it's marked as "Secret" if it contains sensitive data
3. Restart the Space after adding variables

### API Key Issues

- The app will work without API key (rule-based matching)
- For AI features, ensure `GOOGLE_AI_API_KEY` is set correctly
- Check API key is valid at https://aistudio.google.com/apikey

## Custom Domain (Optional)

Hugging Face Spaces don't support custom domains directly, but you can:
- Use the provided `huggingface.co/spaces/...` URL
- Set up a redirect from your domain
- Use Hugging Face's subdomain feature if available

## Monitoring

- **Logs**: Real-time logs in the **"Logs"** tab
- **Metrics**: View usage statistics in Space settings
- **Activity**: See when your app was last accessed

## Best Practices

1. **Keep requirements.txt updated**: Only include necessary packages
2. **Use environment variables**: Don't hardcode API keys
3. **Test locally first**: Make sure app works before deploying
4. **Monitor usage**: Check logs regularly for errors
5. **Update regularly**: Keep dependencies up to date

## Cost

- **Free Tier**: Completely free for public spaces
- **Private Spaces**: Requires paid Hugging Face plan
- **API Usage**: Google Gemini API has its own pricing (see GEMINI_SETUP.md)

## Support

- Hugging Face Docs: https://huggingface.co/docs/hub/spaces
- Community Forum: https://discuss.huggingface.co/
- GitHub Issues: Open an issue in your repository

## Next Steps

After deployment:
1. Test all features
2. Share the Space URL
3. Monitor usage and errors
4. Gather user feedback
5. Iterate and improve

