# 💡 Inspiración Diaria - Carrusel con FastAPI y Streamlit

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.78%2B-green?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.10%2B-red?style=for-the-badge&logo=streamlit)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=for-the-badge&logo=mysql)

Este proyecto es una aplicación web completa que presenta una arquitectura de microservicios. Un **backend (FastAPI)** se conecta a una base de datos MySQL para obtener frases motivacionales y a la API de Unsplash para obtener imágenes inspiradoras. Un **frontend (Streamlit)** consume la API del backend para mostrar esta información en un carrusel visualmente atractivo.

---

## 📸 Captura de Pantalla


![Demo de la Aplicación]([app-demo.png](https://ibb.co/dJGRH7P7))

---

## 🏛️ Arquitectura del Proyecto

El proyecto está dividido en dos servicios independientes que se comunican a través de una API REST:

1.  **Backend (`/backend`)**:
    *   Construido con **FastAPI**.
    *   Expone un endpoint `/api/v1/inspiration`.
    *   Se conecta a una base de datos **MySQL** para obtener una frase aleatoria de la tabla `frases_motivadoras`.
    *   Se conecta a la **API de Unsplash** para obtener una imagen de alta calidad.
    *   Combina ambos datos en una única respuesta JSON, optimizando las llamadas desde el cliente.

2.  **Frontend (`/frontend`)**:
    *   Construido con **Streamlit**.
    *   Consume el endpoint del backend para obtener la frase y la imagen.
    *   Utiliza `streamlit.components.v1.html` para renderizar un componente de tarjeta personalizado con HTML/CSS, superponiendo el texto sobre la imagen de fondo.
    *   Implementa un botón para refrescar el contenido, limpiando la caché de Streamlit para obtener una nueva inspiración.

---

## 🛠️ Stack Tecnológico

*   **Backend:** FastAPI, Uvicorn, MySQL Connector, Requests, Dotenv.
*   **Frontend:** Streamlit, Requests.
*   **Base de Datos:** MySQL (desplegada en Railway para este proyecto).
*   **APIs Externas:** Unsplash API.

---

## ⚙️ Cómo Ejecutar el Proyecto Localmente

Para poner en marcha esta aplicación, necesitas ejecutar ambos servicios en terminales separadas.

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/rodrigocabezasz/inspiracion-diaria-fastapi-streamlit.git
    cd inspiracion-diaria-fastapi-streamlit
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    
4.  **Configura las variables de entorno:**
    Crea un archivo `.env` en la raíz del proyecto y añade tus credenciales de la base de datos y tu clave de Unsplash.
    ```env
    DB_HOST="tu_host"
    DB_USER="tu_usuario"
    DB_PASSWORD="tu_contraseña"
    DB_DATABASE="tu_base_de_datos"
    DB_PORT="tu_puerto"
    UNSPLASH_ACCESS_KEY="tu_clave_de_unsplash"
    ```

5.  **Inicia el Backend (Terminal 1):**
    ```bash
    cd backend
    uvicorn main:app --reload
    ```
    *Espera a que el servidor confirme que está corriendo en `http://127.0.0.1:8000`.*

6.  **Inicia el Frontend (Terminal 2):**
    Abre una **nueva terminal**, activa el mismo entorno virtual (`.\venv\Scripts\activate`) y ejecuta:
    ```bash
    cd frontend
    streamlit run app.py
    ```