#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# profiling_ocupacao.py - Medir e entender o perfil de um kernel
# ----------------------------------------------------------------------------
# OBJETIVO: "medir antes de otimizar". Aqui usamos cuda.event para cronometrar
# um kernel com precisao NA GPU (nao no relogio da CPU) e mostramos o que o
# NVIDIA Nsight Systems/Compute revela sobre ocupancia e memoria.
#
#   - cuda.event(record) + event_elapsed_time = tempo real do kernel
#   - Nsight Systems (nsys) -> visao macro (timeline, transferencias)
#   - Nsight Compute (ncu)  -> visao micro (ocupancia, bytes lidos da DRAM)
#
# Requer GPU NVIDIA. Sem GPU, explica as metricas e os comandos.
#
# Uso:  python profiling_ocupacao.py
# ============================================================================

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import lib_cuda

N = 2_000_000


def medir():
    from numba import cuda
    import numpy as np

    @cuda.jit
    def soma_vetores(a, b, c):
        idx = cuda.grid(1)
        if idx < a.shape[0]:
            c[idx] = a[idx] + b[idx]

    a = np.random.randn(N).astype(np.float32)
    b = np.random.randn(N).astype(np.float32)
    c = np.zeros(N, dtype=np.float32)
    a_d = cuda.to_device(a)
    b_d = cuda.to_device(b)
    c_d = cuda.to_device(c)

    # Eventos CUDA: cronometram eventos na propria GPU (mais exato que a CPU).
    inicio = cuda.event()
    fim = cuda.event()

    tpb = 256
    bpg = (N + tpb - 1) // tpb

    soma_vetores[bpg, tpb](a_d, b_d, c_d)   # warm-up
    cuda.synchronize()

    inicio.record()
    soma_vetores[bpg, tpb](a_d, b_d, c_d)
    fim.record()
    fim.synchronize()                        # espera o evento final
    t_ms = cuda.event_elapsed_time(inicio, fim)
    print(f"Kernel (soma de vetores) via cuda.event: {t_ms:.3f} ms")


def main():
    lib_cuda.cabecalho_ascii()
    print("=" * 64)
    print(" Profiling: medindo o kernel com precisao")
    print("=" * 64)
    lib_cuda.resumo()

    if lib_cuda.tem_cuda():
        medir()
    else:
        lib_cuda.explicar_sem_gpu()

    print()
    print("Comandos do Nsight (rodar no terminal, com GPU NVIDIA):")
    print("  nsys profile --stats=true python meu_kernel.py   # visao macro")
    print("  ncu --set full python meu_kernel.py              # visao micro")
    print()
    print("Metricas-chave do Nsight Compute:")
    print("  sm__warps_active  -> ocupancia real do SM")
    print("  l1tex__t_bytes    -> acessos a L1 / memoria compartilhada")
    print("  dram__bytes       -> acessos a DRAM (memoria global)")
    print("  Roofline          -> o kernel e limitado por calculo ou por memoria?")


if __name__ == "__main__":
    main()
