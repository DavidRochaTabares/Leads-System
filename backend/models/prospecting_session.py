from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base import BaseModel


class ProspectingSession(BaseModel):
    __tablename__ = "prospecting_sessions"

    industry = Column(String, nullable=False)
    location = Column(String, nullable=False)
    max_companies = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="pending")
    progress = Column(Integer, nullable=False, default=0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)

    logs = relationship(
        "ProspectingSessionLog",
        back_populates="session",
        order_by="ProspectingSessionLog.created_at",
        cascade="all, delete-orphan"
    )


class ProspectingSessionLog(BaseModel):
    __tablename__ = "prospecting_session_logs"

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("prospecting_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    level = Column(String, nullable=False, default="info")
    message = Column(Text, nullable=False)

    session = relationship("ProspectingSession", back_populates="logs")
