# 🚀 Daily Resume: Tech-Economy Insights

> **Plataforma de Inteligencia de Mercado potenciada por RAG y Agentes AI**

Este proyecto es una solución de **Ingeniería de Datos y AI** diseñada para analistas de mercado, inversores y entusiastas de la tecnología. Automatiza la ingesta, análisis y síntesis de noticias globales, conectando puntos entre avances tecnológicos y movimientos económicos.

## 🌟 Valor Agregado

En un mundo saturado de información, **Daily Resume** no solo busca noticias; las **entiende**:

*   **🔍 Búsqueda Semántica Inteligente**: Olvídate de las keywords exactas. Pregunta "¿Cómo afecta la IA al desempleo?" y encuentra artículos relevantes por contexto, no solo por palabras clave.
*   **🧠 Agente de Análisis Cognitivo (AI Agent)**:
    *   Lee y analiza cientos de noticias en tiempo real.
    *   Detecta **correlaciones ocultas** entre eventos de tecnología y economía.
    *   Genera un **Informe Ejecutivo** diario con insights accionables.
*   **⚡ Eficiencia de Datos**: Sistema de deduplicación inteligente que evita costos innecesarios de almacenamiento y procesamiento (Embeddings), optimizando el pipeline ELT.

## 🛠️ Arquitectura Técnica

El proyecto sigue una **Arquitectura Hexagonal (Clean Architecture)** para garantizar mantenibilidad y escalabilidad.

### Stack Tecnológico
*   **Lenguaje**: Python 3.11+
*   **Orquestación**: Gestión de dependencias ultra-rápida con `uv`.
*   **Frontend**: Streamlit (con Custom CSS & UI Components).
*   **Database (Vector Store)**: Supabase (PostgreSQL + pgvector).
*   **LLM & Embeddings**: Google Gemini 1.5 Flash (Generación) & Text-Embedding-004.
*   **Data Source**: The Guardian API.

### Estructura del Proyecto
```bash
src/
├── application/     # Casos de uso (Pipelines de Búsqueda e Ingestión)
├── domain/          # Entidades y Reglas de Negocio (Clean Code)
├── infrastructure/  # Adaptadores (Supabase Client, Gemini Client, Guardian API)
├── config/          # Gestión centralizada de configuración
└── ui/              # Interfaz de Usuario (Streamlit)
```

## 🚀 Prueba el Sistema en Vivo

¡Interactúa con la aplicación desplegada y analiza el mercado en tiempo real!

👉 **[Daily Resume App](https://aidailynews-jndrs.streamlit.app/)**

## 👨‍💻 Autor
**Junior Andres Flores**  
*Data Engineer & AI Developer*
