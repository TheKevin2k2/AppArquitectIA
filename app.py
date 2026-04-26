import streamlit as st
import requests
import base64
from PIL import Image
import io
import urllib.parse
import time

# 1. Usamos solo la clave de Google (que ya tienes y es gratis)
API_KEY = "AIzaSyDCoHVw6g5K1UFEePZmkCv7Co12_OHCoYQ"
URL_GEMINI = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={API_KEY}"

st.set_page_config(page_title="ArquitectIA Gratis v8", layout="wide")

st.markdown("<h1 style='text-align: center;'>🏗️ ArquitectIA Free v8.0</h1>", unsafe_allow_html=True)
st.caption("Versión 100% gratuita sin límites de pago")

# 2. Configuración en la barra lateral
with st.sidebar:
    st.header("🎨 Estética")
    estilo = st.selectbox("Estilo:", ["Minimalista", "Moderno Industrial", "Rústico Contemporáneo"])
    clima = st.selectbox("Ambiente:", ["Día Soleado", "Atardecer Cálido", "Nublado"])
    st.divider()
    st.info("Para que salga igual: Activa las SOMBRAS en SketchUp antes de hacer la captura.")

# 3. Entrada de archivos
archivo = st.file_uploader("🖼️ Sube tu captura de SketchUp", type=["jpg", "jpeg", "png"])
instrucciones = st.text_input("📝 Materiales (ej: madera, cemento pulido...):")

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Tu Diseño")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER GRATIS"):
        with col2:
            with st.spinner("🧠 Analizando estructura..."):
                try:
                    # Convertir imagen para Gemini
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    # PROMPT DE "MAPA GEOMÉTRICO"
                    # Obligamos a Gemini a describir la imagen como si fuera un plano técnico
                    prompt_tecnico = (
                        "Describe esta imagen de SketchUp para un motor de renderizado. "
                        "Sé extremadamente específico con los volúmenes: 'un cubo a la izquierda', "
                        "'un ventanal rectangular al centro', 'techo plano'. "
                        f"Aplica estos materiales: {instrucciones} y estilo {estilo}. "
                        "IMPORTANTE: No inventes balcones, ni cambies la forma. Solo describe lo que ves."
                    )

                    payload = {"contents": [{"parts": [
                        {"text": prompt_tecnico},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    # Gemini genera la descripción (Gratis)
                    res = requests.post(URL_GEMINI, json=payload, timeout=20)
                    descripcion = res.json()["candidates"][0]["content"]["parts"][0]["text"]

                    # Limpiamos el texto para la URL
                    clean_description = "".join(e for e in descripcion if e.isalnum() or e == " ")
                    
                    # Usamos el motor de Pollinations (Gratis e ilimitado)
                    # Añadimos 'architecture' y 'photorealistic' para forzar calidad
                    final_prompt = f"Professional architectural photography, high-end render, {clean_description}, hyper-realistic, 8k"
                    encoded_prompt = urllib.parse.quote(final_prompt[:800])
                    
                    # Generamos el render
                    url_render = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed={int(time.time())}"
                    
                    st.image(url_render, use_container_width=True)
                    st.success("¡Render generado!")
                    
                    # Botón de descarga
                    r = requests.get(url_render)
                    st.download_button("💾 Guardar Render", r.content, "render_gratis.png", "image/png")

                except Exception as e:
                    st.error(f"Hubo un error: {e}")
