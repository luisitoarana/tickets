#worker.py
import redis
import json
import time
import sys

# Configuración
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

def conectar_redis():
    """Intenta conectar a Redis en bucle hasta que tenga éxito"""
    while True:
        try:
            print(f"⏳ Intentando conectar a Redis en {REDIS_HOST}:{REDIS_PORT}...")
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
            r.ping() # Ping para verificar conexión real
            print("✅ ¡Conexión exitosa con Redis!")
            return r
        except redis.exceptions.ConnectionError:
            print("❌ Redis no responde. Reintentando en 5 segundos...")
            time.sleep(5)

def iniciar_worker():
    # 1. Conectar (Se quedará aquí hasta que prendas Docker)
    r = conectar_redis()
    
    print("👷 Worker iniciado y esperando tareas...")

    # 2. Bucle principal
    while True:
        try:
            # BLPOP espera tareas. Si Redis se cae aquí, saltará al 'except'
            tarea_raw = r.blpop("task_queue", timeout=5) 
            
            if tarea_raw:
                queue_name, data = tarea_raw
                tarea = json.loads(data)
                
                print(f"⚙️  Procesando Ticket #{tarea.get('ticket_id', '?')}: {tarea.get('task', 'Desconocida')}")
                
                # Simular trabajo (generar PDF, enviar email, etc.)
                time.sleep(0.5) 
                
                print(f"✅ Tarea completada.")
                
        except redis.exceptions.ConnectionError:
            print("⚠️ Conexión perdida con Redis. Re-conectando...")
            r = conectar_redis()
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            time.sleep(1)

if __name__ == "__main__":
    iniciar_worker()