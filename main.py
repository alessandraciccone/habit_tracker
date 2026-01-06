from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.auth import router as auth_router
from app.habits import router as habits_router

# Definisci lo schema di sicurezza Bearer globalmente
security = HTTPBearer()

app = FastAPI(
    title="Habit Tracker API",
    description="API per autenticazione e gestione habits",
    version="1.0.0",
    # Aggiungi la configurazione di sicurezza globale per Swagger
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
    }
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(habits_router, prefix="/habits", tags=["Habits"])