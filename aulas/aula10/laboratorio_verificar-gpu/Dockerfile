FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-numpy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY teste_gpu.py .

CMD ["python3", "teste_gpu.py"]