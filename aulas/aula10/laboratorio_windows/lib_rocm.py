# -*- coding: utf-8 -*-
# ============================================================================
# lib_rocm.py — Diagnóstico de portabilidade CUDA ↔ ROCm (sem quebrar)
# ----------------------------------------------------------------------------
# As GPUs AMD executam código PyTorch escrito para CUDA através da camada HIP,
# que emula a API `torch.cuda`. Este módulo centraliza a detecção do backend
# (CUDA nativo NVIDIA ou ROCm/HIP AMD) e permite que os scripts continuem
# rodando mesmo numa máquina sem GPU nenhuma (ex.: o laboratório Windows).
#
# Uso:
#   import lib_rocm
#   info = lib_rocm.diagnostico()
#   print(info["backend"])
# ============================================================================

import platform
import sys


def tem_torch():
    try:
        import torch  # noqa: F401
        return True
    except ImportError:
        return False


def backend():
    """Devolve 'CUDA', 'ROCm/HIP', 'CPU-torch' ou 'sem-torch'."""
    try:
        import torch
    except ImportError:
        return "sem-torch"

    if torch.cuda.is_available():
        # Em ROCm, o PyTorch preenche torch.version.hip (e não .cuda).
        if getattr(torch.version, "hip", None):
            return "ROCm/HIP"
        return "CUDA"
    return "CPU-torch"


def diagnostico():
    """Monta um dicionário com o ambiente de deep learning disponível."""
    info = {
        "sistema": f"{platform.system()} {platform.release()}",
        "python": platform.python_version(),
        "torch": None,
        "backend": backend(),
        "gpu": None,
        "vram_gb": None,
        "versao_cuda_ou_hip": None,
    }

    if not tem_torch():
        return info

    import torch
    info["torch"] = torch.__version__

    if torch.cuda.is_available():
        info["gpu"] = torch.cuda.get_device_name(0)
        info["vram_gb"] = round(
            torch.cuda.get_device_properties(0).total_memory / (1024 ** 3), 2
        )
        if getattr(torch.version, "hip", None):
            info["versao_cuda_ou_hip"] = f"HIP {torch.version.hip}"
        else:
            info["versao_cuda_ou_hip"] = f"CUDA {torch.version.cuda}"
    return info


def imprimir(info):
    """Imprime o diagnóstico de forma legível."""
    print("=" * 60)
    print("  DIAGNÓSTICO DO AMBIENTE DE DEEP LEARNING")
    print("=" * 60)
    print(f"Sistema Operacional : {info['sistema']}")
    print(f"Versão do Python    : {info['python']}")
    print(f"Versão do PyTorch   : {info['torch'] or '(não instalado)'}")

    backend_nome = info["backend"]
    if backend_nome == "sem-torch":
        print("GPU Disponível?     : NÃO (PyTorch não instalado)")
    elif backend_nome == "CPU-torch":
        print("GPU Disponível?     : NÃO (Executando em CPU)")
    else:
        print("GPU Disponível?     : SIM")
        print(f"Nome do Dispositivo : {info['gpu']}")
        print(f"VRAM Total          : {info['vram_gb']} GB")
        rotulo = "ROCm / HIP (AMD)" if backend_nome == "ROCm/HIP" else "CUDA Nativo (NVIDIA)"
        print(f"Backend Detectado   : {rotulo} - {info['versao_cuda_ou_hip']}")
    print("=" * 60)


def explicar_sem_gpu():
    """Mensagem quando não há GPU (CUDA/ROCm) nem torch."""
    print("Sem GPU CUDA/ROCm (ou sem PyTorch) neste ambiente.")
    print("Os números de benchmark abaixo são de REFERÊNCIA para comparação.")
    print("Em um servidor com GPU (Colab NVIDIA ou Docker rocm/pytorch), o")
    print("MESMO código Python roda sem alterações.")


def cabecalho_ascii():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


if __name__ == "__main__":
    cabecalho_ascii()
    imprimir(diagnostico())
