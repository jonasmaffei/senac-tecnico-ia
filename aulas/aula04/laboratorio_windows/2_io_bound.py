#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# io_bound.py — Quando THREADING ajuda: tarefas de I/O
# ----------------------------------------------------------------------------
# OBJETIVO: mostrar o outro lado do GIL. Em tarefas I/O-bound (rede, disco),
# o Python LIBERA o GIL enquanto espera a resposta. Então as threads ficam
# livres para esperar ao mesmo tempo -> ganho real.
#
# É o oposto do processos_threads.py (CPU-bound). A regra geral:
#   - CPU-bound -> processos (multiprocessing)
#   - I/O-bound -> threads (threading), ou asyncio
#
# Aqui simulamos a latência de rede com time.sleep(), que também libera o GIL
# (é uma espera, não cálculo). Assim o exemplo roda offline e é previsível.
#
# Uso:  python io_bound.py
# Requer: apenas a biblioteca padrão
# ============================================================================

import sys
import threading
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

LATENCIA = 0.5   # segundos que cada "requisição" leva (latência simulada)
N_TAREFAS = 6    # quantas requisições


def requisicao_simulada(identificador, resultados):
    """Simula uma chamada de rede: espera LATENCIA e registra o resultado.

    Durante o sleep, o Python libera o GIL: outras threads podem avançar.
    Guardamos o resultado numa lista compartilhada para conferir no final.
    """
    time.sleep(LATENCIA)              # espera de I/O (libera o GIL)
    resultados.append(identificador)


def main():
    print(f"{N_TAREFAS} 'requisições', cada uma com {LATENCIA}s de latência\n")

    # ── 1) Sequencial: espera uma após a outra ──────────────────────────────
    resultados = []
    inicio = time.perf_counter()
    for i in range(N_TAREFAS):
        requisicao_simulada(i, resultados)
    t_seq = time.perf_counter() - inicio
    print(f"Sequencial (I/O): {t_seq:6.2f}s")

    # ── 2) Threading: dispara todas ao mesmo tempo ──────────────────────────
    resultados = []
    inicio = time.perf_counter()
    threads = [threading.Thread(target=requisicao_simulada, args=(i, resultados))
               for i in range(N_TAREFAS)]
    for t in threads:
        t.start()                      # dispara a thread
    for t in threads:
        t.join()                       # espera todas terminarem
    t_thr = time.perf_counter() - inicio
    print(f"Threading  (I/O): {t_thr:6.2f}s  <- quase {N_TAREFAS}x mais rapido")

    print()
    print(f"Speedup com threads: {t_seq / t_thr:.1f}x")
    print("Aqui o GIL NAO atrapalha: durante a espera o Python libera o lock,")
    print("entao as threads esperam EM PARALELO.")
    print()
    print("Regra geral:")
    print("  CPU-bound (calculo)    -> multiprocessing (processos)")
    print("  I/O-bound (rede/disco) -> threading (threads) ou asyncio")


if __name__ == "__main__":
    main()
