from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from services.supabase_client import get_supabase
from services.sales_pipeline.pipeline_service import PipelineService
from services.sales_pipeline.schemas import PipelineCreate, PipelineUpdate

router = APIRouter(prefix="/sales-pipeline", tags=["sales-pipeline"])


@router.get("/health")
def pipeline_health():
    return {"status": "ok"}


@router.post("/pipelines")
def create_pipeline(
    payload: PipelineCreate,
    supabase: Client = Depends(get_supabase)
):
    """Create a new sales pipeline for a company"""
    service = PipelineService(supabase)
    pipeline = service.create_pipeline_for_company(payload.company_id)
    return pipeline


@router.get("/pipelines/{pipeline_id}")
def get_pipeline(
    pipeline_id: str,
    supabase: Client = Depends(get_supabase)
):
    """Get pipeline by ID"""
    service = PipelineService(supabase)
    pipeline = service.get_pipeline(pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline


@router.get("/companies/{company_id}/pipelines")
def get_company_pipelines(
    company_id: str,
    supabase: Client = Depends(get_supabase)
):
    """Get all pipelines for a company"""
    service = PipelineService(supabase)
    pipelines = service.get_company_pipelines(company_id)
    return pipelines


@router.get("/companies/{company_id}/active-pipeline")
def get_active_pipeline(
    company_id: str,
    supabase: Client = Depends(get_supabase)
):
    """Get active pipeline for a company"""
    service = PipelineService(supabase)
    pipeline = service.get_active_pipeline(company_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="No active pipeline found")
    return pipeline


@router.post("/pipelines/{pipeline_id}/generate-strategy")
def generate_strategy(
    pipeline_id: str,
    supabase: Client = Depends(get_supabase)
):
    """Generate commercial strategy for a pipeline"""
    service = PipelineService(supabase)
    try:
        pipeline = service.generate_strategy(pipeline_id)
        return pipeline
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/pipelines/{pipeline_id}/stage")
def update_stage(
    pipeline_id: str,
    new_stage: str,
    supabase: Client = Depends(get_supabase)
):
    """Update pipeline stage"""
    service = PipelineService(supabase)
    pipeline = service.update_stage(pipeline_id, new_stage)
    return pipeline


@router.post("/pipelines/{pipeline_id}/mark-client")
def mark_as_client(
    pipeline_id: str,
    supabase: Client = Depends(get_supabase)
):
    """Mark pipeline as successfully converted to client"""
    service = PipelineService(supabase)
    pipeline = service.mark_as_client(pipeline_id)
    return pipeline


@router.post("/pipelines/{pipeline_id}/mark-lost")
def mark_as_lost(
    pipeline_id: str,
    supabase: Client = Depends(get_supabase)
):
    """Mark pipeline as lost"""
    service = PipelineService(supabase)
    pipeline = service.mark_as_lost(pipeline_id)
    return pipeline


@router.post("/pipelines/{pipeline_id}/generate-whatsapp-message")
def generate_whatsapp_message(
    pipeline_id: str,
    supabase: Client = Depends(get_supabase)
):
    """Generate WhatsApp message for a pipeline"""
    service = PipelineService(supabase)
    try:
        pipeline = service.generate_whatsapp_message(pipeline_id)
        return pipeline
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pipelines/{pipeline_id}/regenerate-whatsapp-message")
def regenerate_whatsapp_message(
    pipeline_id: str,
    supabase: Client = Depends(get_supabase)
):
    """Regenerate WhatsApp message for a pipeline"""
    service = PipelineService(supabase)
    try:
        pipeline = service.regenerate_whatsapp_message(pipeline_id)
        return pipeline
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pipelines/{pipeline_id}/send-whatsapp-message")
def send_whatsapp_message(
    pipeline_id: str,
    supabase: Client = Depends(get_supabase)
):
    """Send WhatsApp message for a pipeline"""
    service = PipelineService(supabase)
    try:
        pipeline = service.send_whatsapp_message(pipeline_id)
        return pipeline
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
