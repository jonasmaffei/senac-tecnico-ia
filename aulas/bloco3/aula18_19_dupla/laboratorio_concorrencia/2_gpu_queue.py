import datetime
import os
import subprocess
import sys
import time

SPOOL_DIR = os.path.join("reports", "gpu_queue_spool")
LOCK_DIR = os.path.join("reports", "gpu_exclusive.lockdir")
LOG_FILE = os.path.join("reports", "gpu_queue.log")

def log_msg(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted)
    os.makedirs("reports", exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def main():
    prioridade = sys.argv[1] if len(sys.argv) > 1 else "2"
    nome_job = sys.argv[2] if len(sys.argv) > 2 else f"job_{os.getpid()}"
    script = sys.argv[3] if len(sys.argv) > 3 else "train_job.py"
    extra_args = sys.argv[4:]

    os.makedirs(SPOOL_DIR, exist_ok=True)

    timestamp_ns = time.time_ns()
    ticket_filename = f"{prioridade}_{timestamp_ns}_{nome_job}"
    ticket_path = os.path.join(SPOOL_DIR, ticket_filename)

    with open(ticket_path, "w", encoding="utf-8") as f:
        f.write(f"{script} {' '.join(extra_args)}")

    log_msg(f"Job '{nome_job}' (prio={prioridade}) enfileirado: {ticket_filename}")

    # Aguardar vez na fila (ordenacao lexicografica)
    while True:
        arquivos = sorted(os.listdir(SPOOL_DIR))
        if arquivos and arquivos[0] == ticket_filename:
            break
        time.sleep(1)

    # Executar com exclusao mutua
    while True:
        try:
            os.mkdir(LOCK_DIR)
            break
        except FileExistsError:
            time.sleep(1)

    try:
        log_msg(f"Executando '{nome_job}' na GPU...")
        cmd = [sys.executable, script] + extra_args
        res = subprocess.run(cmd)
        log_msg(f"'{nome_job}' concluido (exit code={res.returncode})")
    finally:
        try:
            os.rmdir(LOCK_DIR)
        except Exception:
            pass
        if os.path.exists(ticket_path):
            os.remove(ticket_path)

if __name__ == "__main__":
    main()
