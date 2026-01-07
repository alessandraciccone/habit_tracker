from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth import router as auth_router
from app.habits import router as habits_router

app = FastAPI()

# AGGIUNGI CORS - IMPORTANTE!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL del frontend React
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
app.include_router(auth_router, prefix="/auth")
app.include_router(habits_router, prefix="/habits")