from fastapi import FastAPI

app = FastAPI(title="Taxi App Dummy API")

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