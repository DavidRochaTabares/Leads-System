from typing import Dict, Any, Optional
from supabase import Client
from .repository import SalesPipelineRepository
from .strategy_engine import SalesStrategyEngine
from .whatsapp_message_engine import WhatsAppMessageEngine
from .schemas import PipelineStage
from services.whatsapp_service import WhatsAppService


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
        self.whatsapp_engine = WhatsAppMessageEngine()
        self.whatsapp_service = WhatsAppService()
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
    
    def generate_whatsapp_message(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Generate WhatsApp message for a pipeline
        
        Uses:
        - Company data
        - Sales Brief
        
        Produces:
        - Personalized WhatsApp message
        """
        print(f"[PIPELINE SERVICE] Generating WhatsApp message for pipeline {pipeline_id}")
        
        # Get pipeline
        pipeline = self.repository.get_by_id(pipeline_id)
        if not pipeline:
            raise Exception("Pipeline not found")
        
        # Check if strategy exists
        if not pipeline.get('strategy'):
            raise Exception("Sales Brief not found. Generate strategy first.")
        
        # Get company data
        company = self._get_company_data(pipeline['company_id'])
        if not company:
            raise Exception("Company not found")
        
        # Prepare data for message engine
        company_data = {
            'name': company.get('name'),
            'industry': company.get('industry'),
            'location': company.get('location'),
            'website': company.get('website')
        }
        
        sales_brief = pipeline.get('strategy')
        
        # Generate message using AI
        whatsapp_message = self.whatsapp_engine.generate_message(company_data, sales_brief)
        
        # Update pipeline with message
        updated_pipeline = self.repository.update_pipeline(pipeline_id, {
            'whatsapp_message': whatsapp_message,
            'current_stage': PipelineStage.MESSAGES_READY
        })
        
        print(f"[PIPELINE SERVICE] WhatsApp message generated and saved")
        return updated_pipeline
    
    def regenerate_whatsapp_message(self, pipeline_id: str) -> Dict[str, Any]:
        """Regenerate WhatsApp message with increased version"""
        print(f"[PIPELINE SERVICE] Regenerating WhatsApp message for pipeline {pipeline_id}")
        
        # Get pipeline
        pipeline = self.repository.get_by_id(pipeline_id)
        if not pipeline:
            raise Exception("Pipeline not found")
        
        # Check if strategy exists
        if not pipeline.get('strategy'):
            raise Exception("Sales Brief not found. Generate strategy first.")
        
        # Get company data
        company = self._get_company_data(pipeline['company_id'])
        if not company:
            raise Exception("Company not found")
        
        # Prepare data
        company_data = {
            'name': company.get('name'),
            'industry': company.get('industry'),
            'location': company.get('location'),
            'website': company.get('website')
        }
        
        sales_brief = pipeline.get('strategy')
        
        # Get current version
        current_message = pipeline.get('whatsapp_message', {})
        current_version = current_message.get('version', 0)
        
        # Regenerate message
        whatsapp_message = self.whatsapp_engine.regenerate_message(
            company_data, 
            sales_brief,
            current_version
        )
        
        # Update pipeline
        updated_pipeline = self.repository.update_pipeline(pipeline_id, {
            'whatsapp_message': whatsapp_message
        })
        
        print(f"[PIPELINE SERVICE] WhatsApp message regenerated (version {whatsapp_message['version']})")
        return updated_pipeline
    
    def send_whatsapp_message(self, pipeline_id: str, use_template: bool = True) -> Dict[str, Any]:
        """
        Send WhatsApp message for a pipeline
        
        Flow:
        1. Get pipeline and validate message exists
        2. Get company phone number
        3. Send via WhatsApp API (template for cold outreach)
        4. Update pipeline status
        
        Args:
            pipeline_id: Pipeline ID
            use_template: If True, use template message (for cold outreach)
                         If False, use free text (only works within 24h window)
        """
        print(f"[PIPELINE SERVICE] Sending WhatsApp message for pipeline {pipeline_id}")
        
        # Get pipeline
        pipeline = self.repository.get_by_id(pipeline_id)
        if not pipeline:
            raise Exception("Pipeline not found")
        
        # Get company data
        company = self._get_company_data(pipeline['company_id'])
        if not company:
            raise Exception("Company not found")
        
        # Get phone number
        phone = company.get('phone')
        if not phone:
            raise Exception("Company phone number not found")
        
        # Validate phone number
        if not self.whatsapp_service.validate_phone_number(phone):
            raise Exception(f"Invalid phone number format: {phone}")
        
        # Get Sales Brief
        sales_brief = pipeline.get('strategy')
        if not sales_brief:
            raise Exception("Sales Brief not found. Generate strategy first.")
        
        # Send message
        if use_template:
            # Use template message (for cold outreach)
            whatsapp_message = pipeline.get('whatsapp_message')
            
            # Check if we have saved template variables
            if whatsapp_message and whatsapp_message.get('variables'):
                # Use saved variables
                template_name = whatsapp_message.get('template_name', 'cold_outreach_v2')
                template_variables = whatsapp_message.get('variables')
                print(f"[PIPELINE SERVICE] Using saved template variables")
            else:
                # Generate new variables if not saved
                import os
                template_name = os.getenv('WHATSAPP_TEMPLATE_NAME', 'cold_outreach_v2')
                template_variables = self.whatsapp_engine.generate_template_variables(company, sales_brief)
                print(f"[PIPELINE SERVICE] Generated new template variables")
            
            print(f"[PIPELINE SERVICE] Using template: {template_name}")
            print(f"[PIPELINE SERVICE] Variables: {template_variables}")
            result = self.whatsapp_service.send_template_message(
                phone, 
                template_name, 
                template_variables
            )
        else:
            # Use free text message (only works within 24h window)
            whatsapp_message = pipeline.get('whatsapp_message')
            if not whatsapp_message or not whatsapp_message.get('message'):
                raise Exception("WhatsApp message not generated. Generate message first.")
            
            message_text = whatsapp_message.get('message')
            print(f"[PIPELINE SERVICE] Using free text message")
            result = self.whatsapp_service.send_message(phone, message_text)
        
        if result.get('success'):
            # Update pipeline: message sent successfully
            updated_pipeline = self.repository.update_pipeline(pipeline_id, {
                'message_sent_at': result.get('sent_at'),
                'whatsapp_message_id': result.get('message_id'),
                'delivery_status': 'sent',
                'current_stage': PipelineStage.WAITING_RESPONSE,
                'last_activity': result.get('sent_at'),
                'last_error': None
            })
            
            print(f"[PIPELINE SERVICE] Message sent successfully. ID: {result.get('message_id')}")
            return updated_pipeline
        else:
            # Update pipeline: message failed
            updated_pipeline = self.repository.update_pipeline(pipeline_id, {
                'delivery_status': 'failed',
                'last_error': result.get('error'),
                'last_activity': result.get('sent_at')
            })
            
            print(f"[PIPELINE SERVICE] Message sending failed: {result.get('error')}")
            raise Exception(f"Failed to send message: {result.get('error')}")
    
    def _get_company_data(self, company_id: str) -> Optional[Dict[str, Any]]:
        """Get company data from database"""
        result = self.supabase.table('companies').select('*').eq('id', company_id).execute()
        return result.data[0] if result.data else None
