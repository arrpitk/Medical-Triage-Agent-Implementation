# In rag_engine.py
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List
from loguru import logger

class ConfigurableRAG:
    def __init__(self, config: dict):  # Ensure config is a dictionary
        self.embedder = HuggingFaceEmbeddings(
            model_name=config.get("embedding_model", "sentence-transformers/all-MiniLM-L6-v2")
        )
        self.vectorstore = Chroma(
            embedding_function=self.embedder,
            persist_directory=None
        )
        
    def add_documents(self, documents: List[str]):
        self.vectorstore.add_texts(documents)
        
    def query(self, question: str, k: int = 3):
        try:
            return self.vectorstore.similarity_search(question, k=k)
        except Exception as e:
            logger.error(f"RAG query failed: {str(e)}")
            return []
    
    
    