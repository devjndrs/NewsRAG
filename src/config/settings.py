import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    # Nueva variable para The Guardian
    GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")

    APP_TITLE = "🚀 Daily Resume: Tech-Economy Insights"
    EMBEDDING_MODEL = "text-embedding-004"
    GENERATION_MODEL = "gemini-2.5-flash"
    TABLE_NAME = "tech_insights"
    
    @classmethod
    def validate(cls):
        missing = []
        if not cls.SUPABASE_URL: missing.append("SUPABASE_URL")
        if not cls.SUPABASE_KEY: missing.append("SUPABASE_KEY")
        if not cls.GEMINI_API_KEY: missing.append("GEMINI_API_KEY")
        if not cls.GUARDIAN_API_KEY: missing.append("GUARDIAN_API_KEY")
        
        if missing:
            raise ValueError(f"Faltan variables de entorno: {', '.join(missing)}")

settings = Settings()