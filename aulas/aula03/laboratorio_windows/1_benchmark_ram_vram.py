#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# benchmark_ram_vram.py — RAM (CPU) vs. VRAM (GPU) e o custo do PCIe
# ----------------------------------------------------------------------------
# OBJETIVO: mostrar, na prática, por que a memória é o gargalo da IA:
#
#   1. Operar dados na RAM/RAM (CPU) é mais lento que operar na VRAM (GPU).
#   2. MAS copiar dados da RAM para a VRAM passa pelo barramento PCIe, que é
#      ~100x mais lento que a VRAM interna -> copiar pode custar mais que o
#      próprio cálculo. É a lição central da aula.
#
# Roda em qualquer ambiente:
#   Colab (GPU NVIDIA)   -> mede RAM x VRAM e a transferência PCIe de verdade
#   Windows com GPU AMD  -> mede o que estiver disponível (ou só a RAM)
#   Sem GPU              -> mostra a hierarquia pela RAM e explica o PCIe
#
# Uso:  python benchmark_ram_vram.py
# Requer: numpy (torch/cupy são opcionais, usados só se houver GPU)
# ============================================================================

import sys
import time

try:
    # Console do Windows costuma usar cp1252; forçamos UTF-8 para evitar erros.
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import numpy as np

# Importamos o MÓDULO: assim lemos o backend detectado em runtime.
import lib_backend

N = 10_000_000            # 10 milhões de elementos float32 (~40 MB na memória)
REPETICOES = 50           # quantas vezes repetimos a soma para medir a média
BYTES_POR_ELEMENTO = 4    # float32 = 4 bytes


def medir(funcao, repeticoes=REPETICOES):
    """Executa a função N vezes e devolve o tempo médio em milissegundos.

    Antes de medir, fazemos um 'warm-up' (aquecimento): a primeira execução
    costuma ser mais lenta por causa de alocação e caches frios.
    """
    funcao()                      # warm-up: aquece caches/alocações
    inicio = time.perf_counter()  # relógio de alta precisão
    for _ in range(repeticoes):
        funcao()
    return (time.perf_counter() - inicio) / repeticoes * 1000  # ms por operação


def main():
    mb = N * BYTES_POR_ELEMENTO / 1024**2
    print(f"Vetores com {N:,} elementos float32 (~{mb:.0f} MB cada)\n")

    # ── 1) RAM (CPU): os dados vivem na memória do host ─────────────────────
    # np.arange cria o vetor na RAM; a soma é feita pelos núcleos da CPU.
    a_ram = np.arange(N, dtype=np.float32)
    b_ram = np.arange(N, dtype=np.float32)
    t_ram = medir(lambda: a_ram + b_ram)
    print(f"RAM (CPU)  : {t_ram:8.3f} ms por soma de vetores")

    # ── 2) Detecta se há GPU acessível ─────────────────────────────────────
    xp = lib_backend.detectar_backend()
    estado = lib_backend.info()
    backend = estado["backend"]

    if backend == "NumPy (CPU/RAM)":
        # Sem GPU: a própria CPU já mostrou o caminho da RAM. Explicamos o resto.
        _explicar_sem_gpu(t_ram)
        return

    # ── 3) VRAM (GPU): os mesmos dados, agora na memória da placa ───────────
    usar_cupy = backend.startswith("CuPy")
    usar_torch = backend.startswith("PyTorch")

    try:
        if usar_cupy:
            # asarray empurra os dados da RAM para a VRAM (cópia via PCIe).
            # Medimos ESSA cópia separadamente: é o gargalo que queremos expor.
            inicio = time.perf_counter()
            a_vram = xp.asarray(a_ram)
            b_vram = xp.asarray(b_ram)
            xp.cuda.Stream.null.synchronize()   # espera a GPU terminar a cópia
            t_h2d = (time.perf_counter() - inicio) * 1000
            t_vram = medir(lambda: a_vram + b_vram)
            # Traz de volta VRAM -> RAM (device to host)
            inicio = time.perf_counter()
            resultado = xp.asnumpy(a_vram + b_vram)
            t_d2h = (time.perf_counter() - inicio) * 1000
        elif usar_torch:
            import torch
            a_vram = torch.from_numpy(a_ram).cuda()
            b_vram = torch.from_numpy(b_ram).cuda()
            torch.cuda.synchronize()
            inicio = time.perf_counter()
            a_copia = torch.empty_like(a_ram).cuda()
            a_copia.copy_(torch.from_numpy(a_ram))
            torch.cuda.synchronize()
            t_h2d = (time.perf_counter() - inicio) * 1000
            t_vram = medir(lambda: a_vram + b_vram)
            torch.cuda.synchronize()
            resultado = (a_vram + b_vram).cpu().numpy()
            t_d2h = 0.0  # não medimos separado no caminho torch
        else:
            return
    except Exception as erro:
        print(f"(Não foi possível medir na GPU: {erro})")
        _explicar_sem_gpu(t_ram)
        return

    print(f"VRAM (GPU) : {t_vram:8.3f} ms por soma de vetores")
    print(f"   -> Speedup do cálculo: {t_ram / t_vram:,.0f}x mais rápido na GPU\n")

    # ── 4) O gargalo do PCIe: copiar RAM <-> VRAM ──────────────────────────
    if t_h2d > 0:
        taxa = (N * BYTES_POR_ELEMENTO / 1024**3) / (t_h2d / 1000)
        print(f"Transferência RAM -> VRAM (PCIe): {t_h2d:8.3f} ms  (~{taxa:.1f} GB/s)")
    print(f"Transferência VRAM -> RAM (PCIe): {t_d2h:8.3f} ms")
    print("   -> Copiar custa mais que calcular: por isso minimizamos o tráfego PCIe!")
    print("   -> Dica: mantenha os batches na VRAM e só traga o resultado no final.\n")

    # ── 5) Validação: RAM e VRAM devem dar o mesmo resultado ───────────────
    esperado = a_ram + b_ram
    assert np.allclose(esperado, np.asarray(resultado), atol=1e-2), "Divergiu!"
    print("[OK] Resultados conferem: RAM == VRAM.")


def _explicar_sem_gpu(t_ram):
    """Mensagem didática quando não há GPU acessível no ambiente."""
    print("\nSem GPU acessível: os dados ficaram na RAM, operados pela CPU.")
    print("Mesmo assim, a lição da aula vale:")
    print("  Registradores < Memória Compartilhada < Cache L1/L2 < VRAM < RAM")
    print("  A cópia RAM <-> VRAM passa pelo PCIe (~32 GB/s), ~100x mais lento")
    print("  que a largura de banda interna da VRAM. No Colab (T4 GPU) este")
    print("  mesmo script mede a VRAM e a transferência de verdade.")


if __name__ == "__main__":
    main()
