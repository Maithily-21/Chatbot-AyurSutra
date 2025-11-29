from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from database.database import Base

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    vata_score = Column(Float)
    pitta_score = Column(Float)
    kapha_score = Column(Float)
    dominant_dosha = Column(String)
    secondary_dosha = Column(String)
    assessment_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    message = Column(Text)
    sender = Column(String)  # 'user' or 'bot'
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

