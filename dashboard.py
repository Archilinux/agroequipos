import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Dashboard Directivo", layout="wide")
st.title("📈 Dashboard Directivo - Agro Equipos")
st.markdown("Monitoreo de satisfacción y áreas de oportunidad")

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=60)
def cargar_datos():
    df_ref = conn.read(worksheet="Refacciones").dropna(how="all")
    df_maq = conn.read(worksheet="Maquinaria").dropna(how="all")
    df_ser = conn.read(worksheet="Servicios").dropna(how="all")
    return df_ref, df_maq, df_ser

try:
    df_ref, df_maq, df_ser = cargar_datos()
except Exception as e:
    st.error("Esperando datos... Asegúrate de que las hojas de Excel tengan información.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["🛠️ Refacciones", "🚜 Maquinaria", "🔧 Servicios"])

# --- PESTAÑA 1: REFACCIONES ---
with tab1:
    if df_ref.empty:
        st.info("Aún no hay encuestas registradas en Refacciones.")
    else:
        st.download_button(
            label="📥 Descargar base de datos (Excel/CSV)",
            data=df_ref.to_csv(index=False).encode('utf-8-sig'),
            file_name="Reporte_Refacciones.csv",
            mime="text/csv",
            type="primary"
        )
        
        total_ref = len(df_ref)
        malas_ref = len(df_ref[df_ref['Experiencia'].isin(['Mala', 'Muy mala'])])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Encuestas", total_ref)
        col2.metric("Alertas (Malas / Muy malas)", malas_ref)
        
        st.subheader("Resumen General de Experiencia")
        st.bar_chart(df_ref['Experiencia'].value_counts())
        
        st.subheader("📝 Observaciones de los Clientes")
        obs_ref = df_ref[['Fecha', 'Pieza', 'Experiencia', 'Mejoras']].dropna(subset=['Mejoras'])
        obs_ref = obs_ref[obs_ref['Mejoras'].str.strip() != '']
        st.dataframe(obs_ref, use_container_width=True, hide_index=True)


# --- PESTAÑA 2: MAQUINARIA ---
with tab2:
    if df_maq.empty:
        st.info("Aún no hay encuestas registradas en Maquinaria.")
    else:
        st.download_button(
            label="📥 Descargar base de datos (Excel/CSV)",
            data=df_maq.to_csv(index=False).encode('utf-8-sig'),
            file_name="Reporte_Maquinaria.csv",
            mime="text/csv",
            type="primary"
        )
        
        total_maq = len(df_maq)
        malas_maq = len(df_maq[df_maq['Experiencia'].isin(['Mala', 'Muy mala'])])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Encuestas", total_maq)
        col2.metric("Alertas (Malas / Muy malas)", malas_maq)
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.subheader("Experiencia General")
            st.bar_chart(df_maq['Experiencia'].value_counts())
        with col_g2:
            st.subheader("Encuestas por Vendedor")
            st.bar_chart(df_maq['Vendedor'].value_counts())
            
        st.subheader("📝 Observaciones de los Clientes")
        obs_maq = df_maq[['Fecha', 'Vendedor', 'Equipo', 'Mejoras']].dropna(subset=['Mejoras'])
        obs_maq = obs_maq[obs_maq['Mejoras'].str.strip() != '']
        st.dataframe(obs_maq, use_container_width=True, hide_index=True)


# --- PESTAÑA 3: SERVICIOS ---
with tab3:
    if df_ser.empty:
        st.info("Aún no hay encuestas registradas en Servicios.")
    else:
        st.download_button(
            label="📥 Descargar base de datos (Excel/CSV)",
            data=df_ser.to_csv(index=False).encode('utf-8-sig'),
            file_name="Reporte_Servicios.csv",
            mime="text/csv",
            type="primary"
        )
        
        total_ser = len(df_ser)
        malas_ser = len(df_ser[df_ser['Experiencia'].isin(['Mala', 'Muy mala'])])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Encuestas", total_ser)
        col2.metric("Alertas (Malas / Muy malas)", malas_ser)
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.subheader("Experiencia General")
            st.bar_chart(df_ser['Experiencia'].value_counts())
        with col_g2:
            st.subheader("Encuestas por Técnico")
            st.bar_chart(df_ser['Tecnico'].value_counts())
            
        st.subheader("📝 Observaciones de los Clientes")
        obs_ser = df_ser[['Fecha', 'Tecnico', 'Servicio', 'Mejoras']].dropna(subset=['Mejoras'])
        obs_ser = obs_ser[obs_ser['Mejoras'].str.strip() != '']
        st.dataframe(obs_ser, use_container_width=True, hide_index=True)
