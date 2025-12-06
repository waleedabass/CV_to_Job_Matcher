"""
CV-to-Job-Description Matcher - Main Streamlit Application
AI-powered match scoring & skill-gap reporting
"""

import streamlit as st
import os
from datetime import datetime
import json

from src.document_parser import DocumentParser
from src.skill_extractor import SkillExtractor
from src.matcher import CVJobMatcher
from src.report_generator import ReportGenerator
from src.utils import save_uploaded_file, cleanup_temp_files

# Page configuration
st.set_page_config(
    page_title="CV-to-Job Matcher",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'cv_text' not in st.session_state:
    st.session_state.cv_text = None
if 'jd_text' not in st.session_state:
    st.session_state.jd_text = None
if 'match_result' not in st.session_state:
    st.session_state.match_result = None
if 'analysis_id' not in st.session_state:
    st.session_state.analysis_id = None

def main():
    """Main application entry point"""
    
    # Header
    st.title("CV-to-Job-Description Matcher")
    st.markdown("**AI-powered match scoring & skill-gap reporting**")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select Page",
            ["Upload & Analyze", "View Results", "Privacy & Settings"]
        )
        
        st.markdown("---")
        st.header("AI Settings")
        api_key_input = st.text_input(
            "Gemini API Key (optional)",
            type="password",
            value=st.session_state.get('gemini_api_key', ''),
            help="Enter your Google AI API key to enable AI-powered matching. Get one at https://aistudio.google.com/apikey"
        )
        if api_key_input:
            st.session_state.gemini_api_key = api_key_input
            st.success("API key saved!")
        elif st.session_state.get('gemini_api_key'):
            if st.button("Clear API Key"):
                st.session_state.gemini_api_key = None
                st.rerun()
        
        # Check if API key is available
        has_api_key = bool(st.session_state.get('gemini_api_key') or os.getenv('GOOGLE_AI_API_KEY'))
        if has_api_key:
            st.info("✓ AI-powered matching enabled")
        else:
            st.warning("⚠ Using rule-based matching (add API key for AI)")
        
        st.markdown("---")
        st.header("About")
        st.markdown("""
        This tool helps you:
        - Match your CV with job descriptions
        - Identify skill gaps
        - Get personalized recommendations
        - Understand match scores
        """)
        
        st.markdown("---")
        st.header("Privacy")
        st.markdown("""
        Your data is processed securely.
        You can delete your data at any time.
        """)
    
    # Route to appropriate page
    if page == "Upload & Analyze":
        upload_and_analyze_page()
    elif page == "View Results":
        view_results_page()
    elif page == "Privacy & Settings":
        privacy_settings_page()

