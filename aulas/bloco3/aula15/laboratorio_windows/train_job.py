# ============================================================================
# train_job.py - job de "treinamento" simulado para testar a fila
# ----------------------------------------------------------------------------
# Uso:  python train_job.py --nome "Job A" --epocas 5
#
# Este script NAO treina um modelo de verdade: ele apenas imita o comportamento
# de um job longo (imprime o progresso por epoca e consome tempo). E o suficiente
# para observar a fila serializar os jobs.
#
# Se a biblioteca torch estiver instalada, faz uma multiplicacao de matrizes em
# cada epoca para gerar carga real (na GPU, se houver; senao na CPU). Sem torch,
# faz o mesmo com listas do Python. Assim a aula roda em qualquer maquina.
# ============================================================================

import argparse
import os
import random
import time

parser = argparse.ArgumentParser(description="Job de treinamento simulado")
parser.add_argument("--nome", default="Job", help="Nome do job")
parser.add_argument("--epocas", type=int, default=3, help="Numero de epocas")
parser.add_argument("--tamanho", type=int, default=1024, help="Tamanho da matriz")
args = parser.parse_args()

pid = os.getpid()
print(f"[{args.nome}] PID={pid} | Epocas={args.epocas} | inicio={time.strftime('%H:%M:%S')}")

# -- Verifica se o torch esta disponivel (e se ha GPU) -----------------------
try:
    import torch
    if torch.cuda.is_available():
        device = "cuda:0"
    elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    print(f"[{args.nome}] torch detectado - dispositivo: {device}")
except Exception:
    torch = None
    device = "cpu (listas Python)"
    print(f"[{args.nome}] torch nao instalado - carga simulada com listas Python")

# -- "Treinamento": repete por epoca fazendo uma conta pesada ----------------
for epoca in range(1, args.epocas + 1):
    if torch is not None:
        # Multiplicacao de matrizes (carga real de GPU/CPU, quando possivel)
        a = torch.randn(args.tamanho, args.tamanho)
        b = torch.randn(args.tamanho, args.tamanho)
        if device.startswith("cuda"):
            a, b = a.to(device), b.to(device)
        _ = a @ b
        if device.startswith("cuda"):
            torch.cuda.synchronize()
    else:
        # Sem torch: uma soma pesada em Python puro so para gastar tempo
        n = args.tamanho
        _ = sum(i * j for i in range(min(n, 300)) for j in range(min(n, 300)))

    loss = 1.0 / (epoca * random.uniform(0.8, 1.2))
    print(f"[{args.nome}] Epoca {epoca}/{args.epocas} | loss={loss:.4f}")
    time.sleep(random.uniform(0.5, 1.5))

print(f"[{args.nome}] Treinamento concluido! fim={time.strftime('%H:%M:%S')}")
