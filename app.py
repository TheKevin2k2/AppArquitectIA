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

st.set_page_config(page_title="ArquitectIA: Renderizador Pro", layout="wide")
st.title("🏗️ ArquitectIA: Control de Fachadas")

# 2. Barra Lateral con Control de Materiales
with st.sidebar:
    st.header("🎨 Especificaciones Técnicas")
    estilo = st.selectbox("Estilo Arquitectónico:", ["Minimalista Moderno", "Industrial Loft", "Rústico Elegante", "Futurista", "Mediterráneo"])
    
    st.subheader("Materiales de Exterior")
    mat_paredes = st.selectbox("Paredes/Fachada:", ["Concreto Aparente", "Ladrillo Visto", "Piedra Natural", "Estuco Blanco", "Madera Carbonizada"])
    mat_pisos = st.selectbox("Pisos de Acceso:", ["Microcemento", "Madera de Roble", "Mármol Pulido", "Piedra Tecnológica"])
    mat_ventanas = st.selectbox("Ventanería:", ["Aluminio Negro", "Marcos de Madera", "Acero Corten", "Sin marcos (Vidrio total)"])
    
    st.subheader("Iluminación y Clima")
    clima = st.selectbox("Ambiente:", ["Soleado de tarde", "Atardecer Dorado", "Noche con luces cálidas", "Nublado melancólico"])
    
    detalles_extra = st.text_input("Detalles específicos:", "Mucha vegetación perimetral")
    st.divider()
    st.info("Nota: Se forzará la vista exterior siguiendo la perspectiva de tu captura.")

# 3. Carga de Archivos
archivo = st.file_uploader("Sube tu captura de SketchUp (Vista Exterior)", type=["jpg", "jpeg", "png"])

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Captura de SketchUp")
        st.image(img, use_container_width=True)

    if st.button("✨ GENERAR RENDER EXTERIOR"):
        with col2:
            st.subheader("Renderizado Final")
            
            with st.spinner("🧠 Procesando fachada y materiales..."):
                try:
                    # Preparar imagen para enviar a la IA
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    # PROMPT REFORZADO PARA EXTERIORES
                    instruccion_ia = (
                        f"EXTERIOR architectural photography of the building facade. "
                        f"View from the outside, following the exact perspective of the attached SketchUp image. "
                        f"Style: {estilo}. Materials: Walls {mat_paredes}, floors {mat_pisos}, "
                        f"windows {mat_ventanas}. Lighting: {clima}. "
                        f"Environment: {detalles_extra}. High-end exterior render, 8k, realistic sky, cinematic lighting."
                    )

                    payload = {"contents": [{"parts": [
                        {"text": instruccion_ia},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    # Fase 1: Análisis con Gemini
                    res = requests.post(URL_GEMINI, json=payload, timeout=20)
                    data = res.json()

                    if "candidates" in data:
                        gen_text = data["candidates"][0]["content"]["parts"][0]["text"]
                        st.caption(f"✅ Análisis de fachada optimizado para {estilo}.")
                    else:
                        st.warning("⚠️ Usando motor de respaldo para exteriores.")
                        gen_text = instruccion_ia

                    # Fase 2: Dibujo con Pollinations (Paciencia extra)
                    clean_prompt = "".join(e for e in gen_text if e.isalnum() or e == " ")
                    encoded_prompt = urllib.parse.quote(clean_prompt[:500])
                    seed = int(time.time())
                    url_imagen = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={seed}"
                    
                    with st.spinner("🎨 Aplicando texturas fotorrealistas..."):
                        # Timeout extendido a 120 segundos para renders complejos
                        r = requests.get(url_imagen, timeout=120) 
                        
                        if r.status_code == 200:
                            st.image(r.content, caption=f"Exterior: {mat_paredes} - {clima}", use_container_width=True)
                            st.success("¡Renderizado exterior completado!")
                            st.download_button("💾 Guardar Render Pro", r.content, f"render_exterior_{int(time.time())}.png", "image/png")
                        else:
                            st.error("El servidor de imágenes está saturado.")
                            st.markdown(f"👉 [VER RENDER EN NAVEGADOR]({url_imagen})")

                except requests.exceptions.Timeout:
                    st.error("⌛ El servidor tardó demasiado. Por favor, intenta de nuevo.")
                except Exception as e:
                    st.error(f"Error técnico: {e}")
else:
    st.info("👋 Sube una captura exterior de SketchUp para generar el render.")