def upload_and_analyze_page():
    """Page for uploading CV and JD, then analyzing"""
    
    st.header("Upload Documents")
    
    # Privacy notice
    consent = True  # Default to True
    with st.expander("⚠️ Privacy Notice", expanded=False):
        st.markdown("""
        **Data Usage:**
        - Your documents are processed to generate match scores
        - Data may be temporarily stored for analysis
        - You can request deletion at any time
        
        **Consent:**
        By uploading documents, you consent to the processing of your data
        for the purpose of generating match analysis.
        """)
        consent = st.checkbox("I have read and consent to the privacy notice", value=True)
    
    if not consent:
        st.warning("Please read and consent to the privacy notice to continue.")
        return
    
    col1, col2 = st.columns(2)
    
    # CV Upload
    with col1:
        st.subheader("Upload Your CV")
        cv_option = st.radio(
            "Choose input method:",
            ["Upload File", "Paste Text"],
            key="cv_option"
        )
        
        if cv_option == "Upload File":
            cv_file = st.file_uploader(
                "Upload CV (PDF, DOCX, or TXT)",
                type=['pdf', 'docx', 'txt'],
                key="cv_upload"
            )
            if cv_file:
                try:
                    parser = DocumentParser()
                    cv_text = parser.parse_file(cv_file)
                    st.session_state.cv_text = cv_text
                    st.success(f"CV parsed successfully! ({len(cv_text)} characters)")
                    with st.expander("Preview CV Text"):
                        st.text(cv_text[:500] + "..." if len(cv_text) > 500 else cv_text)
                except Exception as e:
                    st.error(f"Error parsing CV: {str(e)}")
        else:
            cv_text_input = st.text_area(
                "Paste your CV text here:",
                height=200,
                key="cv_text_input"
            )
            if cv_text_input:
                st.session_state.cv_text = cv_text_input
                st.success("CV text captured!")
    
    # Job Description Upload
    with col2:
        st.subheader("💼 Upload Job Description")
        jd_option = st.radio(
            "Choose input method:",
            ["Upload File", "Paste Text"],
            key="jd_option"
        )
        
        if jd_option == "Upload File":
            jd_file = st.file_uploader(
                "Upload Job Description (PDF, DOCX, or TXT)",
                type=['pdf', 'docx', 'txt'],
                key="jd_upload"
            )
            if jd_file:
                try:
                    parser = DocumentParser()
                    jd_text = parser.parse_file(jd_file)
                    st.session_state.jd_text = jd_text
                    st.success(f"JD parsed successfully! ({len(jd_text)} characters)")
                    with st.expander("Preview JD Text"):
                        st.text(jd_text[:500] + "..." if len(jd_text) > 500 else jd_text)
                except Exception as e:
                    st.error(f"Error parsing JD: {str(e)}")
        else:
            jd_text_input = st.text_area(
                "Paste job description text here:",
                height=200,
                key="jd_text_input"
            )
            if jd_text_input:
                st.session_state.jd_text = jd_text_input
                st.success("JD text captured!")
    
    # Analyze button
    st.markdown("---")
    
    if st.button("Analyze Match", type="primary", use_container_width=True):
        if not st.session_state.cv_text or not st.session_state.jd_text:
            st.error("Please upload or paste both CV and Job Description before analyzing.")
            return
        
        with st.spinner("Analyzing match... This may take a few seconds."):
            try:
                # Initialize components
                skill_extractor = SkillExtractor()
                
                # Get API key from session state or environment
                api_key = st.session_state.get('gemini_api_key') or os.getenv('GOOGLE_AI_API_KEY')
                matcher = CVJobMatcher(use_ai=True, api_key=api_key)
                
                # Extract skills
                cv_skills = skill_extractor.extract_skills(st.session_state.cv_text)
                jd_skills = skill_extractor.extract_skills(st.session_state.jd_text)
                
                # Compute match
                match_result = matcher.compute_match(
                    cv_text=st.session_state.cv_text,
                    jd_text=st.session_state.jd_text,
                    cv_skills=cv_skills,
                    jd_skills=jd_skills
                )
                
                # Store result
                st.session_state.match_result = match_result
                st.session_state.analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                st.success("Analysis complete! Navigate to 'View Results' to see details.")
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.exception(e)

