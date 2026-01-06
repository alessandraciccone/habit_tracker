from fastapi import FastAPI
from app.auth import router as auth_router
from app.habits import router as habits_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(habits_router, prefix="/habits")