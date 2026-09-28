@echo off
chcp 65001 > NUL
title Aula 17 — Laboratório de Automação de GPU (Windows Host)

echo ============================================================
echo   🤖 Aula 17 — Automação e Telemetria de GPU (Windows Host)
echo ============================================================
echo.

if not exist ".venv" (
    echo [1/2] Criando ambiente virtual Python (.venv)...
    python -m venv .venv
)

echo [2/2] Ativando ambiente virtual e instalando dependências...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip > NUL
pip install -r requirements.txt

:MENU
cls
echo ============================================================
echo   📊 MENU - Laboratório de Automação de GPU (Aula 17)
echo ============================================================
echo   1. Coletar Métricas de Hardware (1_monitor_gpu.py)
echo   2. Verificar Alertas de Limites (2_alerta_gpu.py)
echo   3. Gerar Dashboard de Gráficos (3_gerar_graficos.py)
echo   4. Enviar Telemetria para Google Sheets (4_enviar_sheets.py)
echo   5. Sair
echo ============================================================
set /p OPCAO="Escolha uma opção (1-5): "

if "%OPCAO%"=="1" (
    cls
    echo Executando Coleta de Métricas...
    python 1_monitor_gpu.py 3 30
    pause
    goto MENU
)

if "%OPCAO%"=="2" (
    cls
    echo Verificando Alertas...
    python 2_alerta_gpu.py 75 90
    pause
    goto MENU
)

if "%OPCAO%"=="3" (
    cls
    echo Gerando Dashboard PNG...
    python 3_gerar_graficos.py
    pause
    goto MENU
)

if "%OPCAO%"=="4" (
    cls
    echo Enviando para Google Sheets API...
    python 4_enviar_sheets.py
    pause
    goto MENU
)

if "%OPCAO%"=="5" (
    echo Encerrando laboratório. Atos de automação concluídos!
    exit /b 0
)

echo Opção inválida! Tente novamente.
pause
goto MENU
