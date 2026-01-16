import httpx
import logging
from datetime import datetime, timedelta
from src.config.settings import settings

logger = logging.getLogger(__name__)

class DataProvider:
    @staticmethod
    def fetch_data():
        """Extrae noticias de tecnología y negocios de The Guardian de las últimas 24 horas."""
        
        # 1. Calcular rango de fechas (últimos 3 días para asegurar volumen)
        today = datetime.now()
        three_days_ago = (today - timedelta(days=3)).strftime('%Y-%m-%d')
        today_str = today.strftime('%Y-%m-%d')
        
        url = "https://content.guardianapis.com/search"
        
        params = {
            "api-key": settings.GUARDIAN_API_KEY,
            "section": "technology|business",
            "from-date": three_days_ago,
            "to-date": today_str,
            "q": "technology OR business OR economy OR ai OR tech",
            "show-fields": "bodyText",
            "page-size": 50 # Pedimos 50 para asegurar mínimo 30 útiles
        }

        try:
            logger.info(f"Conectando a The Guardian API ({three_days_ago} a {today_str})")
            response = httpx.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            
            data = response.json()
            results = data.get("response", {}).get("results", [])
            
            formatted_data = []
            for art in results:
                formatted_data.append({
                    "title": art.get("webTitle"),
                    "content": art.get("fields", {}).get("bodyText", ""),
                    "category": art.get("sectionName"),
                    "url": art.get("webUrl")
                })
            
            logger.info(f"Se extrajeron {len(formatted_data)} noticias exitosamente.")
            return formatted_data

        except Exception as e:
            logger.error(f"Error al extraer datos de The Guardian: {e}")
            return []