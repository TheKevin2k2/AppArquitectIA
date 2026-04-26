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

st.set_page_config(page_title="ArquitectIA: Especificador de Materiales", layout="wide")
st.title("🏗️ ArquitectIA: Control de Acabados")

# 2. Barra Lateral con Control de Materiales
with st.sidebar:
    st.header("🎨 Especificaciones")
    estilo = st.selectbox("Estilo Arquitectónico:", ["Minimalista Moderno", "Industrial Loft", "Rústico Elegante", "Futurista", "Mediterráneo"])
    
    st.subheader("Materiales Principales")
    mat_paredes = st.selectbox("Paredes/Fachada:", ["Concreto Aparente", "Ladrillo Visto", "Piedra Natural", "Estuco Blanco", "Madera Carbonizada"])
    mat_pisos = st.selectbox("Pisos:", ["Microcemento", "Madera de Roble", "Mármol Pulido", "Piedra Tecnológica"])
    mat_ventanas = st.selectbox("Ventanería:", ["Aluminio Negro", "Marcos de Madera", "Acero Corten", "Sin marcos (Vidrio total)"])
    
    st.subheader("Iluminación y Clima")
    clima = st.selectbox("Ambiente:", ["Soleado de tarde", "Atardecer Dorado", "Noche con luces cálidas", "Nublado melancólico"])
    
    detalles_extra = st.text_input("Detalles específicos:", "Mucha vegetación perimetral")
    st.divider()
    st.info("La IA priorizará estos materiales en el render final.")

# 3. Carga de Archivos
archivo = st.file_uploader("Sube tu captura de SketchUp", type=["jpg", "jpeg", "png"])

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Modelo Base")
        st.image(img, use_container_width=True)

    if st.button("✨ GENERAR CON ESTOS MATERIALES"):
        with col2:
            st.subheader("Renderizado con Acabados")
            
            with st.spinner("🧠 Coordinando materiales y luces..."):
                try:
                    # Preparar imagen
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    # CREACIÓN DEL PROMPT TÉCNICO
                    # Aquí unimos todas las elecciones del usuario en una sola instrucción potente
                    instruccion_ia = (
                        f"Architectural photorealistic render. Style: {estilo}. "
                        f"Main materials: Walls made of {mat_paredes}, floors made of {mat_pisos}, "
                        f"and window frames in {mat_ventanas}. Lighting: {clima}. "
                        f"Environment: {detalles_extra}. High-end architectural photography, 8k, realistic textures."
                    )

                    payload = {"contents": [{"parts": [
                        {"text": instruccion_ia},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    # Fase Gemini
                    res = requests.post(URL_GEMINI, json=payload, timeout=15)
                    data = res.json()

                    if "candidates" in data:
                        gen_text = data["candidates"][0]["content"]["parts"][0]["text"]
                        st.caption(f"✅ Materiales detectados: {mat_paredes}, {mat_pisos}.")
                    else:
                        st.warning("⚠️ Modo respaldo activo.")
                        gen_text = instruccion_ia

                    # Fase Dibujo (Pollinations)
                    clean_prompt = "".join(e for e in gen_text if e.isalnum() or e == " ")
                    encoded_prompt = urllib.parse.quote(clean_prompt[:500])
                    seed = int(time.time())
                    url_imagen = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={seed}"
                    
                    with st.spinner("🎨 Aplicando texturas..."):
                        r = requests.get(url_imagen, timeout=120) 
                        
                        if r.status_code == 200:
                            st.image(r.content, caption=f"Fachada: {mat_paredes} | Suelo: {mat_pisos}", use_container_width=True)
                            st.success("¡Render listo para presentación!")
                            st.download_button("💾 Guardar Render Pro", r.content, f"render_{mat_paredes}.png", "image/png")
                        else:
                            st.error("Servidor ocupado. Intenta de nuevo.")

                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.info("👋 Configura los materiales y sube tu captura para empezar.")