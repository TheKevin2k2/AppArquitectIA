import streamlit as st
import requests
import base64
from PIL import Image
import io
import urllib.parse
import time

# 1. Configuración Principal
API_KEY = "AIzaSyDCoHVw6g5K1UFEePZmkCv7Co12_OHCoYQ"
URL_GEMINI = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={API_KEY}"

st.set_page_config(page_title="ArquitectIA Pro", layout="wide")

st.title("🏗️ ArquitectIA: Renderizado de Precisión")

# 2. Instrucciones Dinámicas
st.info("""
**💡 Guía para pegar capturas:**
1. Toma tu captura en SketchUp (**Win + Shift + S**).
2. Haz **un clic** en el recuadro de abajo (ignora si se abre la carpeta).
3. Presiona **Ctrl + V** en tu teclado.
""")

# 3. Barra Lateral
with st.sidebar:
    st.header("🎨 Ajustes")
    estilo = st.selectbox("Estilo:", ["Minimalista Moderno", "Industrial Loft", "Rústico", "Futurista"])
    fidelidad = st.radio("Fidelidad Estructural:", ["Estricta (No mover muros)", "Equilibrada", "Creativa"])
    mat_paredes = st.selectbox("Paredes:", ["Concreto", "Ladrillo", "Piedra", "Estuco", "Madera"])
    clima = st.selectbox("Iluminación:", ["Soleado", "Atardecer", "Noche", "Nublado"])

# 4. Área de Carga y Prompt
instruccion_usuario = st.text_area("📝 Instrucciones de diseño:", placeholder="Ej: Añadir marcos negros a las ventanas y un camino de piedra...")

# El componente de Streamlit ya procesa el pegado si tiene el foco
archivo = st.file_uploader("🔽 PEGA O ARRASTRA AQUÍ TU CAPTURA", type=["jpg", "jpeg", "png"])

if archivo:
    col_pre, col_res = st.columns(2)
    img = Image.open(archivo)
    
    with col_pre:
        st.subheader("Modelo Original")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER"):
        with col_res:
            with st.spinner("🧠 Generando fotorrealismo..."):
                try:
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    # Refuerzo de prompt para respetar SketchUp
                    strict = "Keep the exact original building volume and architectural lines." if fidelidad == "Estricta (No mover muros)" else ""
                    
                    prompt_completo = (
                        f"{strict} Architectural photography. Style: {estilo}. "
                        f"Walls: {mat_paredes}. Light: {clima}. "
                        f"Details: {instruccion_usuario}. High resolution, 8k."
                    )

                    payload = {"contents": [{"parts": [
                        {"text": prompt_completo},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    res = requests.post(URL_GEMINI, json=payload, timeout=20)
                    data = res.json()
                    gen_text = data["candidates"][0]["content"]["parts"][0]["text"] if "candidates" in data else prompt_completo

                    # Dibujo
                    clean_p = "".join(e for e in gen_text if e.isalnum() or e == " ")
                    final_p = f"Professional architectural render, masterpiece, {clean_p}"
                    url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(final_p[:700])}?width=1280&height=720&nologo=true&seed={int(time.time())}"
                    
                    r = requests.get(url_img, timeout=120)
                    if r.status_code == 200:
                        st.image(r.content, use_container_width=True)
                        st.success("¡Render listo!")
                        st.download_button("💾 Descargar", r.content,
