import sys
import os
import pytest
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.infrastructure.database import SupabaseDatabase
from src.config.settings import settings

def test_supabase_connection():
    """Prueba simple de conexión a Supabase usando la nueva arquitectura."""
    try:
        print(f"Testing connection to: {settings.SUPABASE_URL}")
        db = SupabaseDatabase()
        # Verificar que el cliente existe
        assert db.client is not None
        print("✅ Cliente inicializado correctamente.")
        
        # Realizar una consulta simple (count)
        res = db.client.table(settings.TABLE_NAME).select("count", count="exact").execute()
        print(f"✅ Conexión exitosa. Filas en '{settings.TABLE_NAME}': {res.count}")
        
    except Exception as e:
        pytest.fail(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    test_supabase_connection()