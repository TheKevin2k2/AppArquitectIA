import streamlit as st
import requests
import base64
from PIL import Image
import io
import urllib.parse
import time

# 1. Configuración de API
API_KEY = "AIzaSyDCoHVw6g5K1UFEePZmkCv7Co12_OHCoYQ"
URL_GEMINI = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={API_KEY}"

st.set_page_config(page_title="ArquitectIA Gratis v8.1", layout="wide")
st.markdown("<h1 style='text-align: center;'>🏗️ ArquitectIA Free v8.1</h1>", unsafe_allow_html=True)

# 2. Barra lateral
with st.sidebar:
    st.header("🎨 Estética")
    estilo = st.selectbox("Estilo:", ["Minimalista", "Moderno Industrial", "Rústico Contemporáneo"])
    clima = st.selectbox("Ambiente:", ["Día Soleado", "Atardecer Cálido", "Nublado"])
    st.info("💡 Consejo: Si la captura es muy grande, intenta recortarla un poco antes de subirla.")

# 3. Inputs
archivo = st.file_uploader("🖼️ Sube tu captura de SketchUp", type=["jpg", "jpeg", "png"])
instrucciones = st.text_input("📝 Describe materiales (ej: madera, cemento):")

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Tu Diseño")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER GRATIS"):
        with col2:
            with st.spinner("🧠 Analizando geometría..."):
                try:
                    # Preparar imagen (la comprimimos un poco para evitar errores de tamaño)
                    buffered = io.BytesIO()
                    img = img.convert("RGB")
                    img.save(buffered, format="JPEG", quality=85)
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    prompt_tecnico = (
                        f"Describe the architectural volumes of this 3D model accurately. "
                        f"Mention wall placement and roof type. Style: {estilo}. "
                        f"Materials: {instrucciones}. Preserve the original geometry."
                    )

                    payload = {"contents": [{"parts": [
                        {"text": prompt_tecnico},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    # Petición a Gemini
                    res = requests.post(URL_GEMINI, json=payload, timeout=30)
                    res_data = res.json()

                    # VERIFICACIÓN DE ERROR 'CANDIDATES'
                    if "candidates" in res_data and len(res_data["candidates"]) > 0:
                        descripcion = res_data["candidates"][0]["content"]["parts"][0]["text"]
                        
                        # Limpiar y codificar para la IA de dibujo
                        clean_desc = "".join(e for e in descripcion if e.isalnum() or e == " ")
                        final_prompt = f"Professional architectural photography, {clean_desc}, hyper-realistic, 8k"
                        encoded_prompt = urllib.parse.quote(final_prompt[:800])
                        
                        url_render = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed={int(time.time())}"
                        
                        st.image(url_render, use_container_width=True)
                        st.success("¡Render generado!")
                        
                        img_res = requests.get(url_render)
                        st.download_button("💾 Guardar Render", img_res.content, "render.png", "image/png")
                    
                    elif "error" in res_data:
                        st.error(f"Error de Google Gemini: {res_data['error']['message']}")
                    else:
                        st.error("La IA no pudo interpretar esta imagen. Prueba con una captura más clara o menos pesada.")

                except Exception as e:
                    st.error(f"Error técnico inesperado: {e}")
