"""
Hook para formatar arquivos Python usando o Black.
Hook é uma maneira de automatizar ações que são feitas durante o ciclo de 
execução do claude code. É possível definir certos comportamentos que vão acontecer de acordo com o que
o claude code estiver fazendo.

Por exemplo, podemos pedir que seja corrigido a escrita de um determinado arquivo e o claude code vai 
executar o hook descrito em .claude/hooks/formatpy.py.
"""


#!/usr/bin/env python3

import sys
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

LOG_FILE = '/tmp/hook.log'

def log(msg: str):
    with open(LOG_FILE, 'a') as f:
        f.write(msg + '\n')

def md5sum(file_path: Path) -> str:
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    log("==== HOOK EXECUTOU ====")

    try:
        data = json.load(sys.stdin)
    except Exception:
        log("Erro ao ler JSON da entrada")
        return

    file_path = data.get('tool_input', {}).get("file_path")

    log(f"Arquivo: {file_path}")

    if not file_path:
        return

    path = Path(file_path)

    if not path.exists():
        log("Arquivo não existe!")
        return

    md5_before = md5sum(path)
    log(f'MD5 BEFORE: {md5_before}')

    if path.suffix.lower() == '.py':
        try:
            subprocess.run(
                ['black', str(path)],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                text=True
            )
            log(f'Arquivo formatado: {file_path}')
        except Exception as e:
            log(f'Erro ao rodar black: {e}')

    md5_after = md5sum(path)
    log(f'MD5 AFTER: {md5_after}')

if __name__ == '__main__':
    main()