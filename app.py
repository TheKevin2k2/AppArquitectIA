import streamlit as st
import requests
import base64
from PIL import Image
import io
import urllib.parse
import time

# --- CONFIGURACIÓN DE SEGURIDAD ---
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

st.markdown("<h1 class='main-title'>🏗️ ArquitectIA Pro v7.3</h1>", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Ajustes de Precisión")
    estilo = st.selectbox("Estilo Arquitectónico:", ["Moderno Sobrio", "Minimalista", "Industrial", "Rústico Moderno"])
    mat_paredes = st.selectbox("Material Principal:", ["Concreto Visto", "Ladrillo", "Piedra", "Estuco Blanco", "Madera"])
    clima = st.selectbox("Iluminación:", ["Día Soleado", "Atardecer Cálido", "Nublado Realista", "Noche"])
    
    st.divider()
    
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
                        # 1. Preparar imagen
                        buffered = io.BytesIO()
                        img.save(buffered, format="PNG")
                        img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")
                        image_url = f"data:image/png;base64,{img_byte}"

                        # 2. Prompt unido en una sola línea para evitar SyntaxError
                        prompt_final = f"Professional architectural photography. Style: {estilo}. Walls: {mat_paredes}. Lighting: {clima}. {instruccion_usuario}. High-end materials, 8k resolution, strictly preserve original building geometry and footprint."

                        # 3. Llamada al motor Fal.ai
                        url_fal = "https://fal.run/fal-ai/flux/dev/image-to-image"
                        headers = {
                            "Authorization": f"Key {FAL_KEY}",
                            "Content-Type": "application/json"
                        }
                        
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
                            if "images" in data:
                                render_url = data["images"][0]["url"]
                                st.image(render_url, use_container_width=True)
                                st.success("✅ Renderizado completado.")
                                
                                img_res = requests.get(render_url)
                                st.download_button(
                                    label="💾 Descargar Imagen",
                                    data=img_res.content,
                                    file_name="render_arquitectia.png",
                                    mime="image/png"
                                )
                            else:
                                st.error("No se generó la imagen.")
                        else:
                            st.error(f"Error de API: {res.status_code}. Revisa tus créditos.")

                    except Exception as e:
                        st.error(f"Error técnico: {e}")
