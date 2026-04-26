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

# Estilo personalizado para resaltar el área de pegado
st.markdown("""
    <style>
    .stFileUploader {
        border: 2px dashed #4A90E2;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ ArquitectIA: Renderizado Profesional")
st.write("Copia tu captura en SketchUp y **pégala aquí abajo con Ctrl+V**")

# 2. Barra Lateral
with st.sidebar:
    st.header("🎨 Ajustes de Precisión")
    estilo = st.selectbox("Estilo:", ["Minimalista Moderno", "Industrial Loft", "Rústico", "Futurista"])
    
    st.subheader("Rigidez Estructural")
    fidelidad = st.radio("Respeto al volumen original:", ["Máximo (No cambiar formas)", "Equilibrado", "Artístico"])
    
    mat_paredes = st.selectbox("Paredes:", ["Concreto", "Ladrillo", "Piedra", "Estuco", "Madera"])
    clima = st.selectbox("Iluminación:", ["Soleado", "Atardecer", "Noche", "Nublado"])
    
    st.divider()
    st.caption("v2.2 - Corrección de sintaxis")

# 3. Input de usuario (Prompt abierto)
st.subheader("💬 Instrucciones adicionales para la IA")
instruccion_usuario = st.text_area("Ejemplo: 'Que la puerta sea de roble oscuro y añade un jardín seco en el frente'", placeholder="Escribe aquí los detalles que la IA debe respetar...")

# Cargador de archivos
archivo = st.file_uploader("Haz clic aquí y presiona Ctrl + V para pegar la captura", type=["jpg", "jpeg", "png"])

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Referencia original")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER"):
        with col2:
            with st.spinner("🧠 Sincronizando materiales..."):
                try:
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    # PROMPT ULTRA-ESTRICTO
                    prompt_fidelidad = "STRICT GEOMETRY. Do not alter the building's shape, windows, or roof lines." if fidelidad == "Máximo (No cambiar formas)" else "Maintain overall structure."
                    
                    prompt_completo = (
                        f"{prompt_fidelidad} Architectural visualization. Style: {estilo}. "
                        f"Materials: {mat_paredes}. Lighting: {clima}. "
                        f"Specific User Request: {instruccion_usuario}. "
                        f"Photorealistic 8k, architectural accuracy is priority."
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
                    final_p = f"Professional render, architectural photography, exact building shape, {clean_prompt}"
                    encoded_p = urllib.parse.quote(final_p[:600])
                    url_img = f"https://image.pollinations.ai/prompt/{encoded_p}?width=1280&height=720&nologo=true&seed={int(time.time())}"
                    
                    r = requests.get(url_img, timeout=120)
                    
                    # AQUÍ ESTABA EL ERROR: Corregido a 200 y con ":"
                    if r.status_code == 200:
                        st.image(r.content, use_container_width=True)
                        st.success("Render finalizado")
                        st.download_button("💾 Guardar", r.content, "render.png", "image/png")
                    else:
                        st.error(f"Error del servidor: {r.status_code}")
                        
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.info("💡 **Cómo pegar:** Toma la captura (Win + Shift + S), haz un clic en el recuadro azul de arriba y presiona **Ctrl + V**.")
