@echo off
REM ============================================================================
REM iniciar.bat - menu do laboratorio Windows da Aula 10
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

echo Instalando/atualizando dependencias... (torch pode demorar na primeira vez)
call ".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
call ".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt

:menu
cls
echo ============================================================
echo  Aula 10 - Laboratorio Windows (portabilidade CUDA/ROCm)
echo ============================================================
echo.
echo   [1] 1_rocm_pytorch_benchmark.py     - diagnostico + matmul + treino (portatil)
echo   [2] 2_diagnostico_portabilidade.py  - equivalencia CUDA x ROCm
echo   [0] Sair
echo.
set /p op="Escolha uma opcao: "
echo.

if "%op%"=="1" call ".venv\Scripts\python.exe" "1_rocm_pytorch_benchmark.py"
if "%op%"=="2" call ".venv\Scripts\python.exe" "2_diagnostico_portabilidade.py"

if "%op%"=="0" goto fim

echo.
echo ------------------------------------------------------------
pause
goto menu

:fim
echo Ate a proxima!
endlocal
