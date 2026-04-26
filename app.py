import streamlit as st
import requests
import urllib.parse
import time
from PIL import Image
import io

st.set_page_config(page_title="ArquitectIA Ultra-Libre", layout="wide")

st.markdown("<h1 style='text-align: center;'>🏗️ ArquitectIA v9.0 (Sin Límites)</h1>", unsafe_allow_html=True)
st.caption("Versión directa: Sin errores de cuota de Google")

# 1. Ajustes en la barra lateral
with st.sidebar:
    st.header("🎨 Estética del Render")
    estilo = st.selectbox("Estilo:", ["Moderno", "Minimalista", "Industrial", "Rústico"])
    clima = st.selectbox("Iluminación:", ["Día Soleado", "Atardecer", "Nublado", "Noche"])
    st.divider()
    st.info("Esta versión no usa Gemini para evitar bloqueos. La descripción debe ser muy buena.")

# 2. Inputs de usuario
st.subheader("📝 Paso 1: Describe tu casa")
# Aquí el usuario debe ser el "cerebro" que antes era la IA
descripcion_manual = st.text_area(
    "Describe la forma y materiales:", 
    placeholder="Ej: Una casa de dos pisos con ventanales grandes, paredes de concreto gris y un jardín al frente..."
)

archivo = st.file_uploader("🖼️ Paso 2: Sube tu captura de SketchUp", type=["jpg", "jpeg", "png"])

if archivo:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tu Modelo")
        st.image(archivo, use_container_width=True)

    if st.button("🚀 GENERAR RENDER"):
        if not descripcion_manual:
            st.warning("⚠️ Por favor, describe brevemente la casa para ayudar a la IA.")
        else:
            with col2:
                with st.spinner("🎨 Dibujando render..."):
                    try:
                        # Creamos el prompt combinando todo
                        # Agregamos palabras de calidad arquitectónica
                        prompt_base = (
                            f"Professional architectural render, {descripcion_manual}, "
                            f"style {estilo}, {clima} lighting, cinematic, high resolution, 8k, photorealistic"
                        )
                        
                        # Codificamos el texto para la URL
                        prompt_final = urllib.parse.quote(prompt_base)
                        
                        # Generamos la imagen usando el motor de Pollinations
                        # El parámetro &seed ayuda a que cada vez sea distinto
                        url_render = f"https://image.pollinations.ai/prompt/{prompt_final}?width=1280&height=720&nologo=true&seed={int(time.time())}"
                        
                        # Mostramos el resultado
                        st.image(url_render, use_container_width=True)
                        st.success("¡Render listo!")
                        
                        # Opción de descarga
                        r = requests.get(url_render)
                        st.download_button("💾 Guardar Imagen", r.content, "render.png", "image/png")
                        
                    except Exception as e:
                        st.error(f"Error al generar: {e}")
