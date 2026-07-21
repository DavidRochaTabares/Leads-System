from fastapi import APIRouter
from api.schemas import HealthResponse
from core.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        environment=settings.environment,
        version="1.0.0"
    )
