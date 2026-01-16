# Por ahora este archivo simula una fuente de datos
# En el futuro aquí irían llamadas a APIs externas

class DataProvider:
    @staticmethod
    def fetch_data():
        # Simulando datos que venían de ingest_data.py
        return [
            {"title": "Nuevo chip de Nvidia", "content": "La serie 5000 promete un ahorro de energía del 30%", "category": "Hardware"},
            {"title": "Lanzamiento de Gemini 1.5", "content": "Google actualiza su modelo de lenguaje con mayor contexto", "category": "IA"}
        ]
