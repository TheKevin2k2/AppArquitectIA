import streamlit as st
import requests
import base64
from PIL import Image
import io
import urllib.parse
import time

# --- CONFIGURACIÓN DE SEGURIDAD ---
API_KEY = "AIzaSyBLASApDrxbH68KPuNQJxWMCQPLBOYR4yk"
URL_GEMINI = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={API_KEY}"

st.set_page_config(page_title="ArquitectIA v10.6 Ultra", layout="wide")

st.markdown("""
    <style>
    .stFileUploader { border: 2px dashed #4A90E2; padding: 20px; background-color: #f0f2f6; border-radius: 15px; }
    h1 { color: #1E3A8A; text-align: center; font-family: 'Helvetica', sans-serif; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #1E3A8A; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🏗️ ArquitectIA v10.6 (Sin Errores)</h1>", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configuración")
    estilo = st.selectbox("Estilo Visual:", ["Moderno Sobrio", "Minimalista", "Industrial", "Rústico Moderno"])
    clima = st.selectbox("Ambiente/Luz:", ["Día Soleado", "Atardecer Cálido", "Nublado Realista", "Noche"])
    st.divider()
    st.warning("⚠️ REGLAS DE ORO:\n1. Fondo BLANCO en SketchUp.\n2. Sombras ACTIVADAS.\n3. Captura de cerca.")

# --- ÁREA DE TRABAJO ---
instrucciones_usuario = st.text_input("📝 Materiales específicos:", placeholder="Ej: Madera de nogal, concreto, vidrio...")
archivo = st.file_uploader("🖼️ Sube tu captura de SketchUp", type=["jpg", "jpeg", "png"])

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Captura Original")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER"):
        with col2:
            with st.spinner("🧠 Analizando volúmenes..."):
                try:
                    buffered = io.BytesIO()
                    img_convert = img.convert("RGB")
                    img_convert.save(buffered, format="JPEG", quality=90)
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    # PROMPT EN UNA SOLA LÍNEA PARA EVITAR SYNTAXERROR
                    prompt_analisis = f"Analyze this 3D model. Identify architectural volumes and roof shape. Strictly follow the building footprint. Style: {estilo}. Materials: {instrucciones_usuario}. Lighting: {clima}. Do not add extra structures. Do not change the house layout."
                    
                    payload = {"contents": [{"parts": [
                        {"text": prompt_analisis},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    res = requests.post(URL_GEMINI, json=payload, timeout=15)
                    
                    if res.status_code == 200:
                        descripcion_ia = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        descripcion_ia = f"Modern architectural photography, {estilo} style, {clima}."

                    # Generación visual
                    prompt_render = f"Architectural masterpiece, {descripcion_ia}, hyper-realistic materials, 8k, cinematic lighting, sharp focus, professional photography."
                    encoded_prompt = urllib.parse.quote(prompt_render[:900])
                    url_final = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed={int(time.time())}"
                    
                    st.image(url_final, use_container_width=True)
                    st.success("✅ Renderizado listo.")
                    
                    r_img = requests.get(url_final)
                    st.download_button("💾 Descargar Imagen", r_img.content, "render.png", "image/png")

                except Exception as e:
                    st.error(f"Error técnico: {e}")
