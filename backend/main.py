import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
import redis 

# Importaciones absolutas
from database import engine, Base, get_db
from models import Ticket 

# Configuración de Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    r.ping()
    print("✅ FastAPI: Conexión con Redis establecida.")
except redis.exceptions.ConnectionError as e:
    print(f"❌ FastAPI: No se pudo conectar a Redis en {REDIS_HOST}:{REDIS_PORT}. Las tareas asíncronas no funcionarán. Error: {e}")
    r = None 

# Crear la tabla si no existe
Base.metadata.create_all(bind=engine) 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada para POST y PUT
class TicketCreate(BaseModel):
    asunto: str
    mensaje_inicial: str

# =========================
# GET /tickets (Lista)
# =========================
@app.get("/tickets")
def obtener_tickets(db: Session = Depends(get_db)):
    try:
        tickets = db.query(Ticket).order_by(Ticket.TicketID.desc()).all()
        return [
            {
                "id": t.TicketID,
                "asunto": t.Asunto,
                "estado": t.Estado,
                "fecha": t.FechaCreacion,
                "mensaje": t.MensajeInicial 
            }
            for t in tickets
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tickets: {e}")

# =========================
# GET /tickets/{ticket_id} (Detalle)
# =========================
@app.get("/tickets/{ticket_id}")
def obtener_ticket_por_id(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.TicketID == ticket_id).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    
    return {
        "id": ticket.TicketID,
        "asunto": ticket.Asunto,
        "mensaje_inicial": ticket.MensajeInicial,
        "estado": ticket.Estado,
        "fecha": ticket.FechaCreacion
    }

# =========================
# POST /tickets (Crear)
# =========================
@app.post("/tickets")
def crear_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    try:
        nuevo = Ticket(
            Asunto=ticket.asunto,
            MensajeInicial=ticket.mensaje_inicial, 
            Estado="Abierto",
            FechaCreacion=datetime.utcnow()
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        
        # 🟢 LÓGICA DE REDIS (Integración)
        if r:
            task_data = {
                "ticket_id": nuevo.TicketID,
                "asunto": nuevo.Asunto,
                "task": "Procesamiento de ticket (Generación de PDF/Email)"
            }
            r.rpush("task_queue", json.dumps(task_data))
            print(f"🔔 Tarea para Ticket ID {nuevo.TicketID} enviada a Redis.")
        else:
            print(f"⚠️ Redis no está conectado. Tarea para Ticket ID {nuevo.TicketID} no fue enviada.")

        return {
            "id": nuevo.TicketID,
            "status": "creado"
        }

    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail=f"Error al crear ticket en la base de datos: {e}")

# =========================
# PUT /tickets/{ticket_id} (ACTUALIZAR - FALTABA ESTE)
# =========================
@app.put("/tickets/{ticket_id}")
def actualizar_ticket(ticket_id: int, updated_data: TicketCreate, db: Session = Depends(get_db)):
    try:
        ticket = db.query(Ticket).filter(Ticket.TicketID == ticket_id).first()
        
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket no encontrado")
        
        # 1. Aplicar los cambios
        ticket.Asunto = updated_data.asunto
        ticket.MensajeInicial = updated_data.mensaje_inicial

        # 2. Guardar en la DB
        db.commit()
        db.refresh(ticket)
        
        return {"id": ticket.TicketID, "status": "actualizado"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar ticket: {e}")


# =========================
# DELETE /tickets/{ticket_id} (Eliminar)
# =========================
@app.delete("/tickets/{ticket_id}")
def eliminar_ticket(ticket_id: int, db: Session = Depends(get_db)):
    try:
        ticket = db.query(Ticket).filter(Ticket.TicketID == ticket_id).first()
        
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket no encontrado")

        db.delete(ticket)
        db.commit()

        return {"status": "eliminado", "id": ticket_id}

    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error al eliminar ticket: {e}")