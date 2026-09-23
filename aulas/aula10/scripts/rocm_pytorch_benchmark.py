#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# rocm_pytorch_benchmark.py — Diagnóstico e benchmark portável (CUDA ↔ ROCm)
# ----------------------------------------------------------------------------
# OBJETIVO: verificar a afirmação do engenheiro sênior: "o PyTorch em CUDA roda
# em GPUs AMD via ROCm sem mudar uma linha de código Python".
#
# O script:
#   1. Diagnostica o ambiente (CUDA nativo, ROCm/HIP ou CPU).
#   2. Mede a multiplicação de matrizes (matmul).
#   3. Treina por alguns batches uma ResNet-18 sintética e mede o throughput.
#
# O MESMO código roda em NVIDIA (CUDA) e AMD (ROCm) — muda só o hardware.
#
# Uso:  python rocm_pytorch_benchmark.py
# Requer: torch, torchvision (opcionais — sem eles, mostra a referência)
# ============================================================================

import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import lib_rocm


def benchmark_matmul(N=2048):
    """Multiplicação de matrizes N x N: GPU vs. CPU, se houver."""
    import torch

    dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
    A = torch.randn(N, N, device=dispositivo, dtype=torch.float32)
    B = torch.randn(N, N, device=dispositivo, dtype=torch.float32)

    def medir(device):
        a = A.to(device)
        b = B.to(device)
        if device == "cuda":
            torch.cuda.synchronize()
        inicio = time.perf_counter()
        for _ in range(20):
            _ = torch.matmul(a, b)
        if device == "cuda":
            torch.cuda.synchronize()
        return (time.perf_counter() - inicio) / 20

    t_gpu = medir(dispositivo)
    tflops = 2 * N ** 3 / t_gpu / 1e12
    print(f"\nMatMul {N}x{N} em {dispositivo.upper()}: {t_gpu*1000:.2f} ms | {tflops:.2f} TFLOPS")

    if dispositivo == "cuda":
        t_cpu = medir("cpu")
        print(f"MatMul {N}x{N} na CPU          : {t_cpu*1000:.2f} ms")
        print(f"Speedup GPU/CPU                : {t_cpu/t_gpu:.1f}x")


def _cnn_simples(nn):
    """Rede convolucional pequena, usada como fallback sem torchvision.

    Mantém o mesmo formato de entrada (3x224x224) e uma perda de classificação,
    para demonstrar o throughput de treino mesmo sem a ResNet-18.
    """
    return nn.Sequential(
        nn.Conv2d(3, 16, 3, stride=2, padding=1), nn.ReLU(),
        nn.Conv2d(16, 32, 3, stride=2, padding=1), nn.ReLU(),
        nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(32, 1000),
    )


def benchmark_resnet(n_batches=20, batch_size=64):
    """Treina batches sintéticos (ResNet-18 ou CNN simples) e mede imgs/s."""
    try:
        import torch
        import torch.nn as nn
    except ImportError:
        print("\nPyTorch não instalado — pulando o benchmark de treino.")
        return

    # Preferimos a ResNet-18; sem torchvision, usamos uma CNN simples equivalente.
    try:
        import torchvision
        modelo_base = torchvision.models.resnet18(weights=None)
        rotulo = "ResNet-18"
    except ImportError:
        modelo_base = _cnn_simples(nn)
        rotulo = "CNN simples (fallback sem torchvision)"

    dispositivo = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\nTreinando {rotulo} em: {dispositivo.type.upper()}")

    modelo = modelo_base.to(dispositivo)
    criterio = nn.CrossEntropyLoss()
    otimizador = torch.optim.SGD(modelo.parameters(), lr=0.01, momentum=0.9)
    modelo.train()

    forma = (batch_size, 3, 224, 224)   # formato ImageNet
    tempos = []

    # Warm-up: aquece a GPU (primeira passada é sempre mais lenta).
    if dispositivo.type == "cuda":
        _ = modelo(torch.randn(*forma, device=dispositivo))
        torch.cuda.synchronize()

    for i in range(n_batches):
        imgs = torch.randn(*forma, device=dispositivo)
        labels = torch.randint(0, 1000, (batch_size,), device=dispositivo)

        inicio = time.perf_counter()
        otimizador.zero_grad()
        saida = modelo(imgs)
        perda = criterio(saida, labels)
        perda.backward()
        otimizador.step()
        if dispositivo.type == "cuda":
            torch.cuda.synchronize()
        t = time.perf_counter() - inicio
        tempos.append(t)

        if (i + 1) % 5 == 0:
            print(f"  Batch {i+1:02d}/{n_batches} | Perda {perda.item():.4f} | "
                  f"{batch_size/t:.0f} imgs/s")

    t_medio = sum(tempos) / len(tempos)
    print(f"\nTempo médio/batch : {t_medio*1000:.1f} ms")
    print(f"Throughput médio  : {batch_size/t_medio:.1f} imagens/segundo")
    print("(O código é o mesmo em CUDA e ROCm — muda só o dispositivo.)")


def main():
    lib_rocm.cabecalho_ascii()
    info = lib_rocm.diagnostico()
    lib_rocm.imprimir(info)

    if info["backend"] in ("sem-torch", "CPU-torch"):
        lib_rocm.explicar_sem_gpu()
        print()
        print("Referência: o mesmo script, num servidor AMD com ROCm, detecta")
        print("'ROCm/HIP' e roda a ResNet-18 sem qualquer alteração no código.")

    if info["backend"] != "sem-torch":
        benchmark_matmul()
        benchmark_resnet()


if __name__ == "__main__":
    main()
