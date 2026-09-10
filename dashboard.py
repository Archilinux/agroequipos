import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Dashboard Directivo", layout="wide")
st.title("📈 Dashboard Directivo - Agro Equipos")
st.markdown("Monitoreo de satisfacción y áreas de oportunidad")

# --- SELECTOR DE GRÁFICAS ---
tipo_grafica = st.radio(
    "Elige el estilo visual para los reportes:",
    ["📊 Barras", "📈 Líneas", "🌊 Área"],
    horizontal=True
)

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

# Función para cambiar las gráficas
def dibujar_grafica(datos):
    if tipo_grafica == "📊 Barras":
        st.bar_chart(datos)
    elif tipo_grafica == "📈 Líneas":
        st.line_chart(datos)
    else:
        st.area_chart(datos)

# --- CREACIÓN DE PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🛠️ Refacciones", "🚜 Maquinaria", "🔧 Servicios"])

# --- PESTAÑA 1: REFACCIONES ---
with tab1:
    if df_ref.empty:
        st.info("Aún no hay encuestas registradas en Refacciones.")
    else:
        st.download_button("📥 Descargar Reporte (CSV)", data=df_ref.to_csv(index=False).encode('utf-8-sig'), file_name="Refacciones.csv", mime="text/csv", type="primary")
        
        col1, col2 = st.columns(2)
        col1.metric("Total de Encuestas", len(df_ref))
        col2.metric("Alertas (Mala / Muy mala)", len(df_ref[df_ref['Experiencia'].isin(['Mala', 'Muy mala'])]))
        
        st.divider()
        st.subheader("📊 Desempeño Detallado - Refacciones")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Trato del asesor**")
            dibujar_grafica(df_ref['Trato'].value_counts())
            st.markdown("**Conocimiento del asesor**")
            dibujar_grafica(df_ref['Conocimiento'].value_counts())
            st.markdown("**Experiencia General**")
            dibujar_grafica(df_ref['Experiencia'].value_counts())
        with c2:
            st.markdown("**Rapidez de atención**")
            dibujar_grafica(df_ref['Rapidez'].value_counts())
            st.markdown("**Disponibilidad de pieza**")
            dibujar_grafica(df_ref['Disponibilidad'].value_counts())
            st.markdown("**¿Nos recomendaría?**")
            dibujar_grafica(df_ref['Recomendacion'].value_counts())
            
        st.subheader("📝 Observaciones")
        obs_ref = df_ref[['Fecha', 'Pieza', 'Experiencia', 'Mejoras']].dropna(subset=['Mejoras'])
        st.dataframe(obs_ref[obs_ref['Mejoras'].str.strip() != ''], use_container_width=True, hide_index=True)


# --- PESTAÑA 2: MAQUINARIA ---
with tab2:
    if df_maq.empty:
        st.info("Aún no hay encuestas registradas en Maquinaria.")
    else:
        st.download_button("📥 Descargar Reporte (CSV)", data=df_maq.to_csv(index=False).encode('utf-8-sig'), file_name="Maquinaria.csv", mime="text/csv", type="primary")
        
        col1, col2 = st.columns(2)
        col1.metric("Total de Encuestas", len(df_maq))
        col2.metric("Alertas (Mala / Muy mala)", len(df_maq[df_maq['Experiencia'].isin(['Mala', 'Muy mala'])]))
        
        st.divider()
        st.subheader("📊 Desempeño Detallado - Maquinaria")
        
        # Gráfica del personal ocupando todo el ancho
        st.markdown("**Encuestas por Vendedor**")
        dibujar_grafica(df_maq['Vendedor'].value_counts())
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Disposición del vendedor**")
            dibujar_grafica(df_maq['Disposicion'].value_counts())
            st.markdown("**Resolución de dudas**")
            dibujar_grafica(df_maq['Dudas'].value_counts())
            st.markdown("**Condiciones de entrega**")
            dibujar_grafica(df_maq['Condiciones'].value_counts())
        with c2:
            st.markdown("**Claridad en explicación**")
            dibujar_grafica(df_maq['Explicacion'].value_counts())
            st.markdown("**Tiempo de entrega**")
            dibujar_grafica(df_maq['Tiempo_Entrega'].value_counts())
            st.markdown("**Experiencia General**")
            dibujar_grafica(df_maq['Experiencia'].value_counts())
            
        st.subheader("📝 Observaciones")
        obs_maq = df_maq[['Fecha', 'Vendedor', 'Equipo', 'Mejoras']].dropna(subset=['Mejoras'])
        st.dataframe(obs_maq[obs_maq['Mejoras'].str.strip() != ''], use_container_width=True, hide_index=True)


# --- PESTAÑA 3: SERVICIOS ---
with tab3:
    if df_ser.empty:
        st.info("Aún no hay encuestas registradas en Servicios.")
    else:
        st.download_button("📥 Descargar Reporte (CSV)", data=df_ser.to_csv(index=False).encode('utf-8-sig'), file_name="Servicios.csv", mime="text/csv", type="primary")
        
        col1, col2 = st.columns(2)
        col1.metric("Total de Encuestas", len(df_ser))
        col2.metric("Alertas (Mala / Muy mala)", len(df_ser[df_ser['Experiencia'].isin(['Mala', 'Muy mala'])]))
        
        st.divider()
        st.subheader("📊 Desempeño Detallado - Servicios")
        
        # Gráfica del personal ocupando todo el ancho
        st.markdown("**Encuestas por Técnico**")
        dibujar_grafica(df_ser['Tecnico'].value_counts())
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Trato y amabilidad**")
            dibujar_grafica(df_ser['Trato'].value_counts())
            st.markdown("**Rapidez del servicio**")
            dibujar_grafica(df_ser['Rapidez'].value_counts())
            st.markdown("**Experiencia General**")
            dibujar_grafica(df_ser['Experiencia'].value_counts())
        with c2:
            st.markdown("**Claridad del diagnóstico**")
            dibujar_grafica(df_ser['Explicacion'].value_counts())
            st.markdown("**Calidad del trabajo**")
            dibujar_grafica(df_ser['Calidad'].value_counts())
            
        st.subheader("📝 Observaciones")
        obs_ser = df_ser[['Fecha', 'Tecnico', 'Servicio', 'Mejoras']].dropna(subset=['Mejoras'])
        st.dataframe(obs_ser[obs_ser['Mejoras'].str.strip() != ''], use_container_width=True, hide_index=True)
