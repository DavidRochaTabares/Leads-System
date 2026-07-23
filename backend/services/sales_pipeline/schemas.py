from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel


class PipelineStage:
    """Valid pipeline stages"""
    CREATED = "CREATED"
    STRATEGY_READY = "STRATEGY_READY"
    MESSAGES_READY = "MESSAGES_READY"
    READY_TO_CONTACT = "READY_TO_CONTACT"
    CONTACTED = "CONTACTED"
    WAITING_RESPONSE = "WAITING_RESPONSE"
    FOLLOW_UP = "FOLLOW_UP"
    INTERESTED = "INTERESTED"
    MEETING = "MEETING"
    CLIENT = "CLIENT"
    LOST = "LOST"


class CommercialOpportunity(BaseModel):
    """Commercial opportunity (not technical pain point)"""
    description: str  # e.g., "Potential to automate first customer contact"


class BusinessStrength(BaseModel):
    """Business strength with commercial implication"""
    strength: str
    opportunity: str  # How this strength creates a sales opportunity


class SalesBrief(BaseModel):
    """
    Sales Brief - One-page cheat sheet for salesperson
    
    Answers: "If I had to message this company in 30 seconds, what do I need to know?"
    """
    # 1. WHAT WE SHOULD SELL
    primary_service: str
    secondary_service: Optional[str] = None
    estimated_opportunity: str  # Low, Medium, High
    why_this_service: List[str]  # Max 3 justifications for service selection
    
    # 2. WHY THIS COMPANY (max 3 bullet points)
    why_this_company: List[str]  # Max 3, each max 10 words
    
    # 3. HOW TO SELL
    lead_with: str  # What to lead conversation with (practical, not generic)
    main_business_benefit: str  # Main value in business terms
    communication_style: str  # Full recommendation (not just tone)
    decision_maker: str  # Who to contact
    
    # Supporting Information
    commercial_opportunities: List[CommercialOpportunity]  # Not pain points
    business_strengths: List[BusinessStrength]  # With commercial implications
    
    # Success Metrics
    estimated_success_probability: int  # 0-100


class SalesPipeline(BaseModel):
    """Sales Pipeline - Center of commercial workflow"""
    id: str
    company_id: str
    status: str
    current_stage: str
    strategy: Optional[Dict[str, Any]] = None
    strategy_status: str
    messages_status: str
    automation_status: str
    conversation_status: str
    next_action: Optional[str] = None
    next_action_date: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PipelineCreate(BaseModel):
    """Create new pipeline"""
    company_id: str


class PipelineUpdate(BaseModel):
    """Update pipeline"""
    status: Optional[str] = None
    current_stage: Optional[str] = None
    strategy: Optional[Dict[str, Any]] = None
    strategy_status: Optional[str] = None
    messages_status: Optional[str] = None
    automation_status: Optional[str] = None
    conversation_status: Optional[str] = None
    next_action: Optional[str] = None
    next_action_date: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    completed: Optional[bool] = None
