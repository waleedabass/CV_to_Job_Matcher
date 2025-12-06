# Quick Deploy to Hugging Face Spaces

## Fastest Method (5 minutes)

### 1. Create Space
1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in:
   - **Name**: `cv-job-matcher`
   - **SDK**: **Streamlit**
   - **Hardware**: CPU Basic (free)
4. Click **"Create Space"**

### 2. Get Access Token

1. Go to https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Select **"Write"** permissions
4. Copy the token (you'll need it!)

### 3. Push Your Code

**Option A: Include token in URL (Easiest)**
```bash
git remote add huggingface https://Waleed765:YOUR_TOKEN@huggingface.co/spaces/Waleed765/cv-job-matcher
git push huggingface main
```

**Option B: Use credential helper**
```bash
git remote add huggingface https://huggingface.co/spaces/Waleed765/cv-job-matcher
git config --global credential.helper wincred
git push huggingface main
# When prompted:
# Username: Waleed765
# Password: YOUR_TOKEN (paste token, not password!)
```

Replace `YOUR_TOKEN` with the token from step 2.

### 3. Add API Key (Optional)

1. In your Space → **Settings** → **Variables and secrets**
2. Add: `GOOGLE_AI_API_KEY` = your key
3. Mark as **Secret** ✅

### 4. Done! 🎉

Your app is live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/cv-job-matcher
```

## What You Need

- ✅ `app.py` (already have it)
- ✅ `requirements.txt` (already have it)
- ✅ `src/` folder (already have it)
- ✅ Hugging Face account (free)

## Troubleshooting

**Build fails?**
- Check the **Logs** tab
- Make sure `requirements.txt` has all dependencies

**App not starting?**
- Verify `app.py` is in root directory
- Check Streamlit SDK is selected

**Need help?**
- See [DEPLOYMENT_HF.md](DEPLOYMENT_HF.md) for detailed guide

