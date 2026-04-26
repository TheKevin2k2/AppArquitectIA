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

st.set_page_config(page_title="ArquitectIA: Control Estructural", layout="wide")
st.title("🏗️ ArquitectIA: Precisión Estructural v6.0")

# 2. Barra Lateral con más restricciones
with st.sidebar:
    st.header("⚙️ Ajustes de Rigidez")
    # Forzamos un estilo que no sea "loco"
    estilo = st.selectbox("Estilo Técnico:", ["Moderno Sobrio", "Minimalista", "Contemporáneo"])
    st.info("Nota: Esta versión usa 'Flux Pro' para intentar mantener las líneas del diseño original.")
    if st.button("🗑️ Reiniciar App"):
        st.rerun()

# 3. Instrucciones del usuario
st.subheader("📝 Paso 1: Describe la estructura")
forma_detallada = st.text_area(
    "Describe la FORMA exacta de tu modelo (ej: 'Es un cubo de dos pisos con una ventana cuadrada a la izquierda'):",
    placeholder="No dejes que la IA adivine la forma..."
)

# 4. Carga de imagen
archivo = st.file_uploader("🖼️ Paso 2: Sube tu captura (Arrastra desde tu carpeta)", type=["jpg", "jpeg", "png"])

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Modelo de SketchUp")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER"):
        with col2:
            with st.spinner("🧠 Escaneando geometría..."):
                try:
                    # Preparar imagen
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    # PROMPT DE GEOMETRÍA RÍGIDA
                    # Le pedimos a Gemini que sea un inspector de obra
                    prompt_analisis = (
                        "Act as a professional architect. Analyze the attached screenshot of a 3D model. "
                        "Describe the volumes, the exact number of walls, and the position of the windows. "
                        "Be extremely technical. The goal is to generate a photorealistic render "
                        "that respects the building's footprint 100%. "
                        f"Style requested: {estilo}. Extra shape details: {forma_detallada}."
                    )

                    payload = {"contents": [{"parts": [
                        {"text": prompt_analisis},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    res = requests.post(URL_GEMINI, json=payload, timeout=20)
                    descripcion_ia = res.json()["candidates"][0]["content"]["parts"][0]["text"]

                    # MOTOR DE DIBUJO FLUX (Más obediente)
                    # Añadimos parámetros para evitar que 'invente' nuevas casas
                    prompt_render = (
                        f"Architectural photography, ultra-realistic. Building volume exactly like this: {descripcion_ia}. "
                        "Do not change the building's shape or perspective. High-end materials, cinematic lighting, 8k. "
                        "Professional real estate photography."
                    )
                    
                    final_encoded = urllib.parse.quote(prompt_render[:8
