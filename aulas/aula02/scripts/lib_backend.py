# -*- coding: utf-8 -*-
# ============================================================================
# lib_backend.py — detecção automática de backend de processamento
# ----------------------------------------------------------------------------
# Este arquivo é importado pelos scripts da Aula 02 para que o MESMO código
# rode em qualquer ambiente:
#
#   - Google Colab (GPU NVIDIA)  -> usa CuPy (SIMD em GPU)
#   - Linux com ROCm (AMD)       -> usa CuPy-ROCm / PyTorch
#   - Windows com GPU AMD        -> usa PyTorch-DirectML, se instalado
#   - QUALQUER máquina (padrão)  -> usa NumPy (SIMD em CPU, via AVX/SSE)
#
# O objetivo didático: mostrar que o código é o mesmo, só a "engine" de
# paralelismo muda. NumPy já usa instruções SIMD por baixo dos panos.
#
# Uso:
#   from lib_backend import detectar_backend, xp, BACKEND
#   xp.arange(10)   # xp é numpy OU cupy, conforme o backend detectado
# ============================================================================

import importlib

# Ordem de preferência: GPU real primeiro, CPU como rede de segurança.
# Cada item: (nome amigável, módulo Python, função que confirma disponibilidade)
_CANDIDATOS = [
    ("CuPy (GPU NVIDIA/ROCm)", "cupy", lambda m: m.cuda.runtime.getDeviceCount() > 0),
    ("PyTorch CUDA (GPU NVIDIA)", "torch", None),   # tratado à parte abaixo
    ("PyTorch DirectML (GPU AMD no Windows)", "torch_directml", None),
]

BACKEND = "NumPy (CPU SIMD)"
GPU_NOME = ""
xp = None            # numpy ou cupy
torch = None         # preenchido se o backend for PyTorch


def _numa_gpu_valida(mod):
    """Confirma que o CuPy encontrou pelo menos 1 dispositivo GPU."""
    try:
        return mod.cuda.runtime.getDeviceCount() > 0
    except Exception:
        return False


def detectar_backend():
    """Escolhe o melhor backend disponível e ajusta as variáveis globais.

    Devolve o módulo a ser usado como 'xp' (numpy ou cupy) e imprime um resumo.
    """
    global BACKEND, GPU_NOME, xp, torch

    # 1) CuPy — melhor caso: arrays acelerados por GPU com a API do NumPy
    try:
        cupy = importlib.import_module("cupy")
        if _numa_gpu_valida(cupy):
            BACKEND = "CuPy (GPU)"
            xp = cupy
            try:
                GPU_NOME = cupy.cuda.runtime.getDeviceProperties(0)["name"].decode()
            except Exception:
                GPU_NOME = "GPU (CuPy)"
            _resumo()
            return xp
    except Exception:
        pass

    # 2) PyTorch com CUDA (Colab também oferece essa opção)
    try:
        import torch as _torch
        torch = _torch
        if _torch.cuda.is_available():
            BACKEND = "PyTorch CUDA (GPU)"
            GPU_NOME = _torch.cuda.get_device_name(0)
            xp = _TorchXP(_torch)          # wrapper mínimo com API parecida com NumPy
            _resumo()
            return xp
    except Exception:
        torch = None

    # 3) PyTorch-DirectML (GPU AMD no Windows, quando instalado)
    try:
        import torch_directml as dml
        if dml.device_count() > 0:
            BACKEND = "PyTorch DirectML (GPU AMD/Windows)"
            GPU_NOME = dml.device_name(0)
            xp = _DirectMLXP(dml)
            _resumo()
            return xp
    except Exception:
        pass

    # 4) Fallback universal: NumPy (usa SIMD da CPU: AVX/SSE)
    import numpy as _np
    BACKEND = "NumPy (CPU SIMD)"
    GPU_NOME = "CPU"
    xp = _np
    _resumo()
    return xp


def _resumo():
    print("=" * 64)
    print(f" Backend de processamento: {BACKEND}")
    if BACKEND == "NumPy (CPU SIMD)":
        print(" Nenhuma GPU acessível aqui — usando o SIMD da própria CPU.")
        print(" (No Colab com T4 GPU, este mesmo script usaria CuPy.)")
    else:
        print(f" Dispositivo: {GPU_NOME}")
    print("=" * 64)


def info():
    """Devolve o estado atual como dicionário.

    Use esta função (em vez de importar as variáveis) porque o backend é
    definido apenas quando `detectar_backend()` roda. Ex.:
        import lib_backend
        xp = lib_backend.detectar_backend()
        print(lib_backend.info()["backend"])
    """
    return {"backend": BACKEND, "dispositivo": GPU_NOME, "xp": xp}


# ---------------------------------------------------------------------------
# Wrappers mínimos: expõem só o que a Aula 02 usa (arange, asarray, ...)
# e convertem o resultado de volta para NumPy, simplificando o exemplo.
# ---------------------------------------------------------------------------
class _TorchXP:
    def __init__(self, torch):
        self._t = torch

    def arange(self, n, dtype=None):
        return self._t.arange(n, dtype=self._t.float32 if dtype is None else dtype)

    def __getattr__(self, nome):
        return getattr(self._t, nome)


class _DirectMLXP:
    def __init__(self, dml):
        self._dml = dml
        self._device = dml.device()

    def arange(self, n, dtype=None):
        import torch
        return torch.arange(n, dtype=torch.float32, device=self._device)

    def __getattr__(self, nome):
        import torch
        return getattr(torch, nome)


if __name__ == "__main__":
    # Executar este arquivo sozinho apenas mostra qual backend foi detectado.
    detectar_backend()
