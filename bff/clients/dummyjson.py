from typing import Optional

import httpx
from fastapi import HTTPException, status


async def dummyjson_get(endpoint: str, params: Optional[dict] = None) -> dict:
    """Realiza GET na API DummyJSON e retorna o JSON da resposta.

    Mapeia HTTPStatusError para o mesmo status code e RequestError para 502.
    """
    url = f"https://dummyjson.com{endpoint}"
    timeout = httpx.Timeout(10.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Erro na API DummyJSON: {exc.response.text}",
            )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Erro de conexão com DummyJSON: {str(exc)}",
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {str(exc)}",
            )
