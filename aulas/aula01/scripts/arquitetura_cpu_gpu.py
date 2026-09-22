#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# Aula 01 - Arquitetura de Computadores: Sequencial vs. Paralelo
# ----------------------------------------------------------------------------
# OBJETIVO: mostrar, na prática, por que a CPU sozinha não escala para as
# operações matriciais da IA — e por que o paralelismo da GPU é decisivo.
#
# Uso:  python arquitetura_cpu_gpu.py
# Requer: numpy (pip install numpy)
# ============================================================================

import sys
import time

import numpy as np

# No console do Windows (cp1252), caracteres como "✓" podem quebrar a saída.
# Forçamos UTF-8 quando possível; se não der, o Python apenas ignora o símbolo.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# Tamanho da matriz N x N. Aumente (ex.: 400) para ver a diferença crescer.
N = 200

# Matrizes aleatórias em precisão simples (float32), como se usa em GPU
A = np.random.rand(N, N).astype(np.float32)
B = np.random.rand(N, N).astype(np.float32)

print(f"Multiplicacao de matrizes {N}x{N}")
print(f"Total de operacoes: {N**3 * 2:,} (multiply-add)\n")

# ── Versao 1: sequencial (3 loops aninhados) ────────────────────────────────
# Cada resultado C[i,j] é calculado por vez, como a CPU faria em um único núcleo.
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
# Bibliotecas otimizadas exploram paralelismo de hardware (multiplos nucleos
# + instrucoes SIMD) — é o "espírito" do que a GPU faz em escala massiva.
inicio = time.time()
C_np = A @ B
tempo_np = time.time() - inicio
print(f"Vetorizado (NumPy):   {tempo_np:.6f}s")

# ── Validacao: as duas versoes devem produzir o mesmo resultado ─────────────
assert np.allclose(C, C_np, atol=1e-2), "Resultados divergem!"
print(f"\n[OK] Resultados conferem — Speedup: {tempo_seq / tempo_np:.0f}x")
print("-> Em redes neurais, essas matrizes tem milhoes de linhas.")
print("   Sem paralelismo, o treinamento e inviavel.")
