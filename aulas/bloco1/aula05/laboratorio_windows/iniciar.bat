@echo off
REM ============================================================================
REM iniciar.bat - menu do laboratorio Windows da Aula 05
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
echo  Aula 05 - Laboratorio Windows (rede real)
echo ============================================================
echo.
echo   [1] 1_demo_tcp_udp.py    - TCP vs. UDP (confiabilidade x velocidade)
echo   [2] 2_telemetria_tcp.py  - servidor TCP que recebe metricas de GPU
echo   [3] 3_ipv4_ipv6.py       - IPv4 vs. IPv6 na pratica
echo   [4] comandos_rede.sh     - referencia de comandos (Git Bash)
echo   [0] Sair
echo.
set /p op="Escolha uma opcao: "
echo.

if "%op%"=="1" call ".venv\Scripts\python.exe" "1_demo_tcp_udp.py"
if "%op%"=="2" call ".venv\Scripts\python.exe" "2_telemetria_tcp.py"
if "%op%"=="3" call ".venv\Scripts\python.exe" "3_ipv4_ipv6.py"
if "%op%"=="4" (
    where bash >nul 2>nul
    if errorlevel 1 (
        echo Git Bash nao encontrado. Instale o Git for Windows.
    ) else (
        call bash "comandos_rede.sh"
    )
)

if "%op%"=="0" goto fim

echo.
echo ------------------------------------------------------------
pause
goto menu

:fim
echo Ate a proxima!
endlocal
