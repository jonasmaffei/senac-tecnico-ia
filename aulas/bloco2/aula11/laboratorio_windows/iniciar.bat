@echo off
REM ============================================================================
REM iniciar.bat - menu do laboratorio Windows da Aula 11
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
echo  Aula 11 - Laboratorio Windows (aplicacao de modelos)
echo ============================================================
echo.
echo   [1] 1_benchmark_treino.py       - FP32 vs. FP16 (throughput)
echo   [2] 2_comparar_ecossistemas.py  - NVIDIA x AMD + custo (TCO)
echo   [0] Sair
echo.
set /p op="Escolha uma opcao: "
echo.

if "%op%"=="1" call ".venv\Scripts\python.exe" "1_benchmark_treino.py"
if "%op%"=="2" call ".venv\Scripts\python.exe" "2_comparar_ecossistemas.py"

if "%op%"=="0" goto fim

echo.
echo ------------------------------------------------------------
pause
goto menu

:fim
echo Ate a proxima!
endlocal
