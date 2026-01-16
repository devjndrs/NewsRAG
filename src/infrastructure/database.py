from supabase import create_client, Client
from typing import List
from src.domain.interfaces import VectorDatabase
from src.domain.entities import Insight
from src.config.settings import settings

class SupabaseDatabase(VectorDatabase):
    def __init__(self):
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.table_name = settings.TABLE_NAME

    def insert_insights(self, insights: List[Insight]) -> None:
        data = [
            {
                "title": i.title,
                "content": i.content,
                "category": i.category,
                "embedding": i.embedding
            }
            for i in insights
        ]
        self.client.table(self.table_name).insert(data).execute()

    def search_insights(self, query_embedding: List[float], threshold: float = 0.5, count: int = 5) -> List[Insight]:
        result = self.client.rpc("match_insights", {
            "query_embedding": query_embedding,
            "match_threshold": threshold,
            "match_count": count
        }).execute()
        
        insights = []
        if result.data:
            for item in result.data:
                insights.append(Insight(
                    title=item['title'],
                    content=item['content'],
                    category=item['category'],
                    id=item.get('id')
                ))
        return insights
