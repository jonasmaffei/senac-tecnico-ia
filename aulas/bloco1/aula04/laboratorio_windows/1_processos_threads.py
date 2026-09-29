#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# processos_threads.py - Sequencial vs. Threading vs. Multiprocessing
# ----------------------------------------------------------------------------
# OBJETIVO: mostrar, na pratica, o efeito do GIL do Python numa tarefa CPU-bound.
#
#   - Sequencial: uma tarefa de cada vez.
#   - Threading: varias threads, MAS o GIL so deixa uma rodar bytecode por vez
#     -> quase nenhum ganho em tarefas que dependem de CPU.
#   - Multiprocessing: cada tarefa num PROCESSO separado, com memoria propria
#     -> contorna o GIL e da speedup REAL.
#
# E a base do DataLoader do PyTorch: para pre-processar imagens (CPU-bound),
# ele usa PROCESSOS (workers), nao threads.
#
# Roda em qualquer ambiente (Windows, Linux, Colab):
#   python processos_threads.py
# Requer: apenas a biblioteca padrao
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

LIMITE = 500_000       # ate que numero procurar primos (pesado o bastante p/ medir)
N_TAREFAS = 4          # quantas vezes repetimos a tarefa
N_PROCESSOS = max(2, min(N_TAREFAS, (os.cpu_count() or 2)))


def calcular_primos(limite):
    """Tarefa CPU-bound: conta quantos primos existem ate `limite`.

    O laco testa a divisibilidade de cada numero - trabalho pesado de CPU,
    sem I/O. E exatamente o tipo de tarefa em que o GIL atrapalha.
    """
    primos = 0
    for n in range(2, limite):
        if all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1)):
            primos += 1
    return primos


def executar_sequencial():
    """Uma tarefa de cada vez (referencia para comparar o speedup)."""
    inicio = time.perf_counter()
    for _ in range(N_TAREFAS):
        calcular_primos(LIMITE)
    return time.perf_counter() - inicio


def executar_threading():
    """Threads: leves e com memoria compartilhada, mas limitadas pelo GIL."""
    inicio = time.perf_counter()
    threads = [threading.Thread(target=calcular_primos, args=(LIMITE,))
               for _ in range(N_TAREFAS)]
    for t in threads:
        t.start()          # dispara a thread
    for t in threads:
        t.join()           # espera todas terminarem
    return time.perf_counter() - inicio


def executar_multiprocessing():
    """Processos: cada um com sua memoria; contorna o GIL -> speedup real."""
    inicio = time.perf_counter()
    # Pool cria N_PROCESSOS processos e distribui as tarefas entre eles.
    with multiprocessing.Pool(processes=N_PROCESSOS) as pool:
        pool.starmap(calcular_primos, [(LIMITE,)] * N_TAREFAS)
    return time.perf_counter() - inicio


def main():
    # O bloco "if __name__ == '__main__'" e OBRIGATORIO no Windows para o
    # multiprocessing (o novo processo reimporta este arquivo).
    print(f"CPU(s) disponivel(is): {os.cpu_count()} | usando {N_PROCESSOS} processos")
    print(f"{N_TAREFAS} tarefas, cada uma contando primos ate {LIMITE:,}\n")

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
    print("Conclusao: para CPU-bound, paralelize com PROCESSOS, nao threads.")
    print("O DataLoader do PyTorch usa workers (processos) por esse motivo.")


if __name__ == "__main__":
    main()
