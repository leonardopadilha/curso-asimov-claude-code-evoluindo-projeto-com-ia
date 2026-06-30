import os

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

API_KEY = os.getenv("API_KEY")


async def get_api_key(api_key: str = Depends(api_key_header)):
    """Valida o header X-API-Key contra a variável de ambiente API_KEY."""
    if api_key is None or api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chave API inválida ou ausente. Use o header X-API-Key.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key
