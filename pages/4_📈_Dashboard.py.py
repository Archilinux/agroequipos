import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

st.set_page_config(page_title="Dashboard", layout="wide")
st.header("📈 Reportes y Análisis de Satisfacción")

# Conectamos a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Diccionario para convertir texto a número y poder graficar promedios
mapa_valores = {"Muy mala": 1, "Mala": 2, "Regular": 3, "Buena": 4, "Muy buena": 5}

# --- FILTROS GLOBALES ---
col1, col2, col3 = st.columns(3)
with col1:
    fecha_inicio = st.date_input("Desde la fecha:", date(date.today().year, date.today().month, 1))
with col2:
    fecha_fin = st.date_input("Hasta la fecha:", date.today())
with col3:
    st.write("") # Espacio en blanco para alinear el botón
    st.write("")
    if st.button("🔄 Sincronizar con Drive"):
        st.cache_data.clear()

st.divider()

# ==========================================
# REPORTE: MAQUINARIA (POR VENDEDOR)
# ==========================================
try:
    df_maq = conn.read(worksheet="Maquinaria")
    if not df_maq.empty and "Fecha" in df_maq.columns:
        # Convertir a formato fecha y filtrar
        df_maq['Fecha'] = pd.to_datetime(df_maq['Fecha']).dt.date
        df_maq_filtro = df_maq[(df_maq['Fecha'] >= fecha_inicio) & (df_maq['Fecha'] <= fecha_fin)]
        
        st.subheader(f"🚜 Desempeño de Vendedores ({len(df_maq_filtro)} encuestas)")
        
        if not df_maq_filtro.empty:
            # Convertimos la calificación de texto a número
            df_maq_filtro['Puntaje_Experiencia'] = df_maq_filtro['Experiencia'].map(mapa_valores)
            
            # Agrupamos por vendedor para sacar su promedio
            promedios_maq = df_maq_filtro.groupby("Vendedor")['Puntaje_Experiencia'].mean()
            st.bar_chart(promedios_maq)
        else:
            st.info("No hay encuestas de Maquinaria en este periodo.")
except Exception as e:
    st.warning("La pestaña 'Maquinaria' aún no tiene datos o no existe.")

st.divider()

# ==========================================
# REPORTE: SERVICIOS (POR TÉCNICO)
# ==========================================
try:
    df_servicios = conn.read(worksheet="Servicios")
    if not df_servicios.empty and "Fecha" in df_servicios.columns:
        df_servicios['Fecha'] = pd.to_datetime(df_servicios['Fecha']).dt.date
        df_serv_filtro = df_servicios[(df_servicios['Fecha'] >= fecha_inicio) & (df_servicios['Fecha'] <= fecha_fin)]
        
        st.subheader(f"🔧 Evaluación de Técnicos ({len(df_serv_filtro)} encuestas)")
        
        if not df_serv_filtro.empty:
            df_serv_filtro['Puntaje_Calidad'] = df_serv_filtro['Calidad'].map(mapa_valores)
            
            promedios_tec = df_serv_filtro.groupby("Tecnico")['Puntaje_Calidad'].mean()
            st.bar_chart(promedios_tec)
            
            # Tabla desplegable para ver comentarios de quejas/sugerencias
            with st.expander("Ver comentarios de clientes (Servicios)"):
                comentarios = df_serv_filtro[['Fecha', 'Tecnico', 'Mejoras']].dropna(subset=['Mejoras'])
                st.dataframe(comentarios[comentarios['Mejoras'] != ""])
        else:
            st.info("No hay encuestas de Servicios en este periodo.")
except Exception as e:
    st.warning("La pestaña 'Servicios' aún no tiene datos o no existe.")

st.divider()

# ==========================================
# REPORTE: REFACCIONES
# ==========================================
try:
    df_ref = conn.read(worksheet="Refacciones")
    if not df_ref.empty and "Fecha" in df_ref.columns:
        df_ref['Fecha'] = pd.to_datetime(df_ref['Fecha']).dt.date
        df_ref_filtro = df_ref[(df_ref['Fecha'] >= fecha_inicio) & (df_ref['Fecha'] <= fecha_fin)]
        
        st.subheader(f"🛠️ Atención en Mostrador ({len(df_ref_filtro)} encuestas)")
        
        if not df_ref_filtro.empty:
            df_ref_filtro['Puntaje_Atencion'] = df_ref_filtro['Trato'].map(mapa_valores)
            
            # Aquí mostramos el promedio general de atención a lo largo de los días
            promedio_diario = df_ref_filtro.groupby("Fecha")['Puntaje_Atencion'].mean()
            st.line_chart(promedio_diario)
        else:
            st.info("No hay encuestas de Refacciones en este periodo.")
except Exception as e:
    st.warning("La pestaña 'Refacciones' aún no tiene datos o no existe.")