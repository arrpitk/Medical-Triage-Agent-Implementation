from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from typing import List

class ConfigurableRAG:
    def __init__(self, config: dict):
        self.embedder = HuggingFaceEmbeddings(
            model_name=config["embedding_model"]
        )
        self.vectorstore = Chroma(
            embedding_function=self.embedder,
            persist_directory=None  # In-memory
        )
        
    def add_documents(self, documents: List[str]):
        self.vectorstore.add_texts(documents)
        
    def query(self, question: str, k: int = 3) -> List[str]:
        return self.vectorstore.similarity_search(question, k=k)
    