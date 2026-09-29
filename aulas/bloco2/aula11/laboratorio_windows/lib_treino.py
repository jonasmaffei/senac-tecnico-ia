# -*- coding: utf-8 -*-
# ============================================================================
# lib_treino.py - Deteccao de backend e benchmark de treino (portatil)
# ----------------------------------------------------------------------------
# Este modulo centraliza a deteccao do dispositivo (GPU NVIDIA/CUDA, GPU AMD via
# ROCm ou CPU) e executa um treino comparativo FP32 vs. FP16. O MESMO codigo roda
# no Colab (GPU) e no laboratorio Windows/AMD: sem GPU, ele mostra os numeros de
# REFERENCIA em vez de quebrar.
#
# Uso:
#   import lib_treino
#   info = lib_treino.diagnostico()
#   lib_treino.imprimir(info)
# ============================================================================

import platform
import sys
import time


def cabecalho_ascii():
    """Forca saida UTF-8 quando possivel (console Windows cp1252 quebra acentos)."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


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
    """Monta um dicionario com o ambiente de treino disponivel."""
    info = {
        "sistema": f"{platform.system()} {platform.release()}",
        "python": platform.python_version(),
        "torch": None,
        "backend": backend(),
        "gpu": None,
        "vram_gb": None,
        "versao": None,
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
            info["versao"] = f"HIP {torch.version.hip}"
        else:
            info["versao"] = f"CUDA {torch.version.cuda}"
    return info


def imprimir(info):
    print("=" * 64)
    print("  DIAGNOSTICO DO AMBIENTE DE TREINO")
    print("=" * 64)
    print(f"Sistema Operacional : {info['sistema']}")
    print(f"Versao do Python    : {info['python']}")
    print(f"Versao do PyTorch   : {info['torch'] or '(nao instalado)'}")
    if info["backend"] in ("CUDA", "ROCm/HIP"):
        rotulo = "CUDA Nativo (NVIDIA)" if info["backend"] == "CUDA" else "ROCm / HIP (AMD)"
        print("GPU Disponivel?     : SIM")
        print(f"Nome do Dispositivo : {info['gpu']}")
        print(f"VRAM Total          : {info['vram_gb']} GB")
        print(f"Backend Detectado   : {rotulo} - {info['versao']}")
    else:
        print("GPU Disponivel?     : NAO (executando em CPU)")
    print("=" * 64)


def criar_modelo(dispositivo):
    """CNN simples de visao computacional (entrada 224x224, 10 classes)."""
    import torch.nn as nn
    return nn.Sequential(
        nn.Conv2d(3, 32, kernel_size=3, padding=1), nn.BatchNorm2d(32), nn.ReLU(),
        nn.AdaptiveAvgPool2d((1, 1)), nn.Flatten(), nn.Linear(32, 10),
    ).to(dispositivo)


def treinar(dispositivo, usar_fp16=False, lotes=20, tamanho=64):
    """Treina 'lotes' lotes sinteticos e devolve o throughput (imgs/s)."""
    import torch
    import torch.nn as nn

    modelo = criar_modelo(dispositivo)
    otimizador = torch.optim.SGD(modelo.parameters(), lr=0.01)
    criterio = nn.CrossEntropyLoss()
    usa_gpu = dispositivo.type == "cuda"
    scaler = torch.amp.GradScaler("cuda") if (usar_fp16 and usa_gpu) else None

    # Warm-up: 1 lote fora do cronometro (a 1a iteracao compila kernels na GPU).
    x = torch.randn(tamanho, 3, 224, 224, device=dispositivo)
    modelo(x)
    if usa_gpu:
        torch.cuda.synchronize()

    inicio = time.perf_counter()
    for _ in range(lotes):
        imgs = torch.randn(tamanho, 3, 224, 224, device=dispositivo)
        labels = torch.randint(0, 10, (tamanho,), device=dispositivo)
        otimizador.zero_grad()
        if usar_fp16 and usa_gpu:
            with torch.amp.autocast("cuda"):
                perda = criterio(modelo(imgs), labels)
            scaler.scale(perda).backward()
            scaler.step(otimizador)
            scaler.update()
        else:
            perda = criterio(modelo(imgs), labels)
            perda.backward()
            otimizador.step()
    if usa_gpu:
        torch.cuda.synchronize()
    return lotes * tamanho / (time.perf_counter() - inicio)


def referencia_t4():
    """Numeros de referencia medidos numa NVIDIA T4 (para uso sem GPU)."""
    return {"fp32": 180.4, "fp16": 341.2, "vram32": 420.0, "vram16": 260.0}


if __name__ == "__main__":
    cabecalho_ascii()
    imprimir(diagnostico())
