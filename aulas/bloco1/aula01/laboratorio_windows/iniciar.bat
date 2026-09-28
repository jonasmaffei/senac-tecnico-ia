@echo off
REM ============================================================================
REM iniciar.bat - menu do laboratorio Windows da Aula 01
REM ----------------------------------------------------------------------------
REM Uso: duplo clique neste arquivo, OU no Prompt:  iniciar.bat
REM
REM Cria o ambiente virtual (.venv) na primeira execucao, instala as
REM dependencias e mostra um MENU com os experimentos de hardware real.
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
echo  Aula 01 - Laboratorio Windows (hardware real)
echo ============================================================
echo.
echo   [1] 1_hardware.py   - descobrir CPU, RAM e GPU desta maquina
echo   [2] 2_benchmark.py  - sequencial vs. vetorizado (medido aqui)
echo   [0] Sair
echo.
set /p op="Escolha uma opcao: "
echo.

if "%op%"=="1" call ".venv\Scripts\python.exe" "1_hardware.py"
if "%op%"=="2" call ".venv\Scripts\python.exe" "2_benchmark.py"

if "%op%"=="0" goto fim

echo.
echo ------------------------------------------------------------
pause
goto menu

:fim
echo Ate a proxima!
endlocal
