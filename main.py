from fastapi import FastAPI
from pydantic import BaseModel

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