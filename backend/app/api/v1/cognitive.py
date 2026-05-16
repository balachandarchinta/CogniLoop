from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.learner import Learner
from app.core.dependencies import get_current_user
from app.schemas.cognitive import (
    EventInteractionCreate, 
    CognitiveProfileResponse, 
    AttentionAnalysisResponse
)
from app.core.cognitive_profiling.profiler import ProfileEvolutionManager
from app.tasks.profile_update import update_cognitive_profile

router = APIRouter(prefix="/cognitive", tags=["Cognitive Profiling"])

# Initialize the manager for real-time analysis
profile_manager = ProfileEvolutionManager()

@router.get("/profile", response_model=CognitiveProfileResponse)
async def get_cognitive_profile(
    current_user: Learner = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current authenticated user's cognitive profile.
    """
    # In the MVP, we assume the first profile is the active one
    if not current_user.cognitive_profiles:
        # Return a 404 or create a default one. Let's return 404 for now.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cognitive profile not found for this user."
        )
        
    profile = current_user.cognitive_profiles[0]
    
    # We map the SQLAlchemy model dict/JSON fields to our Pydantic schema
    # The DB model (cognitive_profile.py) defines learning_style, cognitive_characteristics, etc. as JSON columns
    return {
        "learner_id": str(profile.learner_id),
        "profile_version": profile.profile_version,
        "learning_style": {
            "primary": profile.learning_style,
            "secondary": "",  # Missing in flat model
            "scores": profile.learning_style_scores or {"visual": 0.25, "auditory": 0.25, "kinesthetic": 0.25, "reading_writing": 0.25},
            "confidence": profile.learning_style_confidence or 0.0,
            "is_multimodal": False,
            "preferred_styles": [profile.learning_style] if profile.learning_style else [],
            "recommendation": ""
        },
        "cognitive_characteristics": {
            "comprehension_speed": profile.comprehension_speed or "moderate",
            "attention_span_minutes": profile.attention_span_minutes or 20.0,
            "retention_rate": profile.retention_rate or 0.7,
            "processing_style": profile.processing_style or "sequential",
            "cognitive_load_tolerance": profile.cognitive_load_tolerance or "medium"
        },
        "behavioral_patterns": {
            "optimal_learning_hours": profile.optimal_learning_hours,
            "average_session_duration": profile.average_session_duration,
            "preferred_break_frequency": profile.preferred_break_frequency,
            "distraction_susceptibility": profile.distraction_susceptibility,
            "multitasking_tendency": profile.multitasking_tendency
        },
        "created_at": profile.created_at,
        "updated_at": profile.updated_at
    }

@router.post("/events", status_code=status.HTTP_202_ACCEPTED)
async def ingest_events(
    events: List[EventInteractionCreate],
    current_user: Learner = Depends(get_current_user)
):
    """
    Ingest raw behavioral events and trigger asynchronous profile update.
    """
    # Convert Pydantic models to dicts for Celery serialization
    events_data = [e.model_dump() for e in events]
    
    # Trigger the Celery background task
    # update_cognitive_profile.delay(str(current_user.id), {"events": events_data})
    
    # For MVP without a running Celery worker, we can just call it synchronously or leave it as .delay
    # We will use .delay() to adhere to the architecture, but if Redis is not up, this might fail.
    # Let's wrap it in a try-except to fallback to synchronous execution for ease of local testing
    try:
        update_cognitive_profile.delay(str(current_user.id), {"events": events_data})
    except Exception as e:
        print(f"Celery delay failed ({e}), running synchronously...")
        update_cognitive_profile(str(current_user.id), {"events": events_data})
        
    return {"message": "Events received. Profile update queued."}

@router.post("/attention/analyze", response_model=AttentionAnalysisResponse)
async def analyze_attention(
    events: List[EventInteractionCreate],
    current_user: Learner = Depends(get_current_user)
):
    """
    Accepts a batch of recent session events and returns real-time distraction analysis and engagement scores.
    """
    class MockEvent:
        def __init__(self, e_dict):
            self.type = e_dict.get('type')
            self.timestamp = e_dict.get('timestamp')
            self.time_spent = e_dict.get('time_spent', 60)
            
    # Convert dicts back to object-like structures for the analyzer
    session_events = [MockEvent(e.model_dump()) for e in events]
    
    analysis = profile_manager.attention_analyzer.analyze_session(session_events)
    
    return analysis
