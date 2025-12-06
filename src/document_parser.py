"""
Document Parser - Handles parsing of PDF, DOCX, and TXT files
"""

import io
import tempfile
import os
from typing import Optional

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


class DocumentParser:
    """Parser for various document formats"""
    
    def __init__(self):
        self.supported_formats = ['pdf', 'docx', 'txt']
    
    def parse_file(self, file) -> str:
        """
        Parse uploaded file and extract text
        
        Args:
            file: Streamlit uploaded file object
            
        Returns:
            Extracted text as string
        """
        file_extension = file.name.split('.')[-1].lower()
        
        if file_extension == 'txt':
            return self._parse_txt(file)
        elif file_extension == 'pdf':
            return self._parse_pdf(file)
        elif file_extension == 'docx':
            return self._parse_docx(file)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _parse_txt(self, file) -> str:
        """Parse plain text file"""
        file.seek(0)
        text = file.read().decode('utf-8', errors='ignore')
        return text
    
    def _parse_pdf(self, file) -> str:
        """Parse PDF file"""
        if not PDF_AVAILABLE:
            raise ImportError("PyPDF2 is required for PDF parsing. Install it with: pip install PyPDF2")
        
        file.seek(0)
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    
    def _parse_docx(self, file) -> str:
        """Parse DOCX file"""
        if not DOCX_AVAILABLE:
            raise ImportError("python-docx is required for DOCX parsing. Install it with: pip install python-docx")
        
        file.seek(0)
        
        # Save to temporary file for python-docx
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            tmp_file.write(file.read())
            tmp_path = tmp_file.name
        
        try:
            doc = Document(tmp_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def parse_text(self, text: str) -> dict:
        """
        Parse text into structured sections
        
        Args:
            text: Raw text content
            
        Returns:
            Dictionary with parsed sections
        """
        sections = {
            'full_text': text,
            'skills': [],
            'experience': [],
            'education': [],
            'summary': ''
        }
        
        # Simple section detection (can be enhanced with NLP)
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Detect section headers
            if any(keyword in line_lower for keyword in ['skills', 'technical skills', 'competencies']):
                current_section = 'skills'
            elif any(keyword in line_lower for keyword in ['experience', 'work experience', 'employment']):
                current_section = 'experience'
            elif any(keyword in line_lower for keyword in ['education', 'academic', 'qualifications']):
                current_section = 'education'
            elif any(keyword in line_lower for keyword in ['summary', 'objective', 'profile']):
                current_section = 'summary'
            
            # Add content to appropriate section
            if line.strip():
                if current_section == 'skills':
                    sections['skills'].append(line.strip())
                elif current_section == 'experience':
                    sections['experience'].append(line.strip())
                elif current_section == 'education':
                    sections['education'].append(line.strip())
                elif current_section == 'summary':
                    sections['summary'] += line.strip() + " "
        
        sections['summary'] = sections['summary'].strip()
        
        return sections

