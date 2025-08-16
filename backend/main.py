# backend/main.py

from fastapi import FastAPI, HTTPException
import requests
import mysql.connector
from mysql.connector import pooling
import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import random

# --- 1. CONFIGURACIÓN ---
load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_PORT = os.getenv("DB_PORT")

# --- 2. POOL DE CONEXIONES ---

try:
    db_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE, port=DB_PORT)
    print("Pool de conexiones a la base de datos creado exitosamente.")
except Exception as e:
    print(f"Error al crear el pool de conexiones: {e}")
    db_pool = None

# --- 3. MODELOS DE DATOS (PYDANTIC) ---
class InspirationResponse(BaseModel):
    frase: str
    autor: str
    clasificacion: Optional[str] = "General"
    tipo: Optional[str] = "Inspiración"
    image_url: str
    image_author: str

# --- 4. LÓGICA DE SERVICIO ---
def get_random_quote_from_db():
    if not db_pool: raise Exception("El pool de la base de datos no está disponible.")
    
    connection = db_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT frase, autor, clasificacion, tipo FROM frases_motivadoras WHERE is_active = TRUE ORDER BY RAND() LIMIT 1")
    quote = cursor.fetchone()
    cursor.close()
    connection.close()
    return quote

def get_random_unsplash_image():
    # ... (sin cambios aquí) ...
    if not UNSPLASH_ACCESS_KEY: return {"url": "https://images.unsplash.com/photo-1519681393784-d120267933ba", "author": "eberhard grossgasteiger"}
    try:
        params = {"query": "motivation landscape", "orientation": "landscape", "client_id": UNSPLASH_ACCESS_KEY}
        response = requests.get("https://api.unsplash.com/photos/random", params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {"url": data['urls']['regular'], "author": data['user']['name']}
    except Exception:
        return {"url": "https://images.unsplash.com/photo-1519681393784-d120267933ba", "author": "eberhard grossgasteiger"}

# --- 5. CREACIÓN DE LA APP FASTAPI ---
app = FastAPI(title="API de Inspiración Diaria", description="Provee una frase motivacional y una imagen de fondo inspiradora.", version="1.0.0")

# --- 6. ENDPOINT PRINCIPAL ---
@app.get("/api/v1/inspiration", response_model=InspirationResponse, summary="Obtener Inspiración Diaria")
def get_daily_inspiration():
    try:
        quote_data = get_random_quote_from_db()
        image_data = get_random_unsplash_image()
        
        if not quote_data: raise HTTPException(status_code=404, detail="No se encontraron frases motivadoras.")
            
        # --- CAMBIO AQUÍ: Pasamos los nuevos campos a la respuesta ---
        return InspirationResponse(
            frase=quote_data['frase'],
            autor=quote_data['autor'],
            clasificacion=quote_data.get('clasificacion'),
            tipo=quote_data.get('tipo'),
            image_url=image_data['url'],
            image_author=image_data['author']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))