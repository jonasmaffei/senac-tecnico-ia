@echo off
REM ============================================================================
REM iniciar.bat - menu do laboratorio Windows da Aula 04
REM ----------------------------------------------------------------------------
REM Uso: duplo clique neste arquivo, OU no Prompt:  iniciar.bat
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
echo  Aula 04 - Laboratorio Windows (hardware real)
echo ============================================================
echo.
echo   [1] 1_processos_threads.py  - sequencial vs. threading vs. multiprocessing
echo   [2] 2_io_bound.py           - quando threading ajuda (I/O)
echo   [3] 3_kernels_cuda.py       - blocos e threads na GPU (conceito sem GPU)
echo   [4] 4_monitor_processos.py  - processos/threads como o htop
echo   [0] Sair
echo.
set /p op="Escolha uma opcao: "
echo.

if "%op%"=="1" call ".venv\Scripts\python.exe" "1_processos_threads.py"
if "%op%"=="2" call ".venv\Scripts\python.exe" "2_io_bound.py"
if "%op%"=="3" call ".venv\Scripts\python.exe" "3_kernels_cuda.py"
if "%op%"=="4" call ".venv\Scripts\python.exe" "4_monitor_processos.py"

if "%op%"=="0" goto fim

echo.
echo ------------------------------------------------------------
pause
goto menu

:fim
echo Ate a proxima!
endlocal
