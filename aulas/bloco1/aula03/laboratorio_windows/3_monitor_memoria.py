#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# monitor_memoria.py - Medindo antes de otimizar
# ----------------------------------------------------------------------------
# OBJETIVO: "antes de otimizar, e preciso medir". Este script mostra:
#
#   1. O painel do nvidia-smi (nome, VRAM usada/total, utilizacao), se houver;
#   2. A memoria usada/instalada no host (psutil, se instalado);
#   3. Um exemplo simulado no MESMO formato, quando nao ha GPU NVIDIA.
#
# E o passo de DIAGNOSTICO da situacao de aprendizagem (GPU a 40%): antes de
# propor melhoria, olhamos os numeros.
#
# Uso:  python monitor_memoria.py
# Requer: (nenhum obrigatorio) - nvidia-smi e psutil sao usados se existirem
# ============================================================================

import shutil
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def painel_nvidia_smi():
    """Consulta GPU(s) NVIDIA via nvidia-smi. Devolve True se conseguiu medir."""
    if shutil.which("nvidia-smi") is None:
        return False

    # Pedimos so os campos que interessam, em CSV sem cabecalho e sem unidades.
    comando = [
        "nvidia-smi",
        "--query-gpu=index,name,memory.used,memory.total,utilization.gpu,temperature.gpu",
        "--format=csv,noheader,nounits",
    ]
    saida = subprocess.run(comando, capture_output=True, text=True).stdout.strip()
    if not saida:
        return False

    print("GPU(s) NVIDIA detectada(s):")
    print(f"  {'idx':>3} | {'nome':<22} | {'VRAM usada':>10} | {'VRAM total':>10} | {'util%':>5} | {'temp':>4}")
    print("  " + "-" * 68)
    for linha in saida.splitlines():
        partes = [p.strip() for p in linha.split(",")]
        if len(partes) != 6:
            continue
        idx, nome, usada, total, util, temp = partes
        print(f"  {idx:>3} | {nome[:22]:<22} | {usada:>7} MB | {total:>7} MB | {util:>5} | {temp:>3}C")
    return True


def memoria_host():
    """Mostra a memoria do host (RAM) usando psutil, se estiver instalado."""
    try:
        import psutil
    except ImportError:
        print("Detalhes da memoria do host: instale o psutil")
        print("   (no Colab:  !pip install psutil -q)")
        return
    info = psutil.virtual_memory()
    usada = info.used / 1024**3
    total = info.total / 1024**3
    print(f"RAM do host (CPU): {usada:.1f} GB usada de {total:.1f} GB ({info.percent:.0f}%)")


def main():
    print("=" * 72)
    print(" Diagnostico de memoria - medir antes de otimizar")
    print("=" * 72)

    tem_gpu = painel_nvidia_smi()
    if not tem_gpu:
        print("Sem nvidia-smi neste ambiente - exemplo SIMULADO (Tesla T4):")
        print(f"  {'idx':>3} | {'nome':<22} | {'VRAM usada':>10} | {'VRAM total':>10} | {'util%':>5} | {'temp':>4}")
        print("  " + "-" * 68)
        print(f"  {'0':>3} | {'Tesla T4':<22} | {'1234':>7} MB | {'15360':>7} MB | {'40':>5} | {'52':>3}C")

    print()
    memoria_host()
    print()
    print("Leitura do painel:")
    print("  - VRAM 'usada' baixa + 'util%' baixa (ex.: 40%) = GPU ociosa.")
    print("  - Causa comum: o host nao entrega os dados rapido (gargalo PCIe,")
    print("    batches mal dimensionados, DataLoader lento).")
    print("  - Acao: aumentar o batch (ou usar mais workers de dados) para")
    print("    ocupar a VRAM e manter a GPU alimentada.")


if __name__ == "__main__":
    main()