def view_results_page():
    """Page for viewing match results"""
    
    st.header("Match Results")
    
    if not st.session_state.match_result:
        st.info("No analysis results available. Please upload documents and run analysis first.")
        return
    
    result = st.session_state.match_result
    
    # Match Score
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Match Score", f"{result['match_score']:.1f}%")
    with col2:
        st.metric("Skills Matched", f"{result['skills_matched']}/{result['total_required_skills']}")
    with col3:
        st.metric("Missing Skills", len(result['missing_skills']))
    
    st.markdown("---")
    
    # Score Breakdown
    st.subheader("Score Breakdown")
    breakdown_cols = st.columns(len(result['score_breakdown']))
    for idx, (component, score) in enumerate(result['score_breakdown'].items()):
        with breakdown_cols[idx]:
            st.metric(component.replace('_', ' ').title(), f"{score:.1f}%")
    
    st.markdown("---")
    
    # Skill Gap Report
    st.subheader("Skill Gap Analysis")
    
    if result['missing_skills']:
        st.warning(f"Found {len(result['missing_skills'])} missing or weakly-matched skills")
        
        for idx, skill_info in enumerate(result['missing_skills'], 1):
            with st.expander(f"#{idx}: {skill_info['skill']}"):
                st.write(f"**Priority:** {skill_info['priority']}")
                st.write(f"**Reason:** {skill_info['reason']}")
                if skill_info.get('suggestions'):
                    st.write("**Suggestions:**")
                    for suggestion in skill_info['suggestions']:
                        st.write(f"- {suggestion}")
    else:
        st.success("Great! No major skill gaps detected.")
    
    st.markdown("---")
    
    # Matched Skills
    st.subheader("Matched Skills")
    if result.get('matched_skills'):
        matched_cols = st.columns(min(3, len(result['matched_skills'])))
        for idx, skill in enumerate(result['matched_skills']):
            with matched_cols[idx % 3]:
                st.success(f"✓ {skill}")
    else:
        st.info("No matched skills to display.")
    
    st.markdown("---")
    
    # Explainability
    st.subheader("Explainability & Evidence")
    with st.expander("View detailed evidence"):
        st.write("**CV Sections Contributing to Score:**")
        for section, contribution in result.get('cv_contributions', {}).items():
            st.write(f"- **{section}**: {contribution:.1f}% contribution")
        
        st.write("**JD Requirements Matched:**")
        for req, matched in result.get('jd_matches', {}).items():
            status = "✓" if matched else "✗"
            st.write(f"{status} {req}")
    
    st.markdown("---")
    
    # Download Report
    st.subheader("Download Report")
    report_gen = ReportGenerator()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Download PDF Report", use_container_width=True):
            try:
                pdf_bytes = report_gen.generate_pdf(result)
                st.download_button(
                    label="Click to Download PDF",
                    data=pdf_bytes,
                    file_name=f"match_report_{st.session_state.analysis_id}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
    
    with col2:
        if st.button("Download CSV Report", use_container_width=True):
            try:
                csv_data = report_gen.generate_csv(result)
                st.download_button(
                    label="Click to Download CSV",
                    data=csv_data,
                    file_name=f"match_report_{st.session_state.analysis_id}.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error generating CSV: {str(e)}")
    
    st.markdown("---")
    
    # Feedback
    st.subheader("Feedback")
    feedback_cols = st.columns(3)
    with feedback_cols[0]:
        if st.button("Accurate", use_container_width=True):
            st.success("Thank you for your feedback!")
    with feedback_cols[1]:
        if st.button("Inaccurate", use_container_width=True):
            feedback_text = st.text_input("Please provide details:", key="feedback_input")
            if feedback_text:
                st.success("Thank you for your detailed feedback!")
    with feedback_cols[2]:
        if st.button("Add Comment", use_container_width=True):
            comment = st.text_area("Your comment:", key="comment_input")
            if comment:
                st.success("Comment recorded!")

def privacy_settings_page():
    """Page for privacy settings and data deletion"""
    
    st.header("Privacy & Settings")
    
    st.subheader("Data Management")
    st.info("You can manage your uploaded data and analysis results here.")
    
    if st.button("Delete All Session Data", type="secondary"):
        st.session_state.cv_text = None
        st.session_state.jd_text = None
        st.session_state.match_result = None
        st.session_state.analysis_id = None
        cleanup_temp_files()
        st.success("All session data has been deleted.")
    
    st.markdown("---")
    
    st.subheader("Privacy Information")
    st.markdown("""
    **What data do we collect?**
    - CV and Job Description text you upload
    - Analysis results and match scores
    - Optional feedback you provide
    
    **How is data used?**
    - To generate match scores and skill gap reports
    - To improve our matching algorithms (with your consent)
    - For system debugging and improvement
    
    **Data Storage:**
    - Data is stored temporarily during your session
    - You can delete data at any time
    - No data is shared with third parties
    
    **Your Rights:**
    - Right to access your data
    - Right to delete your data
    - Right to withdraw consent
    """)
    
    st.markdown("---")
    
    st.subheader("Terms of Service")
    st.markdown("""
    By using this service, you agree to:
    - Use the service for legitimate job matching purposes
    - Not upload malicious or inappropriate content
    - Understand that match scores are AI-generated estimates
    - Acknowledge that results are for informational purposes only
    """)

if __name__ == "__main__":
    main()

