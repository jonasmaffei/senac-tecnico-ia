import os
import subprocess
import sys
import psutil

def main():
    print("=== Processos em Execucao no Host ===")
    procs_python = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
        try:
            if 'python' in (proc.info['name'] or '').lower():
                cmd = ' '.join(proc.info['cmdline'] or [])
                if 'train_job' in cmd or 'gpu_queue' in cmd:
                    procs_python.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    if procs_python:
        for p in procs_python:
            print(f"  PID={p['pid']} | User={p['username']} | Cmd={p['cmdline']}")
    else:
        print("  Nenhum job de treinamento ativo no momento.")

    print("\n=== Estado do Lock de GPU ===")
    lock_dir = os.path.join("reports", "gpu_exclusive.lockdir")
    if os.path.exists(lock_dir):
        print("  GPU OCUPADA (Lock ativo em 'reports/gpu_exclusive.lockdir')")
    else:
        print("  GPU LIVRE")

    print("\n=== Fila Atual de Jobs (reports/gpu_queue_spool) ===")
    spool_dir = os.path.join("reports", "gpu_queue_spool")
    if os.path.exists(spool_dir) and os.listdir(spool_dir):
        for idx, item in enumerate(sorted(os.listdir(spool_dir)), 1):
            print(f"  {idx}. {item}")
    else:
        print("  Fila vazia.")

if __name__ == "__main__":
    main()
