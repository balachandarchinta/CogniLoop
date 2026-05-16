from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class Assessment(Base):
    """
    Assessment model for quizzes, tests, and psychometric evaluations.
    Tracks learner performance and comprehension.
    """
    __tablename__ = "assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learner_id = Column(UUID(as_uuid=True), ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content_library.id", ondelete="SET NULL"))
    
    # Assessment Type
    assessment_type = Column(String(50))  # quiz, psychometric, comprehension, final_test
    
    # Questions & Answers
    questions = Column(JSONB)  # Array of question objects
    answers = Column(JSONB)  # Array of answer objects
    
    # Scoring
    score = Column(Float)  # Percentage or points
    max_score = Column(Float)
    passing_score = Column(Float)
    passed = Column(String(10))  # 'yes', 'no'
    
    # Timing
    time_taken_minutes = Column(Integer)
    time_limit_minutes = Column(Integer)
    
    # Assessment Metadata
    assessment_metadata = Column(JSONB)  # Additional assessment data
    
    # Timestamps
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    learner = relationship("Learner", back_populates="assessments")
    content = relationship("Content", back_populates="assessments")

    def __repr__(self):
        return f"<Assessment(id={self.id}, type={self.assessment_type}, score={self.score})>"

    def to_dict(self):
        """Convert assessment to dictionary"""
        return {
            "id": str(self.id),
            "learner_id": str(self.learner_id),
            "content_id": str(self.content_id) if self.content_id else None,
            "assessment_type": self.assessment_type,
            "questions": self.questions,
            "answers": self.answers,
            "score": self.score,
            "max_score": self.max_score,
            "passing_score": self.passing_score,
            "passed": self.passed,
            "time_taken_minutes": self.time_taken_minutes,
            "time_limit_minutes": self.time_limit_minutes,
            "assessment_metadata": self.assessment_metadata,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

# Made with Bob
