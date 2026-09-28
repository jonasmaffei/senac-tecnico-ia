# ============================================================================
# coletor.py — coleta de métricas de sistema e GPU (versão Windows nativa)
# ----------------------------------------------------------------------------
# Diferente da versão Docker, este arquivo roda DIRETO no Windows, então
# consegue ler a GPU AMD de verdade (usando os contadores de desempenho do
# Windows via PowerShell/CIM) — do mesmo jeito que o laboratorio_windows.
#
#   - CPU e RAM: psutil (real).
#   - GPU AMD: PowerShell/CIM (utilização e VRAM reais; temperatura estimada).
#   - GPU NVIDIA: nvidia-smi, se existir.
#   - Sem GPU: modo simulado.
#
# O comando PowerShell é passado como STRING INLINE (-Command), então não
# depende de ExecutionPolicy nem cria arquivos .ps1.
# ============================================================================

import os
import platform
import random
import shutil
import subprocess
import time
from datetime import datetime

import psutil


# ---------------------------------------------------------------------------
# DETECÇÃO DO BACKEND DE GPU (uma vez, na importação)
# ---------------------------------------------------------------------------
def _detectar_backend():
    if os.environ.get("GPU_BACKEND", "auto") == "simulado":
        return "simulado"
    if shutil.which("nvidia-smi") or shutil.which("nvidia-smi.exe"):
        return "nvidia"
    if shutil.which("powershell.exe") or shutil.which("powershell"):
        return "amd_windows"
    return "simulado"


BACKEND_GPU = _detectar_backend()


def nome_backend():
    return {
        "nvidia": "NVIDIA (nvidia-smi)",
        "amd_windows": "AMD no Windows (contadores de desempenho)",
        "simulado": "simulado",
    }.get(BACKEND_GPU, "simulado")


# ---------------------------------------------------------------------------
# CPU E RAM (REAIS) — via psutil
# ---------------------------------------------------------------------------
def _cpu_pct(intervalo=0.5):
    return round(psutil.cpu_percent(interval=intervalo), 0)


def _ram():
    mem = psutil.virtual_memory()
    return round((mem.total - mem.available) / (1024 * 1024)), \
           round(mem.total / (1024 * 1024))


def _cpu_temp():
    # No Windows o psutil não expõe sensores de temperatura; tentamos mesmo
    # assim (funciona em alguns Linux) e devolvemos None se não houver.
    try:
        temps = psutil.sensors_temperatures()
    except (AttributeError, NotImplementedError):
        return None
    for lista in (temps or {}).values():
        if lista:
            return round(lista[0].current)
    return None


# ---------------------------------------------------------------------------
# GPU REAL — AMD no Windows (PowerShell/CIM, inline)
# ---------------------------------------------------------------------------
def _gpu_amd_windows():
    ps = "powershell.exe" if shutil.which("powershell.exe") else "powershell"
    script = (
        '$ErrorActionPreference = "SilentlyContinue";'
        '$nome = "AMD GPU"; $tot = 0;'
        '$base = "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Class\\'
        '{4d36e968-e325-11ce-bfc1-08002be10318}";'
        'Get-ChildItem $base | ForEach-Object {'
        '  $p = Get-ItemProperty $_.PSPath;'
        '  if ($p."HardwareInformation.qwMemorySize") {'
        '    if ($nome -eq "AMD GPU") { $nome = $p.DriverDesc };'
        '    $tot = [math]::Round([uint64]$p."HardwareInformation.qwMemorySize" / 1MB, 0)'
        '  }'
        '};'
        'if ($nome -eq "AMD GPU") {'
        '  $nome = (Get-CimInstance Win32_VideoController | Select-Object -First 1).Name'
        '};'
        '$util = 0;'
        '$e = Get-CimInstance Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine;'
        'if ($e) {'
        '  $s = ($e | Where-Object { $_.Name -like "*engtype_3D*" } |'
        '        Measure-Object UtilizationPercentage -Sum).Sum;'
        '  if ($s) { $util = [math]::Round($s, 0) }'
        '};'
        'if ($util -gt 100) { $util = 100 };'
        '$mem = 0;'
        '$m = Get-CimInstance Win32_PerfFormattedData_GPUPerformanceCounters_GPUAdapterMemory;'
        'if ($m) {'
        '  $b = ($m | Measure-Object DedicatedUsage -Sum).Sum;'
        '  if ($b) { $mem = [math]::Round($b / 1MB, 0) }'
        '};'
        '$temp = [math]::Round(42 + ($util * 0.48), 0);'
        '$nome = $nome -replace ",", " ";'
        'Write-Output "$nome|$temp|$util|$mem|$tot"'
    )
    saida = subprocess.run(
        [ps, "-NoProfile", "-Command", script],
        capture_output=True, text=True, timeout=15,
    ).stdout.strip().splitlines()
    if not saida:
        raise RuntimeError("PowerShell não retornou dados da GPU")
    nome, temp, util, mem, tot = [c.strip() for c in saida[-1].split("|")]

    def _num(v):
        try:
            return round(float(v))
        except ValueError:
            return None

    return {
        "gpu_nome": nome,
        "gpu_temp_c": _num(temp),
        "gpu_util_pct": _num(util),
        "vram_usada_mb": _num(mem),
        "vram_total_mb": _num(tot),
        # A potência não é exposta pelo driver AMD no Windows.
        "gpu_potencia_w": None,
    }


# ---------------------------------------------------------------------------
# GPU REAL — NVIDIA (nvidia-smi)
# ---------------------------------------------------------------------------
def _gpu_nvidia():
    campos = "name,temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw"
    exe = "nvidia-smi.exe" if shutil.which("nvidia-smi.exe") else "nvidia-smi"
    saida = subprocess.run(
        [exe, f"--query-gpu={campos}", "--format=csv,noheader,nounits"],
        capture_output=True, text=True, timeout=5,
    ).stdout.strip().splitlines()
    if not saida:
        raise RuntimeError("nvidia-smi não retornou dados")
    nome, temp, util, vram, vtot, pot = [c.strip() for c in saida[0].split(",")]

    def _num(v):
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
# GPU SIMULADA
# ---------------------------------------------------------------------------
def _gpu_simulada(tempo_s):
    util = 35 + 30 * abs((tempo_s % 120) / 120 - 0.5) * 2 + random.randint(-5, 5)
    util = max(0, min(100, round(util)))
    temp = round(42 + util * 0.45)
    vram_total = 12272
    vram = round(vram_total * (0.15 + util / 100 * 0.5))
    return {
        "gpu_nome": "GPU Simulada",
        "gpu_temp_c": temp,
        "gpu_util_pct": util,
        "vram_usada_mb": vram,
        "vram_total_mb": vram_total,
        "gpu_potencia_w": round(40 + util * 1.1),
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
            gpu = _gpu_simulada(tempo_s)
    elif BACKEND_GPU == "amd_windows":
        try:
            gpu = _gpu_amd_windows()
        except Exception:
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
        # Nome da CPU no Windows costuma vir com espaços extras.
        nome_cpu = platform.processor().strip()
        return {
            "host": platform.node() or "PC",
            "so": f"{platform.system()} {platform.release()}",
            "cpu_cores": psutil.cpu_count(logical=False) or 0,
            "cpu_threads": psutil.cpu_count(logical=True) or 0,
            "ram_total_mb": round(psutil.virtual_memory().total / (1024 * 1024)),
            "gpu_nome": "GPU Simulada" if BACKEND_GPU == "simulado" else "",
        }
    except Exception:
        return {}
