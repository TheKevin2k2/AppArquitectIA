import streamlit as st
import requests
import base64
from PIL import Image
import io
import urllib.parse
import time

# --- CONFIGURACIÓN DE LA NUEVA API KEY ---
API_KEY = "AIzaSyBLASApDrxbH68KPuNQJxWMCQPLBOYR4yk"
URL_GEMINI = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={API_KEY}"

st.set_page_config(page_title="ArquitectIA Pro v10", layout="wide")

# Estilo visual de la App
st.markdown("""
    <style>
    .stFileUploader { border: 2px dashed #4A90E2; padding: 20px; background-color: #f0f2f6; border-radius: 15px; }
    h1 { color: #1E3A8A; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🏗️ ArquitectIA v10.0 (Acceso Total)</h1>", unsafe_allow_html=True)
st.caption("✅ Conectado con nueva API Key | Generación Ilimitada")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Ajustes Estéticos")
    estilo = st.selectbox("Estilo Arquitectónico:", ["Moderno Sobrio", "Minimalista", "Industrial", "Rústico Moderno"])
    clima = st.selectbox("Iluminación:", ["Día Soleado", "Atardecer Cálido", "Nublado Realista", "Noche"])
    st.divider()
    st.info("💡 Consejo para tu hermano: Activa las sombras en SketchUp y usa fondo blanco para máxima fidelidad.")
    if st.button("🗑️ Reiniciar"):
        st.rerun()

# --- ÁREA DE TRABAJO ---
st.subheader("📝 Paso 1: Detalles opcionales")
instrucciones_usuario = st.text_input("Describe materiales (ej: concreto, madera, vidrio):", placeholder="Si lo dejas vacío, la IA decidirá lo mejor...")

archivo = st.file_uploader("🖼️ Paso 2: Sube tu captura de SketchUp", type=["jpg", "jpeg", "png"])

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Tu Modelo")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER"):
        with col2:
            with st.spinner("🧠 Analizando geometría y aplicando materiales..."):
                try:
                    # 1. Preparar imagen para Google Gemini
                    buffered = io.BytesIO()
                    img_convert = img.convert("RGB")
                    img_convert.save(buffered, format="JPEG", quality=85)
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    # 2. Intentar obtener descripción de la imagen
                    prompt_analisis = f"Act as an architect. Describe the volumes and geometry of this model briefly. Style: {estilo}. Materials: {instrucciones_usuario}."
                    
                    payload = {"contents": [{"parts": [
                        {"text": prompt_analisis},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    res = requests.post(URL_GEMINI, json=payload, timeout=15)
                    
                    # 3. Lógica de respuesta (con respaldo si falla la cuota)
                    if res.status_code == 200:
                        descripcion_ia = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        descripcion_ia = f"Professional architectural photography of a {estilo} building, {clima} lighting."

                    # 4. Generar el render final con Pollinations (Ilimitado)
                    prompt_render = f"Professional architectural render, photorealistic, 8k, {descripcion_ia}, {clima}, cinematic lighting, high quality textures."
                    encoded_prompt = urllib.parse.quote(prompt_render[:800])
                    
                    url_final = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed={int(time.time())}"
                    
                    # 5. Mostrar resultado
                    st.image(url_final, use_container_width=True)
                    st.success("✅ ¡Render finalizado!")
                    
                    # Botón de descarga
                    r_img = requests.get(url_final)
                    st.download_button("💾 Guardar Imagen", r_img.content, "render_arquitectia.png", "image/png")

                except Exception as e:
                    st.error("La IA de dibujo está tardando un poco. Intenta de nuevo en unos segundos.")
