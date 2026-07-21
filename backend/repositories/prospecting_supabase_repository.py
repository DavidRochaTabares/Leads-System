from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import uuid4
from supabase import Client


class ProspectingSupabaseRepository:
    def __init__(self, supabase: Client):
        self.supabase = supabase
    
    def create_session(self, industry: str, location: str, max_companies: int) -> Dict[str, Any]:
        session_data = {
            "id": str(uuid4()),
            "industry": industry,
            "location": location,
            "max_companies": max_companies,
            "status": "pending",
            "progress": 0,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        result = self.supabase.table("prospecting_sessions").insert(session_data).execute()
        return result.data[0] if result.data else session_data
    
    def get_latest(self) -> Optional[Dict[str, Any]]:
        result = self.supabase.table("prospecting_sessions").select("*").order("created_at", desc=True).limit(1).execute()
        return result.data[0] if result.data else None
    
    def get_by_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        result = self.supabase.table("prospecting_sessions").select("*").eq("id", session_id).execute()
        return result.data[0] if result.data else None
    
    def update_status(self, session_id: str, status: str, progress: Optional[int] = None) -> Dict[str, Any]:
        update_data = {"status": status}
        if progress is not None:
            update_data["progress"] = progress
        
        if status == "running":
            update_data["started_at"] = datetime.utcnow().isoformat()
        elif status in ("completed", "failed"):
            update_data["finished_at"] = datetime.utcnow().isoformat()
        
        result = self.supabase.table("prospecting_sessions").update(update_data).eq("id", session_id).execute()
        return result.data[0] if result.data else {}
    
    def add_log(self, session_id: str, message: str, level: str = "info") -> Dict[str, Any]:
        log_data = {
            "id": str(uuid4()),
            "session_id": session_id,
            "message": message,
            "level": level,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        result = self.supabase.table("prospecting_session_logs").insert(log_data).execute()
        return result.data[0] if result.data else log_data
    
    def get_logs(self, session_id: str) -> List[Dict[str, Any]]:
        result = self.supabase.table("prospecting_session_logs").select("*").eq("session_id", session_id).order("created_at").execute()
        return result.data if result.data else []
