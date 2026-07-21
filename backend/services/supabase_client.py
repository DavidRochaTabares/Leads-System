from supabase import create_client, Client
from core.config import settings


class SupabaseClient:
    _instance: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            cls._instance = create_client(settings.supabase_url, settings.supabase_key)
        return cls._instance
    
    @classmethod
    def get_admin_client(cls) -> Client:
        return create_client(settings.supabase_url, settings.supabase_service_key)


def get_supabase() -> Client:
    return SupabaseClient.get_client()
