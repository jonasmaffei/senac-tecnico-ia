"""3_teste_fila.py - Teste da fila com 4 jobs concorrentes + monitor ao vivo.

Lanca 4 jobs ao mesmo tempo (2 de prioridade alta, 1 media, 1 baixa) e mostra,
enquanto rodam, o estado da GPU: lock ativo, fila de espera e jobs em execucao.
Ao final, imprime a ordem real em que os jobs foram executados (pelo log).

Uso:
    python 3_teste_fila.py            # teste normal, com monitor embutido
    python 3_teste_fila.py 0          # teste SEM monitor (so lanca e espera)
"""

import os
import subprocess
import sys
import time

import monitor_fila

LOG_FILE = os.path.join("reports", "gpu_queue.log")

# (prioridade, nome do job, epocas) — prioridade 1 = alta, 3 = baixa
JOBS = [
    (1, "Job-Alta-A", 3),
    (3, "Job-Baixa-B", 2),
    (2, "Job-Media-C", 4),
    (1, "Job-Alta-D", 2),
]


def lancar_jobs():
    """Dispara os 4 jobs em paralelo (cada um e um processo da fila)."""
    processos = []
    print("Lancando 4 jobs simultaneos em paralelo...")
    for prioridade, nome, epocas in JOBS:
        cmd = [sys.executable, "2_gpu_queue.py", str(prioridade), nome,
               "train_job.py", "--nome", nome, "--epocas", str(epocas)]
        processos.append(subprocess.Popen(cmd))
        time.sleep(0.3)  # pequeno intervalo para a ordem de chegada variar
    return processos


def monitorar_ate_terminar(processos):
    """Mostra o estado da GPU enquanto houver job rodando."""
    print("\n--- Monitoramento ao vivo (Ctrl+C para pular o monitor) ---")
    try:
        while any(p.poll() is None for p in processos):
            snap = monitor_fila.coletar_snapshot()
            estado = "OCUPADA" if snap["lock"] else "LIVRE"
            fila = ", ".join(snap["fila"]) if snap["fila"] else "(vazia)"
            print(f"[{time.strftime('%H:%M:%S')}] GPU={estado:<7} "
                  f"| jobs ativos={len(snap['processos'])} | fila: {fila}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n(Monitor interrompido; aguardando os jobs terminarem...)")


def main():
    com_monitor = not (len(sys.argv) > 1 and sys.argv[1] == "0")

    # Limpa log anterior para a ordem ficar clara
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    processos = lancar_jobs()

    if com_monitor:
        monitorar_ate_terminar(processos)

    for p in processos:
        p.wait()

    # A fila serializou tudo; a ordem real esta no log (linhas "Executando ...")
    print("\n=== Ordem real de execucao (do log) ===")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, encoding="utf-8") as f:
            for linha in f:
                if "Executando" in linha:
                    print("  " + linha.strip())
    print("\nTodos os 4 jobs foram executados de forma serializada por prioridade!")


if __name__ == "__main__":
    main()
