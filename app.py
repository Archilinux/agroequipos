import streamlit as st

st.set_page_config(page_title="Agro Equipos", layout="wide")

try:
    # Carga tu logotipo en el menú lateral
    st.sidebar.image("Logo.jpeg", use_container_width=True)
except Exception as e:
    pass

st.title("📊 Agro Equipos - Portal Principal")
st.caption("Desarrollando el Campo y la Construcción")
st.write("👈 Por favor, selecciona el área a evaluar en el menú de la izquierda.")
