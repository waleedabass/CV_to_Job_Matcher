"""
Script to generate PDF user manual from markdown
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import re

def read_markdown_file(filename):
    """Read markdown file and return content"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def parse_markdown_to_elements(md_content):
    """Parse markdown content and convert to ReportLab elements"""
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        leftIndent=20,
        bulletIndent=10
    )
    
    elements = []
    lines = md_content.split('\n')
    in_code_block = False
    in_list = False
    
    for line in lines:
        line = line.strip()
        
        # Skip frontmatter
        if line.startswith('---'):
            continue
        if line.startswith('title:') or line.startswith('emoji:') or line.startswith('colorFrom:'):
            continue
        if line.startswith('colorTo:') or line.startswith('sdk:') or line.startswith('sdk_version:'):
            continue
        if line.startswith('app_file:') or line.startswith('pinned:') or line.startswith('license:'):
            continue
        
        # Skip empty lines in certain contexts
        if not line and not in_list:
            elements.append(Spacer(1, 0.1*inch))
            continue
        
        # Headers
        if line.startswith('# '):
            text = line[2:].strip()
            elements.append(Paragraph(text, title_style))
            elements.append(Spacer(1, 0.2*inch))
        elif line.startswith('## '):
            text = line[3:].strip()
            elements.append(PageBreak())
            elements.append(Paragraph(text, heading1_style))
        elif line.startswith('### '):
            text = line[4:].strip()
            elements.append(Paragraph(text, heading2_style))
        elif line.startswith('#### '):
            text = line[5:].strip()
            elements.append(Paragraph(text, heading3_style))
        # Lists
        elif line.startswith('- ') or line.startswith('* '):
            text = line[2:].strip()
            # Remove markdown formatting
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)
            elements.append(Paragraph(f"• {text}", bullet_style))
            in_list = True
        # Numbered lists
        elif re.match(r'^\d+\.\s', line):
            text = re.sub(r'^\d+\.\s', '', line)
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            elements.append(Paragraph(f"• {text}", bullet_style))
            in_list = True
        # Code blocks
        elif line.startswith('```'):
            in_code_block = not in_code_block
        elif in_code_block:
            continue
        # Regular text
        else:
            if line:
                # Clean markdown formatting
                text = line
                text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
                text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
                text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)
                text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Remove links, keep text
                
                elements.append(Paragraph(text, body_style))
                in_list = False
    
    return elements

def create_pdf():
    """Create PDF user manual"""
    # Read markdown file
    try:
        md_content = read_markdown_file('USER_MANUAL.md')
    except FileNotFoundError:
        print("Error: USER_MANUAL.md not found!")
        return
    
    # Create PDF
    pdf_filename = 'CV_Job_Matcher_User_Manual.pdf'
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Parse markdown to elements
    elements = parse_markdown_to_elements(md_content)
    
    # Add title page
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitlePage',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    title_elements = [
        Spacer(1, 2*inch),
        Paragraph("CV-to-Job-Description Matcher", title_style),
        Spacer(1, 0.3*inch),
        Paragraph("User Manual", subtitle_style),
        Spacer(1, 0.5*inch),
        Paragraph("Version 1.0", styles['Normal']),
        Spacer(1, 0.2*inch),
        Paragraph("December 2025", styles['Normal']),
        Spacer(1, 3*inch),
        Paragraph("Professional Documentation", styles['Normal']),
    ]
    
    # Combine title page with content
    all_elements = title_elements + [PageBreak()] + elements
    
    # Build PDF
    doc.build(all_elements)
    print(f"PDF created successfully: {pdf_filename}")

if __name__ == "__main__":
    try:
        create_pdf()
    except Exception as e:
        print(f"Error creating PDF: {e}")
        import traceback
        traceback.print_exc()

