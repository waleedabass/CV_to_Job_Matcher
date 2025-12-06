# Hugging Face Authentication Guide

## Problem
You're getting: `remote: Invalid username or password. fatal: Authentication failed`

## Solution: Use Access Token

Hugging Face requires an access token (not your password) for Git operations.

### Step 1: Create Access Token

1. Go to https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Fill in:
   - **Name**: `cv-job-matcher-deploy` (or any name)
   - **Type**: **Write** (needed to push code)
   - **Expiration**: Choose your preference
4. Click **"Generate token"**
5. **Copy the token immediately** (you won't see it again!)

### Step 2: Use Token for Authentication

#### Option A: Include Token in URL (Easiest)

```bash
git remote set-url huggingface https://YOUR_USERNAME:YOUR_TOKEN@huggingface.co/spaces/Waleed765/cv-job-matcher
git push huggingface main
```

Replace:
- `YOUR_USERNAME` with your Hugging Face username (Waleed765)
- `YOUR_TOKEN` with the token you just created

#### Option B: Use Git Credential Helper (Recommended)

**Windows:**
```bash
# Set credential helper
git config --global credential.helper wincred

# Push (will prompt for credentials)
git push huggingface main
# Username: Waleed765
# Password: YOUR_TOKEN (paste the token, not your password!)
```

**Linux/Mac:**
```bash
# Set credential helper
git config --global credential.helper store

# Push (will prompt for credentials)
git push huggingface main
# Username: Waleed765
# Password: YOUR_TOKEN
```

#### Option C: Use SSH (Most Secure)

1. Generate SSH key (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Add SSH key to Hugging Face:
   - Go to https://huggingface.co/settings/keys
   - Click "New SSH key"
   - Paste your public key (`~/.ssh/id_ed25519.pub`)

3. Change remote to SSH:
   ```bash
   git remote set-url huggingface git@hf.co:spaces/Waleed765/cv-job-matcher
   git push huggingface main
   ```

## Quick Fix (Copy-Paste Ready)

1. Get your token from https://huggingface.co/settings/tokens
2. Run this command (replace YOUR_TOKEN):

```bash
git remote set-url huggingface https://Waleed765:YOUR_TOKEN@huggingface.co/spaces/Waleed765/cv-job-matcher
git push huggingface main
```

## Security Note

⚠️ **Never commit your token to Git!**
- Tokens in URLs are stored in Git config (local only, but still be careful)
- Use credential helper or SSH for better security
- If token is exposed, revoke it immediately and create a new one

## Troubleshooting

**Still getting authentication error?**
- Verify token has "Write" permissions
- Check token hasn't expired
- Make sure username is correct (case-sensitive)
- Try regenerating the token

**Token not working?**
- Revoke old token
- Create new token with "Write" permissions
- Try again

