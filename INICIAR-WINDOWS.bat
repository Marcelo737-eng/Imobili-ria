@echo off
chcp 65001 >nul
title Sistema de Gestao Imobiliaria
cd /d "%~dp0"

echo ======================================================================
echo   SISTEMA DE GESTAO IMOBILIARIA
echo   Iniciando...
echo ======================================================================
echo.

rem --- procura o Python instalado ---
set PY=
where py >nul 2>nul && set PY=py
if "%PY%"=="" (where python >nul 2>nul && set PY=python)
if "%PY%"=="" (where python3 >nul 2>nul && set PY=python3)

if "%PY%"=="" (
    echo   O PYTHON NAO ESTA INSTALADO NESTE COMPUTADOR.
    echo.
    echo   Como resolver:
    echo     1. Acesse https://www.python.org/downloads/
    echo     2. Baixe a versao mais recente do Windows
    echo     3. Ao instalar, MARQUE a opcao "Add Python to PATH"
    echo     4. Reinicie o computador e execute este arquivo novamente
    echo.
    pause
    exit /b 1
)

rem --- primeira execucao: cria os dados de demonstracao ---
if not exist "dados\imobiliaria.db" (
    echo   Primeira execucao: preparando os dados de demonstracao...
    echo.
    %PY% run.py --somente-demo
    echo.
)

%PY% run.py

echo.
echo ======================================================================
echo   O servidor foi encerrado.
echo ======================================================================
pause
