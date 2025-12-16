# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base # Nota: Importación corregida a .database

class Ticket(Base):
 __tablename__ = "Tickets"

 TicketID = Column(Integer, primary_key=True, index=True)
 Asunto = Column(String(255), nullable=False)
 # NUEVO CAMPO AGREGADO: Para el cuerpo del mensaje
 MensajeInicial = Column(String, nullable=True) 
 Estado = Column(String(50), default="Abierto")
 FechaCreacion = Column(DateTime, default=datetime.utcnow)