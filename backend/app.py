"""
AyurSutra - Main FastAPI Application
Ayurvedic Dosha Detection & Panchakarma Recommendation Chatbot
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, Base
from routes import chat, assessment, pdf
import sys
import os

# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AyurSutra API",
    description="Ayurvedic Dosha Detection & Panchakarma Recommendation Chatbot",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(assessment.router)
app.include_router(pdf.router)

# ❌ REMOVE STATIC REPORTS DIRECTORY (NOT ALLOWED ON RENDER)
# No app.mount("/reports") because we now store PDFs only in /tmp

@app.get("/")
async def root():
    return {
        "message": "Namaste! Welcome to AyurSutra API",
        "version": "1.0.0",
        "endpoints": {
            "websocket": "/ws/chat",
            "assessment": "/api/assessment",
            "pdf": "/api/pdf/generate"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
