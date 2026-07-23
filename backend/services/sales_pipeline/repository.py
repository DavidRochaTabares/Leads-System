from typing import Optional, List, Dict, Any
from supabase import Client
from datetime import datetime


class SalesPipelineRepository:
    """Repository for Sales Pipeline data access"""
    
    def __init__(self, supabase: Client):
        self.supabase = supabase
    
    def create_pipeline(self, company_id: str) -> Dict[str, Any]:
        """Create a new sales pipeline for a company"""
        result = self.supabase.table('sales_pipelines').insert({
            'company_id': company_id,
            'status': 'created',
            'current_stage': 'CREATED',
            'strategy_status': 'pending',
            'messages_status': 'pending',
            'automation_status': 'pending',
            'conversation_status': 'pending',
            'completed': False
        }).execute()
        
        return result.data[0] if result.data else None
    
    def get_by_id(self, pipeline_id: str) -> Optional[Dict[str, Any]]:
        """Get pipeline by ID"""
        result = self.supabase.table('sales_pipelines').select('*').eq('id', pipeline_id).execute()
        return result.data[0] if result.data else None
    
    def get_by_company_id(self, company_id: str) -> List[Dict[str, Any]]:
        """Get all pipelines for a company (ordered by most recent)"""
        result = self.supabase.table('sales_pipelines').select('*').eq(
            'company_id', company_id
        ).order('created_at', desc=True).execute()
        return result.data if result.data else []
    
    def get_active_pipeline(self, company_id: str) -> Optional[Dict[str, Any]]:
        """Get the most recent active pipeline for a company"""
        result = self.supabase.table('sales_pipelines').select('*').eq(
            'company_id', company_id
        ).eq('completed', False).order('created_at', desc=True).limit(1).execute()
        return result.data[0] if result.data else None
    
    def update_pipeline(self, pipeline_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update pipeline fields"""
        result = self.supabase.table('sales_pipelines').update(updates).eq(
            'id', pipeline_id
        ).execute()
        return result.data[0] if result.data else None
    
    def update_stage(self, pipeline_id: str, stage: str) -> Dict[str, Any]:
        """Update pipeline stage"""
        return self.update_pipeline(pipeline_id, {
            'current_stage': stage,
            'last_activity': datetime.utcnow().isoformat()
        })
    
    def update_strategy(self, pipeline_id: str, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Update pipeline strategy"""
        return self.update_pipeline(pipeline_id, {
            'strategy': strategy,
            'strategy_status': 'completed',
            'current_stage': 'STRATEGY_READY',
            'last_activity': datetime.utcnow().isoformat()
        })
    
    def mark_completed(self, pipeline_id: str, final_stage: str) -> Dict[str, Any]:
        """Mark pipeline as completed"""
        return self.update_pipeline(pipeline_id, {
            'completed': True,
            'completed_at': datetime.utcnow().isoformat(),
            'current_stage': final_stage,
            'last_activity': datetime.utcnow().isoformat()
        })
    
    def get_pipelines_by_stage(self, stage: str) -> List[Dict[str, Any]]:
        """Get all pipelines in a specific stage"""
        result = self.supabase.table('sales_pipelines').select('*').eq(
            'current_stage', stage
        ).order('created_at', desc=True).execute()
        return result.data if result.data else []
    
    def get_all_active_pipelines(self) -> List[Dict[str, Any]]:
        """Get all active (not completed) pipelines"""
        result = self.supabase.table('sales_pipelines').select('*').eq(
            'completed', False
        ).order('created_at', desc=True).execute()
        return result.data if result.data else []
