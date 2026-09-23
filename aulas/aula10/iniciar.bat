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

echo Instalando/atualizando dependencias... (torch pode demorar na primeira vez)
call ".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
call ".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt

:menu
cls
echo ============================================================
echo  Aula 10 - Introducao ao ROCm e GPUs AMD
echo ============================================================
echo.
echo   [1] rocm_pytorch_benchmark.py     - diagnostico + matmul + treino (portatil)
echo   [2] diagnostico_portabilidade.py  - equivalencia CUDA x ROCm
echo   [3] lib_rocm.py                   - detectar o backend (CUDA/ROCm/CPU)
echo   [0] Sair
echo.
set /p op="Escolha uma opcao: "
echo.

if "%op%"=="1" (
    call ".venv\Scripts\python.exe" "scripts\rocm_pytorch_benchmark.py"
)
if "%op%"=="2" (
    call ".venv\Scripts\python.exe" "scripts\diagnostico_portabilidade.py"
)
if "%op%"=="3" (
    call ".venv\Scripts\python.exe" "scripts\lib_rocm.py"
)

if "%op%"=="0" goto fim

echo.
echo ------------------------------------------------------------
pause
goto menu

:fim
echo Ate a proxima!
endlocal
