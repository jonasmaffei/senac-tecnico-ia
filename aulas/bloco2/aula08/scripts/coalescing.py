#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# coalescing.py — Acessos coalescidos vs. não-coalescidos à memória global
# ----------------------------------------------------------------------------
# OBJETIVO: entender por que a FORMA de acessar a VRAM importa tanto.
#
#   Coalescido (bom): threads consecutivas do warp acessam endereços
#     consecutivos -> a GPU junta tudo numa única transação de 128 bytes.
#
#   Não-coalescido (ruim): threads acessam endereços espalhados (stride grande)
#     -> cada acesso vira uma transação separada. Pode ser até ~32x mais lento.
#
# Requer GPU NVIDIA. Sem GPU, mostra o conceito e os tempos de referência.
#
# Uso:  python coalescing.py
# ============================================================================

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import lib_cuda

N = 10_000_000


def testar():
    from numba import cuda
    import numpy as np
    import time

    # ── Kernel coalescido: thread i lê o elemento i (endereços seguidos) ────
    @cuda.jit
    def acesso_coalescido(dados, resultado):
        idx = cuda.grid(1)
        if idx < dados.shape[0]:
            resultado[idx] = dados[idx] * 2.0

    # ── Kernel não-coalescido: thread i lê um endereço distante (stride) ────
    @cuda.jit
    def acesso_strided(dados, resultado, stride):
        idx = cuda.grid(1)
        src = (idx * stride) % dados.shape[0]     # endereço espalhado
        if idx < resultado.shape[0]:
            resultado[idx] = dados[src] * 2.0

    dados = np.random.randn(N).astype(np.float32)
    resultado = np.zeros(N, dtype=np.float32)
    dados_d = cuda.to_device(dados)
    res_d = cuda.to_device(resultado)

    tpb = 256
    bpg = (N + tpb - 1) // tpb

    # Warm-up (compila e aquece)
    acesso_coalescido[bpg, tpb](dados_d, res_d)
    cuda.synchronize()

    inicio = time.perf_counter()
    acesso_coalescido[bpg, tpb](dados_d, res_d)
    cuda.synchronize()
    t_coal = time.perf_counter() - inicio

    inicio = time.perf_counter()
    acesso_strided[bpg, tpb](dados_d, res_d, 32)
    cuda.synchronize()
    t_str = time.perf_counter() - inicio

    print(f"Coalescido      : {t_coal*1000:8.2f} ms")
    print(f"Strided (x32)   : {t_str*1000:8.2f} ms")
    print(f"Overhead        : {t_str/t_coal:.1f}x mais lento!")


def main():
    lib_cuda.cabecalho_ascii()
    print("=" * 64)
    print(" Coalescing: como acessar a VRAM sem desperdiçar transações")
    print("=" * 64)
    lib_cuda.resumo()

    if lib_cuda.tem_cuda():
        testar()
    else:
        lib_cuda.explicar_sem_gpu()
        print()
        print("Regra: threads CONSECUTIVAS devem acessar endereços CONSECUTIVOS.")
        print("Coalescido    -> 1 transação de 128B por warp")
        print("Não-coalescido -> até 32 transações separadas (até ~32x mais lento)")
        print()
        print("Referência (T4, N=10M): coalescido ~0.3 ms vs. strided muito maior.")


if __name__ == "__main__":
    main()
