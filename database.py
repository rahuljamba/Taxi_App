import os  # 1. os module import karo
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 2. Render par DATABASE_URL milegi, local par localhost chalega (Fallback mechanism)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/taxi_db")

# Render Database URL fix: Agar URL 'postgres://' se shuru ho rahi hai, toh use 'postgresql://' karo
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Connection Engine banao
engine = create_engine(DATABASE_URL)

# Database session ki factory banao
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class jisse hamare saare database tables inherit karenge
Base = declarative_base()

# Dependency: Isse har API request par ek fresh db session milega
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create table
def create_table():
    Base.metadata.create_all(bind=engine)