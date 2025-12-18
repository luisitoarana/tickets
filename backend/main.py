# backend/main.py
import sys
import os

# 1. Corrección de rutas para Vercel
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from fastapi import FastAPI, HTTPException, Depends, APIRouter 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

# Variables para Redis (opcional)
redis = None
r = None

# Importaciones
from database import engine, Base, get_db
from models import Ticket ,User

# Crear tablas
Base.metadata.create_all(bind=engine) 

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🟢 CAMBIO IMPORTANTE: Usamos un APIRouter en lugar de "app" directamente
router = APIRouter()

class TicketCreate(BaseModel):
    asunto: str
    mensaje_inicial: str

# --- TUS ENDPOINTS (Fíjate que ahora usan @router en vez de @app) ---

@router.get("/tickets")
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

@router.get("/tickets/{ticket_id}")
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

@router.post("/tickets")
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
        
        # Lógica Redis (Si existe)
        if r:
            task_data = {"ticket_id": nuevo.TicketID, "asunto": nuevo.Asunto}
            try:
                r.rpush("task_queue", json.dumps(task_data))
            except:
                pass # Ignoramos error de redis si falla

        return {"id": nuevo.TicketID, "status": "creado"}

    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail=f"Error DB: {e}")

@router.put("/tickets/{ticket_id}")
def actualizar_ticket(ticket_id: int, updated_data: TicketCreate, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.TicketID == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    
    ticket.Asunto = updated_data.asunto
    ticket.MensajeInicial = updated_data.mensaje_inicial
    db.commit()
    return {"id": ticket.TicketID, "status": "actualizado"}

@router.delete("/tickets/{ticket_id}")
def eliminar_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.TicketID == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    db.delete(ticket)
    db.commit()
    return {"status": "eliminado", "id": ticket_id}

# 🟢 LA MAGIA FINAL:
# Incluimos las rutas de dos formas:
# 1. Normal (para localhost) -> /tickets
# 2. Con prefijo /api (para Vercel) -> /api/tickets
app.include_router(router)
app.include_router(router, prefix="/api")

# Ruta de prueba simple
@app.get("/")
def read_root():
    return {"message": "API de Tickets funcionando correctamente"}

# backend/main.py (Añadir esto a tu código existente)

class LoginSchema(BaseModel):
    email: str
    password: str

class RegisterSchema(BaseModel):
    email: str
    password: str
    role: str = "usuario"

@router.post("/auth/register")
def register(user: RegisterSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.Email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya existe")
    
    nuevo_usuario = User(Email=user.email, Password=user.password, Role=user.role)
    db.add(nuevo_usuario)
    db.commit()
    return {"message": "Usuario creado"}

@router.post("/auth/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.Email == user.email, User.Password == user.password).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Aquí podrías generar un JWT, por ahora devolvemos la info del usuario
    return {
        "userId": db_user.UserID,
        "email": db_user.Email,
        "role": db_user.Role
    }