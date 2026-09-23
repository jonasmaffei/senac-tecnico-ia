#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# matmul_tiling.py — Multiplicação de matrizes com MEMÓRIA COMPARTILHADA
# ----------------------------------------------------------------------------
# OBJETIVO: a solução para o gargalo da memória global. Em vez de cada thread
# ler da VRAM a cada conta, o BLOCO inteiro carrega um "tile" (pedaço) de A e
# de B para a memória compartilhada (SRAM, ~5 ciclos) e reutiliza os dados
# entre os threads. Isso reduz os acessos à VRAM por um fator ~TILE.
#
# Compara também com o CuBLAS (via CuPy), a biblioteca otimizada da NVIDIA.
#
# Requer GPU NVIDIA. Sem GPU, mostra o conceito e os tempos de referência.
#
# Uso:  python matmul_tiling.py
# ============================================================================

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import lib_cuda

N = 512
TILE = 16   # deve casar com o tamanho do bloco (16x16 = 256 threads)


def tiling():
    from numba import cuda, float32
    import numpy as np
    import time

    @cuda.jit
    def matmul_shared(A, B, C):
        # Tiles na memória compartilhada do bloco (SRAM rápida).
        tile_A = cuda.shared.array((TILE, TILE), dtype=float32)
        tile_B = cuda.shared.array((TILE, TILE), dtype=float32)

        row, col = cuda.grid(2)
        tx, ty = cuda.threadIdx.x, cuda.threadIdx.y
        M, K = A.shape
        _, N = B.shape

        soma = float32(0.0)
        # Percorre os tiles ao longo da dimensão K
        for t in range((K + TILE - 1) // TILE):
            kr = t * TILE + ty
            kc = t * TILE + tx
            # Cada thread carrega UM elemento para cada tile (com borda segura)
            tile_A[ty, tx] = A[row, kr] if (row < M and kr < K) else 0.0
            tile_B[ty, tx] = B[kc, col] if (kc < K and col < N) else 0.0

            cuda.syncthreads()          # todos carregaram antes de calcular

            for k in range(TILE):       # multiplica já na SRAM (rápido!)
                soma += tile_A[ty, k] * tile_B[k, tx]

            cuda.syncthreads()          # antes de recarregar os tiles

        if row < M and col < N:
            C[row, col] = soma

    A = np.random.randn(N, N).astype(np.float32)
    B = np.random.randn(N, N).astype(np.float32)
    C = np.zeros((N, N), dtype=np.float32)

    A_d = cuda.to_device(A)
    B_d = cuda.to_device(B)
    C_d = cuda.to_device(C)
    bpg = (N + TILE - 1) // TILE

    matmul_shared[(bpg, bpg), (TILE, TILE)](A_d, B_d, C_d)   # warm-up
    cuda.synchronize()

    inicio = time.perf_counter()
    matmul_shared[(bpg, bpg), (TILE, TILE)](A_d, B_d, C_d)
    cuda.synchronize()
    t = time.perf_counter() - inicio

    erro = np.max(np.abs(C_d.copy_to_host() - A @ B))
    print(f"Memória Compartilhada (tiling): {t*1000:8.2f} ms")
    print(f"Erro vs. NumPy                : {erro:.5f}")


def cublas():
    """Comparação com o cuBLAS (biblioteca otimizada via CuPy), se disponível."""
    try:
        import cupy as cp
    except ImportError:
        print("\nCuPy não instalado — não foi possível comparar com o cuBLAS.")
        return

    n = 1024
    A = cp.random.randn(n, n, dtype=cp.float32)
    B = cp.random.randn(n, n, dtype=cp.float32)
    _ = cp.matmul(A, B)                      # warm-up
    cp.cuda.Stream.null.synchronize()

    t0 = __import__("time").perf_counter()
    for _ in range(10):
        C = cp.matmul(A, B)                  # usa cuBLAS por baixo
    cp.cuda.Stream.null.synchronize()
    t_cublas = (__import__("time").perf_counter() - t0) / 10

    A_cpu = cp.asnumpy(A)
    B_cpu = cp.asnumpy(B)
    t0 = __import__("time").perf_counter()
    _ = A_cpu @ B_cpu
    t_cpu = __import__("time").perf_counter() - t0

    print(f"\nComparação (N={n}):")
    print(f"  CPU  (NumPy)       : {t_cpu*1000:8.1f} ms")
    print(f"  GPU  (cuBLAS/CuPy) : {t_cublas*1000:8.2f} ms  ({t_cpu/t_cublas:.1f}x)")


def main():
    lib_cuda.cabecalho_ascii()
    print("=" * 64)
    print(f" Matmul com tiling (memória compartilhada) — N = {N}, TILE = {TILE}")
    print("=" * 64)
    lib_cuda.resumo()

    if lib_cuda.tem_cuda():
        tiling()
        cublas()
    else:
        lib_cuda.explicar_sem_gpu()
        print()
        print("Tiling: carrega um tile TILE x TILE de A e B na SRAM do bloco e")
        print("reutiliza os dados -> cada elemento é lido ~TILE vezes menos da VRAM.")
        print("Precisa de DOIS cuda.syncthreads() (barreira antes/depois do uso).")
        print()
        print("Referência (T4, N=512): global ~120 ms -> tiling ~18 ms (~6.7x).")


if __name__ == "__main__":
    main()
