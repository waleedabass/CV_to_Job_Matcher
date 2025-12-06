# Hugging Face Deployment Checklist

## Pre-Deployment

- [x] `app.py` is in root directory
- [x] `requirements.txt` is in root directory
- [x] All source files in `src/` directory
- [x] `.gitignore` file present
- [x] Code tested locally
- [ ] Code pushed to Git repository (GitHub/GitLab)

## Deployment Steps

### 1. Create Hugging Face Account
- [ ] Sign up at https://huggingface.co/join
- [ ] Verify email

### 2. Create Space
- [ ] Go to https://huggingface.co/spaces
- [ ] Click "Create new Space"
- [ ] Fill in:
  - [ ] Space name: `cv-job-matcher`
  - [ ] SDK: **Streamlit**
  - [ ] Visibility: Public/Private
  - [ ] Hardware: CPU Basic (free)

### 3. Push Code
- [ ] Add Hugging Face remote:
  ```bash
  git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/cv-job-matcher
  ```
- [ ] Push code:
  ```bash
  git push huggingface main
  ```

### 4. Configure Environment
- [ ] Go to Space Settings
- [ ] Add environment variable:
  - Key: `GOOGLE_AI_API_KEY`
  - Value: Your API key
  - Secret: ✅ Checked

### 5. Wait for Build
- [ ] Monitor build in "Logs" tab
- [ ] Wait 2-5 minutes
- [ ] Check for errors

### 6. Test
- [ ] Open app URL
- [ ] Test document upload
- [ ] Test analysis (with/without API key)
- [ ] Test report download
- [ ] Verify all features work

## Post-Deployment

- [ ] Share Space URL
- [ ] Update documentation with live link
- [ ] Monitor usage and errors
- [ ] Set up alerts (if needed)

## Files Required

✅ **Required:**
- `app.py` - Main application
- `requirements.txt` - Dependencies
- `src/` - Source code directory

✅ **Recommended:**
- `README.md` - Project description
- `.gitignore` - Git ignore rules
- `.hfignore` - HF ignore rules

✅ **Optional:**
- `README_HF.md` - Space-specific README
- `.streamlit/config.toml` - Streamlit config

## Troubleshooting

If build fails:
1. Check "Logs" tab for errors
2. Verify all dependencies in `requirements.txt`
3. Ensure `app.py` is in root
4. Check Python version compatibility

If app doesn't start:
1. Verify Streamlit SDK is selected
2. Check `app.py` for syntax errors
3. Review logs for import errors

## Quick Commands

```bash
# Add HF remote
git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/cv-job-matcher

# Push to HF
git push huggingface main

# Update deployment
git add .
git commit -m "Update app"
git push huggingface main
```

## Support

- HF Docs: https://huggingface.co/docs/hub/spaces
- HF Community: https://discuss.huggingface.co/
- Your Space URL: https://huggingface.co/spaces/YOUR_USERNAME/cv-job-matcher

