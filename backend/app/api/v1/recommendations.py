from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db
from app.models.learner import Learner
from app.models.content import Content
from app.core.dependencies import get_current_user
from app.core.recommendation.recommender import RecommendationEngine
from app.core.adaptive_learning.adaptation_engine import AdaptationEngine

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

recommender = RecommendationEngine()
adaptation_engine = AdaptationEngine()

@router.get("/path", response_model=List[Dict[str, Any]])
async def get_personalized_path(
    current_user: Learner = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a personalized learning path for the current user.
    """
    if not current_user.cognitive_profiles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cognitive profile required for recommendations."
        )
        
    profile = current_user.cognitive_profiles[0]
    
    # 1. Get Adaptation Directive
    # (Mocking session data for simplicity)
    mock_session = {"current_difficulty": 0.5, "assessment_scores": [], "recent_engagement_score": 0.5}
    
    # Map SQLAlchemy profile to dict for the engine (same as in adaptive.py)
    profile_dict = {
        "learning_style": profile.learning_style if isinstance(profile.learning_style, dict) else {"primary": profile.learning_style, "scores": profile.learning_style_scores or {}},
        "cognitive_characteristics": {
            "comprehension_speed": profile.comprehension_speed,
            "attention_span_minutes": profile.attention_span_minutes,
            "retention_rate": profile.retention_rate
        }
    }
    
    directive = adaptation_engine.generate_adaptation_directive(profile_dict, mock_session)
    
    # 2. Fetch Content from Library
    all_content_models = db.query(Content).filter(Content.is_active == 'active').all()
    all_content = [c.to_dict() for c in all_content_models]
    
    # 3. Get Completed Content IDs
    completed_ids = [str(i.content_id) for i in current_user.content_interactions if i.completion_percentage == 100.0]
    
    # 4. Generate Path
    path = recommender.generate_learning_path(all_content, completed_ids, profile_dict, directive)
    
    return path

@router.get("/daily", response_model=List[Dict[str, Any]])
async def get_daily_recommendations(
    current_user: Learner = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get quick daily micro-learning recommendations.
    """
    # Similar logic to path but with a smaller window and simpler ranking
    return []
