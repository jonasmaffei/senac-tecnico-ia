#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# primeiro_kernel.py — Primeiro kernel OpenCL (soma de vetores)
# ----------------------------------------------------------------------------
# OBJETIVO: escrever e executar um kernel OpenCL completo com PyOpenCL.
#
# O kernel é escrito em OpenCL C (uma STRING) e compilado EM TEMPO DE EXECUÇÃO
# (JIT) para o dispositivo alvo. É isso que garante a portabilidade: o mesmo
# código-fonte roda em NVIDIA, AMD, Intel ou CPU.
#
# Comparação com o CUDA (Aula 7):
#   get_global_id(0)  <->  cuda.grid(1)
#   __global float*   <->  arrays no device
#   cl.Buffer(...)    <->  cuda.to_device()
#   fila.finish()     <->  cuda.synchronize()
#
# Uso:  python primeiro_kernel.py
# Requer: pyopencl (opcional — sem ele, explica o conceito)
# ============================================================================

import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import numpy as np

import lib_opencl

# ── Código-fonte do kernel (OpenCL C, baseado em C99) ───────────────────────
# A proteção `if (idx < N)` é importante: arredondamos o global_size para
# múltiplo do work-group, então podem sobrar work-items além do fim do vetor.
KERNEL_SRC = """
__kernel void soma_vetores(
    __global const float* a,
    __global const float* b,
    __global       float* c,
    const int n)
{
    // get_global_id(0) equivale ao cuda.grid(1) do CUDA
    int idx = get_global_id(0);
    if (idx < n)
        c[idx] = a[idx] + b[idx];
}
"""

N = 10_000_000
LOCAL_SIZE = 256


def rodar(cl):
    # ── 1. Escolher plataforma e dispositivo ───────────────────────────────
    plataforma = cl.get_platforms()[0]
    dispositivo = plataforma.get_devices()[0]

    ctx = cl.Context([dispositivo])       # contexto agrupa dispositivos/buffers
    fila = cl.CommandQueue(ctx)           # fila envia comandos ao dispositivo

    print(f"Rodando em: {dispositivo.name}")

    # ── 2. Compilar o kernel (JIT) ─────────────────────────────────────────
    programa = cl.Program(ctx, KERNEL_SRC).build()

    # ── 3. Dados de entrada na CPU ─────────────────────────────────────────
    a = np.ones(N, dtype=np.float32)
    b = np.ones(N, dtype=np.float32) * 2
    c = np.zeros(N, dtype=np.float32)

    # ── 4. Alocar buffers na memória do dispositivo ────────────────────────
    mf = cl.mem_flags
    buf_a = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
    buf_b = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
    buf_c = cl.Buffer(ctx, mf.WRITE_ONLY, c.nbytes)

    # ── 5. Executar o kernel ───────────────────────────────────────────────
    # O global_size deve ser múltiplo do local_size (exigência do OpenCL).
    global_size = ((N + LOCAL_SIZE - 1) // LOCAL_SIZE) * LOCAL_SIZE
    inicio = time.perf_counter()
    programa.soma_vetores(
        fila, (global_size,), (LOCAL_SIZE,), buf_a, buf_b, buf_c, np.int32(N)
    )
    fila.finish()                          # equivale a cuda.synchronize()
    t = time.perf_counter() - inicio

    # ── 6. Copiar o resultado de volta para a CPU ──────────────────────────
    cl.enqueue_copy(fila, c, buf_c)
    fila.finish()

    print(f"Tempo (OpenCL)   : {t*1000:8.2f} ms")
    print(f"Resultado[0..4]  = {c[:5]}")
    print(f"Correto?         = {np.allclose(c, a + b)}")


def main():
    lib_opencl.cabecalho_ascii()
    print("=" * 64)
    print(" Primeiro kernel OpenCL: soma de vetores")
    print("=" * 64)

    cl = lib_opencl.carregar()
    if cl is None:
        lib_opencl.explicar_sem_opencl()
        print()
        print("Kernel OpenCL C usado:")
        print(KERNEL_SRC)
        print("Resultado esperado: [3. 3. 3. 3. 3.]")
        return

    try:
        rodar(cl)
    except Exception as erro:
        print(f"Não foi possível executar o kernel: {erro}")
        lib_opencl.explicar_sem_opencl()


if __name__ == "__main__":
    main()
