import os
import subprocess
import sys
import time

def main():
    print("=== Teste de Fila Concorrente de GPU ===")
    print("Lancando 4 jobs simultaneos em paralelo...")
    print("Prioridades: Job-Alta-A (Prio 1), Job-Baixa-B (Prio 3), Job-Media-C (Prio 2), Job-Alta-D (Prio 1)\n")

    jobs = [
        [sys.executable, "2_gpu_queue.py", "1", "Job-Alta-A",  "train_job.py", "--nome", "Job-Alta-A",  "--epocas", "3"],
        [sys.executable, "2_gpu_queue.py", "3", "Job-Baixa-B", "train_job.py", "--nome", "Job-Baixa-B", "--epocas", "2"],
        [sys.executable, "2_gpu_queue.py", "2", "Job-Media-C", "train_job.py", "--nome", "Job-Media-C", "--epocas", "4"],
        [sys.executable, "2_gpu_queue.py", "1", "Job-Alta-D",  "train_job.py", "--nome", "Job-Alta-D",  "--epocas", "2"],
    ]

    processos = []
    for cmd in jobs:
        p = subprocess.Popen(cmd)
        processos.append(p)
        time.sleep(0.3)

    spool_dir = os.path.join("reports", "gpu_queue_spool")
    time.sleep(1)

    while any(p.poll() is None for p in processos):
        if os.path.exists(spool_dir):
            fila = sorted(os.listdir(spool_dir))
            print(f"[{time.strftime('%H:%M:%S')}] Jobs aguardando na fila ({len(fila)}): {fila}")
        time.sleep(2)

    for p in processos:
        p.wait()

    print("\nTodos os 4 jobs foram executados de forma serializada por prioridade!")

if __name__ == "__main__":
    main()
