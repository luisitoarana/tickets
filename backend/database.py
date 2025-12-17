# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# =========================================================
# 🟢 CONFIGURACIÓN DE BASE DE DATOS INTELIGENTE
# =========================================================

# Vercel es un sistema Linux (posix). Windows es (nt).
# Además, Vercel tiene una carpeta /tmp disponible.
if os.name == 'posix' and os.path.exists("/tmp"):
    # ESTAMOS EN VERCEL (NUBE)
    # Usamos 4 barras (////) para indicar una ruta absoluta en Linux
    print("🟢 Usando base de datos en /tmp (Modo Nube)")
    DATABASE_URL = "sqlite:////tmp/tickets.db"
else:
    # ESTAMOS EN WINDOWS (LOCAL)
    # Usamos 3 barras (///) para ruta relativa
    print("🟢 Usando base de datos local (Modo Windows)")
    DATABASE_URL = "sqlite:///./tickets.db"

# Crear el motor de la base de datos
engine = create_engine(
    DATABASE_URL, 
    echo=True, 
    # check_same_thread=False es necesario para SQLite en FastAPI
    connect_args={"check_same_thread": False} 
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Dependencia para obtener la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()