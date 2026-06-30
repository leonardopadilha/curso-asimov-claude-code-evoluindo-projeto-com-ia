from fastapi import FastAPI

from bff.routers.recipes import router as recipes_router

app = FastAPI(
    title="API de Receitas (DummyJSON Proxy)",
    description="Busca e detalhamento de receitas usando a API DummyJSON como backend",
    version="1.0.0",
)

app.include_router(recipes_router)
