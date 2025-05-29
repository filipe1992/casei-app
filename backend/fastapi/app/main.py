from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.config import settings
from app.middleware.error_handler import ErrorHandlerMiddleware, register_error_handlers

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

# Adiciona o middleware de tratamento de erros
app.add_middleware(ErrorHandlerMiddleware)

# Registra os handlers globais de erro
register_error_handlers(app)

# Inclui as rotas da API
app.include_router(api_router, prefix=settings.API_V1_STR) 