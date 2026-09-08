import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

st.set_page_config(page_title="Refacciones", layout="wide")
st.header("🛠️ Encuesta - Refacciones")

# Conectamos a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

escala = ["Muy mala", "Mala", "Regular", "Buena", "Muy buena"]

with st.form("form_refacciones", clear_on_submit=True):
    fecha = st.date_input("Fecha de la compra", date.today())
    cliente = st.text_input("Nombre del Cliente")
    pieza = st.text_input("Refacción adquirida")
    q_trato = st.select_slider("Trato y amabilidad del asesor", options=escala, value="Buena")
    
    if st.form_submit_button("Guardar Encuesta"):
        if pieza:
            # 1. Leer datos existentes
            df_existente = conn.read(worksheet="Refacciones")
            # 2. Crear nueva fila
            nueva_fila = pd.DataFrame([{"Fecha": str(fecha), "Cliente": cliente, "Pieza": pieza, "Trato": q_trato}])
            df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
            # 3. Guardar en Drive
            conn.update(worksheet="Refacciones", data=df_actualizado)
            st.cache_data.clear()
            st.success("✅ Encuesta guardada correctamente.")
        else:
            st.error("Por favor ingresa la refacción adquirida.")