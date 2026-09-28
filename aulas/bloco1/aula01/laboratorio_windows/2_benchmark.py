#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# 2_benchmark.py — Sequencial vs. vetorizado (medido na máquina real)
# ----------------------------------------------------------------------------
# OBJETIVO: mostrar, na prática, por que a CPU sozinha não escala para as
# operações matriciais da IA — e por que o paralelismo (SIMD/GPU) é decisivo.
#
# Uso (no laboratório Windows):
#     python 2_benchmark.py
#     python 2_benchmark.py 300      # matriz 300x300 (demora mais)
# ============================================================================

import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import numpy as np

# Tamanho da matriz N x N. Pode vir por argumento (padrão 200).
N = int(sys.argv[1]) if len(sys.argv) > 1 else 200

A = np.random.rand(N, N).astype(np.float32)
B = np.random.rand(N, N).astype(np.float32)

print(f"Multiplicacao de matrizes {N}x{N}")
print(f"Total de operacoes: {N**3 * 2:,} (multiply-add)\n")

# ── Versao 1: sequencial (3 loops aninhados) ────────────────────────────────
# Cada resultado C[i,j] é calculado um por vez, como a CPU faria em um núcleo.
inicio = time.time()
C = np.zeros((N, N), dtype=np.float32)
for i in range(N):
    for j in range(N):
        soma = 0.0
        for k in range(N):
            soma += A[i, k] * B[k, j]
        C[i, j] = soma
tempo_seq = time.time() - inicio
print(f"Sequencial (3 loops): {tempo_seq:.2f}s")

# ── Versao 2: vetorizada (NumPy delega para o BLAS) ─────────────────────────
# Bibliotecas otimizadas exploram paralelismo de hardware (vários núcleos +
# instruções SIMD) — é o "espírito" do que a GPU faz em escala massiva.
inicio = time.time()
C_np = A @ B
tempo_np = time.time() - inicio
print(f"Vetorizado (NumPy):   {tempo_np:.6f}s")

# ── Validacao ───────────────────────────────────────────────────────────────
assert np.allclose(C, C_np, atol=1e-2), "Resultados divergem!"
print(f"\n[OK] Resultados conferem — Speedup: {tempo_seq / tempo_np:,.0f}x")
print("-> Em redes neurais, essas matrizes têm milhões de linhas.")
print("   Sem paralelismo, o treinamento é inviável.")

# ── Se houver GPU via CuPy, mede também na VRAM ─────────────────────────────
try:
    import cupy as cp
    if cp.cuda.runtime.getDeviceCount() > 0:
        Ag, Bg = cp.asarray(A), cp.asarray(B)
        _ = Ag @ Bg                       # warm-up
        cp.cuda.Stream.null.synchronize()
        inicio = time.perf_counter()
        for _ in range(5):
            _ = Ag @ Bg
        cp.cuda.Stream.null.synchronize()
        t_gpu = (time.perf_counter() - inicio) / 5
        print(f"\nGPU (CuPy):           {t_gpu:.6f}s")
        print(f"   Speedup GPU vs CPU: {tempo_np / t_gpu:,.0f}x")
except Exception:
    pass
