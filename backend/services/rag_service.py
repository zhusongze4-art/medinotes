import logging
from typing import List, Dict
import chromadb
from sentence_transformers import SentenceTransformer
from config import CHROMA_PATH, EMBEDDING_MODEL_NAME

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self.chroma_client.get_or_create_collection(
            name="patient_summaries",
            metadata={"hnsw:space": "cosine"}
        )
        self.encoder = SentenceTransformer(EMBEDDING_MODEL_NAME)
        logger.info("RAG service initialized")

    def index_summary(self, patient_id: str, summary_text: str):
        embedding = self.encoder.encode(summary_text).tolist()
        self.collection.upsert(
            ids=[patient_id],
            embeddings=[embedding],
            documents=[summary_text]
        )
        logger.info(f"Indexed patient {patient_id} into ChromaDB")

    def search_similar(self, query: str, top_k: int = 5) -> List[Dict]:
        query_embedding = self.encoder.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        similar_cases = []
        for i in range(len(results["ids"][0])):
            similar_cases.append({
                "patient_id": results["ids"][0][i],
                "summary": results["documents"][0][i],
                "similarity": round(1 - results["distances"][0][i], 4)
            })
        return similar_cases