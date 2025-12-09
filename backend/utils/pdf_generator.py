from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

app = FastAPI()

@app.post("/api/pdf/generate")
def generate_pdf_endpoint(data: dict):
    # Extract user data
    user_data = data.get("user_data", {})
    dosha_results = data.get("dosha_results", {})
    panchakarma_recs = data.get("panchakarma_recs", [])

    # Create PDF in memory
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Example content
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, f"Name: {user_data.get('name', 'User')}")
    c.drawString(50, 780, f"Age: {user_data.get('age', '')}")
    c.drawString(50, 760, f"Dominant Dosha: {dosha_results.get('dominant', 'N/A')}")

    # Panchakarma recommendations
    y = 740
    c.setFont("Helvetica", 12)
    for rec in panchakarma_recs:
        c.drawString(60, y, f"- {rec}")
        y -= 20

    c.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="AyurSutra_Report.pdf"'}
    )
