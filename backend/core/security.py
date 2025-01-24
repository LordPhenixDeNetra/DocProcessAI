from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from core.config import get_settings

settings = get_settings()

# Définition du header pour la clé API
api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=False)

async def validate_api_key(
        api_key_header: str = Security(api_key_header),
) -> str:
    """
    Valide la clé API fournie dans les headers
    """
    if api_key_header == settings.API_KEY:
        return api_key_header

    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="Invalid API Key"
    )

def create_api_key() -> str:
    """
    Crée une nouvelle clé API (utilitaire pour l'administration)
    """
    import secrets
    return secrets.token_urlsafe(32)