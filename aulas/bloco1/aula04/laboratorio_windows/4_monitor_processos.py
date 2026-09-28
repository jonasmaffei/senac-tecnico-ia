#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# monitor_processos.py — Ver processos e threads (htop/nvtop pela CPU/GPU)
# ----------------------------------------------------------------------------
# OBJETIVO: "enxergar" processos e threads, como o htop faz — mas em Python,
# então funciona também no Windows:
#
#   - PID e contagem de threads do processo atual;
#   - lista as threads ativas (threading.enumerate);
#   - nº de núcleos lógicos/físicos da CPU;
#   - top processos por uso de CPU (psutil, se instalado);
#   - lembrete do que observar no htop (CPU) e no nvtop (GPU).
#
# Uso:  python monitor_processos.py
# Requer: (nenhum obrigatório) — psutil opcional
# ============================================================================

import os
import platform
import sys
import threading

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def info_processo_atual():
    """Mostra o PID do processo, nº de threads e os nomes das threads."""
    print("Processo atual:")
    print(f"  PID            : {os.getpid()}")
    print(f"  Threads ativas : {threading.active_count()}")
    for t in threading.enumerate():
        print(f"    -> {t.name} | daemon={t.daemon}")


def info_cpu():
    """Núcleos lógicos/físicos: quantos paralelismos reais a CPU oferece."""
    logicos = os.cpu_count()
    fisicos = None
    try:
        import psutil
        fisicos = psutil.cpu_count(logical=False)
    except ImportError:
        pass
    print("\nCPU:")
    print(f"  Núcleos lógicos: {logicos}")
    print(f"  Núcleos físicos: {fisicos if fisicos else '(instale psutil para ver)'}")


def top_processos(quantidade=5):
    """Lista os processos que mais usam CPU (como a 1ª tela do htop)."""
    try:
        import psutil
    except ImportError:
        print("\nTop processos: instale o psutil")
        print("   (no Colab:  !pip install psutil -q)")
        return

    # A primeira chamada de cpu_percent é sempre 0; ignoramos e reconsultamos.
    for p in psutil.process_iter(["pid", "name"]):
        try:
            p.cpu_percent(None)
        except Exception:
            pass
    import time
    time.sleep(0.5)   # pequena janela para medir o uso de CPU

    linhas = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "num_threads"]):
        try:
            pid = p.info["pid"]
            # Ignora o "System Idle Process" (PID 0), que acumula o tempo ocioso
            # e distorceria o ranking.
            if pid == 0:
                continue
            linhas.append((p.info["cpu_percent"] or 0.0, pid,
                           p.info["name"], p.info["num_threads"]))
        except Exception:
            continue
    linhas.sort(reverse=True)

    print(f"\nTop {quantidade} processos por uso de CPU:")
    print(f"  {'CPU%':>6} | {'PID':>7} | {'threads':>7} | nome")
    print("  " + "-" * 52)
    for cpu, pid, nome, n_threads in linhas[:quantidade]:
        print(f"  {cpu:>6.1f} | {pid:>7} | {str(n_threads):>7} | {nome}")


def main():
    print("=" * 66)
    print(" Processos e threads — o que o htop mostra, em Python")
    print("=" * 66)

    info_processo_atual()
    info_cpu()
    top_processos()

    print()
    print("O que observar nas ferramentas interativas (Colab/Linux):")
    print("  htop  -> uso de CADA núcleo na CPU, lista de processos e threads")
    print("           (tecle 'H' para mostrar/ocultar threads).")
    print("  nvtop -> uso da GPU e VRAM, temperatura, potência e processos.")
    print()
    print("Dica didática: rode o processos_threads.py e observe no htop que")
    print("o multiprocessing acende VÁRIOS núcleos, enquanto o threading")
    print("mantém praticamente UM núcleo ocupado por causa do GIL.")


if __name__ == "__main__":
    main()
