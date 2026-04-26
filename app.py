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

st.set_page_config(page_title="ArquitectIA Pro", layout="wide")

st.title("🏗️ ArquitectIA: Renderizado de Precisión")

# 2. Barra Lateral
with st.sidebar:
    st.header("🎨 Ajustes")
    estilo = st.selectbox("Estilo:", ["Minimalista Moderno", "Industrial Loft", "Rústico", "Futurista"])
    fidelidad = st.radio("Fidelidad Estructural:", ["Estricta", "Equilibrada", "Creativa"])
    mat_paredes = st.selectbox("Paredes:", ["Concreto", "Ladrillo", "Piedra", "Estuco", "Madera"])
    clima = st.selectbox("Iluminación:", ["Soleado", "Atardecer", "Noche", "Nublado"])

# 3. EL TRUCO DEL PEGADO
st.subheader("📸 Cargar Imagen")
# Usamos un text_input oculto que "atrapa" eventos de pegado en algunos navegadores
captura_pegar = st.text_input("📋 CLIC AQUÍ Y LUEGO CTRL+V (Solo para pegar)", placeholder="Haz clic y pega...")

# Cargador normal (por si el pegado falla)
archivo_subido = st.file_uploader("O arrastra el archivo aquí:", type=["jpg", "jpeg", "png"])

# 4. Detalles de diseño
instruccion_usuario = st.text_area("📝 Órdenes extra:", placeholder="Ej: Añadir mucha luz cálida...")

# Lógica para detectar si se pegó algo o se subió archivo
archivo = archivo_subido

if archivo:
    col_pre, col_res = st.columns(2)
    img = Image.open(archivo)
    
    with col_pre:
        st.subheader("Modelo Original")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER"):
        with col_res:
            with st.spinner("🧠 Procesando..."):
                try:
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    strict = "KEEP EXACT ARCHITECTURAL LINES." if fidelidad == "Estricta" else ""
                    prompt_completo = f"{strict} Architecture {estilo}, walls {mat_paredes}, {clima}. {instruccion_usuario}"

                    payload = {"contents": [{"parts": [
                        {"text": prompt_completo},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    res = requests.post(URL_GEMINI, json=payload, timeout=20)
                    data = res.json()
                    gen_text = data["candidates"][0]["content"]["parts"][0]["text"] if "candidates" in data else prompt_completo

                    clean_p = "".join(e for e in gen_text if e.isalnum() or e == " ")
                    final_p = f"Professional architectural photography, masterpiece, {clean_p}"
                    url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(final_p[:700])}?width=1280&height=720&nologo=true&seed={int(time.time())}"
                    
                    r = requests.get(url_img, timeout=120)
                    if r.status_code == 200:
                        st.image(r.content, use_container_width=True)
                        st.success("¡Render listo!")
                        st.download_button(label="💾 Descargar", data=r.content, file_name="render.png", mime="image/png")
                except Exception as e:
                    st.error(f"Error: {e}")
elif captura_pegar:
    st.warning("⚠️ El navegador no permite pegar imágenes directamente en cuadros de texto por seguridad. Por favor, arrastra el archivo desde tu carpeta de Imágenes.")
