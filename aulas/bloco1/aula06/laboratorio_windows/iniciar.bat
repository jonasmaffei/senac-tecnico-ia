@echo off
REM ============================================================================
REM iniciar.bat - menu do laboratorio Windows da Aula 06
REM ----------------------------------------------------------------------------
REM Uso: duplo clique neste arquivo, OU no Prompt:  iniciar.bat
REM
REM Este laboratorio usa o hardware REAL do laboratorio via Git Bash (.sh).
REM O menu apenas chama o 'bash' com o script escolhido e mantem a janela aberta.
REM ============================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

where bash >nul 2>nul
if errorlevel 1 (
    echo.
    echo [ERRO] Git Bash nao encontrado no PATH.
    echo Instale o "Git for Windows" ^(que inclui o Git Bash^) e reabra.
    echo.
    pause
    exit /b 1
)

:menu
cls
echo ============================================================
echo  Aula 06 - Laboratorio Windows: Linux e GPU (hardware real)
echo ============================================================
echo.
echo   [1] 1_inspecionar.sh  - conhecer o hardware e a GPU
echo   [2] 2_status_gpu.sh   - status + alerta de temperatura
echo   [3] 3_agendar.sh      - agendamento (simula o cron)
echo   [4] monitoramento_linux.py - CPU/RAM/GPU via Python
echo   [0] Sair
echo.
set /p op="Escolha uma opcao: "
echo.

if "%op%"=="1" call bash "1_inspecionar.sh"
if "%op%"=="2" call bash "2_status_gpu.sh"
if "%op%"=="3" call bash "3_agendar.sh"
if "%op%"=="4" (
    call python "monitoramento_linux.py"
)

if "%op%"=="0" goto fim

echo.
echo ------------------------------------------------------------
pause
goto menu

:fim
echo Ate a proxima!
endlocal
