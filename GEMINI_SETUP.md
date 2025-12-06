# Gemini AI Setup Guide

This application uses Google's Gemini AI models for enhanced CV-to-Job matching.

## Models Used

- **Primary**: Gemini 2.0 Flash (experimental) - Fast and efficient
- **Fallback**: Gemini 1.5 Flash - Reliable backup option

## Getting Your API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

## Setting Up the API Key

### Option 1: Environment Variable (Recommended for Production)

**Windows (PowerShell):**
```powershell
$env:GOOGLE_AI_API_KEY="your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set GOOGLE_AI_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export GOOGLE_AI_API_KEY="your_api_key_here"
```

### Option 2: In the Application

1. Run the application
2. Go to the sidebar
3. Enter your API key in the "Gemini API Key" field
4. The key will be saved in your session

### Option 3: For Render Deployment

1. Go to your Render dashboard
2. Select your service
3. Go to "Environment" tab
4. Add environment variable:
   - Key: `GOOGLE_AI_API_KEY`
   - Value: Your API key

## Features Enabled with Gemini

- **Semantic Similarity**: AI-powered understanding of CV-JD match
- **Skill Gap Analysis**: Intelligent recommendations for missing skills
- **Enhanced Matching**: Better context understanding than keyword matching

## Without API Key

The application will still work using rule-based matching:
- Keyword-based skill matching
- Simple semantic similarity
- Basic skill gap analysis

## API Costs

- Gemini 2.0 Flash: Free tier available, then pay-per-use
- Gemini 1.5 Flash: Free tier available, then pay-per-use
- Check [Google AI Pricing](https://ai.google.dev/pricing) for current rates

## Troubleshooting

### "API key is required" error
- Make sure you've set the API key in environment variable or in the app
- Verify the key is correct (no extra spaces)

### "Model not available" error
- The app will automatically fall back to Gemini 1.5 Flash
- If both fail, it will use rule-based matching

### Rate limiting
- Free tier has rate limits
- Consider upgrading if you need higher limits

