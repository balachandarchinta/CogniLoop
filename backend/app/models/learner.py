from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class Learner(Base):
    """
    Learner model representing a user in the system.
    Stores basic user information and authentication details.
    """
    __tablename__ = "learners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    age = Column(Integer)
    education_level = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cognitive_profiles = relationship("CognitiveProfile", back_populates="learner", cascade="all, delete-orphan")
    learning_sessions = relationship("LearningSession", back_populates="learner", cascade="all, delete-orphan")
    content_interactions = relationship("LearnerContentInteraction", back_populates="learner", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="learner", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="learner", cascade="all, delete-orphan")
    learning_paths = relationship("LearningPath", back_populates="learner", cascade="all, delete-orphan")
    daily_routines = relationship("DailyRoutine", back_populates="learner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Learner(id={self.id}, email={self.email}, name={self.full_name})>"

    def to_dict(self):
        """Convert learner to dictionary"""
        return {
            "id": str(self.id),
            "email": self.email,
            "full_name": self.full_name,
            "age": self.age,
            "education_level": self.education_level,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

# Made with Bob
