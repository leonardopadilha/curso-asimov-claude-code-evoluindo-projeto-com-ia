import asyncio

import pytest
from faker import Faker
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from bff.auth import API_KEY_NAME, get_api_key

fake = Faker()


def _run(coro):
    """Executa uma coroutine de forma sincrona, usada para testar get_api_key diretamente fora de um request real."""
    return asyncio.run(coro)


@pytest.fixture
def protected_app():
    """Cria uma app FastAPI minima com uma rota protegida pela dependencia get_api_key."""
    app = FastAPI()

    @app.get("/protected")
    async def protected_route(api_key: str = Depends(get_api_key)):
        return {"api_key": api_key}

    return app


@pytest.fixture
def client(protected_app):
    """Cliente HTTP de testes para a app protegida, usado nos cenarios de integracao."""
    return TestClient(protected_app)


# ---------------------------------------------------------------------------
# Testes de funcionalidade
# ---------------------------------------------------------------------------


def test_get_api_key_returns_key_when_valid(monkeypatch):
    """Garante que get_api_key retorna a propria chave quando ela bate com a variavel de ambiente API_KEY."""
    valid_key = fake.uuid4()
    monkeypatch.setattr("bff.auth.API_KEY", valid_key)

    result = _run(get_api_key(api_key=valid_key))

    assert result == valid_key


def test_protected_route_returns_200_with_valid_header(client, monkeypatch):
    """Verifica que uma requisicao HTTP com o header X-API-Key correto recebe 200 e o corpo esperado."""
    valid_key = fake.password(length=24)
    monkeypatch.setattr("bff.auth.API_KEY", valid_key)

    response = client.get("/protected", headers={API_KEY_NAME: valid_key})

    assert response.status_code == 200
    assert response.json() == {"api_key": valid_key}


@pytest.mark.parametrize("attempt", range(3))
def test_get_api_key_success_with_random_keys(monkeypatch, attempt):
    """Cobre multiplos cenarios de chaves validas geradas dinamicamente com Faker."""
    valid_key = fake.sha256()
    monkeypatch.setattr("bff.auth.API_KEY", valid_key)

    result = _run(get_api_key(api_key=valid_key))

    assert result == valid_key


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


def test_get_api_key_both_empty_strings_are_treated_as_equal(monkeypatch):
    """Caso de fronteira: chave configurada e chave enviada vazias ('') sao consideradas iguais, pois nao ha checagem explicita de string vazia."""
    monkeypatch.setattr("bff.auth.API_KEY", "")

    result = _run(get_api_key(api_key=""))

    assert result == ""


def test_get_api_key_missing_header_raises_401_even_if_api_key_unset(monkeypatch):
    """Caso de fronteira: quando a variavel API_KEY nao esta configurada (None) e o header tambem nao foi enviado (None), o acesso deve ser negado."""
    monkeypatch.setattr("bff.auth.API_KEY", None)

    with pytest.raises(Exception) as exc_info:
        _run(get_api_key(api_key=None))

    assert exc_info.value.status_code == 401


def test_get_api_key_is_case_sensitive(monkeypatch):
    """Caso de fronteira: chaves que diferem apenas por capitalizacao devem ser tratadas como invalidas."""
    valid_key = "MinhaChaveSecreta123"
    monkeypatch.setattr("bff.auth.API_KEY", valid_key)

    with pytest.raises(Exception) as exc_info:
        _run(get_api_key(api_key=valid_key.lower()))

    assert exc_info.value.status_code == 401


# ---------------------------------------------------------------------------
# Dirty cases (entradas invalidas / parametros ausentes)
# ---------------------------------------------------------------------------


def test_get_api_key_missing_header_raises_401(client, monkeypatch):
    """Garante que uma requisicao sem o header X-API-Key recebe 401 Unauthorized."""
    monkeypatch.setattr("bff.auth.API_KEY", fake.sha256())

    response = client.get("/protected")

    assert response.status_code == 401
    assert response.json()["detail"] == "Chave API inválida ou ausente. Use o header X-API-Key."
    assert response.headers["WWW-Authenticate"] == "ApiKey"


def test_get_api_key_wrong_header_name_is_treated_as_missing(client, monkeypatch):
    """Garante que enviar a chave em um header com nome diferente do esperado resulta em 401, pois o header correto nao foi encontrado."""
    monkeypatch.setattr("bff.auth.API_KEY", fake.sha256())

    response = client.get("/protected", headers={"Api-Key-Errada": fake.sha256()})

    assert response.status_code == 401


@pytest.mark.parametrize(
    "invalid_key",
    [
        fake.password(length=12),
        fake.uuid4(),
        fake.word(),
        "",
    ],
)
def test_get_api_key_invalid_key_raises_401(client, monkeypatch, invalid_key):
    """Parametriza diversos valores de chave invalida (texto aleatorio, uuid, palavra, string vazia) e garante 401 em todos os casos."""
    monkeypatch.setattr("bff.auth.API_KEY", fake.sha256())

    response = client.get("/protected", headers={API_KEY_NAME: invalid_key})

    assert response.status_code == 401


def test_get_api_key_with_non_string_type_raises_401(monkeypatch):
    """Caso sujo: simula um tipo incorreto (inteiro) chegando como api_key e garante que a comparacao falha com 401, em vez de lancar um erro nao tratado."""
    monkeypatch.setattr("bff.auth.API_KEY", "chave-valida")

    with pytest.raises(Exception) as exc_info:
        _run(get_api_key(api_key=12345))

    assert exc_info.value.status_code == 401
