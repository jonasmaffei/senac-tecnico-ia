# -*- coding: utf-8 -*-
# ============================================================================
# lib_hw.py — Descobrir o hardware REAL desta máquina (CPU, RAM e GPU)
# ----------------------------------------------------------------------------
# Biblioteca compartilhada pelos scripts do laboratório. Roda no Windows, no
# Linux e no Colab. Não depende de GPU: se não houver, informa 'simulado'.
#
# Uso:
#   import lib_hw
#   lib_hw.imprimir_resumo()
# ============================================================================

import os
import platform
import shutil
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def info_cpu():
    """Modelo do processador e nº de núcleos (físicos e lógicos)."""
    modelo = platform.processor() or platform.machine() or "CPU"
    logicos = os.cpu_count() or 1
    fisicos = None
    try:
        import psutil
        fisicos = psutil.cpu_count(logical=False)
    except ImportError:
        pass
    return {"modelo": modelo, "logicos": logicos, "fisicos": fisicos}


def info_ram():
    """RAM total/usada em GB (via psutil, se disponível)."""
    try:
        import psutil
        m = psutil.virtual_memory()
        return {"total_gb": round(m.total / 1024**3, 1),
                "usada_gb": round(m.used / 1024**3, 1),
                "pct": m.percent}
    except ImportError:
        return None


def info_gpu_windows():
    """Nome da(s) GPU(s) no Windows, via PowerShell (Win32_VideoController)."""
    ps = shutil.which("powershell.exe") or shutil.which("powershell")
    if not ps:
        return []
    script = ("Get-CimInstance Win32_VideoController | "
              "Select-Object -ExpandProperty Name")
    try:
        saida = subprocess.run([ps, "-NoProfile", "-Command", script],
                               capture_output=True, text=True, timeout=20)
        return [l.strip() for l in saida.stdout.splitlines() if l.strip()]
    except Exception:
        return []


def info_gpu():
    """Melhor esforço para nomear a GPU: nvidia-smi → Windows → desconhecida."""
    # 1) NVIDIA
    smi = shutil.which("nvidia-smi") or shutil.which("nvidia-smi.exe")
    if smi:
        try:
            saida = subprocess.run(
                [smi, "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=20).stdout.strip()
            if saida:
                return saida.splitlines()[0].strip()
        except Exception:
            pass
    # 2) AMD/Intel no Windows
    if platform.system() == "Windows":
        gpus = info_gpu_windows()
        if gpus:
            return gpus[0]
    # 3) AMD no Linux
    if shutil.which("rocminfo"):
        return "GPU AMD (rocminfo disponível)"
    return "não identificada"


def detectar_backend():
    """Qual 'engine' de cálculo dá para usar: CuPy → PyTorch CUDA → DirectML → NumPy."""
    try:
        import cupy  # noqa: F401
        if cupy.cuda.runtime.getDeviceCount() > 0:
            return "CuPy (GPU)"
    except Exception:
        pass
    try:
        import torch
        if torch.cuda.is_available():
            return "PyTorch CUDA (GPU)"
    except Exception:
        pass
    try:
        import torch_directml  # noqa: F401
        return "PyTorch DirectML (GPU AMD/Windows)"
    except Exception:
        pass
    return "NumPy (CPU SIMD)"


def resumo():
    """Devolve tudo num dicionário."""
    cpu = info_cpu()
    return {
        "sistema": f"{platform.system()} {platform.release()}",
        "cpu_modelo": cpu["modelo"],
        "cpu_fisicos": cpu["fisicos"],
        "cpu_logicos": cpu["logicos"],
        "ram": info_ram(),
        "gpu": info_gpu(),
        "backend": detectar_backend(),
    }


def imprimir_resumo():
    info = resumo()
    print("=" * 64)
    print(" HARDWARE DESTA MAQUINA")
    print("=" * 64)
    print(f" Sistema : {info['sistema']}")
    print(f" CPU     : {info['cpu_modelo']}")
    print(f" Nucleos : {info['cpu_fisicos'] or '?'} fisicos / {info['cpu_logicos']} logicos")
    if info["ram"]:
        print(f" RAM     : {info['ram']['usada_gb']} GB usados de "
              f"{info['ram']['total_gb']} GB ({info['ram']['pct']}%)")
    print(f" GPU     : {info['gpu']}")
    print(f" Backend : {info['backend']}")
    print("=" * 64)


if __name__ == "__main__":
    imprimir_resumo()
