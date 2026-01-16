import streamlit as st
import sys
import os

# Ensure src is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.config.settings import settings
from src.infrastructure.database import SupabaseDatabase
from src.infrastructure.embeddings import GeminiEmbeddingService
from src.application.pipeline import SearchPipeline

# 1. Configuración de página
st.set_page_config(page_title="Tech-Insights", layout="wide")
st.title(settings.APP_TITLE)

# 2. Inicialización de servicios (Cached)
@st.cache_resource(show_spinner=False)
def init_services():
    try:
        settings.validate()
        db = SupabaseDatabase()
        emb_service = GeminiEmbeddingService()
        pipeline = SearchPipeline(emb_service, db)
        return pipeline
    except Exception as e:
        st.error(f"Error de inicialización: {e}")
        return None

if "search_pipeline" not in st.session_state:
    with st.status("Conectando sistemas...", expanded=True) as status:
        pipeline = init_services()
        if pipeline:
            st.session_state.search_pipeline = pipeline
            st.session_state.initialized = True
            status.update(label="✅ Sistema listo", state="complete", expanded=False)
        else:
            st.stop()

# 3. Interfaz
if st.session_state.get("initialized"):
    query = st.text_input("¿Qué tecnología quieres investigar?")

    if query:
        with st.spinner("Analizando vectorialmente..."):
            try:
                results = st.session_state.search_pipeline.search(query)
                
                if results:
                    st.subheader(f"Resultados para: '{query}'")
                    for res in results:
                        with st.expander(f"📌 {res.title} - Categoria: {res.category}"):
                            st.write(res.content)
                else:
                    st.info("No se encontraron resultados relevantes.")
            except Exception as e:
                st.error(f"Error durante la búsqueda: {e}")

# --- Footer ---
st.sidebar.info(f"""
**Stack:**
- **DB:** Supabase (Table: {settings.TABLE_NAME})
- **Model:** {settings.EMBEDDING_MODEL}
- **Architecture:** Hexagonal (Clean Code)
""")
