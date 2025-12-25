"""
Report Generator Module for Product #2 (AI Document Intelligence)

This module contains the data models and logic required to generate the
Batch-Optimized, Action-First Executive Summary Report as PDF.

It serves as a direct blueprint for the backend implementation.
"""
import random
from typing import List, Dict, Any, Optional
from datetime import datetime
import io

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# --- 1. Data Models (The "Accolades" / Structured Data) ---

class Issue:
    """Represents a single issue found in a document."""
    def __init__(self, priority: int, issue_type: str, detail: str, recommended_action: str):
        self.priority = priority  # 1 (Critical) to 5 (Low)
        self.issue_type = issue_type
        self.detail = detail
        self.recommended_action = recommended_action

    def to_dict(self) -> Dict[str, Any]:
        """Returns a dictionary representation for template rendering."""
        return {
            'priority': self.priority,
            'issue_type': self.issue_type,
            'detail': self.detail,
            'recommended_action': self.recommended_action,
            'priority_icon': {1: '🔴', 2: '⚠️', 3: '🟡', 4: '🟢', 5: '⚪'}.get(self.priority, '⚪')
        }

class Document:
    """Represents a single document processed by the AI."""
    def __init__(self, doc_id: str, doc_type: str, vendor: str, total_amount: float, risk_score: int, issues: List[Issue]):
        self.doc_id = doc_id
        self.doc_type = doc_type
        self.vendor = vendor
        self.total_amount = total_amount
        self.risk_score = risk_score
        self.issues = issues
        
        # Derived properties
        self.has_action = len(issues) > 0
        self.max_issue_priority = min([issue.priority for issue in issues]) if self.has_action else 5
        self.primary_action = self._get_primary_action()

    def _get_primary_action(self) -> str:
        """Determines the single most critical action required for the batch list."""
        if not self.has_action:
            return "✅ NO ACTION REQUIRED"
        
        # Sort issues by priority (1 is highest)
        sorted_issues = sorted(self.issues, key=lambda x: x.priority)
        
        # Map the highest priority issue to a concise action
        top_issue = sorted_issues[0]
        
        if top_issue.priority == 1:
            return f"🔴 {top_issue.issue_type.upper()}"
        elif top_issue.priority == 2:
            return f"⚠️ {top_issue.issue_type.upper()}"
        elif top_issue.priority == 3:
            return f"🟡 {top_issue.issue_type.upper()}"
        else:
            return "🟡 FILE IN DMS"

    def to_dict(self) -> Dict[str, Any]:
        """Returns a dictionary representation for template rendering."""
        return {
            'doc_id': self.doc_id,
            'doc_type': self.doc_type,
            'vendor': self.vendor,
            'total_amount': f"${self.total_amount:,.2f}",
            'risk_score': self.risk_score,
            'issues': [issue.to_dict() for issue in self.issues],
            'has_action': self.has_action,
            'max_issue_priority': self.max_issue_priority,
            'primary_action': self.primary_action,
            'status': 'Error' if self.max_issue_priority <= 2 else 'Pending' if self.has_action else 'Complete',
            'risk_icon': {
                90: '🔴', 60: '⚠️', 30: '🟡', 0: '🟢'
            }.get(self.risk_score // 30 * 30, '🟢')
        }

# --- 2. Core Logic ---

def generate_mock_documents(count: int) -> List[Document]:
    """
    Generates a list of mock documents with varied issues for demonstration.
    
    :param count: The number of documents to generate.
    :return: A list of Document objects.
    """
    mock_docs = []
    doc_types = ['Invoice', 'Contract', 'Tax Document', 'Purchase Order', 'Medical Record', 'Shipping Document']
    
    for i in range(1, count + 1):
        doc_id = f"DOC-{i:04d}"
        doc_type = random.choice(doc_types)
        try:
            vendor = fake.company()
        except:
            vendor = f"Company {random.randint(1, 100)}"
        total_amount = round(random.uniform(100.0, 50000.0), 2)
        risk_score = random.randint(5, 95)
        
        issues: List[Issue] = []
        
        # Simulate issues based on risk score
        if risk_score > 85: # Critical Error (Priority 1)
            issues.append(Issue(1, "CALCULATION ERROR", "Total amount does not match line item sum.", "STOP PAYMENT & INVESTIGATE"))
            issues.append(Issue(2, "COMPLIANCE FAILURE", "Missing required W-9 form.", "Obtain W-9 immediately."))
        elif risk_score > 60: # High Risk (Priority 2)
            issues.append(Issue(2, "VALIDATION FAILURE", "PO Number not found in ERP system.", "Verify PO existence with Procurement."))
            issues.append(Issue(3, "FINANCIAL RISK", "Amount exceeds requester's spending limit.", "Requires secondary manager approval."))
        elif risk_score > 30: # Medium Risk (Priority 3)
            issues.append(Issue(3, "DATA QUALITY", "Vendor address confidence is low (65%).", "Manually verify vendor address."))
            issues.append(Issue(4, "APPROVAL PENDING", "Standard approval required.", "Forward to AP Clerk."))
        
        # Add a random low-priority issue to some documents
        if random.random() < 0.3:
            issues.append(Issue(5, "FILING REQUIRED", "Document needs to be filed in DMS.", "File in Document Management System."))

        mock_docs.append(Document(doc_id, doc_type, vendor, total_amount, risk_score, issues))
        
    return mock_docs

def sort_documents(documents: List[Document]) -> List[Document]:
    """
    Sorts documents based on the user's criteria:
    1. Action Required (Highest Priority First)
    2. Risk Score (Highest to Lowest)
    3. Document ID (Alphabetical tie-breaker)
    """
    # Key: (Has Action, Max Issue Priority, Risk Score, Doc ID)
    # We use -self.has_action to put True (has action) first
    # We use self.max_issue_priority to put 1 (highest priority) first
    # We use -self.risk_score to put highest risk first
    
    return sorted(
        documents,
        key=lambda doc: (-doc.has_action, doc.max_issue_priority, -doc.risk_score, doc.doc_id)
    )

def calculate_batch_metrics(documents: List[Document]) -> Dict[str, Any]:
    """Calculates high-level metrics for the batch dashboard."""
    total_docs = len(documents)
    docs_with_action = sum(1 for doc in documents if doc.has_action)
    total_actions = sum(len(doc.issues) for doc in documents)
    
    risk_scores = [doc.risk_score for doc in documents]
    avg_risk = sum(risk_scores) / total_docs if total_docs else 0
    
    critical_errors = sum(1 for doc in documents if doc.max_issue_priority == 1)
    
    status = "✅ Complete"
    if critical_errors > 0:
        status = "🔴 CRITICAL ERROR"
    elif docs_with_action > 0:
        status = "⚠️ High Priority"
    
    return {
        'total_documents': total_docs,
        'docs_with_action': docs_with_action,
        'total_actions': total_actions,
        'avg_risk_score': f"{avg_risk:.0f} / 100",
        'critical_errors': critical_errors,
        'batch_status': status
    }

# --- 3. Presentation Layer ---

class ReportGenerator:
    """Generates the final PDF report."""
    
    def __init__(self, batch_id: str, documents: List[Document]):
        self.batch_id = batch_id
        self.documents = documents
        self.report_date = datetime.now().strftime("%B %d, %Y, %H:%M UTC")
        
    def generate_pdf(self, output_filename: Optional[str] = None) -> bytes:
        """Generates the complete PDF report and returns as bytes."""
        if not REPORTLAB_AVAILABLE:
            raise ImportError(
                "reportlab is required for PDF generation. "
                "Install it with: pip install reportlab"
            )
        
        # Create PDF buffer
        buffer = io.BytesIO()
        
        # Create document
        if output_filename:
            doc = SimpleDocTemplate(output_filename, pagesize=letter)
        else:
            doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        # Build story (content)
        story = []
        
        # 1. Sort Documents
        sorted_docs = sort_documents(self.documents)
        
        # 2. Calculate Metrics
        metrics = calculate_batch_metrics(self.documents)
        
        # 3. Separate Documents
        docs_requiring_action = [doc for doc in sorted_docs if doc.has_action]
        docs_complete = [doc for doc in sorted_docs if not doc.has_action]
        
        # 4. Build PDF content
        story.extend(self._build_title_page(metrics))
        story.append(PageBreak())
        story.extend(self._build_dashboard(metrics, sorted_docs))
        story.append(PageBreak())
        story.extend(self._build_details(docs_requiring_action))
        if docs_complete:
            story.append(PageBreak())
            story.extend(self._build_complete_docs(docs_complete))
        
        # 5. Build PDF
        doc.build(story)
        
        # Return bytes or save to file
        if output_filename:
            return None  # File saved to disk
        else:
            buffer.seek(0)
            return buffer.getvalue()
    
    def generate_markdown(self) -> str:
        """Generates the complete Markdown report content."""
        
        # 1. Sort Documents
        sorted_docs = sort_documents(self.documents)
        
        # 2. Calculate Metrics
        metrics = calculate_batch_metrics(self.documents)
        
        # 3. Separate Documents for Detail Section
        docs_requiring_action = [doc for doc in sorted_docs if doc.has_action]
        docs_complete = [doc for doc in sorted_docs if not doc.has_action]
        
        # 4. Render Template (using f-strings for simplicity, Jinja2 in real app)
        
        # --- Batch Dashboard ---
        dashboard_md = self._render_dashboard(metrics, sorted_docs)
        
        # --- Document Details ---
        details_md = self._render_details(docs_requiring_action)
        
        # --- Complete Documents ---
        complete_md = self._render_complete_docs(docs_complete)
        
        # 5. Combine and Return
        report_parts = [
            f"# 🚀 Batch Analysis Report: Action-First Executive Summary",
            f"\n**Product:** AI Document Intelligence (Product #2)",
            f"\n**Batch ID:** {self.batch_id}",
            f"\n**Date Generated:** {self.report_date}",
            f"\n**Total Documents in Batch:** {metrics['total_documents']}",
            f"\n\n---",
            f"\n\n## 🎯 **Batch Dashboard: Executive Summary**",
            f"\n\n| Metric | Value | Status | Action Required |",
            f"\n| :--- | :--- | :--- | :--- |",
            f"\n| **Total Documents Processed** | {metrics['total_documents']} | {metrics['batch_status'].split()[0]} | None |",
            f"\n| **Documents Requiring Action** | **{metrics['docs_with_action']}** | {metrics['batch_status'].split()[0]} | **Immediate Review** |",
            f"\n| **Total Actions to be Completed** | {metrics['total_actions']} | 🟡 Medium Priority | **Review and Assign** |",
            f"\n| **Average Batch Risk Score** | {metrics['avg_risk_score']} | 🟢 Low Risk | None |",
            f"\n| **Documents with Critical Errors** | **{metrics['critical_errors']}** | 🔴 CRITICAL | **Stop Processing** |",
            f"\n\n---",
            f"\n\n{dashboard_md}",
            f"\n\n<div style=\"page-break-before: always;\"></div>",
            f"\n\n{details_md}",
            f"\n\n<div style=\"page-break-before: always;\"></div>",
            f"\n\n{complete_md}",
            f"\n\n---",
            f"\n**End of Report**"
        ]
        return "".join(report_parts)

    def _render_dashboard(self, metrics: Dict[str, Any], documents: List[Document]) -> str:
        """Renders the Prioritized Action List table."""
        header = """## 🚨 **Prioritized Action List (Sorted by Action Urgency)**

This table lists all documents, sorted by the most urgent action required (Action Required > Risk Score).

| Priority | Doc ID | Type | Primary Action Required | Risk Score | Status | Assigned To |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"""
        
        rows = []
        for i, doc in enumerate(documents):
            # Determine priority label and assigned team (mocked)
            priority_label = {1: '🔴', 2: '⚠️', 3: '🟡', 4: '🟢', 5: '⚪'}.get(doc.max_issue_priority, '⚪')
            assigned_to = 'Legal Team' if doc.doc_type == 'Contract' and doc.has_action else \
                          'Finance Team' if doc.doc_type in ['Invoice', 'Tax Document'] and doc.has_action else \
                          'AP Clerk' if doc.max_issue_priority >= 4 else \
                          'N/A'
            
            rows.append(
                f"| {priority_label} | {doc.doc_id} | {doc.doc_type} | **{doc.primary_action}** | {doc.risk_score} | {doc.to_dict()['status']} | {assigned_to} |"
            )
            
            # Limit the display for the sake of the sample
            if i == 15 and metrics['total_documents'] > 20:
                rows.append(f"| ... | ... | ... | **{metrics['total_documents'] - 16} Documents with No Action Required** | ... | Complete | N/A |")
                break
                
        return header + "\n" + "\n".join(rows)

    def _render_details(self, documents: List[Document]) -> str:
        """Renders the detailed section for documents requiring action."""
        if not documents:
            return "## 📄 **Document Detail: Action-First Drill-Down**\n\nNo documents require immediate action."
            
        details_md = "## 📄 **Document Detail: Action-First Drill-Down**\n\n"
        details_md += "This section provides the full detail for every document that requires action.\n\n"
        
        for i, doc in enumerate(documents):
            details_md += f"### {i+1}. Document: {doc.doc_id} ({doc.doc_type})\n\n"
            
            # Key Context Table
            details_md += "| Key Context | Value |\n"
            details_md += "| :--- | :--- |\n"
            details_md += f"| **Document ID** | {doc.doc_id} |\n"
            details_md += f"| **Document Type** | {doc.doc_type} |\n"
            details_md += f"| **Vendor/Party** | {doc.vendor} |\n"
            details_md += f"| **Total Amount** | {doc.to_dict()['total_amount']} |\n"
            details_md += f"| **Risk Score** | **{doc.risk_score} / 100** ({doc.primary_action.split()[0]}) |\n\n"
            
            # Action Required Header
            details_md += f"### 🚨 ACTION REQUIRED: {doc.primary_action}\n\n"
            
            # Issues Table (All Issues Displayed)
            details_md += "| Priority | Issue Type | Issue Detail (All Issues Displayed) | Recommended Action |\n"
            details_md += "| :--- | :--- | :--- | :--- |\n"
            
            for issue in doc.issues:
                issue_dict = issue.to_dict()
                details_md += f"| {issue_dict['priority_icon']} {issue_dict['priority']} | **{issue_dict['issue_type']}** | {issue_dict['detail']} | {issue_dict['recommended_action']} |\n"
            
            details_md += "\n---\n\n" # Separator between documents
            
        return details_md

    def _render_complete_docs(self, documents: List[Document]) -> str:
        """Renders a summary of documents that passed all checks."""
        if not documents:
            return "## 🟢 **Documents with No Action Required**\n\nAll documents required action."
            
        complete_md = "## 🟢 **Documents with No Action Required**\n\n"
        complete_md += f"The remaining {len(documents)} documents passed all checks and were automatically routed for standard processing.\n\n"
        
        # Sample the first few for the report
        sample_docs = documents[:10]
        
        complete_md += "| Doc ID | Type | Risk Score | Status | Primary Action |\n"
        complete_md += "| :--- | :--- | :--- | :--- | :--- |\n"
        
        for doc in sample_docs:
            complete_md += f"| {doc.doc_id} | {doc.doc_type} | {doc.risk_score} | Complete | ✅ Filed in DMS |\n"
            
        if len(documents) > 10:
            complete_md += f"| ... | ... | ... | ... | ... ({len(documents) - 10} more) |\n"
            
        return complete_md
    
    def _build_title_page(self, metrics: Dict[str, Any]) -> List:
        """Builds the title page of the PDF report."""
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'SubtitleStyle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=15,
            alignment=TA_CENTER
        )
        
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=8,
            alignment=TA_LEFT
        )
        
        elements = [
            Spacer(1, 2*inch),
            Paragraph("Batch Analysis Report", title_style),
            Paragraph("Action-First Executive Summary", subtitle_style),
            Spacer(1, 0.5*inch),
            Paragraph(f"<b>Product:</b> AI Document Intelligence (Product #2)", info_style),
            Paragraph(f"<b>Batch ID:</b> {self.batch_id}", info_style),
            Paragraph(f"<b>Date Generated:</b> {self.report_date}", info_style),
            Paragraph(f"<b>Total Documents:</b> {metrics['total_documents']}", info_style),
            Spacer(1, 1*inch),
        ]
        
        # Add metrics table
        metrics_data = [
            ['Metric', 'Value', 'Status'],
            ['Total Documents Processed', str(metrics['total_documents']), metrics['batch_status'].split()[0]],
            ['Documents Requiring Action', str(metrics['docs_with_action']), metrics['batch_status'].split()[0]],
            ['Total Actions to Complete', str(metrics['total_actions']), 'Medium Priority'],
            ['Average Batch Risk Score', metrics['avg_risk_score'], 'Low Risk'],
            ['Critical Errors', str(metrics['critical_errors']), 'CRITICAL'],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        elements.append(metrics_table)
        
        return elements
    
    def _build_dashboard(self, metrics: Dict[str, Any], documents: List[Document]) -> List:
        """Builds the prioritized action list table."""
        styles = getSampleStyleSheet()
        
        heading_style = ParagraphStyle(
            'DashboardHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        elements = [
            Paragraph("Prioritized Action List (Sorted by Action Urgency)", heading_style),
            Paragraph("This table lists all documents, sorted by the most urgent action required.", styles['Normal']),
            Spacer(1, 0.2*inch),
        ]
        
        # Build table data
        table_data = [['Priority', 'Doc ID', 'Type', 'Primary Action', 'Risk Score', 'Status', 'Assigned To']]
        
        for doc in documents[:20]:  # Limit to first 20 for PDF
            doc_dict = doc.to_dict()
            priority_icon = {1: 'Critical', 2: 'High', 3: 'Medium', 4: 'Low', 5: 'None'}.get(doc.max_issue_priority, 'None')
            assigned_to = 'Legal Team' if doc.doc_type == 'Contract' and doc.has_action else \
                          'Finance Team' if doc.doc_type in ['Invoice', 'Tax Document'] and doc.has_action else \
                          'AP Clerk' if doc.max_issue_priority >= 4 else \
                          'N/A'
            
            table_data.append([
                priority_icon,
                doc.doc_id,
                doc.doc_type,
                doc.primary_action.replace('🔴', '').replace('⚠️', '').replace('🟡', '').replace('🟢', '').replace('✅', '').strip(),
                str(doc.risk_score),
                doc_dict['status'],
                assigned_to
            ])
        
        if len(documents) > 20:
            table_data.append(['...', '...', '...', f'{len(documents) - 20} more documents', '...', '...', '...'])
        
        # Create table
        table = Table(table_data, colWidths=[0.8*inch, 1*inch, 1.2*inch, 2.5*inch, 0.8*inch, 1*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _build_details(self, documents: List[Document]) -> List:
        """Builds the detailed section for documents requiring action."""
        styles = getSampleStyleSheet()
        
        heading_style = ParagraphStyle(
            'DetailsHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        subheading_style = ParagraphStyle(
            'SubHeading',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        elements = [
            Paragraph("Document Detail: Action-First Drill-Down", heading_style),
            Paragraph("This section provides the full detail for every document that requires action.", styles['Normal']),
            Spacer(1, 0.2*inch),
        ]
        
        if not documents:
            elements.append(Paragraph("No documents require immediate action.", styles['Normal']))
            return elements
        
        for i, doc in enumerate(documents):
            doc_dict = doc.to_dict()
            
            # Document header
            elements.append(Paragraph(f"{i+1}. Document: {doc.doc_id} ({doc.doc_type})", subheading_style))
            
            # Key context table
            context_data = [
                ['Key Context', 'Value'],
                ['Document ID', doc.doc_id],
                ['Document Type', doc.doc_type],
                ['Vendor/Party', doc.vendor],
                ['Total Amount', doc_dict['total_amount']],
                ['Risk Score', f"{doc.risk_score} / 100"],
            ]
            
            context_table = Table(context_data, colWidths=[2*inch, 4*inch])
            context_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            
            elements.append(context_table)
            elements.append(Spacer(1, 0.2*inch))
            
            # Action required
            action_text = doc.primary_action.replace('🔴', 'CRITICAL:').replace('⚠️', 'HIGH:').replace('🟡', 'MEDIUM:').replace('🟢', 'LOW:').replace('✅', '')
            elements.append(Paragraph(f"<b>ACTION REQUIRED:</b> {action_text}", subheading_style))
            elements.append(Spacer(1, 0.1*inch))
            
            # Issues table
            issues_data = [['Priority', 'Issue Type', 'Issue Detail', 'Recommended Action']]
            
            for issue in doc.issues:
                issue_dict = issue.to_dict()
                priority_label = {1: 'Critical', 2: 'High', 3: 'Medium', 4: 'Low', 5: 'Info'}.get(issue.priority, 'Info')
                issues_data.append([
                    priority_label,
                    issue_dict['issue_type'],
                    issue_dict['detail'],
                    issue_dict['recommended_action']
                ])
            
            issues_table = Table(issues_data, colWidths=[0.8*inch, 1.5*inch, 2.5*inch, 2.2*inch])
            issues_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            elements.append(issues_table)
            elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _build_complete_docs(self, documents: List[Document]) -> List:
        """Builds summary of documents with no action required."""
        styles = getSampleStyleSheet()
        
        heading_style = ParagraphStyle(
            'CompleteHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        elements = [
            Paragraph("Documents with No Action Required", heading_style),
            Paragraph(f"The remaining {len(documents)} documents passed all checks and were automatically routed for standard processing.", styles['Normal']),
            Spacer(1, 0.2*inch),
        ]
        
        if not documents:
            elements.append(Paragraph("All documents required action.", styles['Normal']))
            return elements
        
        # Build table
        complete_data = [['Doc ID', 'Type', 'Risk Score', 'Status', 'Primary Action']]
        
        sample_docs = documents[:10]
        for doc in sample_docs:
            complete_data.append([
                doc.doc_id,
                doc.doc_type,
                str(doc.risk_score),
                'Complete',
                'Filed in DMS'
            ])
        
        if len(documents) > 10:
            complete_data.append(['...', '...', '...', '...', f'{len(documents) - 10} more'])
        
        complete_table = Table(complete_data, colWidths=[1*inch, 1.5*inch, 1*inch, 1*inch, 2.5*inch])
        complete_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        
        elements.append(complete_table)
        
        return elements

# --- Example Usage ---
if __name__ == '__main__':
    try:
        from faker import Faker
        fake = Faker()
        Faker.seed(42)
        random.seed(42)
    except ImportError:
        print("Warning: faker not installed. Using placeholder data.")
        class Fake:
            def company(self):
                return f"Company {random.randint(1, 100)}"
        fake = Fake()
    
    # 1. Generate Mock Data (Simulating 100 documents)
    mock_documents = generate_mock_documents(100)
    
    # 2. Initialize Generator
    generator = ReportGenerator("BATCH-20251109-0042", mock_documents)
    
    # 3. Generate PDF Report
    pdf_filename = "Batch_Analysis_Report.pdf"
    try:
        pdf_bytes = generator.generate_pdf(pdf_filename)
        print(f"PDF report generated successfully: {pdf_filename}")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        print("Falling back to markdown generation...")
        final_report_markdown = generator.generate_markdown()
        print(final_report_markdown)
"""
# --- End of File ---
"""
