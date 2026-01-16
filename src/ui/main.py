import streamlit as st
import sys
import os

# Ensure src is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.config.settings import settings
from src.infrastructure.database import SupabaseDatabase
from src.infrastructure.embeddings import GeminiEmbeddingService
from src.infrastructure.llm_service import GeminiLLMService
import importlib
import src.application.pipeline
importlib.reload(src.application.pipeline)
from src.application.pipeline import SearchPipeline, IngestionPipeline

# 1. Configuración de página e Identidad
st.set_page_config(page_title="Tech-Insights AI", layout="wide", page_icon="🚀")

def apply_custom_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Gradient Background */
        .stApp {
            background: linear-gradient(to bottom right, #0f172a, #1e293b);
            color: #f8fafc;
        }
        
        /* Headers */
        h1, h2, h3 {
            background: -webkit-linear-gradient(45deg, #60a5fa, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
        }
        
        /* Cards */
        .stCard {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            transition: transform 0.2s;
        }
        .stCard:hover {
            transform: translateY(-2px);
            border-color: #60a5fa;
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            border: none;
            color: white;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            box-shadow: 0 4px 12px rgba(96, 165, 250, 0.4);
            transform: scale(1.02);
            color: white;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: rgba(255, 255, 255, 0.02);
            border-radius: 8px;
        }
        
        </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# 2. Inicialización de servicios (Cached)
@st.cache_resource(show_spinner=False)
def init_services():
    try:
        settings.validate()
        db = SupabaseDatabase()
        emb_service = GeminiEmbeddingService()
        llm_service = GeminiLLMService()
        
        search_pipe = SearchPipeline(emb_service, db, llm_service)
        ingest_pipe = IngestionPipeline(emb_service, db, llm_service)
        
        return search_pipe, ingest_pipe
    except Exception as e:
        st.error(f"Error de inicialización: {e}")
        return None, None

if "services_loaded" not in st.session_state:
    with st.status("Inicializando sistema neuronal...", expanded=True) as status:
        s_pipe, i_pipe = init_services()
        if s_pipe and i_pipe:
            st.session_state.search_pipeline = s_pipe
            st.session_state.ingest_pipeline = i_pipe
            st.session_state.services_loaded = True
            status.update(label="✅ Sistema Online", state="complete", expanded=False)
        else:
            st.stop()

# 3. Interfaz Principal
st.title(settings.APP_TITLE)
st.markdown("Plataforma de inteligencia de mercado impulsada por RAG y Agentes AI.")

tab1, tab2 = st.tabs(["🔎 Buscador Semántico", "🧠 Análisis de Mercado (AI)"])

# --- TAB 1: BUSCADOR ---
with tab1:
    st.markdown("### Explorar Base de Conocimiento")
    query = st.text_input("¿Qué tendencia o tecnología deseas investigar hoy?", placeholder="Ej: Impacto de la IA en la economía...")

    if query:
        with st.spinner("Realizando búsqueda vectorial..."):
            try:
                results = st.session_state.search_pipeline.search(query)
                
                if results:
                    st.subheader(f"Resultados Relevantes")
                    for i, res in enumerate(results):
                        # Generamos un pequeño resumen visual (1ros 300 caracteres)
                        content_display = f"🤖 <b>AI Insight:</b> {res.relevance}" if res.relevance else (res.content[:300] + "..." if len(res.content) > 300 else res.content)
                        
                        # Link handling
                        link_html = f'<a href="{res.url}" target="_blank" style="color: #60a5fa; text-decoration: none; font-weight: bold;">🔗 Leer noticia completa</a>' if res.url else "<span style='color: #64748b;'>Sin enlace disponible</span>"
                        
                        st.markdown(f"""
                        <div class="stCard">
                            <h3>{res.title}</h3>
                            <p style="color: #94a3b8; font-size: 0.9em;">📂 {res.category} | 🆔 ID: {res.id}</p>
                            <p style="margin-bottom: 15px; font-style: italic; color: #e2e8f0;">{content_display}</p>
                            {link_html}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No se encontraron resultados relevantes en la base de datos.")
            except Exception as e:
                st.error(f"Error durante la búsqueda: {e}")

# --- TAB 2: ANÁLISIS AI ---
with tab2:
    col_header, col_btn = st.columns([3, 1])
    with col_header:
        st.markdown("### Generación de Insights Globales")
        st.caption("Extrae noticias en tiempo real de **The Guardian**, vectoriza el contenido y genera un informe ejecutivo.")
    
    with col_btn:
        st.write("") # Spacer
        if st.button("🔄 Ejecutar Análisis en Vivo"):
            with st.spinner("🤖 Agente AI trabajando: Extrayendo, Vectorizando y Analizando..."):
                try:
                    summary, news_used = st.session_state.ingest_pipeline.run()
                    st.session_state.last_summary = summary
                    st.session_state.last_news = news_used
                    st.success("¡Análisis completado exitosamente!")
                except Exception as e:
                    st.error(f"Error en el pipeline de análisis: {e}")

    # Mostrar Resultados si existen
    if "last_summary" in st.session_state:
        st.markdown("---")
        
        # Columna Izquierda: Resumen (70%), Columna Derecha: Fuentes (30%)
        col_summary, col_sources = st.columns([2, 1])
        
        with col_summary:
            st.markdown("## 📊 Informe Ejecutivo de IA")
            st.markdown(f"""
            <div style="background-color: rgba(30, 41, 59, 0.8); padding: 25px; border-radius: 15px; border-left: 5px solid #8b5cf6;">
                {st.session_state.last_summary}
            </div>
            """, unsafe_allow_html=True)
            
        with col_sources:
            st.markdown("### 📰 Fuentes Analizadas")
            if "last_news" in st.session_state and st.session_state.last_news:
                for item in st.session_state.last_news:
                    with st.expander(f"🔹 {item['title'][:50]}..."):
                        st.caption(f"Categoría: {item['category']}")
                        st.write(item['content'][:300] + "...")
            else:
                st.write("No hay fuentes disponibles.")

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Engine**: {settings.GENERATION_MODEL}")
st.sidebar.markdown("**Data Source**: The Guardian API")
st.sidebar.markdown("**Author**: Junior Andres Flores")
st.sidebar.success("Sistema Operativo")
