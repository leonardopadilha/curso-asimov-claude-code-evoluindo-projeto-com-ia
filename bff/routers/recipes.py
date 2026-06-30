from fastapi import APIRouter, Depends, Path, Query

from bff.auth import get_api_key
from bff.clients.dummyjson import dummyjson_get

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get(
    "/search", summary="Busca receitas por termo", dependencies=[Depends(get_api_key)]
)
async def search_recipes(
    q: str = Query(..., min_length=2, description="Termo de busca"),
    limit: int = Query(10, ge=1, le=50, description="Resultados por página"),
    skip: int = Query(0, ge=0, description="Paginação: quantos pular"),
):
    """Busca receitas na DummyJSON pelo termo `q` com suporte a paginação."""
    data = await dummyjson_get(
        "/recipes/search", params={"q": q, "limit": limit, "skip": skip}
    )
    return data


@router.get(
    "/{recipe_id}",
    summary="Obtém detalhes de uma receita pelo ID",
    dependencies=[Depends(get_api_key)],
)
async def get_recipe_by_id(
    recipe_id: int = Path(
        ..., ge=1, description="ID da receita (1 a 50 na base DummyJSON)"
    )
):
    """Retorna os detalhes completos de uma receita pelo seu ID numérico."""
    data = await dummyjson_get(f"/recipes/{recipe_id}")
    return data
