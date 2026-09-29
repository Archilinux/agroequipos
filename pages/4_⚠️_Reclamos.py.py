import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

st.set_page_config(page_title="Reclamos", layout="wide")

# --- OCULTAR MENÚ LATERAL ---
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.header("⚠️ Buzón de Reclamos y Sugerencias")
st.markdown("Tu opinión es muy importante para mejorar nuestro servicio en Agro Equipos.")

conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("form_reclamos", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        fecha = st.date_input("Fecha de la incidencia", date.today())
        departamento = st.selectbox(
            "Departamento que le atendió", 
            ["Selecciona...", "Refacciones", "Maquinaria", "Servicios", "Administración / Otro"]
        )
    with col2:
        cliente = st.text_input("Nombre del Cliente (Opcional)")
        
    motivo = st.text_area("Describa el motivo de su reclamo o sugerencia", height=150)
    
    if st.form_submit_button("Enviar Reclamo"):
        if departamento != "Selecciona..." and motivo.strip() != "":
            df_existente = conn.read(worksheet="Reclamos")
            
            datos = {
                "Fecha": str(fecha), 
                "Cliente": cliente, 
                "Departamento": departamento, 
                "Motivo": motivo
            }
            
            nueva_fila = pd.DataFrame([datos])
            df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
            
            conn.update(worksheet="Reclamos", data=df_actualizado)
            st.cache_data.clear()
            st.success("✅ Su reclamo ha sido enviado correctamente. Le daremos seguimiento.")
        else:
            st.error("Por favor, selecciona el departamento y describe el motivo.")