#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# monitoramento_linux.py — O kernel como fonte de dados (pseudo-arquivos)
# ----------------------------------------------------------------------------
# OBJETIVO: mostrar que, no Linux, hardware e kernel são expostos como
# "pseudo-arquivos" — dá para lê-los como qualquer arquivo de texto.
#
#   /proc/cpuinfo  -> modelo do processador
#   /proc/meminfo  -> memória RAM em tempo real
#   /proc/uptime   -> tempo ligado
#   /sys/class/drm -> dispositivos gráficos (GPU)
#   /dev/nvidia*   -> dispositivos NVIDIA
#
# Como o laboratório é Windows, o script detecta o sistema: no Linux lê os
# pseudo-arquivos; no Windows usa psutil/PowerShell para mostrar o equivalente.
# Assim o conceito da aula nunca quebra.
#
# Uso:  python monitoramento_linux.py
# Requer: (nenhum obrigatório) — psutil opcional no Windows
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


# ---------------------------------------------------------------------------
# Linux: ler os pseudo-arquivos do kernel
# ---------------------------------------------------------------------------
def ler_arquivo(caminho):
    """Lê um pseudo-arquivo; devolve None se ele não existir."""
    try:
        with open(caminho, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return None


def monitorar_linux():
    print("[Linux] Lendo os pseudo-arquivos do kernel...\n")

    # ── /proc/cpuinfo: nome do processador ─────────────────────────────────
    cpuinfo = ler_arquivo("/proc/cpuinfo") or ""
    for linha in cpuinfo.splitlines():
        if "model name" in linha:
            print(f"  /proc/cpuinfo  -> CPU: {linha.split(':', 1)[1].strip()}")
            break

    # ── /proc/meminfo: RAM total e disponível ──────────────────────────────
    meminfo = ler_arquivo("/proc/meminfo") or ""
    for linha in meminfo.splitlines():
        if linha.startswith(("MemTotal", "MemAvailable")):
            chave, valor = linha.split(":", 1)
            mb = int(valor.strip().split()[0]) / 1024
            print(f"  /proc/meminfo  -> {chave}: {mb:,.0f} MB")

    # ── /proc/uptime: há quanto tempo o servidor está ligado ───────────────
    uptime = ler_arquivo("/proc/uptime")
    if uptime:
        horas = float(uptime.split()[0]) / 3600
        print(f"  /proc/uptime   -> ligado há {horas:.1f} horas")

    # ── /sys/class/drm: dispositivos gráficos (GPU) ────────────────────────
    if os.path.isdir("/sys/class/drm"):
        cards = [c for c in os.listdir("/sys/class/drm") if c.startswith("card")]
        print(f"  /sys/class/drm -> {len(cards)} dispositivo(s): {', '.join(cards) or 'nenhum'}")

    # ── /dev/nvidia*: dispositivos NVIDIA ──────────────────────────────────
    if os.path.isdir("/dev"):
        nvidia = [d for d in os.listdir("/dev") if d.startswith("nvidia")]
        print(f"  /dev/nvidia*   -> {', '.join(nvidia) or 'nenhum'}")


# ---------------------------------------------------------------------------
# Windows: mostrar o equivalente usando psutil/PowerShell
# ---------------------------------------------------------------------------
def monitorar_windows():
    print("[Windows] Sem /proc ou /sys. Mostrando o equivalente via psutil:\n")
    try:
        import psutil
    except ImportError:
        print("  Instale o psutil para ver CPU/RAM:  pip install psutil")
        print("  (No Colab:  !pip install psutil -q)")
        return

    # CPU
    marca = platform.processor() or "CPU"
    nucleos = psutil.cpu_count(logical=False) or "?"
    threads = psutil.cpu_count(logical=True) or "?"
    print(f"  CPU        -> {marca} ({nucleos} núcleos físicos / {threads} lógicos)")

    # RAM
    memoria = psutil.virtual_memory()
    print(f"  RAM        -> {memoria.used / 1024**3:.1f} GB usados "
          f"de {memoria.total / 1024**3:.1f} GB ({memoria.percent:.0f}%)")

    # Uptime (desde o boot)
    import time
    ligado_h = (time.time() - psutil.boot_time()) / 3600
    print(f"  Ligado há  -> {ligado_h:.1f} horas")


# ---------------------------------------------------------------------------
# GPU (vale para os dois sistemas): nvidia-smi, se existir
# ---------------------------------------------------------------------------
def monitorar_gpu():
    print()
    if shutil.which("nvidia-smi"):
        saida = subprocess.run(
            ["nvidia-smi",
             "--query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total",
             "--format=csv,noheader"],
            capture_output=True, text=True,
        ).stdout.strip()
        print("[nvidia-smi] GPU(s) NVIDIA:")
        for linha in saida.splitlines():
            print(f"  {linha}")
    elif shutil.which("rocm-smi"):
        print("[rocm-smi] GPU(s) AMD:")
        print(subprocess.run(["rocm-smi"], capture_output=True, text=True).stdout)
    else:
        print("[GPU] Sem nvidia-smi/rocm-smi neste ambiente.")
        print("      Em Linux, as placas aparecem em /sys/class/drm e /dev/nvidia*.")


def main():
    print("=" * 66)
    print(" O kernel como fonte de dados: pseudo-arquivos e monitoramento")
    print("=" * 66)
    print(f"Sistema detectado: {platform.system()}\n")

    if platform.system() == "Linux":
        monitorar_linux()
    else:
        monitorar_windows()

    monitorar_gpu()

    print()
    print("Ferramentas como htop, nvtop e gpustat leem esses mesmos pseudo-arquivos.")
    print("Use tmux/screen para manter o monitoramento ativo após desconectar o SSH.")


if __name__ == "__main__":
    main()
