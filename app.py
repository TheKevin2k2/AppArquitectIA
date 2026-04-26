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

# Estilo para mejorar la visibilidad del área de carga
st.markdown("""
    <style>
    .stFileUploader {
        border: 2px dashed #4A90E2;
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ ArquitectIA: Renderizado Profesional")

# 2. Instrucciones para el usuario
with st.expander("💡 ¿Cómo cargar tu captura rápido? (Haz clic aquí)", expanded=True):
    st.write("""
    1. Toma la captura en SketchUp (**Win + Shift + S**).
    2. **Arrastra** la miniatura que aparece abajo a la derecha directamente al recuadro gris.
    3. O simplemente guarda la imagen y arrástrala desde tu carpeta.
    """)

# 3. Barra Lateral de Control
with st.sidebar:
    st.header("🎨 Ajustes de Diseño")
    estilo = st.selectbox("Estilo:", ["Minimalista Moderno", "Industrial Loft", "Rústico", "Futurista"])
    fidelidad = st.radio("Fidelidad Estructural:", ["Estricta (No mover muros)", "Equilibrada", "Creativa"])
    mat_paredes = st.selectbox("Paredes:", ["Concreto", "Ladrillo", "Piedra", "Estuco", "Madera"])
    clima = st.selectbox("Iluminación:", ["Soleado", "Atardecer", "Noche", "Nublado"])
    st.divider()
    st.caption("v2.6 - Optimizado para Arrastrar/Soltar")

# 4. Entrada de Datos
st.subheader("📝 Detalles Específicos")
instruccion_usuario = st.text_area("Instrucciones adicionales:", placeholder="Ej: Que la iluminación sea cálida y añade vegetación...")

# Cargador de archivos con instrucción clara
archivo = st.file_uploader("🖼️ ARRASTRA AQUÍ TU CAPTURA DE SKETCHUP", type=["jpg", "jpeg", "png"])

if archivo:
    col_pre, col_res = st.columns(2)
    img = Image.open(archivo)
    
    with col_pre:
        st.subheader("Modelo Original")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER"):
        with col_res:
            with st.spinner("🧠 Analizando geometría y aplicando materiales..."):
                try:
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    # Refuerzo de prompt para respetar el diseño
                    strict_msg = "KEEP THE EXACT ORIGINAL GEOMETRY. DO NOT CHANGE WALLS OR ROOF." if fidelidad == "Estricta (No mover muros)" else ""
                    
                    prompt_completo = (
                        f"{strict_msg} Architectural photography. Style: {estilo}. "
                        f"Walls: {mat_paredes}. Lighting: {clima}. "
                        f"User Details: {instruccion_usuario}. Photorealistic, 8k resolution."
                    )

                    payload = {"contents": [{"parts": [
                        {"text": prompt_completo},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    res = requests.post(URL_GEMINI, json=payload, timeout=20)
                    data = res.json()
                    gen_text = data["candidates"][0]["content"]["parts"][0]["text"] if "candidates" in data else prompt_completo

                    # Fase de dibujo con Pollinations
                    clean_p = "".join(e for e in gen_text if e.isalnum() or e == " ")
                    final_p = f"Professional architectural render, masterpiece, realistic textures, {clean_p}"
                    url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(final_p[:700])}?width=1280&height=720&nologo=true&seed={int(time.time())}"
                    
                    r = requests.get(url_img, timeout=120)
                    if r.status_code == 200:
                        st.image(r.content, use_container_width=True)
                        st.success("¡Renderizado completado!")
                        st.download_button(label="💾 Descargar Imagen", data=r.content, file_name="render_arquitectia.png", mime="image/png")
                    else:
                        st.error("Error en el servidor de imagen. Intenta de nuevo.")
                except Exception as e:
                    st.error(f"Error técnico: {e}")
