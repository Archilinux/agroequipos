import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

st.set_page_config(page_title="Maquinaria", layout="wide")
st.header("🚜 Encuesta - Maquinaria")

# Conectamos a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

escala = ["Muy mala", "Mala", "Regular", "Buena", "Muy buena"]

with st.form("form_maquinaria", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        fecha = st.date_input("Fecha de la venta", date.today())
        vendedor = st.selectbox("Vendedor", ["Selecciona...", "Juan Pérez", "María Gómez"])
    with col2:
        cliente = st.text_input("Nombre del Cliente (Opcional)")
        equipo = st.text_input("Modelo de Maquinaria (ej. Tractor, Aspersora, Remolque)")
        
    st.markdown("#### 🧑‍💼 Atención del Vendedor")
    q_disposicion = st.select_slider("Disposición y voluntad para ayudarle", options=escala, value="Buena")
    q_explicacion = st.select_slider("Claridad en la explicación del equipo", options=escala, value="Buena")
    q_dudas = st.select_slider("Capacidad para resolver dudas técnicas", options=escala, value="Buena")
    
    st.markdown("#### ⏱️ Proceso de Entrega")
    q_tiempo = st.select_slider("Tiempo de espera para recibir el equipo", options=escala, value="Buena")
    q_condiciones = st.select_slider("Condiciones de entrega del equipo", options=escala, value="Buena")
    
    st.markdown("#### ✨ General")
    q_general = st.select_slider("¿Cómo califica su experiencia general?", options=escala, value="Buena")
    comentarios = st.text_area("¿Qué aspecto considera que debemos mejorar?")
    
    if st.form_submit_button("Guardar Encuesta"):
        if vendedor != "Selecciona..." and equipo:
            df_existente = conn.read(worksheet="Maquinaria")
            
            datos = {
                "Fecha": str(fecha), "Cliente": cliente, "Vendedor": vendedor, "Equipo": equipo,
                "Disposicion": q_disposicion, "Explicacion": q_explicacion, "Dudas": q_dudas,
                "Tiempo_Entrega": q_tiempo, "Condiciones": q_condiciones,
                "Experiencia": q_general, "Mejoras": comentarios
            }
            
            df_nuevo = pd.DataFrame([datos])
            df_actualizado = pd.concat([df_existente, df_nuevo], ignore_index=True)
            
            conn.update(worksheet="Maquinaria", data=df_actualizado)
            st.cache_data.clear()
            st.success("✅ Encuesta de maquinaria guardada correctamente.")
        else:
            st.error("Selecciona al vendedor e ingresa el modelo del equipo.")