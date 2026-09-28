# ============================================================================
# train_job.py — job de "treinamento" simulado para testar a fila
# ----------------------------------------------------------------------------
# Uso:  python train_job.py --nome "Job A" --epocas 5
#
# Este script NÃO treina um modelo de verdade: ele apenas imita o comportamento
# de um job longo (imprime o progresso por época e consome tempo). É o suficiente
# para observar a fila serializar os jobs.
#
# Se a biblioteca torch estiver instalada, faz uma multiplicação de matrizes em
# cada época para gerar carga real (na GPU, se houver; senão na CPU). Sem torch,
# faz o mesmo com listas do Python. Assim a aula roda em qualquer máquina.
# ============================================================================

import argparse
import os
import random
import time

parser = argparse.ArgumentParser(description="Job de treinamento simulado")
parser.add_argument("--nome", default="Job", help="Nome do job")
parser.add_argument("--epocas", type=int, default=3, help="Número de épocas")
parser.add_argument("--tamanho", type=int, default=1024, help="Tamanho da matriz")
args = parser.parse_args()

pid = os.getpid()
print(f"[{args.nome}] PID={pid} | Épocas={args.epocas} | inicio={time.strftime('%H:%M:%S')}")

# ── Verifica se o torch está disponível (e se há GPU) ───────────────────────
try:
    import torch
    if torch.cuda.is_available():
        device = "cuda:0"
    elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    print(f"[{args.nome}] torch detectado — dispositivo: {device}")
except Exception:
    torch = None
    device = "cpu (listas Python)"
    print(f"[{args.nome}] torch não instalado — carga simulada com listas Python")

# ── "Treinamento": repete por época fazendo uma conta pesada ────────────────
for epoca in range(1, args.epocas + 1):
    if torch is not None:
        # Multiplicação de matrizes (carga real de GPU/CPU, quando possível)
        a = torch.randn(args.tamanho, args.tamanho)
        b = torch.randn(args.tamanho, args.tamanho)
        if device.startswith("cuda"):
            a, b = a.to(device), b.to(device)
        _ = a @ b
        if device.startswith("cuda"):
            torch.cuda.synchronize()
    else:
        # Sem torch: uma soma pesada em Python puro só para gastar tempo
        n = args.tamanho
        _ = sum(i * j for i in range(min(n, 300)) for j in range(min(n, 300)))

    loss = 1.0 / (epoca * random.uniform(0.8, 1.2))
    print(f"[{args.nome}] Época {epoca}/{args.epocas} | loss={loss:.4f}")
    time.sleep(random.uniform(0.5, 1.5))

print(f"[{args.nome}] Treinamento concluído! fim={time.strftime('%H:%M:%S')}")
