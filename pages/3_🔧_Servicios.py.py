import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

st.set_page_config(page_title="Servicios", layout="wide")
st.header("🔧 Encuesta - Servicios Técnicos")

# Conectamos a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

escala = ["Muy mala", "Mala", "Regular", "Buena", "Muy buena"]

with st.form("form_servicios", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        fecha = st.date_input("Fecha del servicio", date.today())
        tecnico = st.selectbox("Técnico", ["Selecciona...", "Gonzalo", "Eduardo", "Isaac", "Antonio"])
    with col2:
        cliente = st.text_input("Nombre del Cliente (Opcional)")
        tipo_servicio = st.selectbox("Tipo de servicio", ["Mantenimiento", "Reparación", "Garantía"])
        
    st.markdown("#### 🧑‍🔧 Atención del Técnico")
    q_trato = st.select_slider("Trato, respeto y amabilidad", options=escala, value="Buena")
    q_explicacion = st.select_slider("Claridad al explicar el diagnóstico", options=escala, value="Buena")
    
    st.markdown("#### ✅ Calidad y Tiempos")
    q_rapidez = st.select_slider("Rapidez en la reparación", options=escala, value="Buena")
    q_calidad = st.select_slider("Calidad del trabajo (¿Se resolvió el problema?)", options=escala, value="Buena")
    
    st.markdown("#### ✨ General")
    q_general = st.select_slider("¿Cómo califica su experiencia general?", options=escala, value="Buena")
    comentarios = st.text_area("¿Qué aspecto considera que debemos mejorar?")
    
    if st.form_submit_button("Guardar Encuesta"):
        if tecnico != "Selecciona...":
            df_existente = conn.read(worksheet="Servicios")
            
            datos = {
                "Fecha": str(fecha), "Cliente": cliente, "Tecnico": tecnico, "Servicio": tipo_servicio,
                "Trato": q_trato, "Explicacion": q_explicacion, 
                "Rapidez": q_rapidez, "Calidad": q_calidad,
                "Experiencia": q_general, "Mejoras": comentarios
            }
            
            df_nuevo = pd.DataFrame([datos])
            df_actualizado = pd.concat([df_existente, df_nuevo], ignore_index=True)
            
            conn.update(worksheet="Servicios", data=df_actualizado)
            st.cache_data.clear()
            st.success("✅ Encuesta de servicio técnico guardada correctamente.")
        else:
            st.error("Por favor, selecciona al técnico.")
