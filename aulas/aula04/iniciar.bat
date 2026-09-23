@echo off
REM ============================================================================
REM iniciar.bat - atalho para rodar os scripts da aula no Windows
REM ----------------------------------------------------------------------------
REM Uso: duplo clique neste arquivo, OU no Prompt de Comando:  iniciar.bat
REM
REM O script:
REM   1. cria o ambiente virtual (.venv) na primeira execucao;
REM   2. instala as dependencias de requirements.txt;
REM   3. mostra um MENU para escolher qual script rodar.
REM Mantem a janela aberta ao final para voce ver o resultado.
REM ============================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo.
    echo [ERRO] Python nao encontrado no PATH.
    echo Instale em https://www.python.org/downloads/ e marque
    echo "Add Python to PATH" durante a instalacao.
    echo.
    pause
    exit /b 1
)

if not exist ".venv" (
    echo Criando ambiente virtual ^(.venv^)... isso leva alguns segundos.
    python -m venv .venv
)

echo Instalando/atualizando dependencias...
call ".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
call ".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt

:menu
cls
echo ============================================================
echo  Aula 04 - Fundamentos de Processos e Threads
echo ============================================================
echo.
echo   [1] processos_threads.py  - sequencial vs. threading vs. multiprocessing
echo   [2] io_bound.py           - quando threading ajuda (I/O)
echo   [3] kernels_cuda.py       - blocos e threads na GPU (conceito sem GPU)
echo   [4] monitor_processos.py  - processos/threads como o htop
echo   [0] Sair
echo.
set /p op="Escolha uma opcao: "
echo.

if "%op%"=="1" (
    call ".venv\Scripts\python.exe" "scripts\processos_threads.py"
)
if "%op%"=="2" (
    call ".venv\Scripts\python.exe" "scripts\io_bound.py"
)
if "%op%"=="3" (
    call ".venv\Scripts\python.exe" "scripts\kernels_cuda.py"
)
if "%op%"=="4" (
    call ".venv\Scripts\python.exe" "scripts\monitor_processos.py"
)

if "%op%"=="0" goto fim

echo.
echo ------------------------------------------------------------
pause
goto menu

:fim
echo Ate a proxima!
endlocal
