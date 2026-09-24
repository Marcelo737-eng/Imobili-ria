#!/usr/bin/env bash
# Inicia o Sistema de Gestão Imobiliária no Mac ou Linux.
cd "$(dirname "$0")" || exit 1

echo "======================================================================"
echo "  SISTEMA DE GESTÃO IMOBILIÁRIA"
echo "  Iniciando..."
echo "======================================================================"
echo

# procura um Python 3.9 ou mais novo
PY=""
for candidato in python3 python3.13 python3.12 python3.11 python3.10 python3.9 python; do
  if command -v "$candidato" >/dev/null 2>&1; then
    if "$candidato" -c 'import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)' 2>/dev/null; then
      PY="$candidato"
      break
    fi
  fi
done

if [ -z "$PY" ]; then
  echo "  O PYTHON 3.9 (OU MAIS NOVO) NÃO FOI ENCONTRADO."
  echo
  echo "  Como resolver:"
  echo "    macOS:          brew install python3"
  echo "                    ou baixe em https://www.python.org/downloads/"
  echo "    Ubuntu/Debian:  sudo apt install python3"
  echo "    Fedora:         sudo dnf install python3"
  echo
  exit 1
fi

echo "  Usando: $($PY --version)"
echo

# primeira execução: cria os dados de demonstração
if [ ! -f "dados/imobiliaria.db" ]; then
  echo "  Primeira execução: preparando os dados de demonstração..."
  echo
  "$PY" run.py --somente-demo
  echo
fi

"$PY" run.py
