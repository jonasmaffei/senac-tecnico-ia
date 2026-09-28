@echo off
chcp 65001 > NUL
title Aula 18 — Gestão de Processos e Carga de Trabalho (Windows Host)

echo ============================================================
echo   🤖 Aula 18 — Gestão de Processos e Fila de GPU (Windows)
echo ============================================================
echo.

if not exist ".venv" (
    echo [1/2] Criando ambiente virtual Python (.venv)...
    python -m venv .venv
)

echo [2/2] Ativando ambiente virtual e instalando dependências...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip > NUL
pip install -r requirements.txt

:MENU
cls
echo ============================================================
echo   📊 MENU - Laboratório de Gestão de Processos (Aula 18)
echo ============================================================
echo   1. Testar Exclusão Mútua Simples (1_flock_gpu.py)
echo   2. Enfileirar 1 Job com Prioridade (2_gpu_queue.py)
echo   3. Testar Fila Concorrente de 4 Jobs (3_teste_fila.py)
echo   4. Monitorar Processos e Fila ao Vivo (4_monitor_processos_gpu.py)
echo   5. Sair
echo ============================================================
set /p OPCAO="Escolha uma opção (1-5): "

if "%OPCAO%"=="1" (
    cls
    echo Executando Exclusão Mútua Simples...
    python 1_flock_gpu.py train_job.py --nome "Job-Exclusivo" --epocas 3
    pause
    goto MENU
)

if "%OPCAO%"=="2" (
    cls
    echo Enfileirando Job com Prioridade 1 (Alta)...
    python 2_gpu_queue.py 1 "Job-Manual" train_job.py --nome "Job-Manual" --epocas 2
    pause
    goto MENU
)

if "%OPCAO%"=="3" (
    cls
    echo Executando Teste de Fila com 4 Jobs Simultâneos...
    python 3_teste_fila.py
    pause
    goto MENU
)

if "%OPCAO%"=="4" (
    cls
    echo Monitorando Processos e Estado da Fila...
    python 4_monitor_processos_gpu.py
    pause
    goto MENU
)

if "%OPCAO%"=="5" (
    echo Encerrando laboratório. Gestão de processos concluída!
    exit /b 0
)

echo Opção inválida! Tente novamente.
pause
goto MENU
