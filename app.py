import streamlit as st
import requests
import base64
from PIL import Image
import io
import urllib.parse
import time

# 1. Configuración de API
# Consigue tu clave gratis en fal.ai para que la fidelidad sea real
FAL_KEY = "TU_CLAVE_FAL_AI_AQUÍ" 

st.set_page_config(page_title="ArquitectIA Pro: Fidelidad Estricta", layout="wide")
st.title("🏗️ ArquitectIA Pro v7.1 (Motor Fal.ai)")

# Estilo visual
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
    structural_strength = st.slider(
        "Fidelidad Estructural (0.9 = No cambia la forma):",
        min_value=0.0, max_value=1.0, value=0.85, step=0.05
    )
    
    if st.button("🗑️ Limpiar Pantalla"):
        st.rerun()

# 3. Inputs
st.subheader("📝 Detalles de Acabado")
instruccion_usuario = st.text_area(
    "Describe materiales y entorno:",
    placeholder="Ej: Suelo de grava, marcos negros, vegetación frondosa..."
)

archivo = st.file_uploader("🖼️ Sube tu captura de SketchUp", type=["jpg", "jpeg", "png"])

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Modelo Original")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER"):
        if FAL_KEY == "TU_CLAVE_FAL_AI_AQUÍ":
            st.error("⚠️ Falta la clave API de fal.ai en el código.")
        else:
            with col2:
                with st.spinner("🧠 Aplicando texturas a la estructura..."):
                    try:
                        # Preparar imagen
                        buffered = io.BytesIO()
                        img.save(buffered, format="PNG")
                        img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")
                        image_url = f"data:image/png;base64,{img_byte}"

                        prompt_final = (
                            f"Professional architectural photography. Building style: {estilo}. "
                            f"Walls: {mat_paredes}. Lighting: {clima}. {instruccion_usuario}. "
                            "High-end materials, 8k resolution, preserve original geometry."
                        )

                        url_fal = "https://fal.run/fal-ai/flux/dev/image-to-image"
                        headers = {"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"}
                        
                        payload = {
                            "prompt": prompt_final,
                            "image_url": image_url,
                            "strength": 1.0 - structural_strength,
                            "num_inference_steps": 40,
                            "guidance_scale": 7.5
                        }

                        res = requests.post(url_fal, json=payload, headers=headers, timeout=120)
                        
                        if res.status_code == 200:
                            data = res.json()
                            render_url = data["images"][0]["url"]
                            st.image(render_url, use_container_width=True)
                            st.success("Render finalizado.")
                            
                            # Botón de descarga
                            img_res = requests.get(render_url)
                            st.download_button("💾 Guardar Render", img_res.content, "render.png", "image/png")
                        else:
                            st.error(f"Error de API: {res.status_code}")

                    except Exception as e:
                        st.error(f"Error técnico: {e}")
