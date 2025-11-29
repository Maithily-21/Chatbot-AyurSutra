"""
Assessment API Endpoints
Handles dosha assessment and results retrieval
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Assessment
from Training.prakritimodel import calculate_dosha_scores
from Training.panchakarma_model import get_panchakarma_recommendations
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class AssessmentRequest(BaseModel):
    session_id: str
    assessment_data: Dict[str, Any]

class AssessmentResponse(BaseModel):
    dosha_results: Dict[str, Any]
    panchakarma_recs: Dict[str, Any]

@router.post("/api/assessment/calculate", response_model=AssessmentResponse)
async def calculate_assessment(request: AssessmentRequest, db: Session = Depends(get_db)):
    """Calculate dosha scores and get recommendations"""
    try:
        # Calculate dosha results
        dosha_results = calculate_dosha_scores(request.assessment_data)
        
        # Get Panchakarma recommendations
        panchakarma_recs = get_panchakarma_recommendations(dosha_results)
        
        # Save to database
        assessment = Assessment(
            session_id=request.session_id,
            vata_score=dosha_results['percentages']['vata'],
            pitta_score=dosha_results['percentages']['pitta'],
            kapha_score=dosha_results['percentages']['kapha'],
            dominant_dosha=dosha_results['dominant_dosha'],
            secondary_dosha=dosha_results.get('secondary_dosha'),
            assessment_data=request.assessment_data
        )
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        
        return AssessmentResponse(
            dosha_results=dosha_results,
            panchakarma_recs=panchakarma_recs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/assessment/{session_id}")
async def get_assessment(session_id: str, db: Session = Depends(get_db)):
    """Retrieve assessment results by session ID"""
    assessment = db.query(Assessment).filter(Assessment.session_id == session_id).order_by(Assessment.created_at.desc()).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Recalculate recommendations
    panchakarma_recs = get_panchakarma_recommendations({
        'dominant_dosha': assessment.dominant_dosha,
        'secondary_dosha': assessment.secondary_dosha,
        'percentages': {
            'vata': assessment.vata_score,
            'pitta': assessment.pitta_score,
            'kapha': assessment.kapha_score
        }
    })
    
    return {
        'dosha_results': {
            'percentages': {
                'vata': assessment.vata_score,
                'pitta': assessment.pitta_score,
                'kapha': assessment.kapha_score
            },
            'dominant_dosha': assessment.dominant_dosha,
            'secondary_dosha': assessment.secondary_dosha
        },
        'panchakarma_recs': panchakarma_recs,
        'created_at': assessment.created_at.isoformat()
    }

