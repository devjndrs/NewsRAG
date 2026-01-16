import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # App Config
    APP_TITLE = "🚀 Tech-Insights: Buscador Semántico"
    EMBEDDING_MODEL = "text-embedding-004"
    TABLE_NAME = "tech_insights"
    
    @classmethod
    def validate(cls):
        missing = []
        if not cls.SUPABASE_URL: missing.append("SUPABASE_URL")
        if not cls.SUPABASE_KEY: missing.append("SUPABASE_KEY")
        if not cls.GEMINI_API_KEY: missing.append("GEMINI_API_KEY")
        
        if missing:
            raise ValueError(f"Faltan variables de entorno: {', '.join(missing)}")

settings = Settings()
