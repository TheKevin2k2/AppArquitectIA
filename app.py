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
st.title("🏗️ ArquitectIA: Precisión Estructural v6.1")

# 2. Barra Lateral
with st.sidebar:
    st.header("⚙️ Ajustes de Rigidez")
    estilo = st.selectbox("Estilo Técnico:", ["Moderno Sobrio", "Minimalista", "Contemporáneo"])
    st.info("Nota: Esta versión usa 'Flux' para intentar mantener las líneas originales.")
    if st.button("🗑️ Reiniciar App"):
        st.rerun()

# 3. Instrucciones
st.subheader("📝 Paso 1: Describe la estructura")
forma_detallada = st.text_area(
    "Describe la FORMA exacta de tu modelo:",
    placeholder="Ej: Es un cubo de dos pisos con un volado a la izquierda..."
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

                    # PROMPT DE ANÁLISIS
                    prompt_analisis = (
                        "Act as a professional architect. Analyze the attached screenshot. "
                        "Describe volumes and window positions technically. "
                        f"Style: {estilo}. Extra details: {forma_detallada}."
                    )

                    payload = {"contents": [{"parts": [
                        {"text": prompt_analisis},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    res = requests.post(URL_GEMINI, json=payload, timeout=20)
                    data = res.json()
                    
                    if "candidates" in data:
                        descripcion_ia = data["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        descripcion_ia = "Architectural building, modern style."

                    # MOTOR DE DIBUJO FLUX
                    prompt_render = (
                        f"Professional architectural photography, ultra-realistic. "
                        f"Building volume strictly like this: {descripcion_ia}. "
                        "8k resolution, cinematic lighting, realistic materials."
                    )
                    
                    # CORRECCIÓN DEL ERROR DE SINTAXIS AQUÍ:
                    final_encoded = urllib.parse.quote(prompt_render[:800])
                    
                    url_img = f"https://image.pollinations.ai/prompt/{final_encoded}?width=1280&height=720&model=flux&nologo=true&seed={int(time.time())}"
                    
                    r = requests.get(url_img, timeout=120)
                    if r.status_code == 200:
                        st.image(r.content, use_container_width=True)
                        st.success("Renderizado finalizado.")
                        st.download_button("💾 Guardar", r.content, "render.png", "image/png")
                    else:
                        st.error("Error en el motor de imagen.")
                except Exception as e:
                    st.error(f"Error técnico: {e}")
