@echo off
chcp 65001 > NUL
title Aula 18 - Gestao de Processos e Carga de Trabalho (Windows Host)

echo ============================================================
echo     Aula 18 - Gestao de Processos e Fila de GPU (Windows)
echo ============================================================
echo.

if not exist ".venv" (
    echo [1/2] Criando ambiente virtual Python ^(.venv^)...
    python -m venv .venv
)

echo [2/2] Ativando ambiente virtual e instalando dependencias...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip > NUL
pip install -r requirements.txt

:MENU
cls
echo ============================================================
echo     MENU - Laboratorio de Gestao de Processos (Aula 18)
echo ============================================================
echo   1. Testar Exclusao Mutua Simples (1_flock_gpu.py)
echo   2. Enfileirar 1 Job com Prioridade (2_gpu_queue.py)
echo   3. Testar Fila de 4 Jobs COM monitor ao vivo (3_teste_fila.py)
echo   4. Monitorar GPU/Lock/Fila por 15s (4_monitor_processos_gpu.py)
echo   5. Sair
echo ============================================================
set /p OPCAO="Escolha uma opcao (1-5): "

if "%OPCAO%"=="1" (
    cls
    echo Executando Exclusao Mutua Simples...
    python 1_flock_gpu.py train_job.py --nome "Job-Exclusivo" --epocas 3
    pause
    goto MENU
)

if "%OPCAO%"=="2" (
    cls
    echo Enfileirando Job com Prioridade 1 ^(Alta^)...
    python 2_gpu_queue.py 1 "Job-Manual" train_job.py --nome "Job-Manual" --epocas 2
    pause
    goto MENU
)

if "%OPCAO%"=="3" (
    cls
    echo Teste de Fila com 4 Jobs ^+ monitor ao vivo...
    python 3_teste_fila.py
    pause
    goto MENU
)

if "%OPCAO%"=="4" (
    cls
    echo Monitorando GPU/Lock/Fila por 15 segundos...
    python 4_monitor_processos_gpu.py 15 1
    pause
    goto MENU
)

if "%OPCAO%"=="5" (
    echo Encerrando laboratorio. Gestao de processos concluida!
    exit /b 0
)

echo Opcao invalida! Tente novamente.
pause
goto MENU
