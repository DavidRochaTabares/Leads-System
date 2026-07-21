from typing import List, Dict, Any, Optional
from supabase import Client


class CompanyRepository:
    def __init__(self, supabase: Client):
        self.supabase = supabase
    
    def is_duplicate(self, session_id: str, google_maps_url: str) -> bool:
        """Check if company already exists for this session"""
        result = self.supabase.table("companies").select("id").eq("session_id", session_id).eq("google_maps_url", google_maps_url).execute()
        return len(result.data) > 0
    
    def create_company(self, session_id: str, name: str, google_maps_url: str, 
                      website: Optional[str] = None, phone: Optional[str] = None,
                      address: Optional[str] = None, rating: Optional[float] = None,
                      review_count: Optional[int] = None) -> Dict[str, Any]:
        """Save a company to database"""
        company_data = {
            "session_id": session_id,
            "name": name,
            "google_maps_url": google_maps_url,
            "website": website,
            "phone": phone,
            "address": address,
            "rating": rating,
            "review_count": review_count,
        }
        
        result = self.supabase.table("companies").insert(company_data).execute()
        return result.data[0] if result.data else company_data
    
    def get_companies_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all companies for a session"""
        result = self.supabase.table("companies").select("*").eq("session_id", session_id).order("created_at").execute()
        return result.data if result.data else []
    
    def count_companies_by_session(self, session_id: str) -> int:
        """Count companies for a session"""
        result = self.supabase.table("companies").select("id", count="exact").eq("session_id", session_id).execute()
        return result.count if result.count else 0
    
    def update_website_data(self, company_id: str, website_data: Dict[str, Any]) -> None:
        """Update company with scraped website data"""
        from datetime import datetime
        update_data = {
            "emails": website_data.get("emails", []),
            "social_links": website_data.get("social_links", {}),
            "features": website_data.get("features", {}),
            "recommended_services": website_data.get("recommended_services", []),
            "website_scraped_at": datetime.utcnow().isoformat()
        }
        self.supabase.table("companies").update(update_data).eq("id", company_id).execute()
    
    def update_ai_analysis(self, company_id: str, ai_analysis: Dict[str, Any]) -> None:
        """Update company with AI analysis results"""
        from datetime import datetime
        update_data = {
            "ai_analysis": ai_analysis,
            "ai_analyzed_at": datetime.utcnow().isoformat()
        }
        self.supabase.table("companies").update(update_data).eq("id", company_id).execute()
