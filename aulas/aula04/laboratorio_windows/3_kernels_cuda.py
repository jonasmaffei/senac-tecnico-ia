#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# kernels_cuda.py — Configuração de blocos e threads na GPU (CUDA/Numba)
# ----------------------------------------------------------------------------
# OBJETIVO: entender a hierarquia de threads da GPU na prática:
#
#   Thread  -> 1 instância do kernel (1 dado)
#   Warp    -> 32 threads que executam a MESMA instrução (SIMD)
#   Bloco   -> grupo de warps, roda em 1 SM, compartilha memória (shared)
#   Grid    -> todos os blocos = o problema completo
#
# Fazemos dois experimentos:
#   1) Variar threads por bloco (32, 64, ..., 1024) e medir o tempo.
#   2) Grid 2D para processar uma imagem (cada thread = 1 pixel).
#
# ⚠️ Requer GPU NVIDIA + numba. Sem GPU, o script explica o conceito e mostra
#    os números esperados (Tesla T4) — a aula não quebra.
#
# Uso:  python kernels_cuda.py
# ============================================================================

import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def experimento_1d():
    """Varia o número de threads por bloco numa soma de vetores simples."""
    from numba import cuda
    import numpy as np

    N = 1024 * 1024   # 1M elementos
    a = np.ones(N, dtype=np.float32)
    b = np.ones(N, dtype=np.float32)
    c = np.zeros(N, dtype=np.float32)

    a_d = cuda.to_device(a)      # copia para a VRAM
    b_d = cuda.to_device(b)
    c_d = cuda.to_device(c)

    @cuda.jit
    def soma_vetores(a, b, c):
        idx = cuda.grid(1)            # índice GLOBAL desta thread
        if idx < a.shape[0]:          # proteção: não passar do fim do vetor
            c[idx] = a[idx] + b[idx]

    print("Experimento 1 — variar threads por bloco")
    print(f"{'threads/bloco':>13} | {'blocos':>8} | {'tempo (ms)':>10}")
    print("-" * 40)
    for threads_por_bloco in (32, 64, 128, 256, 512, 1024):
        # Quantos blocos são necessários para cobrir N elementos?
        blocos = (N + threads_por_bloco - 1) // threads_por_bloco

        soma_vetores[blocos, threads_por_bloco](a_d, b_d, c_d)  # warm-up
        cuda.synchronize()

        inicio = time.perf_counter()
        for _ in range(50):
            soma_vetores[blocos, threads_por_bloco](a_d, b_d, c_d)
        cuda.synchronize()            # espera a GPU concluir antes de medir
        tempo = (time.perf_counter() - inicio) / 50
        print(f"{threads_por_bloco:>13} | {blocos:>8} | {tempo * 1000:>10.3f}")
    print("-" * 40)
    print("256 threads/bloco costuma ser o ponto ótimo: múltiplo de 32 (warp)")
    print("e maximiza a ocupação do SM sem estourar os limites do bloco.\n")


def experimento_2d():
    """Grid 2D: cada thread processa 1 pixel (ideal para imagens)."""
    from numba import cuda
    import numpy as np

    @cuda.jit
    def escala_cinza(img_rgb, img_gray):
        x, y = cuda.grid(2)            # x = coluna, y = linha
        if x < img_rgb.shape[1] and y < img_rgb.shape[0]:
            r = img_rgb[y, x, 0]
            g = img_rgb[y, x, 1]
            b = img_rgb[y, x, 2]
            # luminância percebida: o olho é mais sensível ao verde
            img_gray[y, x] = np.uint8(0.299 * r + 0.587 * g + 0.114 * b)

    H, W = 1080, 1920                   # Full HD
    img = np.random.randint(0, 256, (H, W, 3), dtype=np.uint8)
    gray = np.zeros((H, W), dtype=np.uint8)

    img_d = cuda.to_device(img)
    gray_d = cuda.to_device(gray)

    BLOCO = (16, 16)                    # 256 threads por bloco, em 2D
    GRID = ((W + 15) // 16, (H + 15) // 16)

    print("Experimento 2 — grid 2D (imagem)")
    print(f"Grid : {GRID[0]} x {GRID[1]} blocos")
    print(f"Bloco: {BLOCO[0]} x {BLOCO[1]} threads")
    print(f"Total de threads: {GRID[0] * GRID[1] * BLOCO[0] * BLOCO[1]:,}")

    escala_cinza[GRID, BLOCO](img_d, gray_d)
    cuda.synchronize()
    resultado = gray_d.copy_to_host()
    print(f"Imagem {H}x{W} convertida para cinza! (shape {resultado.shape})\n")


def explicar_sem_gpu():
    """Quando não há GPU: explica a hierarquia e mostra números esperados."""
    print("Numba/CUDA indisponível neste ambiente (sem GPU NVIDIA).")
    print("Ainda assim, veja o conceito e os números esperados (Tesla T4):\n")
    print("Experimento 1 — variar threads por bloco (valores de referência)")
    print(f"{'threads/bloco':>13} | {'blocos':>8} | {'tempo (ms)':>10}")
    print("-" * 40)
    referencia = [
        (32, 32768, 0.320), (64, 16384, 0.180), (128, 8192, 0.095),
        (256, 4096, 0.088), (512, 2048, 0.101), (1024, 1024, 0.115),
    ]
    for threads_por_bloco, blocos, ms in referencia:
        destaque = "  <- ótimo" if threads_por_bloco == 256 else ""
        print(f"{threads_por_bloco:>13} | {blocos:>8} | {ms:>10.3f}{destaque}")
    print("-" * 40)
    print("256 threads/bloco costuma ser o ponto ótimo (múltiplo de 32 = 1 warp).")
    print()
    print("Hierarquia da GPU: Thread -> Warp (32, SIMD) -> Bloco (1 SM) -> Grid.")
    print("No Colab com T4 GPU, este mesmo script mede os tempos de verdade.")


def main():
    try:
        from numba import cuda
        if not cuda.is_available():
            raise RuntimeError("sem GPU CUDA")
    except Exception:
        explicar_sem_gpu()
        return

    experimento_1d()
    experimento_2d()


if __name__ == "__main__":
    main()
