from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class LearningSession(Base):
    """
    Learning Session model tracking individual learning sessions.
    Records session duration, engagement, and completion metrics.
    """
    __tablename__ = "learning_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learner_id = Column(UUID(as_uuid=True), ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    
    # Session Timing
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration_minutes = Column(Integer)
    
    # Content Accessed
    content_ids = Column(JSONB)  # Array of content IDs accessed during session
    
    # Engagement Metrics
    engagement_score = Column(Float)  # Overall engagement score (0-1)
    distraction_count = Column(Integer, default=0)
    completion_rate = Column(Float)  # Percentage of content completed
    
    # Session Metadata
    session_metadata = Column(JSONB)  # Additional session data
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    learner = relationship("Learner", back_populates="learning_sessions")
    behavioral_events = relationship("BehavioralEvent", back_populates="session", cascade="all, delete-orphan")
    content_interactions = relationship("LearnerContentInteraction", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<LearningSession(id={self.id}, learner_id={self.learner_id}, duration={self.duration_minutes}min)>"

    def to_dict(self):
        """Convert learning session to dictionary"""
        return {
            "id": str(self.id),
            "learner_id": str(self.learner_id),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_minutes": self.duration_minutes,
            "content_ids": self.content_ids,
            "engagement_score": self.engagement_score,
            "distraction_count": self.distraction_count,
            "completion_rate": self.completion_rate,
            "session_metadata": self.session_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class BehavioralEvent(Base):
    """
    Behavioral Event model tracking individual user interactions and behaviors.
    Used for engagement analysis and distraction detection.
    """
    __tablename__ = "behavioral_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learner_id = Column(UUID(as_uuid=True), ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("learning_sessions.id", ondelete="CASCADE"), nullable=False)
    
    # Event Details
    event_type = Column(String(100), nullable=False)  # click, scroll, pause, resume, tab_switch, etc.
    event_data = Column(JSONB)  # Additional event-specific data
    
    # Timing
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    learner = relationship("Learner")
    session = relationship("LearningSession", back_populates="behavioral_events")

    def __repr__(self):
        return f"<BehavioralEvent(id={self.id}, type={self.event_type}, timestamp={self.timestamp})>"

    def to_dict(self):
        """Convert behavioral event to dictionary"""
        return {
            "id": str(self.id),
            "learner_id": str(self.learner_id),
            "session_id": str(self.session_id),
            "event_type": self.event_type,
            "event_data": self.event_data,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

# Made with Bob
