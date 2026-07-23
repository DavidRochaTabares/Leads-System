from typing import Dict, Any, Optional
from supabase import Client
from .repository import SalesPipelineRepository
from .strategy_engine import SalesStrategyEngine
from .schemas import PipelineStage


class PipelineService:
    """
    Sales Pipeline Service
    
    Manages the complete pipeline lifecycle:
    1. Pipeline creation
    2. Strategy generation
    3. Stage transitions
    4. Pipeline management
    """
    
    def __init__(self, supabase: Client):
        self.repository = SalesPipelineRepository(supabase)
        self.strategy_engine = SalesStrategyEngine()
        self.supabase = supabase
    
    def create_pipeline_for_company(self, company_id: str) -> Dict[str, Any]:
        """
        Create a new sales pipeline for a company
        
        This is called automatically after AI Analysis completes
        """
        print(f"[PIPELINE SERVICE] Creating pipeline for company {company_id}")
        
        # Create pipeline in CREATED stage
        pipeline = self.repository.create_pipeline(company_id)
        
        if not pipeline:
            raise Exception("Failed to create pipeline")
        
        print(f"[PIPELINE SERVICE] Pipeline created: {pipeline['id']}")
        return pipeline
    
    def generate_strategy(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Generate commercial strategy for a pipeline
        
        This consumes:
        - Company data
        - AI Analysis
        - Lead Score
        
        And produces:
        - Commercial Strategy
        """
        print(f"[PIPELINE SERVICE] Generating strategy for pipeline {pipeline_id}")
        
        # Get pipeline
        pipeline = self.repository.get_by_id(pipeline_id)
        if not pipeline:
            raise Exception("Pipeline not found")
        
        # Get company data
        company = self._get_company_data(pipeline['company_id'])
        if not company:
            raise Exception("Company not found")
        
        # Check if AI Analysis exists
        if not company.get('ai_analysis'):
            raise Exception("AI Analysis not found. Cannot generate strategy without analysis.")
        
        # Prepare data for strategy engine
        company_data = {
            'name': company.get('name'),
            'industry': company.get('industry'),
            'location': company.get('location'),
            'website': company.get('website'),
            'ai_analysis': company.get('ai_analysis'),
            'lead_score': company.get('ai_analysis', {}).get('lead_score', 50),
            'emails': company.get('emails', []),
            'social_links': company.get('social_links', {}),
            'features': company.get('features', {})
        }
        
        # Generate strategy using AI
        strategy = self.strategy_engine.generate_strategy(company_data)
        
        # Update pipeline with strategy
        updated_pipeline = self.repository.update_strategy(pipeline_id, strategy)
        
        print(f"[PIPELINE SERVICE] Strategy generated and saved")
        return updated_pipeline
    
    def get_pipeline(self, pipeline_id: str) -> Optional[Dict[str, Any]]:
        """Get pipeline by ID"""
        return self.repository.get_by_id(pipeline_id)
    
    def get_company_pipelines(self, company_id: str) -> list:
        """Get all pipelines for a company"""
        return self.repository.get_by_company_id(company_id)
    
    def get_active_pipeline(self, company_id: str) -> Optional[Dict[str, Any]]:
        """Get active pipeline for a company"""
        return self.repository.get_active_pipeline(company_id)
    
    def update_stage(self, pipeline_id: str, new_stage: str) -> Dict[str, Any]:
        """Update pipeline stage"""
        return self.repository.update_stage(pipeline_id, new_stage)
    
    def mark_as_client(self, pipeline_id: str) -> Dict[str, Any]:
        """Mark pipeline as successfully converted to client"""
        return self.repository.mark_completed(pipeline_id, PipelineStage.CLIENT)
    
    def mark_as_lost(self, pipeline_id: str) -> Dict[str, Any]:
        """Mark pipeline as lost"""
        return self.repository.mark_completed(pipeline_id, PipelineStage.LOST)
    
    def _get_company_data(self, company_id: str) -> Optional[Dict[str, Any]]:
        """Get company data from database"""
        result = self.supabase.table('companies').select('*').eq('id', company_id).execute()
        return result.data[0] if result.data else None
