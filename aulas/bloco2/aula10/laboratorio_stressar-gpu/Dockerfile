FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# ------------------------------------------------------------
# Ferramentas básicas + Vulkan
# ------------------------------------------------------------
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    gcc \
    g++ \
    git \
    ca-certificates \
    wget \
    curl \
    vulkan-tools \
    libvulkan1 \
    mesa-utils \
    mesa-vulkan-drivers \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Ambiente Python
# ------------------------------------------------------------
RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip

# ------------------------------------------------------------
# Python Vulkan
# ------------------------------------------------------------
RUN pip install --no-cache-dir \
    vulkan \
    numpy

# ------------------------------------------------------------
# WSL GPU
# ------------------------------------------------------------
ENV LD_LIBRARY_PATH="/usr/lib/wsl/lib:/usr/lib/x86_64-linux-gnu"

# Força a GPU dedicada
ENV MESA_D3D12_DEFAULT_ADAPTER_NAME="Radeon RX 550X"

# Força o ICD Dozen
ENV VK_ICD_FILENAMES="/usr/share/vulkan/icd.d/dzn_icd.x86_64.json"

WORKDIR /app

COPY teste_gpu.py /app/teste_gpu.py

CMD ["python3", "/app/teste_gpu.py"]