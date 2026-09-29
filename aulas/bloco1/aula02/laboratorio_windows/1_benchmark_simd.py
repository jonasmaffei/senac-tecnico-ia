#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# benchmark_simd.py - Sequencial (SISD) vs. SIMD (vetorizado)
# ----------------------------------------------------------------------------
# OBJETIVO: mostrar, na pratica, o ganho do modelo SIMD (Single Instruction,
# Multiple Data): UMA instrucao aplicada a MUITOS dados ao mesmo tempo.
#
#   - Versao sequencial: Python puro, um elemento por vez (modelo SISD).
#   - Versao NumPy: vetorizada - a CPU usa instrucoes SIMD (AVX/SSE).
#   - Se houver GPU, tambem medimos a versao acelerada (CuPy/PyTorch).
#
# Roda em qualquer ambiente:
#   Colab (GPU NVIDIA) -> testa tambem a GPU
#   Windows com GPU AMD -> usa o que estiver disponivel (ou so NumPy)
#   Sem GPU -> compara sequencial vs. NumPy, que ja demonstra o SIMD
#
# Uso:  python benchmark_simd.py
# Requer: numpy (o CuPy/PyTorch sao opcionais)
# ============================================================================

import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import numpy as np

# lib_backend.py fica em ../scripts (compartilhado com o notebook do Colab).
# Adicionamos essa pasta ao caminho de importacao antes de carregar o modulo.
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

# Importamos o MODULO (nao as variaveis): assim lemos o backend ja detectado.
import lib_backend

N = 1_000_000  # quantidade de elementos somados


def tempo(funcao):
    """Executa a funcao e devolve (resultado, segundos gastos)."""
    inicio = time.time()
    resultado = funcao()
    return resultado, time.time() - inicio


def main():
    print(f"Somando {N:,} elementos, vetor a + vetor b\n")

    # -- 1) Sequencial (SISD): um elemento por vez ---------------------------
    a = list(range(N))
    b = list(range(N))
    c_seq, t_seq = tempo(lambda: [a[i] + b[i] for i in range(N)])
    print(f"Sequencial (Python, 1 por vez): {t_seq:.4f}s")

    # -- 2) SIMD com NumPy: todos os elementos de uma vez --------------------
    a_np = np.arange(N)
    b_np = np.arange(N)
    c_np, t_np = tempo(lambda: a_np + b_np)
    print(f"NumPy (SIMD na CPU):            {t_np:.6f}s")
    print(f"   -> Speedup vs. sequencial: {t_seq / t_np:,.0f}x\n")

    # -- 3) GPU (opcional): mesmo codigo, engine diferente -------------------
    xp = lib_backend.detectar_backend()
    estado = lib_backend.info()
    if estado["backend"] != "NumPy (CPU SIMD)":
        try:
            usar_cupy = "cupy" in estado["backend"].lower()
            xa = xp.arange(N, dtype=np.float32) if usar_cupy else xp.arange(N)
            xb = xp.arange(N, dtype=np.float32) if usar_cupy else xp.arange(N)
            _, t_gpu = tempo(lambda: xa + xb)
            print(f"GPU ({estado['dispositivo']}): {t_gpu:.6f}s")
            print(f"   -> Speedup vs. sequencial: {t_seq / t_gpu:,.0f}x")
        except Exception as erro:
            print(f"(Nao foi possivel medir na GPU: {erro})")

    # -- 4) Validacao: tudo deve dar o mesmo resultado -----------------------
    assert list(c_seq) == c_np.tolist(), "Resultados divergem!"
    print("\n[OK] Resultados conferem: sequencial == NumPy.")
    print("-> A diferenca e so a 'engine': o SIMD opera muitos dados por instrucao.")


if __name__ == "__main__":
    main()
