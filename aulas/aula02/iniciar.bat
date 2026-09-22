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
echo  Aula 02 - Modelos de Processamento (SIMD, MIMD, RISC, CISC)
echo ============================================================
echo.
echo   [1] benchmark_simd.py        - sequencial vs. SIMD (NumPy/GPU)
echo   [2] estudo_imagem.py         - imagem 1080p: loop vs. vetorizado
echo   [3] arquitetura_instrucoes.py- RISC/CISC + recursos SIMD da CPU
echo   [4] lib_backend.py           - detectar o backend de processamento

echo   [0] Sair
echo.
set /p op="Escolha uma opcao: "
echo.

if "%op%"=="1" (
    call ".venv\Scripts\python.exe" "scripts\benchmark_simd.py"
)
if "%op%"=="2" (
    call ".venv\Scripts\python.exe" "scripts\estudo_imagem.py"
)
if "%op%"=="3" (
    call ".venv\Scripts\python.exe" "scripts\arquitetura_instrucoes.py"
)
if "%op%"=="4" (
    call ".venv\Scripts\python.exe" "scripts\lib_backend.py"
)

if "%op%"=="0" goto fim

echo.
echo ------------------------------------------------------------
pause
goto menu

:fim
echo Ate a proxima!
endlocal
