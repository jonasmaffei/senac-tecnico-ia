@echo off
REM ============================================================================
REM iniciar.bat - atalho para rodar o monitoramento no Windows
REM ----------------------------------------------------------------------------
REM Uso: dê um duplo clique neste arquivo, OU no Prompt de Comando:
REM     iniciar.bat
REM
REM Ele instala as dependências (se necessário), sobe o servidor e abre o
REM navegador em http://localhost:5000. Feche a janela para parar.
REM ============================================================================

setlocal

REM Vai para a pasta deste arquivo (a raiz do projeto)
cd /d "%~dp0"

echo ============================================================
echo  Monitoramento em tempo real - Aula 14 (Windows)
echo ============================================================
echo.

REM Verifica se o Python esta instalado
where python >nul 2>nul
if errorlevel 1 (
    echo [ERRO] Python nao encontrado no PATH.
    echo Instale em https://www.python.org/downloads/ e marque
    echo "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
)

REM Cria o ambiente virtual na primeira execucao
if not exist ".venv" (
    echo Criando ambiente virtual ^(.venv^)...
    python -m venv .venv
)

REM Instala as dependencias dentro do ambiente virtual
echo Instalando dependencias...
call ".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
call ".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt

REM Abre o navegador depois de um pequeno atraso (o servidor leva ~2s para subir)
start "" cmd /c "timeout /t 3 >nul & start http://localhost:5000"

REM Roda o servidor (mantem a janela aberta enquanto o monitoramento estiver ativo)
echo.
echo Abrindo http://localhost:5000 ...
call ".venv\Scripts\python.exe" "app\servidor.py"

endlocal
