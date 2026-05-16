from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class DailyRoutine(Base):
    """
    Daily Routine model tracking learner's daily schedule and productivity patterns.
    Used to optimize learning session scheduling.
    """
    __tablename__ = "daily_routines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learner_id = Column(UUID(as_uuid=True), ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    
    # Day & Time
    day_of_week = Column(Integer)  # 0-6 (Monday-Sunday)
    time_slot = Column(String(20))  # "09:00-10:00"
    
    # Activity
    activity_type = Column(String(100))  # work, study, exercise, sleep, leisure, etc.
    activity_description = Column(String(500))
    
    # Productivity & Availability
    productivity_level = Column(String(50))  # high, medium, low
    energy_level = Column(String(50))  # high, medium, low
    is_available_for_learning = Column(Boolean, default=False)
    
    # Preferences
    preferred_for_learning = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    learner = relationship("Learner", back_populates="daily_routines")

    def __repr__(self):
        return f"<DailyRoutine(id={self.id}, day={self.day_of_week}, time={self.time_slot}, activity={self.activity_type})>"

    def to_dict(self):
        """Convert daily routine to dictionary"""
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return {
            "id": str(self.id),
            "learner_id": str(self.learner_id),
            "day_of_week": self.day_of_week,
            "day_name": day_names[self.day_of_week] if self.day_of_week is not None and 0 <= self.day_of_week <= 6 else None,
            "time_slot": self.time_slot,
            "activity_type": self.activity_type,
            "activity_description": self.activity_description,
            "productivity_level": self.productivity_level,
            "energy_level": self.energy_level,
            "is_available_for_learning": self.is_available_for_learning,
            "preferred_for_learning": self.preferred_for_learning,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

# Made with Bob
