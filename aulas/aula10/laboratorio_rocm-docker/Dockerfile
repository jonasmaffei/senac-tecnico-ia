# Imagem oficial PyTorch + ROCm (AMD).
# Já inclui ROCm, HIP, PyTorch compilado com HIP e as bibliotecas do framework.
# NÃO é necessário instalar PyTorch aqui dentro: a base já traz tudo.
FROM rocm/pytorch:rocm6.2_ubuntu22.04_py3.10_pytorch_release_2.3.0

# Diretório de trabalho dentro do container
WORKDIR /workspace

# Copia o benchmark a partir do contexto de build (a raiz da aula10).
# Veja o docker-compose.yml: o contexto é ".." (pasta aulas/aula10).
# Os scripts ficam em laboratorio_windows/ (compartilhados com o lab local).
COPY laboratorio_windows/1_rocm_pytorch_benchmark.py ./rocm_pytorch_benchmark.py
COPY laboratorio_windows/lib_rocm.py ./lib_rocm.py

# Comando padrão: roda o diagnóstico + benchmark
CMD ["python3", "rocm_pytorch_benchmark.py"]
