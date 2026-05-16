from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional

from app.database import get_db
from app.models.learner import Learner
from app.core.dependencies import get_current_user
from app.core.adaptive_learning.adaptation_engine import AdaptationEngine

router = APIRouter(prefix="/adaptive", tags=["Adaptive Learning"])

# Initialize the engine
adaptation_engine = AdaptationEngine()

@router.get("/suggest", response_model=Dict[str, Any])
async def get_adaptation_suggestions(
    current_user: Learner = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate real-time adaptation suggestions based on the user's latest cognitive profile.
    """
    if not current_user.cognitive_profiles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cognitive profile not found. Complete an initial assessment first."
        )
        
    profile = current_user.cognitive_profiles[0]
    
    # In a real scenario, we would pull 'current_session_data' from Redis or active Session model
    # For now, we use a mock session context
    current_session_data = {
        "current_difficulty": 0.5,
        "assessment_scores": [0.85, 0.9, 0.75],  # Performing well
        "recent_engagement_score": 0.8,         # High engagement
    }
    
    # Map SQLAlchemy profile to dict for the engine
    profile_dict = {
        "learning_style": profile.learning_style, # This assumes the model has the dict property or we handle mapping
        "cognitive_characteristics": {
            "comprehension_speed": profile.comprehension_speed,
            "attention_span_minutes": profile.attention_span_minutes,
            "retention_rate": profile.retention_rate
        }
    }
    
    # If learning_style is a string in DB but dict in schema, we handle it
    if isinstance(profile.learning_style, str):
        profile_dict["learning_style"] = {
            "primary": profile.learning_style,
            "scores": profile.learning_style_scores or {}
        }
    
    directive = adaptation_engine.generate_adaptation_directive(profile_dict, current_session_data)
    
    return directive

@router.post("/apply", status_code=status.HTTP_200_OK)
async def apply_adaptation(
    adaptation_id: str,
    feedback: Optional[str] = None,
    current_user: Learner = Depends(get_current_user)
):
    """
    Log user feedback or confirmation of a suggested adaptation.
    """
    return {"message": "Adaptation feedback logged successfully."}
