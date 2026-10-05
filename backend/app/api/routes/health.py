from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str
    service: str


@router.get("/health", response_model=HealthResponse)
async def check_health():
    """
    Service health check endpoint.
    Used by frontend, monitoring, and deployment checks.
    """
    return HealthResponse(
        status="ok",
        service="CampusAI Backend"
    )
