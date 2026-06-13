from pydantic import BaseModel
import asyncio
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI(title="Taxi App Dummy API")

class User(BaseModel):
    id: str
    name: str | None = None
    role: str

# Dummy JSON Data
DUMMY_USERS = [
    {"id": 1, "name": "Rahul", "role": "Senior iOS Dev"},
    {"id": 2, "name": "Luffy", "role": "Pirate King"},
    {"id": 3, "name": "Zoro", "role": "Swordsman"}
]

STOCKS = {"RELIANCE": 2500.0, "TATASTEEL": 150.0, "INFY": 1400.0}

@app.get("/")
def home():
    return {"status": "success", "message": "Welcome to Taxi API"}

@app.get("/users")
def get_users():
    return {"status": "success", "data": DUMMY_USERS}

@app.post("/register_user")
def add_users(user: User):
    DUMMY_USERS.append({"id": user.id, "name": user.name, "role": user.role})
    return {"status": "success", "message": f" {user.name} added sucesfully our database !!"}  

# WebSocket Endpoint
# Test stock name - RELIANCE, TATASTEEL, INFY
@app.websocket("/ws/stocks/{ticker}")
async def websocket_endpoint(websocket: WebSocket, ticker: str):
    # 1. Connection Accept karo
    await websocket.accept()
    
    ticker = ticker.upper()
    if ticker not in STOCKS:
        await websocket.send_json({"error": f"Ticker {ticker} not found"})
        await websocket.close()
        return

    current_price = STOCKS[ticker]
    print(f"Client connected for stock: {ticker}")

    try:
        # 2. Continuous Loop chalao jab tak client connected hai
        while True:
            # Price mein random fluctuation (-2 se +2 tak) generate karo
            price_change = random.uniform(-2.0, 2.0)
            current_price = round(current_price + price_change, 2)
            
            # Data pack karo
            payload = {
                "ticker": ticker,
                "price": current_price,
                "change": round(price_change, 2)
            }
            
            # 3. Frontend ko real-time JSON data push karo
            await websocket.send_json(payload)
            
            # 1 second ka delay do taaki network choke na ho
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        # 4. Handle Disconnection safely
        print(f"Client disconnected from stock: {ticker}")

# 1. DATABASE SETUP
DATABASE_URL = "sqlite:///./company.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. DATABASE MODEL (Table Structure)
class Employee(Base):
    __tablename__ = "employee"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mobileNumber = Column(String)
    dob = Column(String) 
    gender = Column(String)
    location = Column(String)
    nationality = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/regiter_employee/")
def regiter_employee(name: str, mobileNumber: str, dob: str, gender: str, location: str, nationality: str, db: Session = Depends(get_db)):
    new_item = Employee(name = name, mobileNumber = mobileNumber, dob = dob, gender = gender, location = location, nationality = nationality)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)  
    return {"status": "success", "data": new_item}

@app.get("/get_employee_list")
def get_employee_list(db: Session = Depends(get_db)):
    employes_list = db.query(Employee).all()
    if not employes_list:
        return {"status": "failed", "message": "employees list is empty."}
    return {"status": "success", "data": employes_list}

@app.get("/get_employee/{emp_id}")
def get_employee(emp_id: int, db: Session = Depends(get_db)):
    item = db.query(Employee).filter(Employee.id == emp_id).first()
    if item is None:
        #raise HTTPException(status_with=404, detail="Item not found")
        return {"status": "failed", "message": "user is not found."}
    return {"status": "success", "data": item}