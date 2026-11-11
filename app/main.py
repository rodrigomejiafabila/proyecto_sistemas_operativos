import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2 import pool

app = FastAPI(title="Procesador de Pedidos Distribuidos")

# Leer configuración desde variables de entorno (preparación para Kubernetes ConfigMaps y Secrets)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Pool de conexiones para soportar concurrencia alta
try:
    db_pool = psycopg2.pool.ThreadedConnectionPool(
        minconn=1,
        maxconn=20,
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    db_pool = None

# Modelo de datos de entrada
class Pedido(BaseModel):
    producto: str
    cantidad: int

@app.get("/health")
def health_check():
    """Endpoint para liveness y readiness probes de Kubernetes"""
    if db_pool:
        return {"status": "ok", "db": "connected"}
    raise HTTPException(status_code=503, detail="Database not connected")

@app.post("/pedidos", status_code=201)
def procesar_pedido(pedido: Pedido):
    """Recibe un pedido, simula carga y lo guarda en persistencia"""
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    # Simulamos un pequeño tiempo de procesamiento (CPU) para que las 
    # pruebas de escalabilidad con réplicas tengan un impacto visible.
    time.sleep(0.05) 
    
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO pedidos (producto, cantidad, estado) 
            VALUES (%s, %s, %s) RETURNING id;
        """
        cursor.execute(query, (pedido.producto, pedido.cantidad, "procesado"))
        pedido_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return {"id": pedido_id, "mensaje": "Pedido procesado con éxito"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db_pool.putconn(conn)

@app.get("/pedidos/conteo")
def contar_pedidos():
    """Útil para la prueba de persistencia (E5) y verificar operaciones guardadas"""
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pedidos;")
        total = cursor.fetchone()[0]
        cursor.close()
        return {"total_operaciones_guardadas": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db_pool.putconn(conn)