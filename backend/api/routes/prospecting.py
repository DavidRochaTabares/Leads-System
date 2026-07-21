import logging
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from uuid import UUID
from supabase import Client
from api.schemas import ProspectingSessionCreate
from services.supabase_client import get_supabase
from repositories.prospecting_supabase_repository import ProspectingSupabaseRepository
from services.prospecting_worker import execute_prospecting_session

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/prospecting", tags=["prospecting"])


@router.get("/health")
def prospecting_health():
    return {"status": "ok"}


@router.post("/sessions")
async def create_session(
    payload: ProspectingSessionCreate,
    supabase: Client = Depends(get_supabase),
):
    import asyncio
    repo = ProspectingSupabaseRepository(supabase)
    session = repo.create_session(payload.industry, payload.location, payload.max_companies)
    repo.add_log(session["id"], "Session created.")
    logger.info(f"Creating background task for session {session['id']}")
    
    def task_done_callback(task):
        try:
            task.result()
        except Exception as e:
            logger.error(f"Task failed with exception: {e}", exc_info=True)
    
    task = asyncio.create_task(execute_prospecting_session(session["id"]))
    task.add_done_callback(task_done_callback)
    logger.info(f"Task created: {task}")
    return session


@router.get("/sessions/latest")
def get_latest_session(supabase: Client = Depends(get_supabase)):
    repo = ProspectingSupabaseRepository(supabase)
    return repo.get_latest()


@router.get("/sessions/{session_id}")
def get_session(session_id: str, supabase: Client = Depends(get_supabase)):
    repo = ProspectingSupabaseRepository(supabase)
    session = repo.get_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/sessions/{session_id}/logs")
def get_session_logs(session_id: str, supabase: Client = Depends(get_supabase)):
    repo = ProspectingSupabaseRepository(supabase)
    return repo.get_logs(session_id)


@router.get("/sessions/{session_id}/companies")
def get_session_companies(session_id: str, supabase: Client = Depends(get_supabase)):
    from repositories.company_repository import CompanyRepository
    repo = CompanyRepository(supabase)
    return repo.get_companies_by_session(session_id)
