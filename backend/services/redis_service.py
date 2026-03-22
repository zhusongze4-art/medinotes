import json
import logging
from typing import List, Optional
from redis import Redis
from models.schemas import PatientRecord, PatientListItem
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

logger = logging.getLogger(__name__)


class RedisService:
    def __init__(self):
        self.client = Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )
        logger.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")

    def save_patient(self, record: PatientRecord):
        key = f"patient:{record.patient_id}"
        self.client.set(key, record.model_dump_json())
        self.client.sadd("patient:ids", record.patient_id)
        logger.info(f"Saved patient {record.patient_id}")

    def get_patient(self, patient_id: str) -> Optional[PatientRecord]:
        key = f"patient:{patient_id}"
        raw = self.client.get(key)
        if not raw:
            return None
        return PatientRecord.model_validate_json(raw)

    def get_all_patients(self) -> List[PatientListItem]:
        all_ids = self.client.smembers("patient:ids")
        results = []
        for pid in all_ids:
            record = self.get_patient(pid)
            if record:
                results.append(PatientListItem(
                    patient_id=record.patient_id,
                    patient_name=record.summary.patient_name,
                    age=record.summary.age,
                    assessment=record.summary.assessment
                ))
        return results

    def search_by_name(self, query: str) -> List[PatientListItem]:
        all_patients = self.get_all_patients()
        return [
            p for p in all_patients
            if query.lower() in p.patient_name.lower()
        ]

    def get_all_records(self) -> List[PatientRecord]:
        all_ids = self.client.smembers("patient:ids")
        results = []
        for pid in all_ids:
            record = self.get_patient(pid)
            if record:
                results.append(record)
        return results