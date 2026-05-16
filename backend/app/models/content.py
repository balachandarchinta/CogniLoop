from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class Content(Base):
    """
    Content model representing learning materials in the library.
    Stores content metadata, difficulty level, and learning objectives.
    """
    __tablename__ = "content_library"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Content Information
    title = Column(String(500), nullable=False)
    subject = Column(String(100))
    topic = Column(String(200))
    description = Column(Text)
    
    # Content Classification
    difficulty_level = Column(String(50))  # beginner, intermediate, advanced
    content_type = Column(String(50))  # video, text, interactive, quiz
    content_format = Column(String(50))  # visual, auditory, textual
    
    # Duration & Prerequisites
    duration_minutes = Column(Integer)
    prerequisites = Column(JSONB)  # Array of prerequisite content IDs
    
    # Learning Objectives
    learning_objectives = Column(JSONB)  # Array of learning objectives
    
    # Content Location
    content_url = Column(Text)
    
    # Metadata
    metadata = Column(JSONB)  # Additional content metadata
    
    # Status
    is_active = Column(String(10), default='active')
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    interactions = relationship("LearnerContentInteraction", back_populates="content", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="content")

    def __repr__(self):
        return f"<Content(id={self.id}, title={self.title}, type={self.content_type})>"

    def to_dict(self):
        """Convert content to dictionary"""
        return {
            "id": str(self.id),
            "title": self.title,
            "subject": self.subject,
            "topic": self.topic,
            "description": self.description,
            "difficulty_level": self.difficulty_level,
            "content_type": self.content_type,
            "content_format": self.content_format,
            "duration_minutes": self.duration_minutes,
            "prerequisites": self.prerequisites,
            "learning_objectives": self.learning_objectives,
            "content_url": self.content_url,
            "metadata": self.metadata,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class LearnerContentInteraction(Base):
    """
    Learner Content Interaction model tracking how learners interact with content.
    Records engagement, completion, and comprehension metrics.
    """
    __tablename__ = "learner_content_interactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learner_id = Column(UUID(as_uuid=True), ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content_library.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("learning_sessions.id", ondelete="CASCADE"), nullable=False)
    
    # Timing
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime)
    time_spent_minutes = Column(Integer)
    
    # Progress & Engagement
    completion_percentage = Column(Float)
    engagement_score = Column(Float)  # 0-1 scale
    comprehension_score = Column(Float)  # Based on quiz/assessment
    
    # Interaction Details
    interaction_data = Column(JSONB)  # Detailed interaction metrics
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    learner = relationship("Learner", back_populates="content_interactions")
    content = relationship("Content", back_populates="interactions")
    session = relationship("LearningSession", back_populates="content_interactions")

    def __repr__(self):
        return f"<LearnerContentInteraction(id={self.id}, learner_id={self.learner_id}, content_id={self.content_id})>"

    def to_dict(self):
        """Convert interaction to dictionary"""
        return {
            "id": str(self.id),
            "learner_id": str(self.learner_id),
            "content_id": str(self.content_id),
            "session_id": str(self.session_id),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "time_spent_minutes": self.time_spent_minutes,
            "completion_percentage": self.completion_percentage,
            "engagement_score": self.engagement_score,
            "comprehension_score": self.comprehension_score,
            "interaction_data": self.interaction_data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

# Made with Bob
