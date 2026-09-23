#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# matmul_global.py — Multiplicação de matrizes com MEMÓRIA GLOBAL (ingênua)
# ----------------------------------------------------------------------------
# OBJETIVO: medir a versão "ingênua" de C = A x B, em que cada thread lê
# diretamente da memória global (VRAM) a cada iteração do laço.
#
# Isso gera ~500 ciclos de latência POR acesso -> é o kernel lento que o
# engenheiro sênior viu no Nsight (na versão da Aula 07). A versão otimizada
# (com tiling em memória compartilhada) está em matmul_tiling.py.
#
# Requer GPU NVIDIA. Sem GPU, mostra o conceito e o tempo de referência.
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
        """C = A x B usando apenas memória global (um acesso por multiplicação)."""
        row, col = cuda.grid(2)
        M, K = A.shape
        _, N = B.shape
        if row < M and col < N:
            soma = 0.0
            for k in range(K):
                # Cada iteração lê da VRAM (alta latência!) — o gargalo.
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
    print(f"Memória Global (ingênua): {t*1000:8.2f} ms")
    print(f"Erro vs. NumPy          : {erro:.6f}")


def main():
    lib_cuda.cabecalho_ascii()
    print("=" * 64)
    print(f" Matmul ingênua (memória global) — N = {N}")
    print("=" * 64)
    lib_cuda.resumo()

    if lib_cuda.tem_cuda():
        testar()
    else:
        lib_cuda.explicar_sem_gpu()
        print()
        print("Cada thread lê A[row,k] e B[k,col] DIRETO da VRAM (~500 ciclos).")
        print("Como isso se repete K vezes, a memória vira o gargalo.")
        print("Referência (T4, N=512): ~120 ms. A versão com tiling: ~18 ms.")


if __name__ == "__main__":
    main()
