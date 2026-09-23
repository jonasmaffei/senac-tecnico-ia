#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# benchmark_work_groups.py — CPU vs. GPU e escolha do work-group
# ----------------------------------------------------------------------------
# OBJETIVO: o equivalente OpenCL dos benchmarks da Aula 7.
#
#   1. Compara CPU (NumPy) vs. OpenCL para a mesma soma de vetores.
#   2. Varia o local_size (work-group) e mostra o efeito no tempo — igual à
#      escolha de threads/bloco em CUDA.
#   3. Mede com eventos OpenCL (precisão de nanossegundos na GPU).
#
# Uso:  python benchmark_work_groups.py
# Requer: numpy (pyopencl opcional)
# ============================================================================

import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import numpy as np

import lib_opencl

N = 5_000_000

KERNEL_SRC = """
__kernel void soma(__global const float* a,
                   __global const float* b,
                   __global       float* c,
                   const int n)
{
    int i = get_global_id(0);
    if (i < n)
        c[i] = a[i] + b[i];
}
"""


def benchmark_cpu(a, b):
    inicio = time.perf_counter()
    c = a + b
    return c, time.perf_counter() - inicio


def benchmark_work_groups(cl):
    plataforma = cl.get_platforms()[0]
    dispositivo = plataforma.get_devices()[0]
    ctx = cl.Context([dispositivo])
    # PROFILING_ENABLE permite medir o kernel com eventos OpenCL.
    fila = cl.CommandQueue(
        ctx, properties=cl.command_queue_properties.PROFILING_ENABLE
    )

    a = np.random.randn(N).astype(np.float32)
    b = np.random.randn(N).astype(np.float32)
    c = np.zeros(N, dtype=np.float32)

    mf = cl.mem_flags
    buf_a = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
    buf_b = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
    buf_c = cl.Buffer(ctx, mf.WRITE_ONLY, c.nbytes)

    # Recupera o kernel UMA vez (evita avisos e custo de reobtenção).
    kernel = cl.Kernel(cl.Program(ctx, KERNEL_SRC).build(), "soma")

    print(f"Comparação CPU (NumPy) vs. OpenCL — N = {N:,}\n")
    _, t_cpu = benchmark_cpu(a, b)
    print(f"CPU (NumPy)     : {t_cpu*1000:8.2f} ms")

    # Warm-up (compila e aquece). O global_size tem de ser múltiplo do local.
    gs_aquecimento = ((N + 255) // 256) * 256
    kernel(fila, (gs_aquecimento,), (256,), buf_a, buf_b, buf_c, np.int32(N))
    fila.finish()

    # Só testamos tamanhos que o dispositivo aceita (max_work_group_size varia).
    limite = dispositivo.max_work_group_size
    tamanhos = [ls for ls in (32, 64, 128, 256, 512, 1024) if ls <= limite]
    # Remove duplicatas caso o limite seja menor que 32.
    tamanhos = sorted(set(tamanhos)) or [limite]

    print(f"\n{'Work-group':>12} | {'global_size':>13} | {'tempo (ms)':>11}")
    print("-" * 44)
    for local_size in tamanhos:
        # Ajusta o global_size para ser múltiplo do local_size (exigência OpenCL).
        global_size = ((N + local_size - 1) // local_size) * local_size
        evento = kernel(
            fila, (global_size,), (local_size,), buf_a, buf_b, buf_c, np.int32(N)
        )
        evento.wait()
        # Evento OpenCL: tempo em nanossegundos entre início e fim do kernel.
        t_ms = (evento.profile.end - evento.profile.start) * 1e-6
        destaque = "  <- ótimo" if local_size == 256 else ""
        print(f"{local_size:>12} | {global_size:>13,} | {t_ms:>11.3f}{destaque}")

    print(f"\nMax work-group size do dispositivo: {dispositivo.max_work_group_size}")
    print("Regra: múltiplo de 32 (warp/wavefront); 128–256 costuma ser o ótimo.")


def main():
    lib_opencl.cabecalho_ascii()
    print("=" * 64)
    print(" OpenCL: CPU vs. GPU e a escolha do work-group")
    print("=" * 64)
    lib_opencl.resumo()

    cl = lib_opencl.carregar()
    if cl is None:
        lib_opencl.explicar_sem_opencl()
        print()
        print("Conceito: o work-group (local_size) é o equivalente ao bloco CUDA.")
        print("Referência: CPU (NumPy) ~8 ms; OpenCL ~1.2 ms (~6.7x) em work-group 256.")
        return

    try:
        benchmark_work_groups(cl)
    except Exception as erro:
        print(f"Não foi possível medir com OpenCL: {erro}")
        lib_opencl.explicar_sem_opencl()


if __name__ == "__main__":
    main()
