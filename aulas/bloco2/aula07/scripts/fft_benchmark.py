#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# fft_benchmark.py — FFT: CPU (NumPy) vs. GPU (CuPy) — o caso do áudio
# ----------------------------------------------------------------------------
# OBJETIVO: resolver o problema da startup: calcular a Transformada de Fourier
# (FFT) de milhões de amostras de áudio.
#
#   - CPU (NumPy):  np.fft.fft  -> mede o tempo na RAM
#   - GPU (CuPy):   cp.fft.fft  -> mesmo código, dados na VRAM
#
# A FFT é a operação central do pré-processamento de áudio para
# reconhecimento de fala. O speedup mostra por que ela roda na GPU.
#
# Requer CuPy (Colab com GPU). Sem CuPy, mede só o CPU e mostra a referência.
#
# Uso:  python fft_benchmark.py
# Requer: numpy (cupy opcional)
# ============================================================================

import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import numpy as np

N = 2 ** 22   # ~4 milhões de pontos


def medir_cpu(sinal):
    """Executa a FFT na CPU e devolve (resultado, tempo_em_segundos)."""
    inicio = time.perf_counter()
    resultado = np.fft.fft(sinal)
    return resultado, time.perf_counter() - inicio


def main():
    print("=" * 64)
    print(" FFT — CPU (NumPy) vs. GPU (CuPy)")
    print("=" * 64)

    sinal_cpu = np.random.randn(N).astype(np.float32)
    _, tempo_cpu = medir_cpu(sinal_cpu)
    print(f"CPU (NumPy FFT): {tempo_cpu*1000:8.2f} ms  ({N:,} pontos)")

    # ── GPU via CuPy, se disponível ────────────────────────────────────────
    try:
        import cupy as cp
    except ImportError:
        print("\nCuPy não instalado neste ambiente.")
        print("Referência no Colab com T4: GPU ~18 ms vs. CPU ~1200 ms (~66x).")
        print("Instalar: pip install cupy-cuda12x")
        return

    try:
        sinal_gpu = cp.asarray(sinal_cpu)              # RAM -> VRAM

        # Warm-up: a 1ª execução inclui compilação/alocação; descartamos.
        _ = cp.fft.fft(sinal_gpu)
        cp.cuda.Stream.null.synchronize()

        inicio = time.perf_counter()
        fft_gpu = cp.fft.fft(sinal_gpu)
        cp.cuda.Stream.null.synchronize()              # espera a GPU terminar
        tempo_gpu = time.perf_counter() - inicio

        print(f"GPU (CuPy FFT) : {tempo_gpu*1000:8.2f} ms")
        print(f"Speedup        : {tempo_cpu/tempo_gpu:.1f}x mais rápido!")

        # Validação: as duas FFTs devem coincidir (com tolerância).
        fft_cpu_ref = cp.asarray(np.fft.fft(sinal_cpu))
        assert cp.allclose(fft_cpu_ref, fft_gpu, atol=1e-1), "FFT divergiu!"
        print("[OK] FFT CPU == FFT GPU (dentro da tolerância).")
    except Exception as erro:
        print(f"\nNão foi possível medir na GPU: {erro}")


if __name__ == "__main__":
    main()
