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

st.set_page_config(page_title="ArquitectIA: Edición Profesional", layout="wide")
st.title("🏗️ ArquitectIA: Control Total de Diseño")

# 2. Barra Lateral con Control de Materiales
with st.sidebar:
    st.header("🎨 Parámetros Técnicos")
    estilo = st.selectbox("Estilo Base:", ["Minimalista Moderno", "Industrial Loft", "Rústico Elegante", "Futurista", "Contemporáneo"])
    
    st.subheader("Fidelidad del Diseño")
    fidelidad = st.select_slider("Nivel de respeto al modelo original:", options=["Creativo", "Equilibrado", "Estricto"], value="Estricto")
    
    st.subheader("Acabados")
    mat_paredes = st.selectbox("Paredes:", ["Concreto Aparente", "Ladrillo Visto", "Piedra", "Blanco Liso", "Madera"])
    clima = st.selectbox("Iluminación:", ["Soleado de tarde", "Atardecer", "Luz de Luna", "Nublado"])
    
    st.divider()
    st.info("💡 Tip: Para subir capturas rápido, presiona 'Impr Pant' en SketchUp y luego haz clic en el cargador de abajo y presiona Ctrl+V.")

# 3. Área Principal de Instrucciones
st.subheader("📝 Instrucciones Personalizadas")
prompt_usuario = st.text_area(
    "Describe detalles específicos (ej: 'añadir un auto deportivo rojo en la entrada', 'que las ventanas tengan reflejos verdes'):",
    placeholder="Escribe aquí tu visión para el render..."
)

# El cargador de archivos de Streamlit ya permite pegar imágenes directamente (Ctrl+V)
archivo = st.file_uploader("Sube o PEGA (Ctrl+V) tu captura de SketchUp", type=["jpg", "jpeg", "png"])

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Modelo Original")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER PROFESIONAL"):
        with col2:
            st.subheader("Resultado Final")
            
            with st.spinner("🧠 Sincronizando visión con el modelo 3D..."):
                try:
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    # PROMPT REFORZADO PARA EVITAR QUE CAMBIE EL DISEÑO
                    instruccion_base = (
                        f"ARCHITECTURAL RENDER. You MUST maintain the EXACT structural geometry and perspective of the building in the image. "
                        f"Do not change walls, roofs, or openings. Style: {estilo}. "
                        f"Materials: {mat_paredes}. Lighting: {clima}. "
                        f"User instructions: {prompt_usuario}. "
                        f"High-end exterior photography, architectural accuracy, photorealistic textures."
                    )

                    payload = {"contents": [{"parts": [
                        {"text": instruccion_base},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    res = requests.post(URL_GEMINI, json=payload, timeout=20)
                    data = res.json()

                    if "candidates" in data:
                        gen_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        gen_text = instruccion_base

                    # Fase de Dibujo
                    clean_prompt = "".join(e for e in gen_text if e.isalnum() or e == " ")
                    # Añadimos palabras clave de control para Pollinations
                    final_prompt = f"highly detailed architectural render, exact structure, {clean_prompt}"
                    encoded_prompt = urllib.parse.quote(final_prompt[:600])
                    seed = int(time.time())
                    url_imagen = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1240&height=720&nologo=true&seed={seed}"
                    
                    with st.spinner("🎨 Aplicando materiales..."):
                        r = requests.get(url_imagen, timeout=120) 
                        
                        if r.status_code == 200:
                            st.image(r.content, use_container_width=True)
                            st.success("¡Renderizado con éxito!")
                            st.download_button("💾 Descargar", r.content, f"render.png", "image/png")
                        else:
                            st.error("Error en el servidor de arte.")
                            st.markdown(f"👉 [Enlace directo]({url_imagen})")

                except Exception as e:
                    st.error(f"Error: {e}")
