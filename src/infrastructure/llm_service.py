from google import genai
from typing import List
from src.domain.interfaces import LLMService
from src.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class GeminiLLMService(LLMService):
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.GENERATION_MODEL

    def generate_summary(self, texts: List[str]) -> str:
        if not texts:
            return "No hay textos suficientes para generar un resumen."
            
        # Concatenamos los textos, limitando un poco para no explotar el contexto si son muchos
        # Tomamos los primeros 500 caracteres de cada noticia para el resumen
        context = "\n\n".join([f"- {t[:1000]}..." for t in texts])
        
        prompt = f"""
        Actúa como un analista experto en Tecnología y Economía Global.
        Analiza las siguientes noticias recientes (fragmentos):
        
        {context}
        
        TAREA:
        1. Identifica los 3 temas principales que conectan la tecnología con la economía actual.
        2. Busca correlaciones ocultas: ¿Cómo afectan los avances técnicos a los mercados o viceversa?
        3. Genera un "Resumen Ejecutivo de Insights" breve pero denso en información.
        
        Salida en formato Markdown amigable.
        """
        
        import time
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                import traceback
                error_msg = str(e)
                print(f"Intento {attempt + 1}/{max_retries} fallido: {error_msg}")
                
                # Si es el último intento, hacemos log y devolvemos error
                if attempt == max_retries - 1:
                    traceback.print_exc()
                    logger.error(f"Error generando resumen con GEMINI tras {max_retries} intentos: {e}")
                    return f"Error al generar el resumen de insights: {e}"
                
                # Si es error de cuota (429), esperamos más
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    wait_time = (attempt + 1) * 10 # 10s, 20s...
                    print(f"Detectado límite de cuota. Esperando {wait_time} segundos...")
                    time.sleep(wait_time)
                else:
                    # Otro error, esperamos un poco por si acaso
                    time.sleep(2)
    
    def explain_relevance(self, query: str, insights: List[dict]) -> List[str]:
        if not insights:
            return []
            
        # Construimos el prompt en lote
        context = ""
        for i, item in enumerate(insights):
            context += f"Item {i}: Title: '{item.title}', Content Fragment: '{item.content[:200]}...'\n"
            
        prompt = f"""
        Usuario busca: "{query}"
        
        Tengo estos artículos encontrados:
        {context}
        
        Para cada Item (0 a {len(insights)-1}), explica en UNA sola frase corta (máx 20 palabras) por qué este artículo es relevante para la búsqueda del usuario.
        No repitas el título. Ve al grano. Ejemplo: "Menciona específicamente el impacto de la inflación..."
        
        Formato de salida requerido (una línea por item):
        0: explicación...
        1: explicación...
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            # Procesar la respuesta para extraer la lista
            lines = response.text.strip().split('\n')
            # Intentar limpiar mapearlo
            explanations = []
            for i in range(len(insights)):
                found = False
                for line in lines:
                    if line.strip().startswith(f"{i}:"):
                        explanations.append(line.split(":", 1)[1].strip())
                        found = True
                        break
                if not found:
                    explanations.append("Relacionado semánticamente con su búsqueda.")
            
            return explanations
        except Exception as e:
            logger.error(f"Error generando explanations: {e}")
            return ["Información relevante encontrada."] * len(insights)
