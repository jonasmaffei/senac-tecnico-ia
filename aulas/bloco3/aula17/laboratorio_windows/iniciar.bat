@echo off
title Aula 17 - Laboratorio de Automacao de GPU

if exist ".venv" goto :INICIAR_ENV

echo [1/2] Criando ambiente virtual Python (.venv)...
python -m venv .venv

:INICIAR_ENV
echo [2/2] Ativando ambiente virtual e instalando dependencias...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip > NUL
pip install -r requirements.txt

:MENU
cls
echo ============================================================
echo    MENU - Laboratorio de Automacao de GPU (Aula 17)
echo ============================================================
echo    1. Coletar Metricas de Hardware (1_monitor_gpu.py)
echo    2. Verificar Alertas de Limites (2_alerta_gpu.py)
echo    3. Gerar Dashboard de Graficos (3_gerar_graficos.py)
echo    4. Enviar Telemetria para Google Sheets (4_enviar_sheets.py)
echo    5. Sair
echo ============================================================
set /p OPCAO="Escolha uma opcao (1-5): "

if "%OPCAO%"=="1" goto OP1
if "%OPCAO%"=="2" goto OP2
if "%OPCAO%"=="3" goto OP3
if "%OPCAO%"=="4" goto OP4
if "%OPCAO%"=="5" goto OP5

echo Opcao invalida! Tente novamente.
pause
goto MENU

:OP1
cls
echo Executando Coleta de Metricas...
python 1_monitor_gpu.py 3 30
pause
goto MENU

:OP2
cls
echo Verificando Alertas...
python 2_alerta_gpu.py 75 90
pause
goto MENU

:OP3
cls
echo Gerando Dashboard PNG...
python 3_gerar_graficos.py
pause
goto MENU

:OP4
cls
echo Enviando para Google Sheets API...
python 4_enviar_sheets.py
pause
goto MENU

:OP5
echo Encerrando laboratorio. Atos de automacao concluidos!
exit /b 0