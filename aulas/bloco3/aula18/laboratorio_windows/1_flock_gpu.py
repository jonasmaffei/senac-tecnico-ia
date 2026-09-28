import datetime
import os
import subprocess
import sys
import time

LOCK_DIR = os.path.join("reports", "gpu_lock.lockdir")

def adquirir_lock_atomiic():
    pid = os.getpid()
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] PID {pid} aguardando lock da GPU...")

    os.makedirs("reports", exist_ok=True)
    while True:
        try:
            os.mkdir(LOCK_DIR)
            print(f"[{ts}] PID {pid} adquiriu lock exclusivo na GPU.")
            break
        except FileExistsError:
            time.sleep(1)

def liberar_lock_atomiic():
    try:
        os.rmdir(LOCK_DIR)
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Lock liberado com sucesso.")
    except Exception as e:
        print(f"Aviso ao liberar lock: {e}")

def main():
    script = sys.argv[1] if len(sys.argv) > 1 else "train_job.py"
    args = sys.argv[2:]

    adquirir_lock_atomiic()
    try:
        cmd = [sys.executable, script] + args
        res = subprocess.run(cmd)
        sys.exit(res.returncode)
    finally:
        liberar_lock_atomiic()

if __name__ == "__main__":
    main()
