import models
import database
import schemas
import crud
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import *
from schemas import *
from crud import *
from database import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允许所有来源跨域（开发环境用，生产环境建议写具体域名）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或 ["http://localhost:5173"] 只允许你的前端
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
