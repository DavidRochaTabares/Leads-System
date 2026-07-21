from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from models.prospecting_session import ProspectingSession, ProspectingSessionLog
from repositories.base import BaseRepository


class ProspectingSessionRepository(BaseRepository[ProspectingSession]):
    def __init__(self, db: Session):
        super().__init__(ProspectingSession, db)

    def get_latest(self) -> Optional[ProspectingSession]:
        return (
            self.db.query(ProspectingSession)
            .order_by(ProspectingSession.created_at.desc())
            .first()
        )

    def get_with_logs(self, session_id: UUID) -> Optional[ProspectingSession]:
        return (
            self.db.query(ProspectingSession)
            .filter(ProspectingSession.id == session_id)
            .first()
        )

    def add_log(
        self,
        session_id: UUID,
        message: str,
        level: str = "info",
    ) -> ProspectingSessionLog:
        log = ProspectingSessionLog(
            session_id=session_id,
            message=message,
            level=level,
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def update_status(
        self,
        session_id: UUID,
        status: str,
        progress: Optional[int] = None,
        error_message: Optional[str] = None,
    ) -> Optional[ProspectingSession]:
        session = self.get_by_id(session_id)
        if not session:
            return None

        session.status = status
        if progress is not None:
            session.progress = progress
        if error_message is not None:
            session.error_message = error_message

        if status == "running" and not session.started_at:
            session.started_at = datetime.utcnow()
        if status in ("completed", "failed") and not session.finished_at:
            session.finished_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(session)
        return session

    def get_logs(self, session_id: UUID) -> List[ProspectingSessionLog]:
        return (
            self.db.query(ProspectingSessionLog)
            .filter(ProspectingSessionLog.session_id == session_id)
            .order_by(ProspectingSessionLog.created_at.asc())
            .all()
        )
