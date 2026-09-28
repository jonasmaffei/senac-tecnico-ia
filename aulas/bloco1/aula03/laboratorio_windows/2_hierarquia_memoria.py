#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# hierarquia_memoria.py — A pirâmide de latência, medida na prática
# ----------------------------------------------------------------------------
# OBJETIVO: mostrar que "memória rápida é pequena e perto do processador".
#
# Não controlamos registradores/SRAM compartilhada por software na CPU, mas
# conseguimos reproduzir o EFEITO da hierarquia: somar vetores de tamanhos
# crescentes e medir a LARGURA DE BANDA efetiva (GB/s). Enquanto o vetor cabe
# no cache, a leitura é rápida e a banda é alta; ao passar para a RAM, a banda
# cai — esse degrau é a assinatura visível da hierarquia de memória.
#
# A lição vale para a GPU: Registradores (~1 ciclo) < Shared (~5) <
# Cache L1/L2 (~30) < VRAM Global (~500) < RAM via PCIe (milhares).
#
# Uso:  python hierarquia_memoria.py
# Requer: numpy
# ============================================================================

import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import numpy as np

# Tamanhos crescentes (em elementos float32). Conforme o vetor cresce, ele deixa
# de caber no cache e passa a ser lido da RAM -> a largura de banda cai.
TAMANHOS = [
    100_000,        # ~0.4 MB -> cabe no cache L2
    10_000_000,     # ~40 MB  -> limite do cache L3 (depende da CPU)
    100_000_000,    # ~400 MB -> já é RAM, com folga
]

ALVO_ELEMENTOS = 200_000_000   # processa bastante para diluir o overhead do Python


def banda_gb_s(n):
    """Devolve a largura de banda efetiva (GB/s) ao reduzir um vetor de n itens.

    Repetimos até somar ~ALVO_ELEMENTOS, então o custo fixo de cada chamada
    some e o que sobra é o tempo que a CPU gasta lendo a memória de verdade.
    """
    vetor = np.ones(n, dtype=np.float32)
    repeticoes = max(1, ALVO_ELEMENTOS // n)
    vetor.sum()                    # warm-up: aquece caches e o interpretador
    inicio = time.perf_counter()
    for _ in range(repeticoes):
        vetor.sum()                # percorre TODA a memória
    decorrido = time.perf_counter() - inicio
    bytes_lidos = repeticoes * n * 4      # float32 = 4 bytes por elemento
    return bytes_lidos / decorrido / 1024**3


def main():
    print("=" * 70)
    print(" Hierarquia de memória na prática: largura de banda efetiva")
    print("=" * 70)
    print(f"{'Tamanho':>14} | {'~MB':>7} | {'GB/s':>7} | leitura")
    print("-" * 70)

    resultados = []
    for n in TAMANHOS:
        gb = banda_gb_s(n)
        resultados.append(gb)
        mb = n * 4 / 1024**2
        print(f"{n:>14,} | {mb:>7.1f} | {gb:>7.1f} | ", end="")
        # rótulo didático com base no tamanho relativamente ao cache
        if mb < 1:
            print("cache L2 (rápido)")
        elif mb < 64:
            print("cache L3 / limiar")
        else:
            print("RAM (lento)")

    print("-" * 70)
    if resultados[0] > 0:
        queda = resultados[0] / resultados[-1]
        print(f"Da memória cache para a RAM, a banda caiu ~{queda:.1f}x.")
    print("O degrau = o vetor deixou de caber no cache e foi lido da RAM.")
    print()
    print("Na GPU, a mesma ideia fica ainda mais radical:")
    print("  Registradores .....  ~1 ciclo    (por thread)")
    print("  Shared (SRAM) .....  ~1-5 ciclos (por bloco)")
    print("  Cache L1/L2 .......  ~20-50      (automático)")
    print("  VRAM Global .......  ~400-800    (toda a GPU)")
    print("  RAM via PCIe ......  milhares    (host <-> placa)")
    print()
    print("Regra de ouro: mantenha os dados no nível mais ALTO (rápido) e")
    print("reaproveite-os o máximo possível antes de voltar para a VRAM/RAM.")


if __name__ == "__main__":
    main()
