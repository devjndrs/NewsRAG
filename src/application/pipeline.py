from typing import List
from src.domain.entities import Insight
from src.domain.interfaces import EmbeddingService, VectorDatabase
from src.infrastructure.api_client import DataProvider

class IngestionPipeline:
    def __init__(self, embedding_service: EmbeddingService, database: VectorDatabase):
        self.embedding_service = embedding_service
        self.database = database

    def run(self):
        # 1. Fetch Data
        raw_data = DataProvider.fetch_data()
        
        insights = []
        for item in raw_data:
            # 2. Embed
            emb = self.embedding_service.generate_embedding(item['content'], task_type="RETRIEVAL_DOCUMENT")
            
            # 3. Create Entity
            insight = Insight(
                title=item['title'],
                content=item['content'],
                category=item['category'],
                embedding=emb
            )
            insights.append(insight)
        
        # 4. Save
        if insights:
            self.database.insert_insights(insights)
            print(f"✅ Ingested {len(insights)} items.")

class SearchPipeline:
    def __init__(self, embedding_service: EmbeddingService, database: VectorDatabase):
        self.embedding_service = embedding_service
        self.database = database

    def search(self, query: str) -> List[Insight]:
        # 1. Embed query
        query_embedding = self.embedding_service.generate_embedding(query, task_type="RETRIEVAL_QUERY")
        
        # 2. Search DB
        results = self.database.search_insights(query_embedding, threshold=0.4, count=5)
        
        return results
