import streamlit as st
import requests
import base64
from PIL import Image
import io
import urllib.parse
import time
import os

# 1. Configuración de API (CAMBIO DE MOTOR)
# Necesitas una clave de fal.ai. Consíguela gratis registrándote en fal.ai
FAL_KEY = "TU_CLAVE_FAL_AI_AQUÍ" # <--- REEMPLAZA ESTO

st.set_page_config(page_title="ArquitectIA Pro: Fidelidad Estricta", layout="wide")
st.title("🏗️ ArquitectIA Pro v7.0 (Motor Fal.ai)")

# Estilo para el área de carga
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

# 2. Barra Lateral
with st.sidebar:
    st.header("⚙️ Control de Render")
    estilo = st.selectbox("Estilo Técnico:", ["Moderno", "Minimalista", "Industrial", "Rústico Moderno"])
    mat_paredes = st.selectbox("Material Paredes:", ["Concreto Visto", "Ladrillo", "Piedra", "Estuco Blanco", "Madera"])
    clima = st.selectbox("Iluminación:", ["Día Soleado", "Atardecer Cálido", "Nublado Realista", "Noche"])
    
    st.divider()
    
    # Nuevo Slider de Control de Estructura
    structural_strength = st.slider(
        "Fidelidad Estructural (Cuanto más alto, menos cambia la forma):",
        min_value=0.0, max_value=1.0, value=0.85, step=0.05
    )
    
    st.info("Nota: v7.0 usa tecnología Image-to-Image estricta sobre la captura original.")

# 3. Inputs de usuario
st.subheader("📝 Detalles de Acabado")
instruccion_usuario = st.text_area(
    "Describe materiales específicos y entorno (ej: 'Suelo de grava, marcos negros, vegetación frondosa'):",
    placeholder="No dejes que la IA adivine los materiales..."
)

# 4. Carga de imagen
archivo = st.file_uploader("🖼️ Sube tu captura de SketchUp", type=["jpg", "jpeg", "png"])

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Modelo de SketchUp (Plantilla)")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER FIEL"):
        if FAL_KEY == "TU_CLAVE_FAL_AI_AQUÍ":
            st.error("⚠️ Error: No has puesto tu clave API de fal.ai en el código.")
        else:
            with col2:
                with st.spinner("🧠 Aplicando texturas fotorrealistas a la estructura..."):
                    try:
                        # Preparar imagen (Base64)
                        buffered = io.BytesIO()
                        img.save(buffered, format="PNG")
                        img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")
                        image_url = f"data:image/png;base64,{img_byte}"

                        # Crear prompt de arquitectura
                        prompt_final = (
                            f"Professional architectural photography of the building shown in the reference image. "
                            f"Style: {estilo}. Walls made of {mat_paredes}. Lighting: {clima}. "
                            f"Details: {instruccion_usuario}. Hyper-realistic, 8k resolution, octane render. "
                            f"Preserve the exact geometry of the original image."
                        )

                        # URL del endpoint de Fal.ai (usando Flux Realism o similar)
                        url_fal = "https://fal.run/fal-ai/flux/dev/image-to-image"
                        
                        headers = {
                            "Authorization": f"Key {FAL_KEY}",
                            "Content-Type": "application/json"
                        }
                        
                        payload = {
                            "prompt": prompt_final,
                            "image_url": image_url,
                            "strength": 1.0 - structural_strength, # Control de fidelidad
                            "num_inference_steps": 40,
                            "guidance_scale": 7.5,
                            "enable_safety_checker": True
                        }

                        # Llamada a la API de Fal.ai
                        res = requests.post(url_fal, json=payload, headers=headers, timeout=120)
                        
                        if res.status_code == 200:
                            data = res.json()
                            if "images" in data and len(data["images"]) > 0:
                                render_url = data["images"][0]["url"]
                                st.image(render_url, use_container_width=True)
                                st.success("¡Renderizado con alta fidelidad estructural!")
                                
                                # Botón para
