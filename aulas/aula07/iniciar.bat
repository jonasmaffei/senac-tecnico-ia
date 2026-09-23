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
echo  Aula 07 - Introducao ao Modelo CUDA
echo ============================================================
echo.
echo   [1] indice_global.py    - hierarquia CUDA e o indice global
echo   [2] primeiro_kernel.py  - fluxo host -> device -> host
echo   [3] fft_benchmark.py    - FFT: CPU (NumPy) vs. GPU (CuPy)
echo   [4] lib_cuda.py         - detectar se ha CUDA disponivel
echo   [0] Sair
echo.
set /p op="Escolha uma opcao: "
echo.

if "%op%"=="1" (
    call ".venv\Scripts\python.exe" "scripts\indice_global.py"
)
if "%op%"=="2" (
    call ".venv\Scripts\python.exe" "scripts\primeiro_kernel.py"
)
if "%op%"=="3" (
    call ".venv\Scripts\python.exe" "scripts\fft_benchmark.py"
)
if "%op%"=="4" (
    call ".venv\Scripts\python.exe" "scripts\lib_cuda.py"
)

if "%op%"=="0" goto fim

echo.
echo ------------------------------------------------------------
pause
goto menu

:fim
echo Ate a proxima!
endlocal
