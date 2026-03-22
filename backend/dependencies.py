from services.llm_service import LLMService
from services.redis_service import RedisService
from services.duckdb_service import DuckDBService
from services.rag_service import RAGService

llm_service = LLMService()
redis_service = RedisService()
duckdb_service = DuckDBService()
rag_service = RAGService()