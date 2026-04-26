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

st.set_page_config(page_title="ArquitectIA Pro", layout="wide")

st.title("🏗️ ArquitectIA: Renderizado de Precisión")

# 2. Barra Lateral
with st.sidebar:
    st.header("🎨 Ajustes")
    estilo = st.selectbox("Estilo:", ["Minimalista Moderno", "Industrial Loft", "Rústico", "Futurista"])
    fidelidad = st.radio("Fidelidad Estructural:", ["Estricta", "Equilibrada", "Creativa"])
    mat_paredes = st.selectbox("Paredes:", ["Concreto", "Ladrillo", "Piedra", "Estuco", "Madera"])
    clima = st.selectbox("Iluminación:", ["Soleado", "Atardecer", "Noche", "Nublado"])
    st.divider()
    st.caption("v2.5 - Emergency Paste Mode")

# 3. ZONA DE CARGA (Doble Vía)
st.subheader("📸 Paso 1: Sube tu modelo")
tabs = st.tabs(["📁 Subir Archivo", "📋 Pegar Captura (Alternativo)"])

with tabs[0]:
    archivo_subido = st.file_uploader("Arrastra aquí tu captura de SketchUp", type=["jpg", "jpeg", "png"])

with tabs[1]:
    st.write("Si el Ctrl+V no funciona arriba, usa este método:")
    # Este componente es un truco: permite recibir datos de imagen si el navegador bloquea el uploader
    archivo_pegado = st.chat_input("Haz clic aquí y presiona Ctrl+V (o escribe algo y dale enter)")
    st.caption("Nota: Algunos navegadores requieren que guardes la imagen y la arrastres si el portapapeles está protegido.")

# Decidir qué archivo usar
archivo = archivo_subido if archivo_subido else archivo_pegado

# 4. Instrucciones de diseño
st.subheader("📝 Paso 2: Detalles del Render")
instruccion_usuario = st.text_area("Órdenes para la IA:", placeholder="Ej: Que las ventanas tengan marcos negros...")

if archivo:
    col_pre, col_res = st.columns(2)
    
    # Manejo de la imagen (archivo o datos de chat)
    try:
        if hasattr(archivo, 'read'):
            img = Image.open(archivo)
        else:
            st.warning("Para pegar imágenes, lo más seguro es arrastrar el archivo directamente al recuadro de 'Subir Archivo'.")
            st.stop()
            
        with col_pre:
            st.subheader("Modelo Original")
            st.image(img, use_container_width=True)

        if st.button("🚀 GENERAR RENDER"):
            with col_res:
                with st.spinner("🧠 Generando fotorrealismo..."):
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG")
                    img_byte = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    strict = "KEEP EXACT GEOMETRY. DO NOT CHANGE THE BUILDING SHAPE." if fidelidad == "Estricta" else ""
                    prompt_completo = f"{strict} Architecture style {estilo}, walls {mat_paredes}, {clima}. {instruccion_usuario}"

                    payload = {"contents": [{"parts": [
                        {"text": prompt_completo},
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_byte}}
                    ]}]}

                    res = requests.post(URL_GEMINI, json=payload, timeout=20)
                    data = res.json()
                    gen_text = data["candidates"][0]["content"]["parts"][0]["text"] if "candidates" in data else prompt_completo

                    clean_p = "".join(e for e in gen_text if e.isalnum() or e == " ")
                    final_p = f"Professional architectural photography, masterpiece, {clean_p}"
                    url_img = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(final_p[:700])}?width=1280&height=720&nologo=true&seed={int(time.time())}"
                    
                    r = requests.get(url_img, timeout=120)
                    if r.status_code == 200:
                        st.image(r.content, use_container_width=True)
                        st.success("¡Render listo!")
                        st.download_button(label="💾 Descargar Imagen", data=r.content, file_name="render.png", mime="image/png")
    except Exception as e:
        st.error(f"Error al procesar la imagen: {e}")
