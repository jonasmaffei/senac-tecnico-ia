# -*- coding: utf-8 -*-
# ============================================================================
# lib_backend.py - deteccao automatica de backend de processamento
# ----------------------------------------------------------------------------
# Este arquivo e importado pelos scripts da Aula 03 para que o MESMO codigo
# rode em qualquer ambiente (mesmo padrao da Aula 02):
#
#   - Google Colab (GPU NVIDIA)  -> usa CuPy (memoria na VRAM)
#   - Linux com ROCm (AMD)       -> usa CuPy-ROCm / PyTorch
#   - Windows com GPU AMD        -> usa PyTorch-DirectML, se instalado
#   - QUALQUER maquina (padrao)  -> usa NumPy (memoria na RAM)
#
# O objetivo didatico: mostrar que o codigo e o mesmo; o que muda e ONDE os
# dados ficam (RAM do host x VRAM da placa). NumPy trabalha na RAM; CuPy
# trabalha na VRAM - e a copia entre as duas passa pelo barramento PCIe.
#
# Uso:
#   from lib_backend import detectar_backend
#   xp = detectar_backend()   # xp e numpy OU cupy, conforme o backend
# ============================================================================

import importlib

# Ordem de preferencia: GPU real primeiro, CPU como rede de seguranca.
# Cada item: (nome amigavel, modulo Python)
_CANDIDATOS = [
    ("CuPy (GPU NVIDIA/ROCm)", "cupy"),
    ("PyTorch CUDA (GPU NVIDIA)", "torch"),
    ("PyTorch DirectML (GPU AMD no Windows)", "torch_directml"),
]

BACKEND = "NumPy (CPU/RAM)"
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
    """Escolhe o melhor backend disponivel e ajusta as variaveis globais.

    Devolve o modulo a ser usado como 'xp' (numpy ou cupy) e imprime um resumo.
    """
    global BACKEND, GPU_NOME, xp, torch

    # 1) CuPy - melhor caso: arrays na VRAM com a API parecida com o NumPy
    try:
        cupy = importlib.import_module("cupy")
        if _numa_gpu_valida(cupy):
            BACKEND = "CuPy (GPU/VRAM)"
            xp = cupy
            try:
                GPU_NOME = cupy.cuda.runtime.getDeviceProperties(0)["name"].decode()
            except Exception:
                GPU_NOME = "GPU (CuPy)"
            _resumo()
            return xp
    except Exception:
        pass

    # 2) PyTorch com CUDA (Colab tambem oferece essa opcao)
    try:
        import torch as _torch
        torch = _torch
        if _torch.cuda.is_available():
            BACKEND = "PyTorch CUDA (GPU/VRAM)"
            GPU_NOME = _torch.cuda.get_device_name(0)
            xp = _TorchXP(_torch)
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

    # 4) Fallback universal: NumPy na RAM (mostra a hierarquia pela CPU)
    import numpy as _np
    BACKEND = "NumPy (CPU/RAM)"
    GPU_NOME = "CPU"
    xp = _np
    _resumo()
    return xp


def _resumo():
    print("=" * 64)
    print(f" Backend de processamento: {BACKEND}")
    if BACKEND == "NumPy (CPU/RAM)":
        print(" Nenhuma GPU acessivel aqui - os dados ficam na RAM do host.")
        print(" (No Colab com T4 GPU, este mesmo script usaria a VRAM.)")
    else:
        print(f" Dispositivo: {GPU_NOME}  (dados na VRAM)")
    print("=" * 64)


def info():
    """Devolve o estado atual como dicionario.

    Use esta funcao (em vez de importar as variaveis) porque o backend e
    definido apenas quando `detectar_backend()` roda.
    """
    return {"backend": BACKEND, "dispositivo": GPU_NOME, "xp": xp}


# ---------------------------------------------------------------------------
# Wrappers minimos: expoem so o que a Aula 03 usa e simplificam o exemplo.
# ---------------------------------------------------------------------------
class _TorchXP:
    def __init__(self, torch):
        self._t = torch

    def zeros(self, n, dtype=None):
        return self._t.zeros(n, dtype=self._t.float32 if dtype is None else dtype)

    def __getattr__(self, nome):
        return getattr(self._t, nome)


class _DirectMLXP:
    def __init__(self, dml):
        self._dml = dml
        self._device = dml.device()

    def zeros(self, n, dtype=None):
        import torch
        return torch.zeros(n, dtype=torch.float32, device=self._device)

    def __getattr__(self, nome):
        import torch
        return getattr(torch, nome)


if __name__ == "__main__":
    # Executar este arquivo sozinho apenas mostra qual backend foi detectado.
    detectar_backend()
