import streamlit as st

# Configuración básica
st.set_page_config(page_title="Test de Streamlit", page_icon="✅")

st.title("🛠️ Prueba de Funcionamiento")
st.write("Si puedes ver este mensaje, **Streamlit está funcionando correctamente** en tu máquina local.")

# Un componente interactivo simple
nombre = st.text_input("Escribe tu nombre para probar la interactividad:")

if st.button("¡Saludar!"):
    if nombre:
        st.success(f"¡Hola, {nombre}! El motor de Streamlit responde bien.")
    else:
        st.warning("Escribe algo en la caja de texto arriba.")

# Información del entorno
st.divider()
st.subheader("Información del Sistema")
st.code(f"""
- Entorno: Localhost
- Puerto: 8501
- Estado: Operativo
""")