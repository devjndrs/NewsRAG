from typing import List, Optional
from src.domain.entities import Insight
from src.domain.interfaces import EmbeddingService, VectorDatabase, LLMService
from src.infrastructure.api_client import DataProvider

class IngestionPipeline:
    def __init__(self, embedding_service: EmbeddingService, database: VectorDatabase, llm_service: LLMService):
        self.embedding_service = embedding_service
        self.database = database
        self.llm_service = llm_service

    def run(self) -> tuple[str, list]:
        # 1. Fetch Data
        raw_data = DataProvider.fetch_data()
        
        if not raw_data:
            return "No se encontraron noticias recientes.", []

        # Deduplication Logic
        urls = [item.get('url') for item in raw_data if item.get('url')]
        existing_urls = set(self.database.get_existing_urls(urls))
        
        insights = []
        texts_for_summary = []
        new_items_count = 0
        
        print(f"Procesando {len(raw_data)} noticias (Ya existen: {len(existing_urls)})...")
        
        for item in raw_data:
            # Siempre añadimos al contexto del resumen para tener el panorama completo
            texts_for_summary.append(f"Title: {item['title']}\nContent: {item['content']}")
            
            # Solo procesamos (embedding + insert) si NO existe en la BD
            if item.get('url') not in existing_urls:
                # 2. Embed
                emb = self.embedding_service.generate_embedding(item['content'], task_type="RETRIEVAL_DOCUMENT")
                
                # 3. Create Entity
                insight = Insight(
                    title=item['title'],
                    content=item['content'],
                    category=item['category'],
                    url=item.get('url'),
                    embedding=emb
                )
                insights.append(insight)
                new_items_count += 1
        
        # 4. Save (Only new items)
        if insights:
            self.database.insert_insights(insights)
            print(f"✅ Se insertaron {len(insights)} nuevas noticias.")
        else:
            print("✨ Todas las noticias ya existían en la base de datos. No se duplicó información.")
            
        # 5. Generate Summary (Based on ALL fetched news, fresh or old)
        print("Generando resumen de insights...")
        summary = self.llm_service.generate_summary(texts_for_summary)
        return summary, raw_data

class SearchPipeline:
    def __init__(self, embedding_service: EmbeddingService, database: VectorDatabase, llm_service: Optional[LLMService] = None):
        self.embedding_service = embedding_service
        self.database = database
        self.llm_service = llm_service

    def search(self, query: str) -> List[Insight]:
        # 1. Embed query
        query_embedding = self.embedding_service.generate_embedding(query, task_type="RETRIEVAL_QUERY")
        
        # 2. Search DB
        results = self.database.search_insights(query_embedding, threshold=0.4, count=5)
        
        # 3. Enhance with AI Explanation (if available)
        if results and self.llm_service:
            explanations = self.llm_service.explain_relevance(query, results)
            for i, res in enumerate(results):
                # Ensure we don't index out of bounds
                if i < len(explanations):
                    res.relevance = explanations[i]
        
        return results
