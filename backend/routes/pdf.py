from fastapi import APIRouter, Response
from pdf_generator import generate_pdf_report

router = APIRouter()

@router.post("/generate")
async def generate_pdf(data: dict):
    user_data = data["user_data"]
    dosha_results = data["dosha_results"]
    panchakarma_recs = data["panchakarma_recs"]

    pdf_path = generate_pdf_report(user_data, dosha_results, panchakarma_recs)

    return Response(
        content=open(pdf_path, "rb").read(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="AyurSutra_Report.pdf"'
        }
    )
