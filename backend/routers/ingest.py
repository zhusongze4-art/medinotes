from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, HTTPException
from models.schemas import DialogueRequest, PatientRecord
from dependencies import llm_service, redis_service, duckdb_service, rag_service

router = APIRouter()


@router.post("/ingest")
async def ingest_dialogue(req: DialogueRequest):
    try:
        summary = llm_service.generate_summary(req.dialogue)

        patient_id = str(uuid4())
        record = PatientRecord(
            patient_id=patient_id,
            summary=summary,
            raw_dialogue=req.dialogue,
            created_at=datetime.now()
        )

        redis_service.save_patient(record)
        duckdb_service.sync_patient(patient_id, summary)
        rag_service.index_summary(patient_id, summary.model_dump_json())

        return {"patient_id": patient_id, "summary": summary}

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))