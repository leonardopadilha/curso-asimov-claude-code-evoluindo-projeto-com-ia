# CLAUDE.md

Este arquivo fornece orientações ao Claude Code (claude.ai/code) ao trabalhar com o código deste repositório.

## Visão Geral do Projeto

BFF (Backend for Frontend) educativo construído com FastAPI que faz proxy da API pública [DummyJSON Recipes](https://dummyjson.com/docs/recipes), adicionando autenticação via chave de API.

## Comandos

**Configuração:**
```bash
# Ativar o ambiente virtual
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

**Rodar o servidor de desenvolvimento:**
```bash
dotenv run fastapi dev bff/main.py
```
O servidor sobe em `http://127.0.0.1:8000`. O Swagger UI está disponível em `/docs`.

**Variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto:
```env
API_KEY=SuaChaveSecretaAqui
```

## Arquitetura

Não há banco de dados nem camada de models. O código é dividido por responsabilidade:

```
bff/
  main.py              # cria a instância FastAPI e inclui os routers
  auth.py              # dependência de autenticação (get_api_key)
  clients/
    dummyjson.py        # cliente HTTP para a API DummyJSON
  routers/
    recipes.py           # endpoints de receitas (APIRouter)
```

**Fluxo de uma requisição:**
```
Cliente → validação do header X-API-Key (get_api_key) → handler do endpoint (routers/recipes.py) → dummyjson_get() (clients/dummyjson.py) → API DummyJSON
```

**Componentes principais:**
- `bff/auth.py` — `get_api_key`, dependência FastAPI que valida o header `X-API-Key` contra a variável de ambiente `API_KEY`. Aplicada via `dependencies=[Depends(get_api_key)]` em cada rota.
- `bff/clients/dummyjson.py` — `dummyjson_get(endpoint, params)`, helper HTTP assíncrono compartilhado usando `httpx.AsyncClient`. Mapeia `httpx.HTTPStatusError` e `httpx.RequestError` para os códigos `HTTPException` apropriados.
- `bff/routers/recipes.py` — `APIRouter` com dois endpoints: `GET /recipes/search` (query: `q`, `limit`, `skip`) e `GET /recipes/{recipe_id}` (path param). Incluído na app via `app.include_router(...)` em `main.py`.
