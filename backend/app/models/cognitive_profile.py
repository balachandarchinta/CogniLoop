from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class CognitiveProfile(Base):
    """
    Cognitive Profile model storing learner's cognitive characteristics,
    learning style, behavioral patterns, and preferences.
    """
    __tablename__ = "cognitive_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learner_id = Column(UUID(as_uuid=True), ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    
    # Learning Style
    learning_style = Column(String(50))  # visual, auditory, kinesthetic, reading_writing
    learning_style_confidence = Column(Float)
    learning_style_scores = Column(JSONB)  # {"visual": 0.85, "auditory": 0.45, ...}
    
    # Cognitive Characteristics
    comprehension_speed = Column(String(50))  # slow, moderate, fast
    attention_span_minutes = Column(Integer)
    retention_rate = Column(Float)
    processing_style = Column(String(50))  # sequential, global, holistic
    cognitive_load_tolerance = Column(String(50))  # low, medium, high
    
    # Behavioral Patterns
    optimal_learning_hours = Column(JSONB)  # ["09:00-11:00", "15:00-17:00"]
    average_session_duration = Column(Integer)  # minutes
    preferred_break_frequency = Column(Integer)  # minutes
    distraction_susceptibility = Column(String(50))  # low, medium, high
    multitasking_tendency = Column(String(50))  # low, medium, high
    
    # Content Preferences
    preferred_formats = Column(JSONB)  # ["video", "infographic", "interactive"]
    preferred_complexity = Column(String(50))  # beginner, intermediate, advanced
    preferred_pace = Column(String(50))  # slow, moderate, fast
    example_preference = Column(String(50))  # abstract, real_world, mixed
    
    # Cognitive Strengths & Weaknesses
    cognitive_strengths = Column(JSONB)  # ["pattern_recognition", "visual_memory"]
    cognitive_weaknesses = Column(JSONB)  # ["sustained_attention", "abstract_reasoning"]
    
    # Learner Type Classification
    learner_type = Column(String(100))  # visual_interactive, auditory_sequential, etc.
    
    # Confidence Metrics
    overall_confidence = Column(Float, default=0.5)
    data_points_collected = Column(Integer, default=0)
    profile_stability = Column(Float, default=0.3)
    
    # Versioning
    profile_version = Column(Integer, default=1)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    learner = relationship("Learner", back_populates="cognitive_profiles")

    def __repr__(self):
        return f"<CognitiveProfile(id={self.id}, learner_id={self.learner_id}, style={self.learning_style})>"

    def to_dict(self):
        """Convert cognitive profile to dictionary"""
        return {
            "id": str(self.id),
            "learner_id": str(self.learner_id),
            "learning_style": {
                "primary": self.learning_style,
                "confidence": self.learning_style_confidence,
                "scores": self.learning_style_scores,
            },
            "cognitive_characteristics": {
                "comprehension_speed": self.comprehension_speed,
                "attention_span_minutes": self.attention_span_minutes,
                "retention_rate": self.retention_rate,
                "processing_style": self.processing_style,
                "cognitive_load_tolerance": self.cognitive_load_tolerance,
            },
            "behavioral_patterns": {
                "optimal_learning_hours": self.optimal_learning_hours,
                "average_session_duration": self.average_session_duration,
                "preferred_break_frequency": self.preferred_break_frequency,
                "distraction_susceptibility": self.distraction_susceptibility,
                "multitasking_tendency": self.multitasking_tendency,
            },
            "content_preferences": {
                "preferred_formats": self.preferred_formats,
                "preferred_complexity": self.preferred_complexity,
                "preferred_pace": self.preferred_pace,
                "example_preference": self.example_preference,
            },
            "cognitive_strengths": self.cognitive_strengths,
            "cognitive_weaknesses": self.cognitive_weaknesses,
            "learner_type": self.learner_type,
            "confidence_metrics": {
                "overall_confidence": self.overall_confidence,
                "data_points_collected": self.data_points_collected,
                "profile_stability": self.profile_stability,
            },
            "profile_version": self.profile_version,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

# Made with Bob
