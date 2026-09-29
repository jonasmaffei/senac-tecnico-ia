#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# matmul_global.py - Multiplicacao de matrizes com MEMORIA GLOBAL (ingenua)
# ----------------------------------------------------------------------------
# OBJETIVO: medir a versao "ingenua" de C = A x B, em que cada thread le
# diretamente da memoria global (VRAM) a cada iteracao do laco.
#
# Isso gera ~500 ciclos de latencia POR acesso -> e o kernel lento que o
# engenheiro senior viu no Nsight (na versao da Aula 07). A versao otimizada
# (com tiling em memoria compartilhada) esta em matmul_tiling.py.
#
# Requer GPU NVIDIA. Sem GPU, mostra o conceito e o tempo de referencia.
#
# Uso:  python matmul_global.py
# ============================================================================

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import lib_cuda

N = 512   # matriz N x N


def testar():
    from numba import cuda
    import numpy as np
    import time

    @cuda.jit
    def matmul_global(A, B, C):
        """C = A x B usando apenas memoria global (um acesso por multiplicacao)."""
        row, col = cuda.grid(2)
        M, K = A.shape
        _, N = B.shape
        if row < M and col < N:
            soma = 0.0
            for k in range(K):
                # Cada iteracao le da VRAM (alta latencia!) - o gargalo.
                soma += A[row, k] * B[k, col]
            C[row, col] = soma

    A = np.random.randn(N, N).astype(np.float32)
    B = np.random.randn(N, N).astype(np.float32)
    C = np.zeros((N, N), dtype=np.float32)

    A_d = cuda.to_device(A)
    B_d = cuda.to_device(B)
    C_d = cuda.to_device(C)

    tpb = 16                     # bloco 16x16 = 256 threads
    bpg = (N + tpb - 1) // tpb

    matmul_global[(bpg, bpg), (tpb, tpb)](A_d, B_d, C_d)   # warm-up
    cuda.synchronize()

    inicio = time.perf_counter()
    matmul_global[(bpg, bpg), (tpb, tpb)](A_d, B_d, C_d)
    cuda.synchronize()
    t = time.perf_counter() - inicio

    erro = np.max(np.abs(C_d.copy_to_host() - A @ B))
    print(f"Memoria Global (ingenua): {t*1000:8.2f} ms")
    print(f"Erro vs. NumPy          : {erro:.6f}")


def main():
    lib_cuda.cabecalho_ascii()
    print("=" * 64)
    print(f" Matmul ingenua (memoria global) - N = {N}")
    print("=" * 64)
    lib_cuda.resumo()

    if lib_cuda.tem_cuda():
        testar()
    else:
        lib_cuda.explicar_sem_gpu()
        print()
        print("Cada thread le A[row,k] e B[k,col] DIRETO da VRAM (~500 ciclos).")
        print("Como isso se repete K vezes, a memoria vira o gargalo.")
        print("Referencia (T4, N=512): ~120 ms. A versao com tiling: ~18 ms.")


if __name__ == "__main__":
    main()
