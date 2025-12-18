# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Intentamos obtener la URL de Neon desde las variables de entorno de Vercel
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # ESTAMOS EN VERCEL (Usando Postgres de Neon)
    # Corrección para SQLAlchemy: postgres:// -> postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    engine = create_engine(DATABASE_URL)
    print("🟢 Conectado a PostgreSQL en la nube (Neon)")
else:
    # ESTAMOS EN WINDOWS (Usando SQLite local)
    print("🟢 Usando base de datos local (SQLite)")
    DATABASE_URL = "sqlite:///./tickets.db"
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False} 
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()