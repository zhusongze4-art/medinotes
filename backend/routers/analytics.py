from fastapi import APIRouter
from models.schemas import AnalyticsResponse
from dependencies import duckdb_service

router = APIRouter()


@router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics():
    return duckdb_service.get_analytics()