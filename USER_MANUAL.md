# CV-to-Job-Description Matcher
## User Manual

**Version 1.0**  
**Date: December 2025**

---

## Table of Contents

1. [Introduction](#introduction)
2. [System Overview](#system-overview)
3. [Getting Started](#getting-started)
4. [Features and Functionality](#features-and-functionality)
5. [Step-by-Step Guide](#step-by-step-guide)
6. [AI Integration](#ai-integration)
7. [Report Generation](#report-generation)
8. [Privacy and Data Management](#privacy-and-data-management)
9. [Troubleshooting](#troubleshooting)
10. [Frequently Asked Questions](#frequently-asked-questions)
11. [Technical Specifications](#technical-specifications)
12. [Support and Contact](#support-and-contact)

---

## 1. Introduction

### 1.1 Purpose

The CV-to-Job-Description Matcher is an AI-powered web application designed to help job applicants understand how well their curriculum vitae (CV) or resume matches specific job descriptions. The system provides comprehensive match analysis, skill gap identification, and actionable recommendations to improve job application success rates.

### 1.2 Target Audience

This application is designed for:
- Job seekers evaluating their fit for specific positions
- Career counselors assisting clients with job applications
- Recruitment professionals analyzing candidate qualifications
- Students preparing for job applications
- Professionals seeking career transitions

### 1.3 Key Benefits

- **Objective Analysis**: Receive unbiased, data-driven match scores
- **Skill Gap Identification**: Understand exactly what skills are missing
- **Actionable Recommendations**: Get specific suggestions for improvement
- **Time Efficiency**: Quick analysis in under 30 seconds
- **Privacy-Focused**: Full control over your data

---

## 2. System Overview

### 2.1 What the System Does

The CV-to-Job-Description Matcher performs the following functions:

1. **Document Processing**: Accepts CV and job description documents in multiple formats
2. **Text Extraction**: Extracts and parses text from uploaded documents
3. **Skill Extraction**: Identifies technical skills, qualifications, and experience
4. **Match Analysis**: Computes comprehensive match scores using AI and rule-based algorithms
5. **Gap Analysis**: Identifies missing or weakly-matched skills
6. **Report Generation**: Creates downloadable PDF and CSV reports

### 2.2 System Architecture

The application consists of three main components:

- **Document Parser**: Handles PDF, DOCX, and TXT file processing
- **Matching Engine**: Combines AI-powered semantic analysis with rule-based matching
- **Report Generator**: Creates formatted reports for download

### 2.3 Supported File Formats

**Input Formats:**
- PDF (Portable Document Format)
- DOCX (Microsoft Word)
- TXT (Plain Text)

**Output Formats:**
- PDF Reports
- CSV Data Files

---

## 3. Getting Started

### 3.1 Accessing the Application

The application is available as a web-based service. Access it through:
- Hugging Face Spaces deployment
- Render cloud deployment
- Local installation (for developers)

### 3.2 System Requirements

**For End Users:**
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- JavaScript enabled

**For Local Installation:**
- Python 3.8 or higher
- 2 GB RAM minimum
- 500 MB disk space

### 3.3 First-Time Setup

1. Navigate to the application URL
2. Review the privacy notice
3. (Optional) Configure AI settings if you have a Google AI API key
4. Begin using the application

---

## 4. Features and Functionality

### 4.1 Core Features

**Document Upload**
- Support for multiple file formats
- Text paste option for quick testing
- File validation and error handling
- Document preview functionality

**Match Analysis**
- Composite match score (0-100%)
- Score breakdown by component
- Skills matched count
- Missing skills identification

**Skill Gap Analysis**
- Ranked list of missing skills
- Priority classification (High/Medium/Low)
- Detailed explanations for each gap
- Learning recommendations

**Explainability**
- Score component breakdown
- CV section contributions
- Job requirement matching status
- Evidence-based insights

**Report Generation**
- Professional PDF reports
- CSV data export
- Customizable report content
- Download functionality

**Privacy Controls**
- Session data management
- Data deletion capability
- Privacy notice compliance
- Secure data handling

### 4.2 Advanced Features

**AI-Powered Matching** (Optional)
- Google Gemini 2.0 Flash integration
- Enhanced semantic understanding
- Intelligent skill gap recommendations
- Context-aware analysis

**Feedback System**
- Accuracy feedback collection
- Comment submission
- Model improvement contribution

---

## 5. Step-by-Step Guide

### 5.1 Uploading Documents

**Step 1: Navigate to Upload Page**
- Click on "Upload & Analyze" in the navigation sidebar
- Review the privacy notice and provide consent if required

**Step 2: Upload Your CV**
- Choose between "Upload File" or "Paste Text"
- If uploading:
  - Click "Upload CV" button
  - Select your CV file (PDF, DOCX, or TXT)
  - Wait for parsing confirmation
- If pasting:
  - Copy your CV text
  - Paste into the text area
  - Click outside the box to save

**Step 3: Upload Job Description**
- Follow the same process as Step 2
- Upload or paste the job description text
- Verify both documents are loaded successfully

**Step 4: Review Preview**
- Expand the preview sections to verify text extraction
- Ensure all important information is captured
- Make corrections if needed

### 5.2 Running Analysis

**Step 1: Initiate Analysis**
- Click the "Analyze Match" button
- Wait for processing (typically 5-15 seconds)
- Processing indicator will show progress

**Step 2: Review Results**
- Navigate to "View Results" page
- Examine the match score and breakdown
- Review skill gap analysis

**Step 3: Interpret Results**
- Match Score: Overall fit percentage
- Skills Matched: Number of required skills found
- Missing Skills: Areas needing improvement
- Score Breakdown: Component-wise analysis

### 5.3 Understanding Match Scores

**Composite Score Components:**

1. **Skill Overlap (35%)**
   - Direct skill matches
   - Partial skill matches
   - Skill taxonomy alignment

2. **Semantic Similarity (40%)**
   - AI-powered text understanding
   - Contextual relevance
   - Keyword-based fallback

3. **Experience Match (15%)**
   - Years of experience comparison
   - Experience level alignment
   - Relevant experience identification

4. **Education Match (10%)**
   - Degree level matching
   - Qualification alignment
   - Certification recognition

**Score Interpretation:**
- 80-100%: Excellent match, strong candidate
- 60-79%: Good match, competitive candidate
- 40-59%: Moderate match, some gaps to address
- 0-39%: Weak match, significant improvements needed

### 5.4 Analyzing Skill Gaps

**Understanding Skill Gap Reports:**

Each missing skill includes:
- **Skill Name**: The required skill not found
- **Priority**: High, Medium, or Low importance
- **Reason**: Explanation of why it's needed
- **Suggestions**: Actionable recommendations

**Priority Levels:**
- **High**: Critical skill, likely required for role
- **Medium**: Important skill, enhances candidacy
- **Low**: Nice-to-have skill, optional enhancement

**Action Items:**
1. Review high-priority gaps first
2. Assess feasibility of acquiring skills
3. Consider alternative ways to demonstrate competency
4. Plan skill development timeline

### 5.5 Downloading Reports

**PDF Report:**
1. Navigate to "View Results" page
2. Scroll to "Download Report" section
3. Click "Download PDF Report"
4. Click the download button when it appears
5. Save the file to your desired location

**CSV Report:**
1. Follow steps 1-2 above
2. Click "Download CSV Report"
3. Click the download button
4. Open in Excel or similar spreadsheet application

**Report Contents:**
- Match score and breakdown
- Matched skills list
- Missing skills with details
- Recommendations
- Analysis metadata

---

## 6. AI Integration

### 6.1 Enabling AI Features

**Option 1: Environment Variable**
- Set GOOGLE_AI_API_KEY environment variable
- Application automatically detects and uses AI

**Option 2: Application Interface**
- Navigate to sidebar
- Enter API key in "Gemini API Key" field
- Key is saved for current session

### 6.2 Obtaining API Key

1. Visit Google AI Studio: https://aistudio.google.com/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the generated key
5. Store securely

### 6.3 AI vs Rule-Based Matching

**AI-Powered Mode:**
- Enhanced semantic understanding
- Context-aware skill matching
- Intelligent recommendations
- Better handling of synonyms and variations

**Rule-Based Mode:**
- Keyword matching
- Pattern recognition
- Heuristic scoring
- No API key required

**Automatic Fallback:**
- System automatically uses rule-based matching if AI unavailable
- Seamless transition between modes
- No user intervention required

### 6.4 AI Model Information

**Primary Model:** Gemini 2.0 Flash (Experimental)
- Latest Google AI model
- Fast processing
- High accuracy

**Fallback Model:** Gemini 1.5 Flash
- Stable production model
- Reliable performance
- Proven accuracy

---

## 7. Report Generation

### 7.1 PDF Reports

**Structure:**
- Title and metadata
- Executive summary
- Match score visualization
- Score breakdown table
- Skills analysis
- Recommendations section

**Use Cases:**
- Sharing with career advisors
- Documenting analysis results
- Tracking improvement over time
- Portfolio documentation

### 7.2 CSV Reports

**Structure:**
- Tabular data format
- Comma-separated values
- Importable to spreadsheet applications

**Contents:**
- Match scores
- Skills lists
- Gap analysis data
- Recommendations

**Use Cases:**
- Data analysis
- Comparison tracking
- Bulk processing
- Integration with other tools

---

## 8. Privacy and Data Management

### 8.1 Data Collection

**What is Collected:**
- Uploaded CV and job description text
- Analysis results and scores
- User feedback (optional)
- Session metadata

**What is NOT Collected:**
- Personal identification beyond document content
- Browser history
- Location data
- Third-party tracking

### 8.2 Data Storage

**Session Storage:**
- Data stored temporarily during active session
- Cleared when session ends
- No permanent storage by default

**User Control:**
- Delete session data at any time
- Privacy settings page available
- Explicit consent required

### 8.3 Data Deletion

**Manual Deletion:**
1. Navigate to "Privacy & Settings" page
2. Click "Delete All Session Data"
3. Confirm deletion
4. All session data removed immediately

**Automatic Deletion:**
- Session data cleared on browser close
- Temporary files removed after processing
- No persistent storage

### 8.4 Privacy Compliance

**Standards:**
- GDPR principles compliance
- Data minimization
- User consent required
- Right to deletion

**Security:**
- HTTPS encryption
- Secure data transmission
- No data sharing with third parties
- API key protection

---

## 9. Troubleshooting

### 9.1 Common Issues

**Issue: File Upload Fails**

**Symptoms:**
- Error message on upload
- File not processing
- Parser errors

**Solutions:**
1. Verify file format (PDF, DOCX, TXT only)
2. Check file size (recommended under 10MB)
3. Ensure file is not corrupted
4. Try converting to different format
5. Use text paste option as alternative

**Issue: Low Match Scores**

**Symptoms:**
- Unexpectedly low scores
- Missing obvious skills
- Incorrect gap identification

**Solutions:**
1. Verify CV text extraction is complete
2. Check skill section formatting
3. Ensure skills are clearly listed
4. Try enabling AI mode for better analysis
5. Review skill taxonomy alignment

**Issue: Analysis Takes Too Long**

**Symptoms:**
- Processing exceeds 30 seconds
- Timeout errors
- Application unresponsive

**Solutions:**
1. Check internet connection
2. Reduce document size
3. Try text paste instead of file upload
4. Verify API key if using AI mode
5. Refresh page and retry

**Issue: Reports Not Downloading**

**Symptoms:**
- Download button not working
- File not saving
- Error messages

**Solutions:**
1. Check browser download settings
2. Verify pop-up blocker is disabled
3. Check available disk space
4. Try different browser
5. Use CSV format as alternative

### 9.2 Error Messages

**"File format not supported"**
- Solution: Convert to PDF, DOCX, or TXT format

**"Text extraction failed"**
- Solution: Ensure file is not password-protected or corrupted

**"API key invalid"**
- Solution: Verify key is correct and has proper permissions

**"Analysis timeout"**
- Solution: Reduce document size or try again later

**"Session expired"**
- Solution: Refresh page and re-upload documents

### 9.3 Performance Optimization

**Best Practices:**
- Keep CV under 5 pages
- Use standard resume formats
- Clearly label skill sections
- Avoid complex formatting
- Use text paste for quick tests

---

## 10. Frequently Asked Questions

### 10.1 General Questions

**Q: Is the application free to use?**
A: Yes, the basic application is free. AI features require a Google AI API key, which has its own pricing structure.

**Q: How accurate are the match scores?**
A: Scores are based on algorithmic analysis and should be used as guidance. Actual hiring decisions involve many factors beyond what can be analyzed automatically.

**Q: Can I use this for multiple job applications?**
A: Yes, you can analyze your CV against multiple job descriptions. Each analysis is independent.

**Q: How long does analysis take?**
A: Typically 5-15 seconds for standard documents. AI-powered analysis may take slightly longer.

**Q: Do I need to create an account?**
A: No account creation is required. The application works with session-based storage.

### 10.2 Technical Questions

**Q: What file formats are supported?**
A: PDF, DOCX (Microsoft Word), and TXT (plain text) formats are supported.

**Q: Is my data secure?**
A: Yes, data is processed securely with HTTPS encryption. No data is permanently stored without your consent.

**Q: Can I use the application offline?**
A: No, the application requires an internet connection as it is a web-based service.

**Q: What browsers are supported?**
A: Modern browsers including Chrome, Firefox, Safari, and Edge are supported.

**Q: How do I enable AI features?**
A: Obtain a Google AI API key and enter it in the application sidebar or set it as an environment variable.

### 10.3 Results Interpretation

**Q: What does a 75% match score mean?**
A: A 75% score indicates a good match with most requirements met. Some skill gaps may exist but the candidate is competitive.

**Q: How should I prioritize skill gaps?**
A: Focus on high-priority gaps first, as these are likely critical for the role. Medium and low-priority gaps can be addressed over time.

**Q: Can I dispute the analysis results?**
A: The system provides feedback options. You can submit feedback if you believe results are inaccurate.

**Q: How often should I re-analyze?**
A: Re-analyze when you update your CV, acquire new skills, or apply for different types of positions.

---

## 11. Technical Specifications

### 11.1 System Architecture

**Frontend:**
- Streamlit web framework
- Responsive design
- Client-side processing

**Backend:**
- Python 3.8+
- Document parsing libraries
- AI integration (optional)
- Report generation

**AI Integration:**
- Google Gemini 2.0 Flash (primary)
- Google Gemini 1.5 Flash (fallback)
- Automatic fallback mechanisms

### 11.2 Performance Metrics

**Processing Times:**
- Small documents (<2 pages): <12 seconds
- Medium documents (2-5 pages): 12-20 seconds
- Large documents (5-10 pages): 20-30 seconds

**Accuracy Metrics:**
- Skill extraction: ~90% accuracy
- Match scoring: Validated against human assessments
- Gap identification: Context-aware recommendations

### 11.3 Limitations

**Current Limitations:**
- English language only
- Standard resume formats work best
- Limited to text-based analysis
- No image or graphic processing
- No real-time collaboration

**Future Enhancements:**
- Multi-language support
- Advanced formatting recognition
- Image-based document processing
- Collaborative features
- Integration with job portals

---

## 12. Support and Contact

### 12.1 Getting Help

**Documentation:**
- User Manual (this document)
- Deployment guides
- Technical documentation
- FAQ section

**Community Support:**
- GitHub repository issues
- Community forums
- Discussion boards

**Direct Support:**
- Email support (if available)
- Issue tracking system
- Feature requests

### 12.2 Reporting Issues

**When Reporting Issues:**
1. Describe the problem clearly
2. Include steps to reproduce
3. Provide error messages
4. Specify browser and version
5. Include document types used

**Information to Include:**
- Application version
- Browser type and version
- Operating system
- Error messages
- Screenshots (if applicable)

### 12.3 Feature Requests

**How to Request Features:**
- Submit through issue tracker
- Provide use case description
- Explain expected benefits
- Suggest implementation approach

### 12.4 Version Information

**Current Version:** 1.0  
**Release Date:** December 2025  
**Last Updated:** December 2025

---

## Appendix A: Glossary

**CV (Curriculum Vitae):** A detailed document outlining a person's educational and professional history.

**Job Description (JD):** A document describing the duties, responsibilities, and requirements of a job position.

**Match Score:** A numerical percentage indicating how well a CV matches a job description.

**Skill Gap:** A required skill or qualification that is missing or insufficiently demonstrated in a CV.

**Semantic Similarity:** A measure of how similar two texts are in meaning, beyond simple keyword matching.

**Embedding:** A numerical representation of text used for semantic analysis.

**API Key:** A unique identifier used to authenticate and access external services.

**Session:** A period of interaction with the application, typically from page load to browser close.

---

## Appendix B: Keyboard Shortcuts

**Navigation:**
- Tab: Move between form fields
- Enter: Submit forms
- Escape: Close modals
- Arrow Keys: Navigate options

**Browser Shortcuts:**
- Ctrl/Cmd + R: Refresh page
- Ctrl/Cmd + S: Save page (for reports)
- Ctrl/Cmd + P: Print page

---

## Document Information

**Title:** CV-to-Job-Description Matcher User Manual  
**Version:** 1.0  
**Date:** December 2025  
**Author:** Development Team  
**Status:** Current  
**Classification:** Public Documentation

---

**End of User Manual**

