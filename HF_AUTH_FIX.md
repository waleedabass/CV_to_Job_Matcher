# Fixing Hugging Face Authentication Issues

## Problem
Even with token in URL, getting: `remote: Invalid username or password`

## Solutions to Try

### Solution 1: Use Credential Helper (Recommended)

```powershell
# Remove token from URL
git remote set-url huggingface https://huggingface.co/spaces/Waleed765/cv-job-matcher

# Set credential helper
git config --global credential.helper wincred

# Push (will prompt for credentials)
git push huggingface main
```

**When prompted:**
- Username: `Waleed765`
- Password: `hf_HJIqMETIPfSSiOUEMgZQRMpEjgxTXETwmuN` (your full token)

### Solution 2: Verify Token Permissions

1. Go to https://huggingface.co/settings/tokens
2. Check your token:
   - ✅ Must have **"Write"** permission (not just "Read")
   - ✅ Must not be expired
3. If needed, create a NEW token with **"Write"** permissions

### Solution 3: URL Encode Special Characters

If your token has special characters, try encoding them:

```powershell
# Remove the remote first
git remote remove huggingface

# Add with encoded token (if token has special chars)
# Replace any special characters in token with URL encoding
git remote add huggingface https://Waleed765:YOUR_ENCODED_TOKEN@huggingface.co/spaces/Waleed765/cv-job-matcher
```

### Solution 4: Use SSH Instead

1. **Generate SSH key** (if you don't have one):
   ```powershell
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Press Enter to accept default location
   # Press Enter for no passphrase (or set one)
   ```

2. **Copy your public key**:
   ```powershell
   cat ~/.ssh/id_ed25519.pub
   # Or on Windows:
   type C:\Users\Sikandar\.ssh\id_ed25519.pub
   ```

3. **Add SSH key to Hugging Face**:
   - Go to https://huggingface.co/settings/keys
   - Click "New SSH key"
   - Paste your public key
   - Save

4. **Change remote to SSH**:
   ```powershell
   git remote set-url huggingface git@hf.co:spaces/Waleed765/cv-job-matcher
   git push huggingface main
   ```

### Solution 5: Check Token Format

Your token should:
- Start with `hf_` ✅ (yours does)
- Be the FULL token (not truncated)
- Have "Write" permissions

### Solution 6: Create New Token

If nothing works, create a fresh token:

1. Go to https://huggingface.co/settings/tokens
2. Delete old token (if needed)
3. Create new token:
   - Name: `cv-job-matcher-v2`
   - Type: **Write** (important!)
   - Generate
4. Copy the NEW token
5. Try authentication again

## Quick Test

Test if your token works:

```powershell
# Test with curl (if you have it)
curl -H "Authorization: Bearer hf_HJIqMETIPfSSiOUEMgZQRMpEjgxTXETwmuN" https://huggingface.co/api/whoami
```

Should return your username if token is valid.

## Most Likely Issue

**Token doesn't have "Write" permissions!**

Check at: https://huggingface.co/settings/tokens
- Your token must show **"Write"** not just "Read"
- If it only has "Read", create a new one with "Write"

## Step-by-Step Fix

1. **Verify token permissions**:
   - Go to https://huggingface.co/settings/tokens
   - Find your token
   - Check it has **"Write"** permission

2. **If token is Read-only, create new one**:
   - Click "New token"
   - Select **"Write"**
   - Copy new token

3. **Use credential helper**:
   ```powershell
   git remote set-url huggingface https://huggingface.co/spaces/Waleed765/cv-job-matcher
   git config --global credential.helper wincred
   git push huggingface main
   # Username: Waleed765
   # Password: [paste your NEW token with Write permissions]
   ```

