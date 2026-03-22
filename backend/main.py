import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ingest, patients, analytics

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s"
)

app = FastAPI(
    title="MediNotes API",
    description="AI-Powered Electronic Health Record System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/api")
app.include_router(patients.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}