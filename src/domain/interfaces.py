from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .entities import Insight

class EmbeddingService(ABC):
    @abstractmethod
    def generate_embedding(self, text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> List[float]:
        pass

class VectorDatabase(ABC):
    @abstractmethod
    def insert_insights(self, insights: List[Insight]) -> None:
        pass
    
    @abstractmethod
    def search_insights(self, query_embedding: List[float], threshold: float = 0.5, count: int = 5) -> List[Insight]:
        pass

    @abstractmethod
    def get_existing_urls(self, urls: List[str]) -> List[str]:
        pass

class LLMService(ABC):
    @abstractmethod
    def generate_summary(self, texts: List[str]) -> str:
        """Genera un resumen analítico correlacionando los textos proporcionados."""
        pass

    @abstractmethod
    def explain_relevance(self, query: str, insights: List[Any]) -> List[str]:
        """Genera una breve explicación de por qué cada insight es relevante para la query."""
        pass
