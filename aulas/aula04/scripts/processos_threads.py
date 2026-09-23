#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# processos_threads.py — Sequencial vs. Threading vs. Multiprocessing
# ----------------------------------------------------------------------------
# OBJETIVO: mostrar, na prática, o efeito do GIL do Python numa tarefa CPU-bound.
#
#   - Sequencial: uma tarefa de cada vez.
#   - Threading: várias threads, MAS o GIL só deixa uma rodar bytecode por vez
#     -> quase nenhum ganho em tarefas que dependem de CPU.
#   - Multiprocessing: cada tarefa num PROCESSO separado, com memória própria
#     -> contorna o GIL e dá speedup REAL.
#
# É a base do DataLoader do PyTorch: para pré-processar imagens (CPU-bound),
# ele usa PROCESSOS (workers), não threads.
#
# Roda em qualquer ambiente (Windows, Linux, Colab):
#   python processos_threads.py
# Requer: apenas a biblioteca padrão
# ============================================================================

import math
import multiprocessing
import os
import sys
import threading
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

LIMITE = 500_000       # até que número procurar primos (pesado o bastante p/ medir)
N_TAREFAS = 4          # quantas vezes repetimos a tarefa
N_PROCESSOS = max(2, min(N_TAREFAS, (os.cpu_count() or 2)))


def calcular_primos(limite):
    """Tarefa CPU-bound: conta quantos primos existem até `limite`.

    O laço testa a divisibilidade de cada número — trabalho pesado de CPU,
    sem I/O. É exatamente o tipo de tarefa em que o GIL atrapalha.
    """
    primos = 0
    for n in range(2, limite):
        if all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1)):
            primos += 1
    return primos


def executar_sequencial():
    """Uma tarefa de cada vez (referência para comparar o speedup)."""
    inicio = time.perf_counter()
    for _ in range(N_TAREFAS):
        calcular_primos(LIMITE)
    return time.perf_counter() - inicio


def executar_threading():
    """Threads: leves e com memória compartilhada, mas limitadas pelo GIL."""
    inicio = time.perf_counter()
    threads = [threading.Thread(target=calcular_primos, args=(LIMITE,))
               for _ in range(N_TAREFAS)]
    for t in threads:
        t.start()          # dispara a thread
    for t in threads:
        t.join()           # espera todas terminarem
    return time.perf_counter() - inicio


def executar_multiprocessing():
    """Processos: cada um com sua memória; contorna o GIL -> speedup real."""
    inicio = time.perf_counter()
    # Pool cria N_PROCESSOS processos e distribui as tarefas entre eles.
    with multiprocessing.Pool(processes=N_PROCESSOS) as pool:
        pool.starmap(calcular_primos, [(LIMITE,)] * N_TAREFAS)
    return time.perf_counter() - inicio


def main():
    # O bloco "if __name__ == '__main__'" é OBRIGATÓRIO no Windows para o
    # multiprocessing (o novo processo reimporta este arquivo).
    print(f"CPU(s) disponível(is): {os.cpu_count()} | usando {N_PROCESSOS} processos")
    print(f"{N_TAREFAS} tarefas, cada uma contando primos até {LIMITE:,}\n")

    t_seq = executar_sequencial()
    print(f"Sequencial      : {t_seq:6.2f}s")

    t_thr = executar_threading()
    print(f"Threading       : {t_thr:6.2f}s  (GIL -> quase sem ganho em CPU-bound)")

    t_mp = executar_multiprocessing()
    print(f"Multiprocessing : {t_mp:6.2f}s  (processos -> speedup real)")
    print()
    print(f"Speedup Threading      : {t_seq / t_thr:.2f}x")
    print(f"Speedup Multiprocessing: {t_seq / t_mp:.2f}x")
    print()
    print("Conclusão: para CPU-bound, paralelize com PROCESSOS, não threads.")
    print("O DataLoader do PyTorch usa workers (processos) por esse motivo.")


if __name__ == "__main__":
    main()
