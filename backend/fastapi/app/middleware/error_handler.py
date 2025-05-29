from typing import Callable, Dict, Any
from fastapi import Request, Response, FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import traceback
import logging

from app.errors.base import (
    AppError,
    ErrorCode,
    BusinessError,
    SystemError,
    create_validation_error
)

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Middleware para capturar e tratar todos os erros não tratados da aplicação.
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except AppError as e:
            # Erros já formatados pela aplicação
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
        except ValidationError as e:
            # Erros de validação do Pydantic
            error = create_validation_error(
                error_code=ErrorCode.INVALID_CONTENT,
                message="Erro de validação dos dados",
                validation_errors=format_validation_errors(e.errors())
            )
            return JSONResponse(
                status_code=error.status_code,
                content={"detail": error.detail}
            )
        except SQLAlchemyError as e:
            # Erros de banco de dados
            logger.error(f"Database error: {str(e)}\n{traceback.format_exc()}")
            error = SystemError(
                error_code=ErrorCode.DATABASE_ERROR,
                message="Erro interno do banco de dados",
                details={"error": str(e)} if not is_production() else None
            )
            return JSONResponse(
                status_code=error.status_code,
                content={"detail": error.detail}
            )
        except ValueError as e:
            # Erros de valor inválido
            error = create_validation_error(
                error_code=ErrorCode.INVALID_CONTENT,
                message=str(e),
                validation_errors={"value": str(e)}
            )
            return JSONResponse(
                status_code=error.status_code,
                content={"detail": error.detail}
            )
        except Exception as e:
            # Erros não tratados
            logger.error(f"Unhandled error: {str(e)}\n{traceback.format_exc()}")
            error = SystemError(
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                message="Erro interno do servidor",
                details={"error": str(e)} if not is_production() else None
            )
            return JSONResponse(
                status_code=error.status_code,
                content={"detail": error.detail}
            )

def register_error_handlers(app: FastAPI) -> None:
    """
    Registra handlers globais para tipos específicos de erro.
    """
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        Handler para erros de validação do FastAPI.
        Converte os erros para nosso formato padrão.
        """
        errors = format_validation_errors(exc.errors())
        error = create_validation_error(
            error_code=ErrorCode.INVALID_CONTENT,
            message="Erro de validação dos dados da requisição",
            validation_errors=errors
        )
        return JSONResponse(
            status_code=error.status_code,
            content={"detail": error.detail}
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
        """
        Handler para erros de validação do Pydantic.
        Converte os erros para nosso formato padrão.
        """
        errors = format_validation_errors(exc.errors())
        error = create_validation_error(
            error_code=ErrorCode.INVALID_CONTENT,
            message="Erro de validação dos dados",
            validation_errors=errors
        )
        return JSONResponse(
            status_code=error.status_code,
            content={"detail": error.detail}
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """
        Handler para erros de valor inválido.
        """
        error = create_validation_error(
            error_code=ErrorCode.INVALID_CONTENT,
            message=str(exc),
            validation_errors={"value": str(exc)}
        )
        return JSONResponse(
            status_code=error.status_code,
            content={"detail": error.detail}
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        """
        Handler para erros do SQLAlchemy.
        """
        logger.error(f"Database error: {str(exc)}\n{traceback.format_exc()}")
        error = SystemError(
            error_code=ErrorCode.DATABASE_ERROR,
            message="Erro interno do banco de dados",
            details={"error": str(exc)} if not is_production() else None
        )
        return JSONResponse(
            status_code=error.status_code,
            content={"detail": error.detail}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """
        Handler para qualquer erro não tratado.
        """
        logger.error(f"Unhandled error: {str(exc)}\n{traceback.format_exc()}")
        error = SystemError(
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
            message="Erro interno do servidor",
            details={"error": str(exc)} if not is_production() else None
        )
        return JSONResponse(
            status_code=error.status_code,
            content={"detail": error.detail}
        )

def format_validation_errors(errors: list) -> Dict[str, Any]:
    """
    Formata os erros de validação do Pydantic para um formato mais amigável.
    
    Exemplo de saída:
    {
        "nome": {
            "msg": "campo obrigatório",
            "type": "missing",
            "field": "nome",
            "location": "body"
        },
        "email": {
            "msg": "email inválido",
            "type": "value_error.email",
            "field": "email",
            "location": "body"
        }
    }
    """
    formatted_errors = {}
    for error in errors:
        location = " -> ".join(str(loc) for loc in error["loc"])
        field = error["loc"][-1] if error["loc"] else "unknown"
        formatted_errors[location] = {
            "msg": error["msg"],
            "type": error["type"],
            "field": field,
            "location": error["loc"][0] if error["loc"] else "unknown"
        }
    return formatted_errors

def is_production() -> bool:
    """
    Verifica se o ambiente é de produção.
    Em produção, alguns detalhes de erro são omitidos por segurança.
    """
    from app.core.config import settings
    return settings.ENVIRONMENT == "production" 