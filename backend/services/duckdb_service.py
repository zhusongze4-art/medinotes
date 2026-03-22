import logging
from typing import List
import duckdb
from models.schemas import (
    ClinicalSummary, AgeStats, AgeGroup,
    MedicationCount, AnalyticsResponse
)
from config import DUCKDB_PATH, TRACKED_MEDICATIONS

logger = logging.getLogger(__name__)


class DuckDBService:
    def __init__(self):
        self.conn = duckdb.connect(DUCKDB_PATH)
        self._init_table()
        logger.info(f"DuckDB initialized at {DUCKDB_PATH}")

    def _init_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id VARCHAR PRIMARY KEY,
                name VARCHAR,
                age INTEGER,
                diagnoses VARCHAR,
                medications VARCHAR,
                summary_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def sync_patient(self, patient_id: str, summary: ClinicalSummary):
        self.conn.execute("""
            INSERT OR REPLACE INTO patients
            (patient_id, name, age, diagnoses, medications, summary_text)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            patient_id,
            summary.patient_name,
            summary.age,
            ",".join(summary.diagnoses),
            ",".join(summary.medications),
            summary.model_dump_json()
        ])
        logger.info(f"Synced patient {patient_id} to DuckDB")

    def get_age_stats(self) -> AgeStats:
        row = self.conn.execute("""
            SELECT
                COUNT(*) as total,
                MIN(age) as min_age,
                MAX(age) as max_age,
                ROUND(AVG(age), 1) as avg_age
            FROM patients
            WHERE age IS NOT NULL
        """).fetchone()
        return AgeStats(
            total=row[0],
            min_age=row[1],
            max_age=row[2],
            avg_age=row[3]
        )

    def get_age_distribution(self) -> List[AgeGroup]:
        rows = self.conn.execute("""
            SELECT
                CASE
                    WHEN age < 30 THEN '<30'
                    WHEN age BETWEEN 30 AND 50 THEN '30-50'
                    WHEN age BETWEEN 51 AND 70 THEN '51-70'
                    ELSE '>70'
                END as age_group,
                COUNT(*) as count
            FROM patients
            WHERE age IS NOT NULL
            GROUP BY age_group
            ORDER BY age_group
        """).fetchall()
        return [AgeGroup(group=row[0], count=row[1]) for row in rows]

    def get_medication_frequency(self) -> List[MedicationCount]:
        results = []
        for med in TRACKED_MEDICATIONS:
            row = self.conn.execute("""
                SELECT COUNT(*) FROM patients
                WHERE LOWER(summary_text) LIKE ?
            """, [f"%{med.lower()}%"]).fetchone()
            if row[0] > 0:
                results.append(MedicationCount(medication=med, count=row[0]))
        results.sort(key=lambda x: x.count, reverse=True)
        return results

    def get_analytics(self) -> AnalyticsResponse:
        return AnalyticsResponse(
            age_stats=self.get_age_stats(),
            age_distribution=self.get_age_distribution(),
            medication_frequency=self.get_medication_frequency()
        )