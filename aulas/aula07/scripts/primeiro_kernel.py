#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# primeiro_kernel.py — Fluxo completo de um programa CUDA
# ----------------------------------------------------------------------------
# OBJETIVO: ver as 5 etapas de qualquer programa CUDA, do host ao device:
#
#   1. CPU aloca arrays na VRAM       <- cuda.to_device()
#   2. CPU lança o kernel             <- kernel[blocos, threads](...)
#   3. GPU executa N threads em paralelo
#   4. CPU aguarda a sincronização    <- cuda.synchronize()
#   5. CPU copia o resultado de volta <- copy_to_host()
#
# Fazemos duas operações simples e muito usadas em pré-processamento de áudio:
#   - somar dois vetores (kernel elementwise);
#   - escalar e calcular média móvel de um sinal.
#
# Requer GPU NVIDIA (numba.cuda). Sem GPU, mostra o resultado esperado.
#
# Uso:  python primeiro_kernel.py
# ============================================================================

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import lib_cuda


def soma_vetores():
    """Soma elemento a elemento: c[i] = a[i] + b[i]."""
    from numba import cuda
    import numpy as np

    @cuda.jit
    def soma_vetores_gpu(a, b, c):
        idx = cuda.grid(1)                 # índice global desta thread
        if idx < c.shape[0]:               # proteção contra o fim do vetor
            c[idx] = a[idx] + b[idx]

    N = 10_000_000
    a = np.ones(N, dtype=np.float32)
    b = np.ones(N, dtype=np.float32) * 2
    c = np.zeros(N, dtype=np.float32)

    a_d = cuda.to_device(a)                # 1. RAM -> VRAM
    b_d = cuda.to_device(b)
    c_d = cuda.to_device(c)

    threads_por_bloco = 256
    blocos_por_grade = (N + threads_por_bloco - 1) // threads_por_bloco

    print(f"N = {N:,} elementos")
    print(f"Threads por bloco : {threads_por_bloco}")
    print(f"Blocos na grade   : {blocos_por_grade:,}")
    print(f"Threads totais    : {threads_por_bloco * blocos_por_grade:,}")

    soma_vetores_gpu[blocos_por_grade, threads_por_bloco](a_d, b_d, c_d)  # 2 e 3
    cuda.synchronize()                     # 4

    resultado = c_d.copy_to_host()         # 5
    print(f"\nResultado[0..4] = {resultado[:5]}")
    print("Esperado: [3. 3. 3. 3. 3.]")


def escalar_e_media():
    """Escala um sinal e calcula uma média móvel (cada thread, uma janela)."""
    from numba import cuda
    import numpy as np

    @cuda.jit
    def escalar_sinal(sinal, fator, resultado):
        idx = cuda.grid(1)
        if idx < sinal.shape[0]:
            resultado[idx] = sinal[idx] * fator

    @cuda.jit
    def media_movel_gpu(sinal, janela, resultado):
        # Cada thread calcula a média de uma janela que começa no seu índice.
        idx = cuda.grid(1)
        inicio = idx
        fim = min(idx + janela, sinal.shape[0])
        if inicio < sinal.shape[0]:
            soma = 0.0
            for i in range(inicio, fim):
                soma += sinal[i]
            resultado[idx] = soma / (fim - inicio)

    N = 1_000_000
    sinal = np.sin(np.linspace(0, 100, N)).astype(np.float32)
    sinal_d = cuda.to_device(sinal)
    escalado_d = cuda.device_array(N, dtype=np.float32)   # aloca só na VRAM
    media_d = cuda.device_array(N, dtype=np.float32)

    tpb = 256
    bpg = (N + tpb - 1) // tpb
    escalar_sinal[bpg, tpb](sinal_d, 2.5, escalado_d)
    media_movel_gpu[bpg, tpb](sinal_d, 10, media_d)
    cuda.synchronize()

    print(f"\nOriginal  [0] = {sinal[0]:.4f}")
    print(f"Escalado  [0] = {escalado_d.copy_to_host()[0]:.4f} (x2.5)")
    print(f"Média móv [0] = {media_d.copy_to_host()[0]:.4f}")


def main():
    lib_cuda.cabecalho_ascii()
    print("=" * 64)
    print(" Primeiro kernel CUDA: fluxo host -> device -> host")
    print("=" * 64)
    lib_cuda.resumo()

    if lib_cuda.tem_cuda():
        print("\n--- 1) Soma de vetores ---")
        soma_vetores()
        print("\n--- 2) Escala e média móvel ---")
        escalar_e_media()
    else:
        lib_cuda.explicar_sem_gpu()
        print()
        print("Resultado esperado da soma: [3. 3. 3. 3. 3.]")
        print("O kernel de soma com N=10M usa 39.063 blocos de 256 threads.")


if __name__ == "__main__":
    main()
