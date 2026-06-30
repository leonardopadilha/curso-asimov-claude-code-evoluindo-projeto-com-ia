---
description: Formata todos os arquivos python do projeto usando o comando black.
allowed-tools: Bash(black *)
---

# Formatador

Verifica se o 'black' está instalado e formata o código Python do projeto.

Passos:

1. Execute `black --version` para verificar se o black está disponível.
2. Se o comando falhar ou não for encontrado:
    - Informe ao usuário que o `black` não está instalado.
    - Mostre como instalar: `pip install black`
    - Não tente instalar. Encerre.
3. Se o black estiver disponível, execute `black .` na raiz do projeto para formatar todos os arquivos Python.
4. Informe ao usuário quais arquivos foram reformatados (se houver).