"""
Report Generator - Generates PDF and CSV reports
"""

from typing import Dict, Any
import io
import csv

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class ReportGenerator:
    """Generate downloadable reports in PDF and CSV formats"""
    
    def __init__(self):
        self.reportlab_available = REPORTLAB_AVAILABLE
    
    def generate_pdf(self, match_result: Dict[str, Any]) -> bytes:
        """
        Generate PDF report
        
        Args:
            match_result: Match analysis result dictionary
            
        Returns:
            PDF file as bytes
        """
        if not self.reportlab_available:
            raise ImportError(
                "reportlab is required for PDF generation. "
                "Install it with: pip install reportlab"
            )
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30
        )
        story.append(Paragraph("CV-to-Job Match Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Match Score
        score_style = ParagraphStyle(
            'ScoreStyle',
            parent=styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#2ca02c')
        )
        story.append(Paragraph(f"Match Score: {match_result['match_score']:.1f}%", score_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Score Breakdown
        story.append(Paragraph("Score Breakdown", styles['Heading2']))
        breakdown_data = [['Component', 'Score (%)']]
        for component, score in match_result['score_breakdown'].items():
            breakdown_data.append([
                component.replace('_', ' ').title(),
                f"{score:.1f}%"
            ])
        
        breakdown_table = Table(breakdown_data)
        breakdown_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(breakdown_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Skills Matched
        story.append(Paragraph("Matched Skills", styles['Heading2']))
        if match_result.get('matched_skills'):
            for skill in match_result['matched_skills']:
                story.append(Paragraph(f"✓ {skill}", styles['Normal']))
        else:
            story.append(Paragraph("No matched skills to display.", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Missing Skills
        if match_result.get('missing_skills'):
            story.append(Paragraph("Skill Gap Analysis", styles['Heading2']))
            story.append(Paragraph(
                f"Found {len(match_result['missing_skills'])} missing or weakly-matched skills",
                styles['Normal']
            ))
            story.append(Spacer(1, 0.1*inch))
            
            for idx, skill_info in enumerate(match_result['missing_skills'], 1):
                story.append(Paragraph(
                    f"#{idx}: {skill_info['skill']}",
                    styles['Heading3']
                ))
                story.append(Paragraph(f"Priority: {skill_info['priority']}", styles['Normal']))
                story.append(Paragraph(f"Reason: {skill_info['reason']}", styles['Normal']))
                if skill_info.get('suggestions'):
                    story.append(Paragraph("Suggestions:", styles['Normal']))
                    for suggestion in skill_info['suggestions']:
                        story.append(Paragraph(f"  • {suggestion}", styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_csv(self, match_result: Dict[str, Any]) -> str:
        """
        Generate CSV report
        
        Args:
            match_result: Match analysis result dictionary
            
        Returns:
            CSV content as string
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['CV-to-Job Match Report'])
        writer.writerow([])
        
        # Match Score
        writer.writerow(['Match Score', f"{match_result['match_score']:.1f}%"])
        writer.writerow(['Skills Matched', f"{match_result['skills_matched']}/{match_result['total_required_skills']}"])
        writer.writerow([])
        
        # Score Breakdown
        writer.writerow(['Score Breakdown'])
        writer.writerow(['Component', 'Score (%)'])
        for component, score in match_result['score_breakdown'].items():
            writer.writerow([
                component.replace('_', ' ').title(),
                f"{score:.1f}%"
            ])
        writer.writerow([])
        
        # Matched Skills
        writer.writerow(['Matched Skills'])
        if match_result.get('matched_skills'):
            for skill in match_result['matched_skills']:
                writer.writerow([skill])
        else:
            writer.writerow(['No matched skills'])
        writer.writerow([])
        
        # Missing Skills
        if match_result.get('missing_skills'):
            writer.writerow(['Missing Skills'])
            writer.writerow(['Skill', 'Priority', 'Reason', 'Suggestions'])
            for skill_info in match_result['missing_skills']:
                suggestions = '; '.join(skill_info.get('suggestions', []))
                writer.writerow([
                    skill_info['skill'],
                    skill_info['priority'],
                    skill_info['reason'],
                    suggestions
                ])
        
        return output.getvalue()

