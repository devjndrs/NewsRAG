from google import genai
from typing import List
from src.domain.interfaces import EmbeddingService
from src.config.settings import settings

class GeminiEmbeddingService(EmbeddingService):
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.EMBEDDING_MODEL

    def generate_embedding(self, text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> List[float]:
        try:
            result = self.client.models.embed_content(
                model=self.model_name,
                contents=text,
                config={'task_type': task_type}
            )
            return result.embeddings[0].values
        except Exception as e:
            # Handle logging usage in real implementation
            print(f"Error generando embedding: {e}")
            raise e
