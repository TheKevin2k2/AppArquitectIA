import streamlit as st
from PIL import Image
import requests
import urllib.parse
import time

st.set_page_config(page_title="ArquitectIA Open-Source", layout="wide")

# --- LÓGICA DE DATOS DEL EXCEL (FASE 3 Y 4) ---
precios_unitarios = {
    "Residencial de Lujo": {
        "Mármol Carrara": {"unidad": "m2", "costo": 2500, "color": "#E5E4E2"},
        "Nogal Americano": {"unidad": "m2", "costo": 1800, "color": "#4B3621"},
        "Concreto Aparente": {"unidad": "m2", "costo": 950, "color": "#808080"}
    },
    "Nave Industrial": {
        "Estructura Metálica": {"unidad": "kg", "costo": 45, "color": "#2F4F4F"},
        "Concreto HR": {"unidad": "m3", "costo": 2200, "color": "#A9A9A9"},
        "Lámina Pintro": {"unidad": "m2", "costo": 320, "color": "#708090"}
    }
}

st.title("🏗️ Sistema de Presupuestación ArquitectIA")
st.caption("Módulo de Cálculo Gratuito basado en Plan Maestro v1")

with st.sidebar:
    st.header("📋 Especialización (Fase 2)")
    modulo = st.radio("Tipo de Proyecto:", ["Residencial de Lujo", "Nave Industrial"])
    
    material = st.selectbox("Seleccionar Material (Layout):", list(precios_unitarios[modulo].keys()))
    
    st.divider()
    st.subheader("📊 Calculadora de Insumos")
    cantidad = st.number_input("Cantidad detectada (m2/ml):", min_value=1.0, value=10.0)
    
    datos_mat = precios_unitarios[modulo][material]
    total_partida = cantidad * datos_mat['costo']
    
    st.metric("Total Partida Est.", f"${total_partida:,} MXN")
    st.caption(f"Unidad: {datos_mat['unidad']} | Basado en TPU Fase 3")

# --- INTERFAZ DE RENDER GRATUITO ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🖼️ Captura de Layout")
    archivo = st.file_uploader("Sube tu modelo (Fondo Blanco)", type=["jpg", "png"])
    if archivo:
        img = Image.open(archivo)
        st.image(img, use_container_width=True)

with col2:
    st.subheader("⚡ Visualización de Concepto")
    if archivo and st.button("PROCESAR VISTA Y COSTOS"):
        with st.spinner("Generando atmósfera..."):
            # En lugar de cambiar la casa, generamos un fondo que combine
            estilo_prompt = f"Professional architectural site, {modulo}, {material}, photorealistic atmosphere, 8k"
            url_atmosfera = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(estilo_prompt)}?width=800&height=600&seed={int(time.time())}"
            
            # Mostramos el costo y el material como capas de datos
            st.info(f"**Análisis de Especialización:** {modulo}")
            st.write(f"Aplicando lógica de {material} sobre geometría detectada.")
            
            # Simulamos el renderizado mediante la IA gratuita (Atmósfera)
            st.image(url_atmosfera, caption="Referencia de Iluminación y Material", use_container_width=True)
            
            # Fase 4: Generadores (Tabla de resultados)
            st.success("✅ Memoria de cálculo generada")
            st.table({
                "Concepto": [f"Suministro y colocación de {material}"],
                "Cantidad": [cantidad],
                "Unidad": [datos_mat['unidad']],
                "P.U.": [f"${datos_mat['costo']}"],
                "Importe": [f"${total_partida}"]
            })

st.divider()
st.info("💡 **Tip de Negocio:** Esta versión no gasta dinero. Puedes cobrar por el 'Análisis de Costos' y usar la imagen de la derecha solo como referencia visual de materiales.")
