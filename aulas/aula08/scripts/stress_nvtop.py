#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# stress_nvtop.py — Teste de estresse da GPU (para observar no nvtop)
# ----------------------------------------------------------------------------
# OBJETIVO: gerar carga contínua na GPU para ver, em tempo real, a utilização,
# a VRAM, a temperatura e a potência no `nvtop` (Linux) ou no Gerenciador de
# Tarefas (Windows). É a ponte entre esta aula e o monitoramento da Aula 14.
#
# Rode em um terminal e observe o nvtop em outro.
#
# Requer GPU (CuPy no Colab; senão usa NumPy na CPU como demonstração).
#
# Uso:  python stress_nvtop.py            # roda continuamente (Ctrl+C para sair)
#       python stress_nvtop.py 10         # roda por 10 segundos
# ============================================================================

import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

TAMANHO = 8192


def estressar_gpu(segundos):
    import cupy as cp

    print("Iniciando estresse da GPU (observe no nvtop)...")
    A = cp.random.randn(TAMANHO, TAMANHO, dtype=cp.float32)
    B = cp.random.randn(TAMANHO, TAMANHO, dtype=cp.float32)

    inicio = time.perf_counter()
    iteracoes = 0
    try:
        while segundos is None or (time.perf_counter() - inicio) < segundos:
            _ = cp.matmul(A, B)                # multiplica matrizes grandes
            cp.cuda.Stream.null.synchronize()  # força a GPU a terminar
            iteracoes += 1
            if iteracoes % 5 == 0:
                print(f"  {iteracoes} multiplicações...")
    except KeyboardInterrupt:
        print("\nEstresse interrompido pelo usuário.")
    print(f"Encerrado após {iteracoes} multiplicações.")


def estressar_cpu(segundos):
    import numpy as np

    print("CuPy não disponível — estressando a CPU (demonstração).")
    A = np.random.randn(1024, 1024).astype(np.float32)
    B = np.random.randn(1024, 1024).astype(np.float32)
    inicio = time.perf_counter()
    iteracoes = 0
    try:
        while segundos is None or (time.perf_counter() - inicio) < segundos:
            _ = A @ B
            iteracoes += 1
    except KeyboardInterrupt:
        print("\nInterrompido.")
    print(f"Encerrado após {iteracoes} multiplicações (CPU).")
    print("No Colab com GPU, este mesmo script usa o CuPy e estressa a VRAM.")


def main():
    segundos = None
    if len(sys.argv) > 1:
        try:
            segundos = float(sys.argv[1])
        except ValueError:
            segundos = None

    try:
        import cupy  # noqa: F401
        estressar_gpu(segundos)
    except ImportError:
        estressar_cpu(segundos)


if __name__ == "__main__":
    main()
