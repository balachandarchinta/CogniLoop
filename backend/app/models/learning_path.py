from sqlalchemy import Column, String, Integer, Float, DateTime, Date, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class LearningPath(Base):
    """
    Learning Path model representing a personalized sequence of content.
    Tracks learner progress through a structured learning journey.
    """
    __tablename__ = "learning_paths"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learner_id = Column(UUID(as_uuid=True), ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    
    # Path Information
    path_name = Column(String(255))
    subject = Column(String(100))
    description = Column(String(1000))
    
    # Content Sequence
    content_sequence = Column(JSONB)  # Ordered array of content IDs
    
    # Progress Tracking
    current_position = Column(Integer, default=0)  # Index in content_sequence
    progress_percentage = Column(Float, default=0.0)
    completed_content_ids = Column(JSONB, default=[])  # Array of completed content IDs
    
    # Milestones
    milestones = Column(JSONB)  # Array of milestone objects
    completed_milestones = Column(JSONB, default=[])
    
    # Timing
    estimated_completion_date = Column(Date)
    actual_completion_date = Column(Date)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    
    # Path Metadata
    path_metadata = Column(JSONB)  # Additional path data
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    learner = relationship("Learner", back_populates="learning_paths")

    def __repr__(self):
        return f"<LearningPath(id={self.id}, name={self.path_name}, progress={self.progress_percentage}%)>"

    def to_dict(self):
        """Convert learning path to dictionary"""
        return {
            "id": str(self.id),
            "learner_id": str(self.learner_id),
            "path_name": self.path_name,
            "subject": self.subject,
            "description": self.description,
            "content_sequence": self.content_sequence,
            "current_position": self.current_position,
            "progress_percentage": self.progress_percentage,
            "completed_content_ids": self.completed_content_ids,
            "milestones": self.milestones,
            "completed_milestones": self.completed_milestones,
            "estimated_completion_date": self.estimated_completion_date.isoformat() if self.estimated_completion_date else None,
            "actual_completion_date": self.actual_completion_date.isoformat() if self.actual_completion_date else None,
            "is_active": self.is_active,
            "is_completed": self.is_completed,
            "path_metadata": self.path_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

# Made with Bob
