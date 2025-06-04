from enum import Enum
from typing import Optional, Dict, Any
from fastapi import HTTPException, status

class ErrorCode(str, Enum):
    # Códigos de erro 404 - Not Found
    NOT_FOUND = "NOT_FOUND"

    # Códigos de erro 400 - Business Error
    ALREADY_EXISTS = "ALREADY_EXISTS"
    ACCESS_DENIED = "ACCESS_DENIED"
    INVALID_CONTENT = "INVALID_CONTENT"
    
    # Códigos de erro 500 - System Error
    DATABASE_ERROR = "DATABASE_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"

class AppError(HTTPException):
    """Classe base para todos os erros da aplicação"""
    def __init__(
        self,
        status_code: int,
        error_code: ErrorCode,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None
    ):
        self.error_code = error_code
        self.details = details or {}
        
        # Formata a resposta de erro
        error_response = {
            "error_code": error_code,
            "message": message,
            "details": self.details
        }
        
        super().__init__(
            status_code=status_code,
            detail=error_response,
            headers=headers
        )

class NotFoundError(AppError):
    """
    Erro 404 - Recurso não encontrado
    Use quando um recurso específico não pode ser encontrado no sistema
    """
    def __init__(
        self,
        error_code: ErrorCode,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=error_code,
            message=message,
            details=details
        )

class BusinessError(AppError):
    """
    Erro 400 - Erro de negócio
    Use para violações de regras de negócio, validações e conflitos
    """
    def __init__(
        self,
        error_code: ErrorCode,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=error_code,
            message=message,
            details=details
        )

class SystemError(AppError):
    """
    Erro 500 - Erro do sistema
    Use para erros internos, problemas de infraestrutura e falhas inesperadas
    """
    def __init__(
        self,
        error_code: ErrorCode,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=error_code,
            message=message,
            details=details
        )

# Funções auxiliares para criar erros comuns
def create_not_found_error(
    resource_type: str,
    resource_id: Any = None
) -> NotFoundError:
    """Cria um erro padronizado para recursos não encontrados"""
    details = {"resource_id": str(resource_id)} if resource_id else None
    return NotFoundError(
        error_code=ErrorCode.NOT_FOUND,
        message=f"{resource_type} não encontrado(a)",
        details=details
    )

def create_already_exists_error(
    resource_type: str,
    identifier: Any = None
) -> BusinessError:
    """Cria um erro padronizado para recursos que já existem"""
    details = {"identifier": str(identifier)} if identifier else None
    return BusinessError(
        error_code=ErrorCode.ALREADY_EXISTS,
        message=f"{resource_type} já existe",
        details=details
    )

def create_validation_error(
    error_code: ErrorCode,
    message: str,
    validation_errors: Dict[str, Any]
) -> BusinessError:
    """Cria um erro padronizado para falhas de validação"""
    return BusinessError(
        error_code=error_code,
        message=message,
        details={"validation_errors": validation_errors}
    )

def create_access_denied_error(
    resource_type: str,
    resource_id: Any = None
) -> BusinessError:
    """Cria um erro padronizado para acesso negado"""
    details = {"resource_id": str(resource_id)} if resource_id else None
    return BusinessError(
        error_code=ErrorCode.ACCESS_DENIED,
        message=f"Acesso negado ao(à) {resource_type}",
        details=details
    ) 