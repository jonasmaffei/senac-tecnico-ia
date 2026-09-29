@echo off
chcp 65001 > NUL
title Aula 19 - Otimizacao de Energia em GPUs (Windows Host)

echo ============================================================
echo     Aula 19 - Energia, Termica e Power Limit de GPU
echo ============================================================
echo.

if not exist ".venv" (
    echo [1/2] Criando ambiente virtual Python ^(.venv^)...
    python -m venv .venv
)

echo [2/2] Ativando ambiente virtual e instalando dependencias...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip > NUL
pip install -r requirements.txt

:MENU
cls
echo ============================================================
echo   MENU - Otimizacao de Energia em GPUs (Aula 19)
echo ============================================================
echo   1. Monitorar Temperatura e Potencia (1_monitor_thermal.py)
echo   2. Verificar Alertas Termicos (2_alerta_termico.py)
echo   3. Benchmark de Eficiencia por Power Limit (3_benchmark_energia.py)
echo   4. Controle do Power Limit (4_controle_pl.py)
echo   5. Sair
echo ============================================================
set /p OPCAO="Escolha uma opcao (1-5): "

if "%OPCAO%"=="1" (
    cls
    echo Coletando 6 amostras a cada 2 segundos...
    python 1_monitor_thermal.py 2 6
    pause
    goto MENU
)

if "%OPCAO%"=="2" (
    cls
    echo Verificando alertas termicos...
    python 2_alerta_termico.py 80 88
    pause
    goto MENU
)

if "%OPCAO%"=="3" (
    cls
    echo Gerando benchmark de eficiencia...
    python 3_benchmark_energia.py
    pause
    goto MENU
)

if "%OPCAO%"=="4" (
    cls
    echo Aplicando Power Limit de 180W ^(se suportado^)...
    python 4_controle_pl.py 180
    pause
    goto MENU
)

if "%OPCAO%"=="5" (
    echo Encerrando laboratorio. Operacao energetica concluida!
    exit /b 0
)

echo Opcao invalida! Tente novamente.
pause
goto MENU
