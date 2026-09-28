#!/usr/bin/env python3
# train_job.py — Job de treinamento simulado para testar a fila de GPU
# Uso: python3 train_job.py --nome "Job A" --epocas 5 --gpu 0

import argparse
import time
import random
import os

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nome", default="Job", help="Nome do job")
    parser.add_argument("--epocas", type=int, default=3, help="Número de épocas")
    parser.add_argument("--gpu", type=int, default=0, help="Índice da GPU")
    args = parser.parse_args()

    pid = os.getpid()
    print(f"[{args.nome}] PID={pid} | GPU={args.gpu} | Épocas={args.epocas}")

    device = f"cuda:{args.gpu}" if HAS_TORCH and torch.cuda.is_available() else "cpu"
    print(f"[{args.nome}] Dispositivo ativo: {device}")

    for epoca in range(1, args.epocas + 1):
        if HAS_TORCH and torch.cuda.is_available():
            a = torch.randn(2048, 2048, device=device)
            b = torch.randn(2048, 2048, device=device)
            c = torch.mm(a, b)
            torch.cuda.synchronize()

        loss = 1.0 / (epoca * random.uniform(0.8, 1.2))
        print(f"[{args.nome}] Época {epoca}/{args.epocas} | loss={loss:.4f}")
        time.sleep(random.uniform(0.5, 1.2))

    print(f"[{args.nome}] Treinamento concluído com sucesso!")

if __name__ == "__main__":
    main()
