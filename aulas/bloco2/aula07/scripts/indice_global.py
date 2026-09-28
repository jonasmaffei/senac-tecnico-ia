#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# indice_global.py — A hierarquia CUDA e a fórmula do índice global
# ----------------------------------------------------------------------------
# OBJETIVO: entender como cada thread da GPU descobre QUAL dado processar.
#
#   threadIdx -> posição da thread DENTRO do bloco (0..blockDim-1)
#   blockIdx  -> posição do bloco dentro da grade (0..gridDim-1)
#   blockDim  -> quantos threads tem cada bloco
#   gridDim   -> quantos blocos tem a grade
#
# A fórmula que garante um índice ÚNICO por thread (grade 1D):
#
#   idx = blockIdx.x * blockDim.x + threadIdx.x
#
# Existe o atalho cuda.grid(1) para grade 1D e cuda.grid(2) para grade 2D.
#
# Requer GPU NVIDIA (numba.cuda). Sem GPU, mostra a fórmula e um exemplo em CPU.
#
# Uso:  python indice_global.py
# ============================================================================

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import lib_cuda


def explicar_formula():
    """Mostra, com números, como a fórmula distribui os índices."""
    print("Exemplo de grade 1D: 3 blocos x 4 threads = 12 threads")
    print(f"{'bloco':>5} {'thread':>7} {'idx = bloco*4 + thread':>24}")
    print("-" * 40)
    for bloco in range(3):
        for thread in range(4):
            idx = bloco * 4 + thread
            print(f"{bloco:>5} {thread:>7} {idx:>24}")


def rodar_na_gpu():
    """Executa kernels 1D e 2D de verdade e imprime os índices preenchidos."""
    from numba import cuda
    import numpy as np

    # ── Kernel 1D: cada thread escreve seu próprio índice global ───────────
    @cuda.jit
    def kernel_1d(arr):
        idx = cuda.grid(1)                 # equivale a blockIdx*blockDim+threadIdx
        if idx < arr.shape[0]:
            arr[idx] = idx

    N = 32
    arr = np.zeros(N, dtype=np.int32)
    arr_d = cuda.to_device(arr)
    kernel_1d[1, N](arr_d)                 # 1 bloco, 32 threads
    cuda.synchronize()
    print("\nÍndices 1D preenchidos pela GPU:")
    print(" ", arr_d.copy_to_host().tolist())

    # ── Kernel 2D: ideal para imagens (linha/coluna) ───────────────────────
    @cuda.jit
    def kernel_2d(matriz):
        col, row = cuda.grid(2)            # x = coluna, y = linha
        if col < matriz.shape[1] and row < matriz.shape[0]:
            matriz[row, col] = row * 1000 + col

    H, W = 4, 8
    mat = np.zeros((H, W), dtype=np.int32)
    mat_d = cuda.to_device(mat)
    kernel_2d[(1, 1), (W, H)](mat_d)
    cuda.synchronize()
    print("\nÍndices 2D (row*1000 + col) preenchidos pela GPU:")
    print(mat_d.copy_to_host())


def main():
    lib_cuda.cabecalho_ascii()
    print("=" * 64)
    print(" Hierarquia CUDA: threadIdx, blockIdx, blockDim, gridDim")
    print("=" * 64)
    explicar_formula()

    lib_cuda.resumo()
    if lib_cuda.tem_cuda():
        rodar_na_gpu()
    else:
        print()
        print("Sem GPU: o resultado do kernel 1D seria exatamente os índices")
        print("mostrados na tabela acima (0, 1, 2, ..., 11).")
        print("O kernel 2D preencheria a matriz com row*1000 + col.")


if __name__ == "__main__":
    main()
