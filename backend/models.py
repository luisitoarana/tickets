# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "Users"
    UserID = Column(Integer, primary_key=True, index=True)
    Email = Column(String(255), unique=True, nullable=False)
    Password = Column(String(255), nullable=False) 
    Role = Column(String(50), default="usuario") # "usuario" o "soporte"
class Ticket(Base):
    __tablename__ = "Tickets"
    TicketID = Column(Integer, primary_key=True, index=True)
    Asunto = Column(String(255), nullable=False)
    MensajeInicial = Column(String, nullable=True) 
    Estado = Column(String(50), default="Abierto")
    FechaCreacion = Column(DateTime, default=datetime.utcnow)