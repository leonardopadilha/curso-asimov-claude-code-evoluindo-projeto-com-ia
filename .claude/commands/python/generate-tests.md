---
description: Gerar testes unitários com pytest para uma função ou método (com Faker e parametrização)
argument-hint: target=<function-name> [framework=<fastapi|django>]
params:
  - name: target
    type: string
    description: Nome da função ou método a ser testado
    required: true

  - name: framework
    type: string
    description: Framework utilizado (ex: fastapi, django)
    required: false
---

Antes de gerar os testes:
- Analise cuidadosamente a implementação da função ou método {{target}}
- Entenda sua lógica, dependências e possíveis cenários de uso
- Identifique comportamentos esperados, exceções e pontos críticos

Gere testes unitários utilizando pytest para a função ou método: {{target}}.

## Requisitos

### 1. Testes de Funcionalidade
- Validar o comportamento esperado da função/método
- Cobrir casos de uso comuns

### 2. Edge Cases (Casos Limite)
- Testar valores de fronteira
- Incluir limites (ex: inputs vazios, valores mínimos/máximos, None quando aplicável)

### 3. Dirty Cases (Casos de Erro)
- Entradas inválidas
- Tipos incorretos
- Parâmetros obrigatórios ausentes
- Garantir que exceções apropriadas sejam lançadas

### 4. Uso de Faker (OBRIGATÓRIO quando aplicável)
- Utilizar a biblioteca Faker para gerar dados dinâmicos
- Exemplos:
  - nomes
  - emails
  - textos
  - números
- Evitar dados hardcoded quando Faker fizer sentido

### 5. Parametrização (pytest.mark.parametrize)
- Utilizar pytest.mark.parametrize sempre que houver múltiplos cenários semelhantes
- Aplicar principalmente em:
  - testes de funcionalidade com variações de input
  - edge cases
  - validação de erros

### 6. Dependências Externas (IMPORTANTE)
Se a função/método:
- Chama APIs
- Usa banco de dados
- Acessa arquivos
- Depende de serviços externos

👉 Utilizar mocks (pytest + unittest.mock ou pytest-mock)

### 7. Estrutura dos Testes
- Usar SOMENTE funções (NÃO usar classes de teste)
- Seguir convenções do pytest
- Nomes descritivos (ex: test_create_user_success)
- Utilizar fixtures quando apropriado

### 8. Docstrings (OBRIGATÓRIO)
- Cada função de teste deve conter uma docstring
- A docstring deve explicar claramente o propósito do teste
- Ser objetiva e descritiva

### 9. Formato da Saída
- Retornar APENAS o código dos testes
- Incluir imports necessários
- Código limpo, organizado e idiomático

### 10. Compatibilidade com Framework
- Se framework={{framework}}, adaptar os testes conforme necessário  
  (ex: FastAPI → TestClient, Django → pytest-django)

---

Agora gere os testes para: {{target}}
