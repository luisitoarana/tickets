# backend/main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from fastapi import FastAPI, HTTPException, Depends, APIRouter 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from database import engine, Base, get_db
from models import Ticket, User 

Base.metadata.create_all(bind=engine) 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

# --- SCHEMAS ---
class TicketCreate(BaseModel):
    asunto: str
    mensaje_inicial: str

class LoginSchema(BaseModel):
    email: str
    password: str

class RegisterSchema(BaseModel):
    email: str
    password: str
    role: str = "usuario"

# --- ENDPOINTS DE TICKETS ---
@router.get("/tickets")
def obtener_tickets(db: Session = Depends(get_db)):
    # ... (tu código de obtener_tickets)
    tickets = db.query(Ticket).order_by(Ticket.TicketID.desc()).all()
    return [{"id": t.TicketID, "asunto": t.Asunto, "estado": t.Estado, "fecha": t.FechaCreacion, "mensaje": t.MensajeInicial} for t in tickets]

@router.post("/tickets")
def crear_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    # ... (tu código de crear_ticket)
    nuevo = Ticket(Asunto=ticket.asunto, MensajeInicial=ticket.mensaje_inicial, Estado="Abierto", FechaCreacion=datetime.utcnow())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"id": nuevo.TicketID, "status": "creado"}

@router.put("/tickets/{ticket_id}")
def actualizar_ticket(ticket_id: int, updated_data: TicketCreate, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.TicketID == ticket_id).first()
    if not ticket: raise HTTPException(status_code=404, detail="Ticket no encontrado")
    ticket.Asunto = updated_data.asunto
    ticket.MensajeInicial = updated_data.mensaje_inicial
    db.commit()
    return {"id": ticket.TicketID, "status": "actualizado"}

@router.delete("/tickets/{ticket_id}")
def eliminar_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.TicketID == ticket_id).first()
    if not ticket: raise HTTPException(status_code=404, detail="Ticket no encontrado")
    db.delete(ticket)
    db.commit()
    return {"status": "eliminado", "id": ticket_id}

# --- ENDPOINTS DE AUTENTICACIÓN (Ahora dentro del router) ---
@router.post("/auth/register")
def register(user: RegisterSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.Email == user.email).first()
    if db_user: raise HTTPException(status_code=400, detail="El email ya existe")
    nuevo_usuario = User(Email=user.email, Password=user.password, Role=user.role)
    db.add(nuevo_usuario)
    db.commit()
    return {"message": "Usuario creado"}

@router.post("/auth/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.Email == user.email, User.Password == user.password).first()
    if not db_user: raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"userId": db_user.UserID, "email": db_user.Email, "role": db_user.Role}

# 🟢 IMPORTANTE: INCLUIR EL ROUTER AL FINAL 🟢
app.include_router(router)
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "API de Tickets funcionando correctamente"}