# MediNotes — AI-Powered Electronic Health Record System

An end-to-end clinical documentation platform that transforms unstructured patient-physician dialogues into structured SOAP clinical summaries using LLM, with RAG-based similar case retrieval and a dual-database analytics architecture.

## Architecture

```
Patient Dialogue → LLM Pipeline (Qwen2.5) → Structured SOAP Summary
                                                    ↓
                              ┌──────────────────────┼──────────────────────┐
                              ↓                      ↓                      ↓
                           Redis                  DuckDB                ChromaDB
                      (Record Storage)      (SQL Analytics)        (Vector Search)
                              ↓                      ↓                      ↓
                       Patient Search        Analytics Dashboard    Similar Case Retrieval
```

## Tech Stack

- **Backend**: FastAPI, Python
- **Frontend**: React, Ant Design, Recharts
- **LLM**: Qwen2.5-1.5B-Instruct via Hugging Face Transformers
- **Databases**: Redis (key-value store), DuckDB (analytical queries), ChromaDB (vector search)
- **Embedding**: all-MiniLM-L6-v2 (Sentence Transformers)
- **DevOps**: Docker Compose, AWS EC2

## Features

- **LLM Summarization Pipeline**: Converts patient-physician dialogues into structured SOAP notes with Pydantic schema validation and automatic retry logic
- **Dual-Database Architecture**: Redis for real-time record CRUD, DuckDB for population-level SQL analytics
- **RAG Clinical Decision Support**: Semantic similarity search across patient histories using sentence embeddings and ChromaDB
- **Patient Search**: Case-insensitive substring matching across patient records
- **Analytics Dashboard**: Age statistics, age distribution charts, and medication frequency analysis

## Getting Started

### Prerequisites
- Python 3.9 - 3.12
- Node.js 18+
- Docker (for Redis)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Redis
```bash
docker run -d -p 6379:6379 --name medinotes-redis redis:7-alpine
```

### Docker Compose (all services)
```bash
docker-compose up --build
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ingest` | Submit dialogue, generate SOAP summary |
| GET | `/api/patients` | List all patients (with optional search) |
| GET | `/api/patients/{id}` | Get patient detail |
| POST | `/api/search/similar` | RAG-based similar case retrieval |
| GET | `/api/analytics` | Age stats, distribution, medication frequency |
| GET | `/api/health` | Health check |
