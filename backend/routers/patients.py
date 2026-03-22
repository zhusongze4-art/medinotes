from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.schemas import PatientRecord, PatientListItem
from dependencies import redis_service, rag_service

router = APIRouter()


@router.get("/patients", response_model=List[PatientListItem])
async def list_patients(query: Optional[str] = Query(default=None)):
    if query:
        return redis_service.search_by_name(query)
    return redis_service.get_all_patients()


@router.get("/patients/{patient_id}", response_model=PatientRecord)
async def get_patient(patient_id: str):
    record = redis_service.get_patient(patient_id)
    if not record:
        raise HTTPException(status_code=404, detail="Patient not found")
    return record


@router.post("/search/similar")
async def search_similar_cases(query: str, top_k: int = 5):
    results = rag_service.search_similar(query, top_k)
    return {"results": results}