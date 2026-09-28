@echo off
REM ============================================================================
REM iniciar.bat - menu do laboratorio Windows da Aula 03
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
echo  Aula 03 - Laboratorio Windows (hardware real)
echo ============================================================
echo.
echo   [1] 1_benchmark_ram_vram.py  - RAM (CPU) vs. VRAM (GPU) + custo do PCIe
echo   [2] 2_hierarquia_memoria.py  - a piramide de latencia na pratica
echo   [3] 3_monitor_memoria.py     - diagnostico de memoria (nvidia-smi/RAM)
echo   [0] Sair
echo.
set /p op="Escolha uma opcao: "
echo.

if "%op%"=="1" call ".venv\Scripts\python.exe" "1_benchmark_ram_vram.py"
if "%op%"=="2" call ".venv\Scripts\python.exe" "2_hierarquia_memoria.py"
if "%op%"=="3" call ".venv\Scripts\python.exe" "3_monitor_memoria.py"

if "%op%"=="0" goto fim

echo.
echo ------------------------------------------------------------
pause
goto menu

:fim
echo Ate a proxima!
endlocal
