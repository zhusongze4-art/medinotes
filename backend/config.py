import os


# ============ Redis 配置 ============
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# ============ DuckDB 配置 ============
DUCKDB_PATH = os.getenv("DUCKDB_PATH", "medinotes.duckdb")

# ============ ChromaDB 配置 ============
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")

# ============ LLM 配置 ============
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "Qwen/Qwen2.5-1.5B-Instruct")
LLM_MAX_NEW_TOKENS = int(os.getenv("LLM_MAX_NEW_TOKENS", 512))
LLM_MAX_RETRIES = int(os.getenv("LLM_MAX_RETRIES", 3))

# ============ Embedding 模型配置 ============
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

# ============ 分析配置 ============
TRACKED_MEDICATIONS = [
    "sertraline", "cbt", "therapy", "ibuprofen",
    "metformin", "lisinopril", "amoxicillin", "omeprazole"
]