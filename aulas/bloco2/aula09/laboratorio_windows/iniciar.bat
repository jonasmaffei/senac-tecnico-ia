@echo off
REM ============================================================================
REM iniciar.bat - menu do laboratorio Windows da Aula 09
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
echo  Aula 09 - Laboratorio Windows: OpenCL (GPU AMD real)
echo ============================================================
echo.
echo   [1] 1_listar_dispositivos.py    - plataformas e dispositivos OpenCL
echo   [2] 2_primeiro_kernel.py        - primeiro kernel OpenCL (soma de vetores)
echo   [3] 3_benchmark_work_groups.py  - CPU vs. OpenCL e escolha do work-group
echo   [0] Sair
echo.
set /p op="Escolha uma opcao: "
echo.

if "%op%"=="1" call ".venv\Scripts\python.exe" "1_listar_dispositivos.py"
if "%op%"=="2" call ".venv\Scripts\python.exe" "2_primeiro_kernel.py"
if "%op%"=="3" call ".venv\Scripts\python.exe" "3_benchmark_work_groups.py"

if "%op%"=="0" goto fim

echo.
echo ------------------------------------------------------------
pause
goto menu

:fim
echo Ate a proxima!
endlocal
