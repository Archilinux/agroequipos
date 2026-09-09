# ==========================================
# 1. MÓDULO DE REFACCIONES
# ==========================================
if eleccion == "🛠️ Refacciones":
    st.header("🛠️ Encuesta de Satisfacción - Refacciones")
    with st.form("form_refacciones", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            fecha_registro = st.date_input("Fecha de la compra", date.today())
        with col2:
            cliente = st.text_input("Nombre del Cliente (Opcional)")
            
        pieza = st.text_input("Refacción adquirida")
        
        st.markdown("#### 🧑‍💼 Atención en Mostrador")
        q_trato = st.select_slider("Trato y amabilidad del asesor", options=escala, value="Buena")
        q_rapidez = st.select_slider("Rapidez con la que fue atendido", options=escala, value="Buena")
        q_conocimiento = st.select_slider("Conocimiento del asesor para ayudarle", options=escala, value="Buena")
        
        st.markdown("#### 📦 Disponibilidad y Producto")
        q_disponibilidad = st.select_slider("Disponibilidad inmediata de la refacción", options=escala, value="Buena")
        
        st.markdown("#### ✨ General")
        q_general = st.select_slider("¿Cómo califica su experiencia general?", options=escala, value="Buena")
        q_recomendacion = st.radio("¿Nos recomendaría?", ["Sí", "Tal vez", "No"])
        comentarios = st.text_area("¿Qué aspecto considera que debemos mejorar?")
        
        if st.form_submit_button("Guardar Encuesta"):
            if pieza:
                datos = {
                    "Fecha": str(fecha_registro), "Cliente": cliente, "Pieza": pieza,
                    "Trato": q_trato, "Rapidez": q_rapidez, "Conocimiento": q_conocimiento,
                    "Disponibilidad": q_disponibilidad, "Experiencia": q_general, 
                    "Recomendacion": q_recomendacion, "Mejoras": comentarios
                }
                if guardar_encuesta("Refacciones", datos):
                    st.success("✅ Encuesta guardada en Google Drive.")
            else:
                st.error("Por favor, ingresa la refacción adquirida.")
