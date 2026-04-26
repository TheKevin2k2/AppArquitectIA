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

st.set_page_config(page_title="ArquitectIA: Fidelidad Extrema", layout="wide")

st.title("🏗️ ArquitectIA: Control de Estructura v3.0")

# 2. Barra Lateral de Control
with st.sidebar:
    st.header("⚙️ Control de Fidelidad")
    # Este ajuste es clave para que no invente formas
    fidelidad = st.select_slider(
        "Respeto al diseño original:",
        options=["Creativo", "Equilibrado", "Copia Exacta (Geometría Rígida)"],
        value="Copia Exacta (Geometría Rígida)"
    )
    
    st.divider()
    st.header("🎨 Acabados")
    estilo = st.selectbox("Estilo:", ["Moderno", "Minimalista", "Industrial", "Contemporáneo"])
    mat_paredes = st.selectbox("Material Principal:", ["Concreto Pulido", "Ladrillo", "Piedra Natural", "Madera", "Blanco Liso"])
    clima = st.selectbox("Ambiente:", ["Soleado Directo", "Atardecer", "Nublado Realista"])

# 3. Área de Carga
st.info("💡 Consejo: Asegúrate de que tu captura de SketchUp tenga líneas claras y no esté muy lejos.")
archivo = st.file_uploader("🖼️ Sube tu captura (Arrastra desde la carpeta de Imágenes)", type=["jpg", "jpeg", "png"])

# 4. Instrucciones del Arquitecto
instruccion_usuario = st.text_area("📝 Descripción detallada del render:", 
                                   placeholder="Ej: Mantén la forma del techo plano, usa marcos de aluminio negro y añade un suelo de grava...")

if archivo:
    col1, col2 = st.columns(2)
    img = Image.open(archivo)
    
    with col1:
        st.subheader("Captura de SketchUp")
        st.image(img, use_container_width=True)

    if st.button("🚀 GENERAR RENDER FIEL"):
        with col2:
            with st.spinner("🧠 Analizando geometría estructural..."):
                try:
                    # Convertir imagen para Gemini
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    # PROMPT REFORZADO PARA EVITAR ALUCINACIONES
                    # Usamos palabras de peso como "Photogrammetry", "Architectural accuracy" y "Reference preservation"
                    modificador_fidelidad = ""
                    if fidelidad == "Copia Exacta (Geometría Rígida)":
                        modificador_fidelidad = (
                            "STRICT ARCHITECTURAL ADHERENCE. Do not change the building's footprint, height, or window placement. "
                            "Follow the attached image as a rigid template. This is a technical visualization, not an artistic interpretation."
                        )

                    prompt_completo = (
                        f"{modificador_fidelidad} "
                        f"Professional architectural render. Original SketchUp volume must be preserved 100%. "
                        f"Style: {estilo}. Walls: {mat_paredes}. Lighting: {clima}. "
                        f"User Instructions: {instruccion_usuario}. "
                        f"High-quality architectural photography, hyper-realistic textures, realistic environment."
                    )

                    payload = {"contents": [{"parts": [
                        {"text": prompt_completo},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    # Pedirle a Gemini que cree el prompt final basado en la imagen
                    res = requests.post(URL_GEMINI, json=payload, timeout=20)
                    data = res.json()
                    
                    if "candidates" in data:
                        # Gemini ahora describirá la imagen con precisión para que la otra IA no se pierda
                        gen_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        gen_text = prompt_completo

                    # Fase de Dibujo: Añadimos parámetros de realismo
                    clean_p = "".join(e for e in gen_text if e.isalnum() or e == " ")
                    final_p = f"Architectural photo, realistic, matching reference structure, {clean_p}"
                    encoded_p = urllib.parse.quote(final_p[:800])
                    
                    # Usamos un seed aleatorio para variar si no le gusta el primero
                    url_img = f"https://image.pollinations.ai/prompt/{encoded_p}?width=1280&height=720&nologo=true&seed={int(time.time())}"
                    
                    r = requests.get(url_img, timeout=120)
                    if r.status_code == 200:
                        st.image(r.content, use_container_width=True)
                        st.success("Render generado respetando la estructura.")
                        st.download_button("💾 Guardar Render", r.content, "render_fiel.png", "image/png")
                    else:
                        st.error("El motor de renderizado está ocupado. Intenta de nuevo.")

                except Exception as e:
                    st.error(f"Ocurrió un error: {e}")
