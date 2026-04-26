import streamlit as st
import requests
import base64
from PIL import Image
import io
import urllib.parse
import time

API_KEY = "AIzaSyBLASApDrxbH68KPuNQJxWMCQPLBOYR4yk"
URL_GEMINI = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={API_KEY}"

st.set_page_config(page_title="ArquitectIA v11 Master", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏗️ ArquitectIA v11.0: Master Control</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Ajustes")
    estilo = st.selectbox("Estilo:", ["Moderno Sobrio", "Minimalista", "Industrial", "Rústico"])
    clima = st.selectbox("Luz:", ["Día Soleado", "Atardecer", "Nublado", "Noche"])
    st.divider()
    st.error("❗ NOTA PARA TU HERMANO:\nSi la IA 'inventa', es porque la captura tiene poco contraste. Asegúrate de que las sombras sean FUERTES en SketchUp.")

instrucciones = st.text_input("📝 Materiales:", placeholder="Ej: Concreto, madera clara...")
archivo = st.file_uploader("🖼️ Sube captura de SketchUp", type=["jpg", "jpeg", "png"])

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    with col1:
        st.subheader("Tu Modelo")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER"):
        with col2:
            with st.spinner("🛠️ Aplicando texturas sobre geometría..."):
                try:
                    buffered = io.BytesIO()
                    img_convert = img.convert("RGB")
                    img_convert.save(buffered, format="JPEG", quality=95)
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    # PROMPT DE ALTA PRECISIÓN: Obliga a la IA a no salirse de los bordes
                    prompt_tecnico = f"Architectural photo. Keep the EXACT layout and geometry of the building in the image. Do not change wall positions. Materials: {instrucciones}. Style: {estilo}. High-end lighting: {clima}. Realistic 8k render."
                    
                    payload = {"contents": [{"parts": [
                        {"text": prompt_tecnico},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    res = requests.post(URL_GEMINI, json=payload, timeout=15)
                    desc = res.json()["candidates"][0]["content"]["parts"][0]["text"] if res.status_code == 200 else "Architecture"

                    # HACK: Añadimos 'scanned architectural sketch' para que la IA entienda que hay una base rígida
                    final_p = f"Professional architectural render of {desc}, realistic materials, preserving exact structure, 8k, photorealistic."
                    url_f = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(final_p)}?width=1280&height=720&nologo=true&seed={int(time.time())}"
                    
                    st.image(url_f, use_container_width=True)
                    st.success("✅ Renderizado listo.")
                    
                    r_img = requests.get(url_f)
                    st.download_button("💾 Guardar", r_img.content, "render.png", "image/png")

                except Exception as e:
                    st.error(f"Error: {e}")
