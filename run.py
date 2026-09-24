#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ponto de entrada do Sistema de Gestão Imobiliária.

Uso mais simples:
    python3 run.py              (Linux/Mac)
    py run.py                   (Windows)

Outras opções:
    python3 run.py --demo            cria dados de demonstração e inicia
    python3 run.py --somente-demo    apenas cria os dados de demonstração
    python3 run.py --porta 9000      usa outra porta
    python3 run.py --sem-navegador   não abre o navegador automaticamente
    python3 run.py --reset           apaga todos os dados (pede confirmação)
"""
import sys

# ---------------------------------------------------------------------------
# Verificação de versão ANTES de importar qualquer coisa do projeto,
# para que quem estiver em um Python antigo receba uma mensagem clara.
# ---------------------------------------------------------------------------
VERSAO_MINIMA = (3, 9)

if sys.version_info < VERSAO_MINIMA:
    atual = ".".join(str(n) for n in sys.version_info[:3])
    print("=" * 70)
    print("  NAO FOI POSSIVEL INICIAR: versao do Python muito antiga")
    print("=" * 70)
    print("  Este sistema precisa do Python 3.9 ou mais novo.")
    print("  Versao encontrada: " + atual)
    print("")
    print("  Baixe a versao atual em: https://www.python.org/downloads/")
    print("")
    print("  Se voce tem mais de um Python instalado, tente:")
    print("     python3.11 run.py      (Linux/Mac)")
    print("     py -3.11 run.py        (Windows)")
    print("=" * 70)
    sys.exit(1)

import argparse
import os
import shutil
import socket
import threading
import webbrowser
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

try:
    from app import config, db, servidor
except ImportError as exc:
    print("=" * 70)
    print("  NAO FOI POSSIVEL INICIAR: arquivos do sistema nao encontrados")
    print("=" * 70)
    print("  Detalhe tecnico: " + str(exc))
    print("")
    print("  Verifique se a pasta 'app' esta ao lado do arquivo run.py.")
    print("  Pasta atual: " + str(RAIZ))
    existentes = sorted(p.name for p in RAIZ.iterdir()) if RAIZ.is_dir() else []
    print("  Conteudo encontrado: " + (", ".join(existentes) or "(vazio)"))
    print("")
    print("  Se voce baixou um arquivo .zip, extraia todo o conteudo antes de")
    print("  executar (nao rode de dentro do zip).")
    print("=" * 70)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Ajuda de rede
# ---------------------------------------------------------------------------
def ip_da_rede_local() -> str:
    """Descobre o IP da máquina na rede local (para acessar pelo celular)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))       # não envia dados, só resolve a rota
            return s.getsockname()[0]
        finally:
            s.close()
    except OSError:
        try:
            return socket.gethostbyname(socket.gethostname())
        except OSError:
            return ""


def porta_livre(host: str, porta: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host if host != "0.0.0.0" else "", porta))
            return True
        except OSError:
            return False


def escolher_porta(host: str, desejada: int) -> int:
    """Se a porta estiver ocupada, procura a próxima livre e avisa."""
    if porta_livre(host, desejada):
        return desejada
    for tentativa in range(desejada + 1, desejada + 21):
        if porta_livre(host, tentativa):
            print("-" * 70)
            print("  AVISO: a porta %d ja estava em uso por outro programa." % desejada)
            print("  O sistema vai usar a porta %d." % tentativa)
            print("-" * 70)
            return tentativa
    print("=" * 70)
    print("  NAO FOI POSSIVEL INICIAR: nenhuma porta livre encontrada")
    print("=" * 70)
    print("  As portas de %d a %d estao ocupadas." % (desejada, desejada + 20))
    print("  Feche o outro programa ou escolha uma porta:")
    print("     python3 run.py --porta 8500")
    print("=" * 70)
    sys.exit(1)


def abrir_navegador(url: str) -> None:
    def tarefa():
        try:
            webbrowser.open(url)
        except Exception:
            pass
    threading.Timer(1.2, tarefa).start()


# ---------------------------------------------------------------------------
def main() -> None:
    p = argparse.ArgumentParser(
        description="Sistema de Gestão Imobiliária",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--host", default=config.HOST,
                   help="endereço de escuta (padrão: 0.0.0.0, aceita a rede local)")
    p.add_argument("--porta", type=int, default=config.PORT,
                   help="porta do servidor (padrão: 8000)")
    p.add_argument("--demo", action="store_true",
                   help="cria os dados de demonstração e inicia")
    p.add_argument("--somente-demo", action="store_true",
                   help="cria os dados de demonstração e encerra")
    p.add_argument("--sem-navegador", action="store_true",
                   help="não abre o navegador automaticamente")
    p.add_argument("--reset", action="store_true",
                   help="APAGA o banco e os arquivos enviados antes de iniciar")
    args = p.parse_args()

    if args.reset:
        print("Isso apagará TODOS os dados: imóveis, clientes, fotos e documentos.")
        resposta = input("Digite 'apagar' para confirmar: ")
        if resposta.strip().lower() != "apagar":
            print("Operação cancelada. Nada foi alterado.")
            return
        if config.DATA_DIR.exists():
            shutil.rmtree(config.DATA_DIR)
        print("Dados removidos.")

    if args.demo or args.somente_demo:
        db.inicializar()
        from app import seguranca
        seguranca.garantir_admin_inicial()
        from app.demo import popular
        popular()
        if args.somente_demo:
            return

    porta = escolher_porta(args.host, args.porta)
    url_local = "http://localhost:%d" % porta

    if not args.sem_navegador and os.environ.get("IMOB_SEM_NAVEGADOR") != "1":
        abrir_navegador(url_local)

    try:
        servidor.iniciar(args.host, porta, ip_rede=ip_da_rede_local())
    except PermissionError:
        print("=" * 70)
        print("  NAO FOI POSSIVEL INICIAR: permissao negada na porta %d" % porta)
        print("=" * 70)
        print("  Portas abaixo de 1024 exigem administrador. Use uma porta alta:")
        print("     python3 run.py --porta 8000")
        print("=" * 70)
        sys.exit(1)
    except OSError as exc:
        print("=" * 70)
        print("  NAO FOI POSSIVEL INICIAR O SERVIDOR")
        print("=" * 70)
        print("  Detalhe tecnico: " + str(exc))
        print("  Tente outra porta:  python3 run.py --porta 8500")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
