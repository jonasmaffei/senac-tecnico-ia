import argparse
import os
import random
import sys
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nome", default="Job", help="Nome do job")
    parser.add_argument("--epocas", type=int, default=3, help="Número de épocas")
    parser.add_argument("--gpu", type=int, default=0, help="Índice da GPU")
    args = parser.parse_args()

    pid = os.getpid()
    print(f"[{args.nome}] PID={pid} | GPU={args.gpu} | Épocas={args.epocas}")

    for epoca in range(1, args.epocas + 1):
        loss = 1.0 / (epoca * random.uniform(0.8, 1.2))
        print(f"[{args.nome}] Época {epoca}/{args.epocas} | loss={loss:.4f}")
        time.sleep(random.uniform(0.8, 1.5))

    print(f"[{args.nome}] Treinamento concluído com sucesso!")

if __name__ == "__main__":
    main()
