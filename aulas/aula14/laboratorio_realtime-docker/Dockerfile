# ============================================================================
# Dockerfile — imagem do webservice de monitoramento em tempo real (Aula 14)
# ----------------------------------------------------------------------------
# Imagem leve baseada em Python 3.11 (slim) que instala apenas Flask e psutil.
# Build:
#   docker build -t monitor-realtime .
# Ou, preferencialmente, com o docker compose (veja o README).
# ============================================================================

FROM python:3.11-slim

# Evita que o Python grave arquivos .pyc e melhora os logs no container.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copia só o requirements primeiro: assim o Docker reaproveita o cache da
# instalação das dependências quando apenas o código muda.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação.
COPY app/ ./app/

# A pasta de relatórios é montada como volume pelo docker-compose.
RUN mkdir -p /app/reports

# A aplicação roda na porta 5000.
EXPOSE 5000

# Comando padrão do container.
CMD ["python", "app/servidor.py"]
