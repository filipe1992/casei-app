from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.config import settings
from app.routes import auth, guests, invitations, timeline, gift_shop, dashboard
from app.db.session import engine, get_db
from app.db.init_db import init_db


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo as rotas
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(guests.router, prefix=f"{settings.API_V1_STR}/guests", tags=["guests"])
app.include_router(invitations.router, prefix=f"{settings.API_V1_STR}/invitations", tags=["invitations"])
app.include_router(timeline.router, prefix=f"{settings.API_V1_STR}/timeline", tags=["timeline"])
app.include_router(gift_shop.router, prefix=f"{settings.API_V1_STR}/gift-shop", tags=["gift-shop"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["dashboard"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do WeddingPlanner!"}

@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    init_db(db)
