from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://localhost:5432/taxi_db"

# 2. Connection Engine banao
engine = create_engine(DATABASE_URL)

# 3. Database session ki factory banao
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base class jisse hamare saare database tables inherit karenge
Base = declarative_base()

# 5. Dependency: Isse har API request par ek fresh db session milega aur kaam hone par close ho jayega
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create table
def create_table():
    Base.metadata.create_all(bind = engine)       