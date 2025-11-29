"""
PDF Report Generator using WeasyPrint
Creates personalized Ayurvedic assessment reports
"""
from weasyprint import HTML, CSS
from datetime import datetime
import os

def generate_pdf_report(user_data, dosha_results, panchakarma_recs):
    """
    Generate PDF report with assessment results and recommendations
    
    Args:
        user_data: User information and assessment responses
        dosha_results: Dosha scores and percentages
        panchakarma_recs: Panchakarma therapy recommendations
        
    Returns:
        PDF file path
    """
    
    # HTML template for PDF
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: 'Georgia', serif;
                color: #2c3e50;
                line-height: 1.6;
            }}
            .header {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 32px;
            }}
            .section {{
                margin-bottom: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #f5576c;
            }}
            .section h2 {{
                color: #f5576c;
                margin-top: 0;
                border-bottom: 2px solid #f5576c;
                padding-bottom: 10px;
            }}
            .dosha-chart {{
                display: flex;
                justify-content: space-around;
                margin: 20px 0;
            }}
            .dosha-item {{
                text-align: center;
                padding: 15px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .dosha-item h3 {{
                margin: 0 0 10px 0;
                color: #2c3e50;
            }}
            .dosha-percentage {{
                font-size: 24px;
                font-weight: bold;
                color: #f5576c;
            }}
            .therapy-card {{
                background: white;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                border-left: 3px solid #f5576c;
            }}
            .therapy-card h4 {{
                margin-top: 0;
                color: #2c3e50;
            }}
            .list-item {{
                margin: 8px 0;
                padding-left: 20px;
            }}
            .disclaimer {{
                background: #fff3cd;
                border: 1px solid #ffc107;
                padding: 15px;
                border-radius: 8px;
                margin-top: 30px;
                font-size: 12px;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌿 AyurSutra Wellness Report</h1>
            <p>Personalized Ayurvedic Assessment & Recommendations</p>
            <p>Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="section">
            <h2>Your Dosha Assessment Results</h2>
            <div class="dosha-chart">
                <div class="dosha-item">
                    <h3>Vata</h3>
                    <div class="dosha-percentage">{dosha_results['percentages']['vata']}%</div>
                </div>
                <div class="dosha-item">
                    <h3>Pitta</h3>
                    <div class="dosha-percentage">{dosha_results['percentages']['pitta']}%</div>
                </div>
                <div class="dosha-item">
                    <h3>Kapha</h3>
                    <div class="dosha-percentage">{dosha_results['percentages']['kapha']}%</div>
                </div>
            </div>
            <p><strong>Dominant Dosha:</strong> {dosha_results['dominant_dosha'].title()}</p>
            <p><strong>Secondary Dosha:</strong> {dosha_results.get('secondary_dosha', 'N/A').title()}</p>
        </div>
        
        <div class="section">
            <h2>Recommended Panchakarma Therapies</h2>
            <p><strong>Primary Therapies:</strong></p>
            {''.join([f'<div class="therapy-card"><h4>{therapy["name"]}</h4><p>{therapy["description"]}</p><p><strong>Duration:</strong> {therapy["duration"]}</p><p><strong>Benefits:</strong> {therapy["benefits"]}</p><p><strong>Precautions:</strong> {therapy["precautions"]}</p></div>' for therapy in panchakarma_recs.get('therapy_details', [])])}
        </div>
        
        <div class="section">
            <h2>Dietary Recommendations (Ahara)</h2>
            <p><strong>Foods to Favor:</strong></p>
            <ul>
                {''.join([f'<li class="list-item">{item}</li>' for item in panchakarma_recs.get('dietary', {}).get('favor', [])])}
            </ul>
            <p><strong>Foods to Avoid:</strong></p>
            <ul>
                {''.join([f'<li class="list-item">{item}</li>' for item in panchakarma_recs.get('dietary', {}).get('avoid', [])])}
            </ul>
        </div>
        
        <div class="section">
            <h2>Lifestyle Modifications (Vihara)</h2>
            <p><strong>Daily Routine:</strong> {panchakarma_recs.get('lifestyle', {}).get('routine', 'N/A')}</p>
            <p><strong>Yoga Practices:</strong> {panchakarma_recs.get('lifestyle', {}).get('yoga', 'N/A')}</p>
            <p><strong>Pranayama:</strong> {panchakarma_recs.get('lifestyle', {}).get('pranayama', 'N/A')}</p>
        </div>
        
        <div class="disclaimer">
            <strong>⚠️ Important Disclaimer:</strong> This assessment is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified Ayurvedic practitioners or healthcare providers with any questions you may have regarding your health condition. Panchakarma therapies should be performed under the supervision of trained Ayurvedic physicians.
        </div>
        
        <div class="footer">
            <p>AyurSutra - Your Ayurvedic Wellness Companion</p>
            <p>Generated by AyurSutra Bot | www.ayursutra.com</p>
        </div>
    </body>
    </html>
    """
    
    # Generate PDF
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    pdf_path = os.path.join(reports_dir, f'assessment_report_{timestamp}.pdf')
    
    HTML(string=html_content).write_pdf(pdf_path)
    
    return pdf_path

