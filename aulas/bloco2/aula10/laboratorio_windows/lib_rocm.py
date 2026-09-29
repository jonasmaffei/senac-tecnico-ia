# -*- coding: utf-8 -*-
# ============================================================================
# lib_rocm.py - Diagnostico de portabilidade CUDA <-> ROCm (sem quebrar)
# ----------------------------------------------------------------------------
# As GPUs AMD executam codigo PyTorch escrito para CUDA atraves da camada HIP,
# que emula a API `torch.cuda`. Este modulo centraliza a deteccao do backend
# (CUDA nativo NVIDIA ou ROCm/HIP AMD) e permite que os scripts continuem
# rodando mesmo numa maquina sem GPU nenhuma (ex.: o laboratorio Windows).
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
        # Em ROCm, o PyTorch preenche torch.version.hip (e nao .cuda).
        if getattr(torch.version, "hip", None):
            return "ROCm/HIP"
        return "CUDA"
    return "CPU-torch"


def diagnostico():
    """Monta um dicionario com o ambiente de deep learning disponivel."""
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
    """Imprime o diagnostico de forma legivel."""
    print("=" * 60)
    print("  DIAGNOSTICO DO AMBIENTE DE DEEP LEARNING")
    print("=" * 60)
    print(f"Sistema Operacional : {info['sistema']}")
    print(f"Versao do Python    : {info['python']}")
    print(f"Versao do PyTorch   : {info['torch'] or '(nao instalado)'}")

    backend_nome = info["backend"]
    if backend_nome == "sem-torch":
        print("GPU Disponivel?     : NAO (PyTorch nao instalado)")
    elif backend_nome == "CPU-torch":
        print("GPU Disponivel?     : NAO (Executando em CPU)")
    else:
        print("GPU Disponivel?     : SIM")
        print(f"Nome do Dispositivo : {info['gpu']}")
        print(f"VRAM Total          : {info['vram_gb']} GB")
        rotulo = "ROCm / HIP (AMD)" if backend_nome == "ROCm/HIP" else "CUDA Nativo (NVIDIA)"
        print(f"Backend Detectado   : {rotulo} - {info['versao_cuda_ou_hip']}")
    print("=" * 60)


def explicar_sem_gpu():
    """Mensagem quando nao ha GPU (CUDA/ROCm) nem torch."""
    print("Sem GPU CUDA/ROCm (ou sem PyTorch) neste ambiente.")
    print("Os numeros de benchmark abaixo sao de REFERENCIA para comparacao.")
    print("Em um servidor com GPU (Colab NVIDIA ou Docker rocm/pytorch), o")
    print("MESMO codigo Python roda sem alteracoes.")


def cabecalho_ascii():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


if __name__ == "__main__":
    cabecalho_ascii()
    imprimir(diagnostico())
