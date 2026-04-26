import streamlit as st
import requests
import base64
from PIL import Image
import io
import urllib.parse
import time

# --- CONFIGURACIÓN DE SEGURIDAD ---
# El código buscará la clave en la sección "Secrets" de Streamlit Cloud
try:
    FAL_KEY = st.secrets["FAL_KEY"]
except:
    FAL_KEY = "FALTA_CLAVE"

st.set_page_config(page_title="ArquitectIA Pro: Control Estructural", layout="wide")

# --- INTERFAZ VISUAL ---
st.markdown("""
    <style>
    .stFileUploader {
        border: 2px dashed #4A90E2;
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 15px;
    }
    .main-title {
        color: #1E3A8A;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🏗️ ArquitectIA Pro v7.2</h1>", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Ajustes de Precisión")
    estilo = st.selectbox("Estilo Arquitectónico:", ["Moderno Sobrio", "Minimalista", "Industrial", "Rústico Moderno"])
    mat_paredes = st.selectbox("Material Principal:", ["Concreto Visto", "Ladrillo", "Piedra", "Estuco Blanco", "Madera"])
    clima = st.selectbox("Iluminación:", ["Día Soleado", "Atardecer Cálido", "Nublado Realista", "Noche"])
    
    st.divider()
    
    # Este es el control más importante para tu hermano
    structural_strength = st.slider(
        "Fidelidad Estructural (0.90 = No cambia la forma):",
        min_value=0.0, max_value=1.0, value=0.90, step=0.05
    )
    
    st.info("💡 Consejo: Usa 0.90 para que la IA respete cada muro de SketchUp.")
    
    if st.button("🗑️ Limpiar Pantalla"):
        st.rerun()

# --- ÁREA DE TRABAJO ---
st.subheader("📝 Detalles Finales")
instruccion_usuario = st.text_area(
    "Describe materiales específicos y el entorno:",
    placeholder="Ej: Suelo de madera clara, marcos de ventanas negros, añadir mucha vegetación y jardín..."
)

archivo = st.file_uploader("🖼️ Sube tu captura de SketchUp aquí", type=["jpg", "jpeg", "png"])

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Tu Modelo Original")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER PROFESIONAL"):
        if FAL_KEY == "FALTA_CLAVE":
            st.error("⚠️ Error: No has configurado la clave 'FAL_KEY' en los Secrets de Streamlit.")
        else:
            with col2:
                with st.spinner("🧠 Procesando geometría y texturas..."):
                    try:
                        # 1. Preparar imagen para la IA
                        buffered = io.BytesIO()
                        img.save(buffered, format="PNG")
                        img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")
                        image_url = f"data:image/png;base64,{img_byte}"

                        # 2. Configurar el prompt técnico
                        prompt_final = (
                            f"Professional architectural photography of the building in the reference image. "
                            f"Style: {estilo}. Main material: {mat_paredes}. Lighting: {clima}. "
                            f"Details: {instruccion_usuario}. High-end materials, 8k resolution, "
                            f"strictly
