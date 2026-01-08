from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth import router as auth_router
from app.habits import router as habits_router
from app.database import engine, Base
from app.models_sql import UserDB, HabitDB, HabitLogDB

# Crea le tabelle all'avvio
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(auth_router, prefix="/auth")
app.include_router(habits_router, prefix="/habits")

from fastapi.middleware.cors import CORSMiddleware

