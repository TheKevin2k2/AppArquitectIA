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

st.set_page_config(page_title="ArquitectIA Pro: Control Total", layout="wide")

# Título y manual de uso rápido
st.title("🏗️ ArquitectIA: Renderizado Profesional")

# 2. Barra Lateral
with st.sidebar:
    st.header("🎨 Ajustes de Precisión")
    estilo = st.selectbox("Estilo:", ["Minimalista Moderno", "Industrial Loft", "Rústico", "Futurista"])
    fidelidad = st.radio("Respeto al volumen original:", ["Máximo (No cambiar formas)", "Equilibrado", "Artístico"])
    mat_paredes = st.selectbox("Paredes:", ["Concreto", "Ladrillo", "Piedra", "Estuco", "Madera"])
    clima = st.selectbox("Iluminación:", ["Soleado", "Atardecer", "Noche", "Nublado"])
    st.divider()
    st.caption("v2.3 - Clipboard Fix")

# 3. ZONA DE CARGA (Aquí está el truco)
st.subheader("📸 Sube o Pega tu Captura")
col_input, col_info = st.columns([2, 1])

with col_info:
    st.info("""
    **Para pegar con Ctrl+V:**
    1. Toma la captura (Win+Shift+S).
    2. Haz UN CLIC en el recuadro de abajo.
    3. Presiona Ctrl+V.
    *Si falla, guarda la imagen y arrástrala.*
    """)

# El cargador de Streamlit en versiones recientes soporta pegar si tiene el foco
archivo = st.file_uploader("Área de carga (Soporta Pegado Directo)", type=["jpg", "jpeg", "png"])

# 4. Input de usuario
st.subheader("💬 Instrucciones adicionales")
instruccion_usuario = st.text_area("Ejemplo: 'Añadir ventanales de piso a techo'", placeholder="Escribe aquí...")

if archivo:
    col_pre, col_res = st.columns(2)
    img = Image.open(archivo)
    
    with col_pre:
        st.subheader("Referencia original")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER"):
        with col_res:
            with st.spinner("🧠 Generando texturas de alta calidad..."):
                try:
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    prompt_fidelidad = "STRICT GEOMETRY. DO NOT ALTER THE BUILDING SHAPE." if fidelidad == "Máximo (No cambiar formas)" else "Maintain overall structure."
                    
                    prompt_completo = (
                        f"{prompt_fidelidad} Architectural visualization. Style: {estilo}. "
                        f"Materials: {mat_paredes}. Lighting: {clima}. "
                        f"User Request: {instruccion_usuario}. Photorealistic 8k."
                    )

                    payload = {"contents": [{"parts": [
                        {"text": prompt_completo},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    res = requests.post(URL_GEMINI, json=payload, timeout=20)
                    data = res.json()
                    gen_text = data["candidates"][0]["content"]["parts"][0]["text"] if "candidates" in data else prompt_completo

                    # Fase de dibujo
                    clean_prompt = "".join(e for e in gen_text if e.isalnum() or e == " ")
                    final_p = f"Professional architectural photography, masterpiece, exact building shape, {clean_prompt}"
                    encoded_p = urllib.parse.quote(final_p[:700])
                    url_img = f"https://image.pollinations.ai/prompt/{encoded_p}?width=1280&height=720&nologo=true&seed={int(time.time())}"
                    
                    r = requests.get(url_img, timeout=120)
                    if r.status_code == 200:
                        st.image(r.content, use_container_width=True)
                        st.success("Render finalizado")
                        st.download_button("💾 Guardar", r.content, "render_arquitectia.png", "image/png")
                    else:
                        st.error("Servidor saturado. Reintenta en 5 segundos.")
                except Exception as e:
                    st.error(f"Error: {e}")
