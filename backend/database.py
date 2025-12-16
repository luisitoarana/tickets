# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# CAMBIADO A SQLITE PARA PRUEBA INMEDIATA Y ELIMINAR EL ERROR 500
# Si quieres volver a SQL Server, lee la sección 3 (Configuración de SQL Server)
DATABASE_URL = "sqlite:///./tickets.db" 

engine = create_engine(
    DATABASE_URL, 
    echo=True, 
    # Necesario para SQLite en FastAPI/Threads
    connect_args={"check_same_thread": False} 
)

SessionLocal = sessionmaker(
 autocommit=False,
 autoflush=False,
 bind=engine
)

Base = declarative_base()

# Función para obtener la sesión de DB (buena práctica de FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()