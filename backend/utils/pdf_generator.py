from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
import os
from datetime import datetime

def generate_pdf_report(user_data, dosha_results, panchakarma_recs):
    """
    Generate a PDF report with user dosha results and panchakarma recommendations.
    
    Args:
        user_data: Dictionary with user information
        dosha_results: Dictionary with dosha analysis results
        panchakarma_recs: List of panchakarma recommendations
    
    Returns:
        Path to the generated PDF file
    """
    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(reports_dir, f"AyurSutra_Report_{timestamp}.pdf")
    
    # Create PDF
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "AyurSutra Assessment Report")
    
    # Horizontal line
    c.line(50, height - 65, width - 50, height - 65)
    
    y_position = height - 100
    
    # User Information Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, "User Information")
    y_position -= 25
    
    c.setFont("Helvetica", 11)
    for key, value in user_data.items():
        c.drawString(60, y_position, f"{key.replace('_', ' ').title()}: {value}")
        y_position -= 20
    
    y_position -= 15
    
    # Dosha Results Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, "Dosha Analysis Results")
    y_position -= 25
    
    c.setFont("Helvetica", 11)
    for key, value in dosha_results.items():
        c.drawString(60, y_position, f"{key.replace('_', ' ').title()}: {value}")
        y_position -= 20
    
    y_position -= 15
    
    # Panchakarma Recommendations Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, "Panchakarma Recommendations")
    y_position -= 25
    
    c.setFont("Helvetica", 11)
    if panchakarma_recs:
        for rec in panchakarma_recs:
            if isinstance(rec, dict):
                rec_text = rec.get('name', 'Treatment') + ": " + rec.get('description', '')
            else:
                rec_text = str(rec)
            
            # Wrap text if too long
            if len(rec_text) > 80:
                words = rec_text.split()
                line = ""
                for word in words:
                    if len(line + word) > 80:
                        c.drawString(60, y_position, line)
                        y_position -= 15
                        line = word + " "
                    else:
                        line += word + " "
                if line:
                    c.drawString(60, y_position, line)
                    y_position -= 15
            else:
                c.drawString(60, y_position, f"• {rec_text}")
                y_position -= 20
    
    y_position -= 15
    
    # Footer
    c.setFont("Helvetica", 9)
    c.drawString(50, 30, f"Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(width - 150, 30, "AyurSutra Assistant")
    
    # Save the PDF
    c.save()
    
    return pdf_path
