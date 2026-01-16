import sys
import os
import pytest
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.infrastructure.api_client import DataProvider
from src.infrastructure.database import SupabaseDatabase
from src.infrastructure.embeddings import GeminiEmbeddingService
from src.infrastructure.llm_service import GeminiLLMService
from src.application.pipeline import IngestionPipeline
from src.config.settings import settings

def test_guardian_fetch():
    """Prueba que la API de The Guardian devuelva datos correctamente."""
    print("\n--- Test 1: Fetching Data from The Guardian ---")
    try:
        data = DataProvider.fetch_data()
        
        if not data:
            pytest.skip("La API no devolvió datos (puede ser por filtros o límite de requests), pero no falló.")
        
        assert isinstance(data, list)
        print(f"✅ Se obtuvieron {len(data)} noticias.")
        
        if len(data) < 30:
            print("⚠️ ADVERTENCIA: Se obtuvieron menos de 30 noticias. Considera ampliar el rango de fechas.")
        
        first_item = data[0]
        assert "title" in first_item
        assert "content" in first_item
        assert "category" in first_item
        
        print(f"Ejemplo: {first_item['title']}")
        
    except Exception as e:
        pytest.fail(f"❌ Falló la extracción de datos: {e}")

def test_full_ingestion_flow():
    """Prueba el flujo completo: Fetch -> Embed -> Insert en Supabase -> Resumen."""
    print("\n--- Test 2: Full Ingestion Pipeline + Summary ---")
    
    # Validar configuración antes de empezar
    try:
        settings.validate()
        print("✅ Configuración validada.")
    except Exception as e:
        pytest.fail(f"❌ Error de configuración: {e}")

    try:
        # Inicializar servicios reales
        db = SupabaseDatabase()
        emb_service = GeminiEmbeddingService()
        llm_service = GeminiLLMService()
        
        pipeline = IngestionPipeline(emb_service, db, llm_service)
        
        # Ejecutar pipeline
        print("Ejecutando pipeline de ingestión y análisis...")
        summary = pipeline.run()
        
        print("\n" + "="*50)
        print("📊 RESUMEN DE INSIGHTS GENERADO:")
        print("="*50)
        print(summary)
        print("="*50)
        
        assert summary is not None
        assert len(summary) > 50
        
        print("✅ Pipeline ejecutado exitosamente.")
        
    except Exception as e:
        pytest.fail(f"❌ Falló el pipeline de ingestión: {e}")

if __name__ == "__main__":
    # Permite ejecutar el test directamente con python
    test_guardian_fetch()
    test_full_ingestion_flow()
