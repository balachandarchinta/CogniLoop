from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class EventInteractionCreate(BaseModel):
    """Schema for incoming behavioral events and interactions"""
    type: str = Field(..., description="Type of event (e.g., 'tab_switch', 'video_pause', 'scroll')")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    time_spent: Optional[int] = Field(None, description="Time spent in seconds")
    content_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class LearningStyleScore(BaseModel):
    visual: float
    auditory: float
    kinesthetic: float
    reading_writing: float

class LearningStyle(BaseModel):
    primary: str
    secondary: str
    scores: LearningStyleScore
    confidence: float
    is_multimodal: bool
    preferred_styles: List[str]
    recommendation: str

class CognitiveCharacteristics(BaseModel):
    comprehension_speed: str
    attention_span_minutes: float
    retention_rate: float
    processing_style: Optional[str] = "sequential"
    cognitive_load_tolerance: Optional[str] = "medium"

class CognitiveProfileResponse(BaseModel):
    """Schema for returning the cognitive profile"""
    learner_id: str
    profile_version: int
    learning_style: LearningStyle
    cognitive_characteristics: CognitiveCharacteristics
    behavioral_patterns: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DistractionIndicators(BaseModel):
    tab_switch: bool
    rapid_navigation: bool
    low_scroll_depth: bool
    no_interaction: bool
    incomplete_content: bool

class DistractionAnalysis(BaseModel):
    distracted: bool
    level: str
    score: float
    indicators: DistractionIndicators
    recommended_action: str

class AttentionAnalysisResponse(BaseModel):
    """Schema for real-time attention analysis"""
    average_attention_span: float
    std_deviation: float
    attention_drops: int
    distraction_analysis: Optional[DistractionAnalysis] = None
