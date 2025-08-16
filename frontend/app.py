# frontend/app.py (VERSIÓN FINAL USANDO st.components.v1.html)

import streamlit as st
import requests
import streamlit.components.v1 as stc # <-- 1. IMPORTAMOS EL MÓDULO DE COMPONENTES

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Inspiración Diaria", page_icon="💡", layout="centered")

# --- 2. URL DEL BACKEND ---
API_URL = "http://127.0.0.1:8000/api/v1/inspiration"

# --- 3. FUNCIÓN PARA CARGAR DATOS ---
@st.cache_data(ttl=3600)
def get_inspiration_data():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API: {e}")
        return None

# --- 4. RENDERIZADO DE LA PÁGINA ---
st.title("💡 Tu Dosis de Inspiración Diaria")

if st.button("Generar Nueva Inspiración ✨"):
    st.cache_data.clear()

data = get_inspiration_data()

if data:
    frase = data.get("frase", "No hay frase disponible.")
    autor = data.get("autor", "Autor desconocido.")
    image_url = data.get("image_url")
    image_author = data.get("image_author")
    clasificacion = data.get("clasificacion", "General")
    tipo = data.get("tipo", "Inspiración")

    # Plantilla HTML. La dejamos multi-línea para legibilidad, ya que stc.html no tiene problemas con eso.
    html_template = """
    <div style="
        position: relative;
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{image_url}');
        background-size: cover; background-position: center; border-radius: 15px;
        padding: 2rem; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        height: 550px; /* Usamos height en lugar de min-height para stc.html */
        display: flex; flex-direction: column;
        justify-content: space-between;
    ">
        <!-- Sección de Etiquetas (Tags) -->
        <div style="display: flex; gap: 0.5rem; justify-content: flex-start;">
            <span style="font-size: 0.8rem; background-color: rgba(255,255,255,0.2);text-align: right; padding: 0.3rem 0.8rem; border-radius: 15px;">
                {clasificacion}
            </span>
            <span style="font-size: 0.8rem; background-color: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 15px;">
                {tipo}
            </span>
        </div>

        <!-- Sección de la Frase y Autor -->
        <div style="text-align: center;">
            <p style="font-size: 2.2rem; font-style: italic;">“{frase}”</p>
            <p style="font-size: 1.1rem; font-weight: bold; text-align: right; margin-top: 1.5rem;">- {autor}</p>
        </div>
        
        <!-- Div vacío para mantener la estructura flexbox (space-between) -->
        <div></div>
    </div>
    """

    # Rellenamos la plantilla
    html_content = html_template.format(
        image_url=image_url,
        clasificacion=clasificacion,
        tipo=tipo,
        frase=frase,
        autor=autor
    )

    # --- 2. RENDERIZAMOS CON stc.html ---
    # Le pasamos también una altura para que el iframe se ajuste al contenido.
    stc.html(html_content, height=580)

else:
    st.warning("No se pudo obtener la inspiración. Asegúrate de que el backend esté corriendo y la base de datos tenga frases.")