---
title: CV-to-Job-Description Matcher
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.52.1
app_file: app.py
pinned: false
license: mit
---

# CV-to-Job-Description Matcher

AI-powered match scoring & skill-gap reporting system that helps job applicants understand how well their CV matches job descriptions.

## Features

- 📄 **Document Upload**: Support for PDF, DOCX, and TXT files
- 🤖 **AI-Powered Matching**: Uses Google Gemini 2.0 Flash for intelligent matching
- 🎯 **Skill Gap Analysis**: Identifies missing skills with AI-generated recommendations
- 📊 **Detailed Reports**: Downloadable PDF and CSV reports
- 🔍 **Explainability**: See which parts of your CV contributed to the score
- 🔒 **Privacy-Focused**: Delete your data at any time

## How to Use

1. **Upload Documents**: Upload your CV and Job Description (PDF, DOCX, or TXT)
2. **Set API Key** (Optional): Enter your Google AI API key in the sidebar for AI features
   - Get your key from: https://aistudio.google.com/apikey
   - Without API key, the app uses rule-based matching (still functional!)
3. **Analyze**: Click "Analyze Match" to get your match score
4. **View Results**: See detailed analysis, skill gaps, and recommendations
5. **Download Reports**: Export PDF or CSV reports

## AI Integration

This app uses **Google Gemini AI** for enhanced matching:
- **Primary**: Gemini 2.0 Flash (experimental)
- **Fallback**: Gemini 1.5 Flash

The app automatically falls back to rule-based matching if AI is unavailable.

## Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: Google Gemini 2.0 Flash / 1.5 Flash
- **Document Processing**: PyPDF2, python-docx
- **Report Generation**: reportlab

## Setup

### For Users
Just use the app! No setup required. API key is optional for enhanced AI features.

### For Developers
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Privacy

- Your data is processed securely
- No data is stored permanently
- You can delete session data at any time
- API keys are stored only in your session

## License

MIT License - Free to use and modify

## Support

For issues or questions, open an issue in the repository.

