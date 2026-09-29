#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# diagnostico_portabilidade.py - CUDA, HIP e rocm-smi: o que roda onde
# ----------------------------------------------------------------------------
# OBJETIVO: mostrar de forma didatica a equivalencia entre os ecossistemas
# NVIDIA (CUDA) e AMD (ROCm), e detectar o que existe no ambiente atual.
#
#   CUDA (NVIDIA)   ->  ROCm/HIP (AMD)
#   nvcc            ->  hipcc
#   cuBLAS          ->  rocBLAS
#   cuDNN           ->  MIOpen
#   cuFFT           ->  rocFFT
#   nvidia-smi      ->  rocm-smi
#   nvidia/cuda     ->  rocm/pytorch (imagem Docker)
#
# Uso:  python diagnostico_portabilidade.py
# Requer: (nenhum obrigatorio)
# ============================================================================

import shutil
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import lib_rocm

EQUIVALENCIAS = [
    ("Compilador",        "nvcc",                 "hipcc"),
    ("Algebra linear",    "cuBLAS",               "rocBLAS"),
    ("Deep learning",     "cuDNN",                "MIOpen"),
    ("FFT",               "cuFFT",                "rocFFT"),
    ("Numeros aleatorios","cuRAND",               "rocRAND"),
    ("Profiling",         "Nsight / nvprof",      "Radeon GPU Profiler"),
    ("Monitoramento",     "nvidia-smi",           "rocm-smi"),
    ("Container",         "nvidia/cuda",          "rocm/pytorch"),
    ("Kernel (prefixo)",  "cudaMalloc / blockIdx","hipMalloc / hipBlockIdx"),
    ("Sincronizacao",     "__syncthreads()",      "__syncthreads() (igual!)"),
]


def detectar_ferramentas():
    """Verifica quais utilitarios de GPU estao instalados no PATH."""
    print("\nFerramentas encontradas neste ambiente:")
    for nome in ("nvidia-smi", "rocm-smi", "rocminfo", "hipcc", "nvcc"):
        caminho = shutil.which(nome)
        estado = caminho if caminho else "nao encontrado"
        print(f"  {nome:<12} -> {estado}")


def tabela_equivalentes():
    """Imprime a tabela de equivalencia CUDA <-> ROCm."""
    print("\nEquivalencia CUDA (NVIDIA) x ROCm (AMD):")
    print(f"  {'Conceito':<20} {'CUDA':<30} {'ROCm/HIP'}")
    print("  " + "-" * 78)
    for conceito, cuda_eq, rocm_eq in EQUIVALENCIAS:
        print(f"  {conceito:<20} {cuda_eq:<30} {rocm_eq}")


def main():
    lib_rocm.cabecalho_ascii()
    print("=" * 64)
    print(" Portabilidade CUDA x ROCm: o que muda e o que NAO muda")
    print("=" * 64)

    info = lib_rocm.diagnostico()
    lib_rocm.imprimir(info)
    detectar_ferramentas()
    tabela_equivalentes()

    print()
    print("Mensagem central: em PyTorch, o codigo Python e IDENTICO.")
    print("`torch.cuda.is_available()` retorna True tambem no ROCm - porque")
    print("a camada HIP emula a API CUDA. O que muda e so o ambiente:")
    print("  - NVIDIA: driver CUDA + nvcc")
    print("  - AMD:    ROCm + hipcc + rocm-smi")
    print("  - Em ambos os casos, use containers prontos (nvidia/cuda ou rocm/pytorch).")


if __name__ == "__main__":
    main()
