---
title: CV-to-Job-Description Matcher
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.52.1"
app_file: app.py
pinned: false
license: mit
---

# CV-to-Job-Description Matcher

AI-powered match scoring & skill-gap reporting system that helps job applicants understand how well their CV matches job descriptions.

## Features

- 📄 **Document Upload**: Support for PDF, DOCX, and TXT files
- 🔍 **AI-Powered Matching**: Computes match scores using multiple algorithms
- 🎯 **Skill Gap Analysis**: Identifies missing skills with recommendations
- 📊 **Detailed Reports**: Downloadable PDF and CSV reports
- 🔍 **Explainability**: See which parts of your CV contributed to the score
- 🔒 **Privacy-Focused**: Delete your data at any time

## Project Structure

```
.
├── app.py                 # Main Streamlit application
├── src/
│   ├── __init__.py
│   ├── document_parser.py    # PDF/DOCX/TXT parsing
│   ├── skill_extractor.py     # Skill extraction from text
│   ├── matcher.py             # Match scoring algorithms
│   ├── gemini_client.py      # Gemini AI integration
│   ├── report_generator.py     # PDF/CSV report generation
│   └── utils.py                # Utility functions
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment configuration
└── README.md             # This file
```

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd SE-Project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## Deployment

### Option 1: Hugging Face Spaces (Recommended)

**Quick Deploy:**
1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Select **Streamlit** as SDK
4. Connect your GitHub repository or push code directly
5. Add `GOOGLE_AI_API_KEY` in Space settings (optional, for AI features)
6. Your app will be live in 2-5 minutes!

**Detailed Instructions:** See [DEPLOYMENT_HF.md](DEPLOYMENT_HF.md)

### Option 2: Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Add environment variable: `GOOGLE_AI_API_KEY` (optional)
6. Deploy!

**Detailed Instructions:** See [DEPLOYMENT.md](DEPLOYMENT.md)

## Usage

1. **Upload Documents**:
   - Upload your CV (PDF, DOCX, or TXT)
   - Upload the Job Description (PDF, DOCX, or TXT)
   - Or paste text directly

2. **Analyze**:
   - Click "Analyze Match" button
   - Wait for processing (usually 5-15 seconds)

3. **View Results**:
   - See your match score percentage
   - Review skill gap analysis
   - Check explainability details

4. **Download Reports**:
   - Download PDF or CSV reports
   - Share with career advisors or mentors

## System Requirements

Based on the SRS document, the system implements:

### Functional Requirements
- ✅ Document parsing (PDF, DOCX, TXT)
- ✅ Skill extraction from CV and JD
- ✅ Match score computation
- ✅ Skill gap analysis
- ✅ Report generation (PDF/CSV)
- ✅ Explainability features
- ✅ Privacy controls

### Non-Functional Requirements
- ✅ Web-based interface (Streamlit)
- ✅ Fast processing (< 30 seconds)
- ✅ User-friendly UI
- ✅ Privacy-focused design

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/ML**: Google Gemini 2.0 Flash (primary), Gemini 1.5 Flash (fallback)
- **Document Processing**: PyPDF2, python-docx
- **Report Generation**: reportlab
- **Deployment**: Render

## AI Integration

This application uses **Google Gemini AI** for enhanced matching:

- **Primary Model**: Gemini 2.0 Flash (experimental) - Fast and efficient
- **Fallback Model**: Gemini 1.5 Flash - Reliable backup

### Setting Up Gemini API Key

1. Get your API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Set it as environment variable: `GOOGLE_AI_API_KEY`
3. Or enter it in the app sidebar

See [GEMINI_SETUP.md](GEMINI_SETUP.md) for detailed instructions.

**Note**: The app works without an API key using rule-based matching, but AI provides much better results.

## Limitations & Future Enhancements

Current implementation is a prototype/demo version. Future enhancements could include:

- Advanced NLP models (BERT, GPT embeddings)
- Integration with job portals
- User accounts and history
- Advanced skill taxonomy
- Multi-language support
- Real-time collaboration features

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is created for educational purposes based on the Software Requirements Specification document.

## Support

For issues or questions, please open an issue on the GitHub repository.

## Acknowledgments

- Based on Software Requirements Specification (SRS) document
- Inspired by Software Engineering best practices (Ian Sommerville, 10th ed.)

