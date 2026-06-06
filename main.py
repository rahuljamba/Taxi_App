from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn
import models
from database import engine, get_db

# Server start hote hi Postgres mein table sync karo
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic Schema: iPhone/iOS App se jo JSON data aayega, usko structural check dega
class UserRegisterRequest(BaseModel):
    full_name: str
    country_code: str
    mobile_number: str
    email: str
    password: str

def main():
    print("Hello from app-dev! Server starting...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.get("/")
async def root():
    return {"message": "welcome api world!"}

# POST API: Registration Endpoint
@app.post("/auth/users/register")
async def userRegister(user: UserRegisterRequest, db: Session = Depends(get_db)):
    # 1. Check karo email pehle se exist toh nahi karta database mein
    db_user = db.query(models.DBUser).filter(models.DBUser.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Pydantic request data ko SQLAlchemy Database Model object mein map karo
    new_user = models.DBUser(**user.model_dump())
    
    # 3. Database session mein add aur commit karo
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.get("/users/get_users")
async def usersList(db: Session = Depends(get_db)):
    return db.query(models.DBUser).all()

if __name__ == "__main__":
    main()