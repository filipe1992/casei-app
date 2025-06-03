# from contextlib import asynccontextmanager
# from typing import AsyncGenerator
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api.api import api_router
# from app.core.config import settings
# from app.middleware.error_handler import ErrorHandlerMiddleware, register_error_handlers
# from app.db.init_db import init_db
# from app.db.session import async_session_maker

# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
#     """
#     Gerenciador de contexto do ciclo de vida da aplicação
#     """
#     try:
#         # Código executado na inicialização
#         async with async_session_maker() as session:
#             await init_db(session)
#         yield
#     finally:
#         # Código executado no encerramento (se necessário)
#         pass

# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     version=settings.VERSION,
#     openapi_url=f"{settings.API_V1_STR}/openapi.json",
#     lifespan=lifespan
# )

# # Configurar CORS
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

# # Adiciona o middleware de tratamento de erros
# app.add_middleware(ErrorHandlerMiddleware)

# # Registra os handlers globais de erro
# register_error_handlers(app)

# # Inclui as rotas da API
# app.include_router(api_router, prefix=settings.API_V1_STR) 