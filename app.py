import streamlit as st
import requests
import base64
from PIL import Image
import io
import urllib.parse
import time

# --- CONFIGURACIÓN DE SEGURIDAD ---
API_KEY = "AIzaSyBLASApDrxbH68KPuNQJxWMCQPLBOYR4yk"
URL_GEMINI = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={API_KEY}"

st.set_page_config(page_title="ArquitectIA v10.5 Ultra", layout="wide")

# Estilo visual para que se vea profesional
st.markdown("""
    <style>
    .stFileUploader { border: 2px dashed #4A90E2; padding: 20px; background-color: #f0f2f6; border-radius: 15px; }
    h1 { color: #1E3A8A; text-align: center; font-family: 'Helvetica', sans-serif; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #1E3A8A; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🏗️ ArquitectIA v10.5 (Fidelidad Optimizada)</h1>", unsafe_allow_html=True)
st.caption("🚀 Conexión activa | Modo de análisis geométrico profundo")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configuración")
    estilo = st.selectbox("Estilo Visual:", ["Moderno Sobrio", "Minimalista", "Industrial", "Rústico Moderno"])
    clima = st.selectbox("Ambiente/Luz:", ["Día Soleado", "Atardecer Cálido", "Nublado Realista", "Noche"])
    
    st.divider()
    st.warning("⚠️ IMPORTANTE PARA TU HERMANO:\n1. Fondo de SketchUp en BLANCO.\n2. Sombras ACTIVADAS.\n3. Sin esto, el render será absurdo.")
    
    if st.button("🗑️ Limpiar Todo"):
        st.rerun()

# --- ÁREA DE TRABAJO ---
col_inputs = st.columns([1, 1])
with col_inputs[0]:
    instrucciones_usuario = st.text_input("📝 Materiales específicos:", placeholder="Ej: Madera de nogal, concreto pulido, cristales negros...")

archivo = st.file_uploader("🖼️ Sube tu captura de SketchUp", type=["jpg", "jpeg", "png"])

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Captura Original")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER PROFESIONAL"):
        with col2:
            with st.spinner("🧠 Analizando volúmenes y texturizando..."):
                try:
                    # 1. Procesar imagen para la IA
                    buffered = io.BytesIO()
                    img_convert = img.convert("RGB")
                    img_convert.save(buffered, format="JPEG", quality=90)
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    # 2. Prompt técnico agresivo para evitar que la IA invente
                    prompt_analisis = (
                        f"Analyze this 3D model. Identify the exact architectural volumes, wall positions, and roof shape. "
                        f"Describe it as a high-end architectural photograph. "
                        f"Strictly follow the building footprint. Style: {estilo}. "
                        f"Materials to apply: {instrucciones_usuario}. Lighting: {clima}. "
                        "Do
