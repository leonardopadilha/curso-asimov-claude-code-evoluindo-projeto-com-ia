---
name: gitignore
description: Identifica a linguagem do projeto (C, Python ou TypeScript) e aplica o template de .gitignore correspondente, removendo duplicatas de forma idempotente.
disable-model-invocation: true
---

# SKILL.md: Gitignore Automator (v2)

## Role

Você é um especialista em Git e automação. Sua tarefa é gerenciar o arquivo .gitignore do projeto atual de forma idempotente e organizada.
Context

A estrutura da skill reside em .claude/skills/gitignore/:

* Templates: templates/ (Arquivos: C.gitignore, Python.gitignore, Typescript.gitignore).

* Validação: Script Python scripts/done.py.

## Workflow

### Identificação de Linguagem:

Analise os arquivos na raiz do projeto.

REGRA CRÍTICA: Se a linguagem principal identificada não possuir um template correspondente na pasta templates/, interrompa a execução imediatamente. Informe ao usuário: "Linguagem não suportada pela skill gitignore. Nenhuma alteração foi feita."

### Verificação de Estado:

Localize o template (ex: Python.gitignore).

Execute o script: python3 .claude/skills/gitignore/scripts/done.py <caminho_do_template> .gitignore.

### Ação (Se o script retornar False):

Se o .gitignore do projeto não existir, crie-o com o conteúdo do template.

Se já existir, realize o append do conteúdo do template ao final do arquivo.

### Otimização e Limpeza (Bash Uniq):

Após adicionar o conteúdo, você deve garantir que o arquivo não contenha linhas duplicadas consecutivas ou desordem.

Execute o seguinte comando bash na raiz do projeto:
sort .gitignore | uniq > .gitignore.tmp && mv .gitignore.tmp .gitignore

Nota: Usamos o sort antes do uniq pois o uniq do Linux apenas remove duplicatas adjacentes.

### Constraints

* Não prossiga se a linguagem for ambígua ou inexistente nos templates.

* Preserve sempre as quebras de linha para manter a legibilidade.

* Use caminhos relativos ao diretório de trabalho do projeto.