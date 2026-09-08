import streamlit as st

st.set_page_config(page_title="Agro Equipos", layout="wide")

try:
    st.sidebar.image("Logo.png", use_container_width=True)
except:
    pass

st.title("📊 Agro Equipos - Portal Principal")
st.caption("Desarrollando el Campo y la Construcción")
st.write("👈 Por favor, selecciona el área a evaluar en el menú de la izquierda.")
