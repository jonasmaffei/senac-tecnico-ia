#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# estudo_imagem.py — Estudo de caso: GPUs combinam SIMD + MIMD
# ----------------------------------------------------------------------------
# OBJETIVO: processar uma imagem (converter para tons de cinza) de duas formas:
#
#   - CPU com loops: pixel a pixel (sequencial).
#   - Vetorizado (SIMD): todos os pixels de uma vez, com NumPy.
#
# É o "espírito" do que a GPU faz: dentro de um warp/Wavefront, todas as lanes
# executam a MESMA instrução (SIMD); e vários blocos/SMs processam pedaços
# diferentes ao mesmo tempo (MIMD).
#
# Uso:  python estudo_imagem.py
# Requer: numpy
# ============================================================================

import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import numpy as np

# Resolução Full HD (1080p): H linhas x W colunas x 3 canais (RGB)
H, W = 1080, 1920
rng = np.random.default_rng(42)     # semente fixa => resultado reprodutível
imagem = rng.integers(0, 256, (H, W, 3), dtype=np.uint8)

print(f"Imagem {W}x{H} ({H * W:,} pixels)\n")

# ── 1) CPU, pixel a pixel (sequencial) ──────────────────────────────────────
# Pesos da luminância: quanto cada canal contribui para o brilho percebido.
inicio = time.time()
cinza_loop = np.zeros((H, W), dtype=np.uint8)
for i in range(H):
    for j in range(W):
        r, g, b = imagem[i, j]
        cinza_loop[i, j] = int(0.299 * r + 0.587 * g + 0.114 * b)
t_loop = time.time() - inicio
print(f"CPU (loop por pixel): {t_loop:.3f}s")

# ── 2) Vetorizado (SIMD): a mesma conta, em todos os pixels de uma vez ───────
inicio = time.time()
r = imagem[:, :, 0].astype(np.float32)   # canal vermelho inteiro
g = imagem[:, :, 1].astype(np.float32)   # canal verde inteiro
b = imagem[:, :, 2].astype(np.float32)   # canal azul inteiro
cinza_simd = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
t_simd = time.time() - inicio
print(f"Vetorizado (SIMD):    {t_simd:.3f}s")
print(f"   -> Speedup: {t_loop / t_simd:,.0f}x mais rapido\n")

# ── 3) Validação ────────────────────────────────────────────────────────────
diferenca = np.abs(cinza_loop.astype(int) - cinza_simd.astype(int)).max()
print(f"[OK] Maior diferenca entre as versoes: {diferenca} (arredondamento)")

print("""
Como a GPU faz isso em hardware:
  1. Divide a imagem em blocos (ex.: 16x16)
  2. Cada bloco vai para um SM (Streaming Multiprocessor)  -> MIMD entre blocos
  3. Dentro do SM, 32 threads (1 warp) executam a MESMA instrucao -> SIMD
  4. Varios SMs processam blocos diferentes ao mesmo tempo
""")
