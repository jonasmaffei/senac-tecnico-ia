# ============================================================================
# coletor.py — coleta de métricas de sistema e GPU
# ----------------------------------------------------------------------------
# Faz a ponte entre o sistema operacional e o webservice:
#
#   - CPU e RAM: lidas de verdade com a biblioteca psutil (funciona no
#     container Linux do Docker sem nenhuma permissão especial).
#   - GPU: no container Docker do Windows (WSL 2) não há acesso à placa AMD.
#     Por isso simulamos a GPU com valores plausíveis. Se o container rodar em
#     uma máquina Linux com GPU NVIDIA exposta (docker run --gpus all), ele
#     passa a usar o nvidia-smi de verdade automaticamente.
#
# A função principal é `coletar()`, que devolve UM dicionário (uma "amostra")
# no mesmo espírito do CSV do laboratório_windows.
# ============================================================================

import os
import random
import shutil
import subprocess
import time
from datetime import datetime

import psutil


# ---------------------------------------------------------------------------
# DETECÇÃO DO BACKEND DE GPU (feita uma vez, na importação)
# ---------------------------------------------------------------------------
def _detectar_backend():
    # Procura o nvidia-smi no PATH do container. Só existe se a GPU NVIDIA
    # tiver sido exposta ao Docker com --gpus all.
    if os.environ.get("GPU_BACKEND", "auto") == "simulado":
        return "simulado"
    if shutil.which("nvidia-smi"):
        return "nvidia"
    return "simulado"


BACKEND_GPU = _detectar_backend()


def nome_backend():
    """Texto amigável sobre como a GPU está sendo lida."""
    return "NVIDIA (nvidia-smi)" if BACKEND_GPU == "nvidia" else "simulado"


# ---------------------------------------------------------------------------
# CPU E RAM (REAIS) — via psutil
# ---------------------------------------------------------------------------
def _cpu_pct(intervalo=0.5):
    # psutil.cpu_percent precisa de um intervalo para medir a variação de uso.
    return round(psutil.cpu_percent(interval=intervalo), 0)


def _ram():
    # Em MB (mesmo formato do laboratório_windows).
    mem = psutil.virtual_memory()
    total = round(mem.total / (1024 * 1024))
    usada = round((mem.total - mem.available) / (1024 * 1024))
    return usada, total


def _cpu_temp():
    # A temperatura da CPU nem sempre é exposta no container. Tentamos os
    # sensores do psutil e, se não houver, devolvemos None (o gráfico some).
    try:
        temps = psutil.sensors_temperatures()
    except (AttributeError, NotImplementedError):
        return None
    if not temps:
        return None
    for nome in ("coretemp", "k10temp", "cpu_thermal", "acpitz"):
        if nome in temps and temps[nome]:
            return round(temps[nome][0].current)
    for lista in temps.values():
        if lista:
            return round(lista[0].current)
    return None


# ---------------------------------------------------------------------------
# GPU SIMULADA — valores que variam de forma parecida com uso real
# ---------------------------------------------------------------------------
def _gpu_simulada(tempo_s):
    # Utilização: combina uma onda (carga subindo e descendo) com ruído leve.
    util = 35 + 30 * abs((tempo_s % 120) / 120 - 0.5) * 2 + random.randint(-5, 5)
    util = max(0, min(100, round(util)))
    # Temperatura acompanha a utilização (mais uso -> mais quente).
    temp = round(42 + util * 0.45)
    # VRAM cresce com a carga.
    vram_total = 12272
    vram = round(vram_total * (0.15 + util / 100 * 0.5))
    # Potência estimada.
    potencia = round(40 + util * 1.1)
    return {
        "gpu_nome": "GPU Simulada (Docker)",
        "gpu_temp_c": temp,
        "gpu_util_pct": util,
        "vram_usada_mb": vram,
        "vram_total_mb": vram_total,
        "gpu_potencia_w": potencia,
    }


# ---------------------------------------------------------------------------
# GPU REAL — NVIDIA via nvidia-smi (só em Linux com --gpus all)
# ---------------------------------------------------------------------------
def _gpu_nvidia():
    # Pede os campos exatamente no formato CSV que sabemos interpretar.
    campos = (
        "name,temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw"
    )
    saida = subprocess.run(
        ["nvidia-smi", f"--query-gpu={campos}",
         "--format=csv,noheader,nounits"],
        capture_output=True, text=True, timeout=5,
    ).stdout.strip().splitlines()
    if not saida:
        raise RuntimeError("nvidia-smi não retornou dados")
    nome, temp, util, vram, vtot, pot = [c.strip() for c in saida[0].split(",")]

    def _num(v):
        # Alguns campos podem vir "N/A"; nesse caso devolvemos None.
        try:
            return round(float(v))
        except ValueError:
            return None

    return {
        "gpu_nome": nome,
        "gpu_temp_c": _num(temp),
        "gpu_util_pct": _num(util),
        "vram_usada_mb": _num(vram),
        "vram_total_mb": _num(vtot),
        "gpu_potencia_w": _num(pot),
    }


# ---------------------------------------------------------------------------
# INTERFACE PÚBLICA
# ---------------------------------------------------------------------------
def coletar(tempo_s=None):
    """Coleta UMA amostra completa (sistema + GPU) e devolve um dicionário."""
    if tempo_s is None:
        tempo_s = time.time()

    cpu = _cpu_pct()
    ram_usada, ram_total = _ram()

    if BACKEND_GPU == "nvidia":
        try:
            gpu = _gpu_nvidia()
        except Exception:
            # Se o nvidia-smi falhar, não derruba o serviço: cai no simulado.
            gpu = _gpu_simulada(tempo_s)
    else:
        gpu = _gpu_simulada(tempo_s)

    amostra = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_pct": cpu,
        "ram_usada_mb": ram_usada,
        "ram_total_mb": ram_total,
        "cpu_temp_c": _cpu_temp(),
    }
    amostra.update(gpu)
    return amostra


def especificacoes():
    """Dados fixos da máquina, para os cartões do topo do painel."""
    try:
        import platform
        nucleos = psutil.cpu_count(logical=False) or 0
        threads = psutil.cpu_count(logical=True) or 0
        ram_total = round(psutil.virtual_memory().total / (1024 * 1024))
        return {
            "host": platform.node() or "container",
            "so": f"{platform.system()} {platform.release()}",
            "cpu_cores": nucleos,
            "cpu_threads": threads,
            "ram_total_mb": ram_total,
            "gpu_nome": "GPU Simulada (Docker)" if BACKEND_GPU == "simulado"
                         else "NVIDIA",
        }
    except Exception:
        return {}
