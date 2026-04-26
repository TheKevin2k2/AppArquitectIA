import streamlit as st
import requests
import base64
from PIL import Image
import io
import urllib.parse
import time

# 1. Configuración de la API
API_KEY = "AIzaSyDCoHVw6g5K1UFEePZmkCv7Co12_OHCoYQ"
URL_GEMINI = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={API_KEY}"

st.set_page_config(page_title="ArquitectIA: Control Estructural", layout="wide")

st.title("🏗️ ArquitectIA: Precisión Estructural v4.0")

# 2. Barra Lateral
with st.sidebar:
    st.header("⚙️ Nivel de Calco")
    metodo = st.radio("Prioridad:", ["Fotorrealismo (Puede variar formas)", "Estructura Rígida (Fiel al modelo)"])
    st.divider()
    estilo = st.selectbox("Estilo:", ["Moderno Sobrio", "Minimalista", "Industrial", "Piedra y Madera"])
    clima = st.selectbox("Luz:", ["Día Soleado", "Atardecer Cálido", "Nublado Suave"])

# 3. Instrucciones y Carga
st.subheader("📝 Paso 1: Describe tu diseño")
instruccion_usuario = st.text_area("Detalla la forma (ej: 'Techo plano con volado a la derecha, dos ventanales altos'):")

archivo = st.file_uploader("🖼️ Paso 2: Sube tu captura de SketchUp", type=["jpg", "jpeg", "png"])

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Tu Modelo")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER FIEL"):
        with col2:
            with st.spinner("🧠 Analizando volúmenes estructurales..."):
                try:
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    # PROMPT TÉCNICO PARA GEMINI
                    # Le pedimos que sea un "escáner" de formas
                    instruccion_gemini = (
                        "Analiza esta imagen de SketchUp. Actúa como un experto en fotogrametría. "
                        "Describe la geometría exacta: posición de muros, tipo de techos, ubicación de vanos y ventanas. "
                        "Tu descripción será usada para recrear la imagen EXACTAMENTE igual. "
                        f"Estilo solicitado: {estilo}. Luz: {clima}. "
                        f"Instrucciones extra: {instruccion_usuario}. "
                        "IMPORTANTE: No añadas elementos que no existan en el volumen original."
                    )

                    payload = {"contents": [{"parts": [
                        {"text": instruccion_gemini},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    res = requests.post(URL_GEMINI, json=payload, timeout=20)
                    data = res.json()
                    
                    if "candidates" in data:
                        descripcion_tecnica = data["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        descripcion_tecnica = f"Architectural render of {estilo} building, precise geometry."

                    # Fase de Dibujo: Refuerzo de palabras clave de "No Cambio"
                    clean_p = "".join(e for e in descripcion_tecnica if e.isalnum() or e == " ")
                    final_p = (
                        f"Architectural professional photography, "
                        f"STRICTLY FOLLOWING THIS GEOMETRY: {clean_p}. "
                        "High resolution, photorealistic materials, do not change original shapes."
                    )
                    
                    encoded_p = urllib.parse.quote(final_p[:800])
                    url_img = f"https://image.pollinations.ai/prompt/{encoded_p}?width=1280&height=720&nologo=true&seed={int(time.time())}"
                    
                    r = requests.get(url_img, timeout=120)
                    if r.status_code == 200:
                        st.image(r.content, use_container_width=True)
                        st.success("Render finalizado.")
                        st.download_button("💾 Descargar", r.content, "render.png", "image/png")

                except Exception as e:
                    st.error(f"Error: {e}")
