"""lib_energia.py - Utilitarios de energia e termica para o laboratorio (Aula 19).

Detecta o backend disponivel no host:
  - NVIDIA  -> usa `nvidia-smi` (leitura real de temperatura/potencia/clock)
  - AMD/Win -> le a GPU AMD via contadores do Windows (PowerShell/CIM)
  - SIMULADO-> gera valores plausiveis para exercitar os conceitos

Tambem define um modelo empirico de consumo e eficiencia usado no benchmark.
"""

import datetime
import math
import os
import random
import shutil
import subprocess

# ---------------------------------------------------------------------------
# Deteccao de backend
# ---------------------------------------------------------------------------


def detectar_backend():
    """Retorna 'nvidia', 'amd' ou 'simulado' (override por GPU19_BACKEND)."""
    override = os.environ.get("GPU19_BACKEND", "").strip().lower()
    if override in ("nvidia", "amd", "simulado"):
        return override
    if shutil.which("nvidia-smi"):
        return "nvidia"
    if os.name == "nt":
        # Em Windows com GPU AMD/Intel exposta, usamos os contadores do host
        if _consultar_gpu_amd():
            return "amd"
    return "simulado"


def _consultar_gpu_amd():
    """Le nome e uso da primeira GPU AMD/Intel via PowerShell CIM.

    Retorna um dict ou None se nao conseguir consultar.
    """
    if os.name != "nt":
        return None
    ps = (
        "$g = Get-CimInstance Win32_VideoController | "
        "Where-Object { $_.Name -notmatch 'Basic|Remote' } | Select-Object -First 1; "
        "$u = (Get-Counter '\\GPU Engine(*)\\Utilization Percentage' -ErrorAction SilentlyContinue)."
        "CounterSamples | Measure-Object -Property CookedValue -Sum; "
        "Write-Output ($g.Name + '|' + [math]::Round($u.Sum,1))"
    )
    try:
        saida = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", ps],
            text=True, stderr=subprocess.DEVNULL, timeout=10
        ).strip()
        if "|" in saida:
            nome, uso = saida.split("|", 1)
            return {"nome": nome.strip() or "GPU AMD", "uso": float(uso or 0)}
    except Exception:
        return None
    return None


# ---------------------------------------------------------------------------
# Leitura de metricas
# ---------------------------------------------------------------------------


def ler_nvidia():
    """Le uma amostra da GPU 0 via nvidia-smi. Retorna dict ou None."""
    campos = ("index,temperature.gpu,power.draw,enforced.power.limit,"
              "utilization.gpu,clocks.sm,clocks.mem")
    try:
        saida = subprocess.check_output(
            ["nvidia-smi", f"--query-gpu={campos}", "--format=csv,noheader,nounits"],
            text=True, stderr=subprocess.DEVNULL
        ).strip().split("\n")[0]
        idx, temp, pwr, plim, util, clk_sm, clk_mem = [c.strip() for c in saida.split(",")]
        return {
            "gpu_index": int(idx),
            "gpu_name": "NVIDIA GPU",
            "temp_c": float(temp),
            "power_w": float(pwr),
            "power_limit_w": float(plim),
            "util_gpu_pct": float(util),
            "clock_sm_mhz": int(float(clk_sm)),
            "clock_mem_mhz": int(float(clk_mem)),
        }
    except Exception:
        return None


def ler_amd():
    """Le a GPU AMD do Windows e estima temperatura/potencia.

    O Windows nao expoe temperatura/potencia da AMD sem drivers especificos,
    entao usamos o uso (%) e o nome reais e derivamos os demais de forma honesta.
    """
    info = _consultar_gpu_amd()
    if not info:
        return None
    uso = max(0.0, min(info["uso"], 100.0))
    # Estimativas transparentes a partir do uso (nao sao leituras do sensor)
    return {
        "gpu_index": 0,
        "gpu_name": info["nome"],
        "temp_c": round(40 + uso * 0.45, 1),
        "power_w": round(35 + uso * 1.6, 1),
        "power_limit_w": 180.0,
        "util_gpu_pct": round(uso, 1),
        "clock_sm_mhz": int(1000 + uso * 9),
        "clock_mem_mhz": 4000,
    }


def ler_simulado(uso=None):
    """Gera uma amostra sintetica plausivel de uma GPU em treino."""
    uso = uso if uso is not None else random.uniform(40, 100)
    return {
        "gpu_index": 0,
        "gpu_name": "GPU Simulada (referencia T4)",
        "temp_c": round(50 + uso * 0.35, 1),
        "power_w": round(40 + uso * 0.7, 1),
        "power_limit_w": 70.0,
        "util_gpu_pct": round(uso, 1),
        "clock_sm_mhz": int(1000 + uso * 6),
        "clock_mem_mhz": 5001,
    }


def ler_amostra():
    """Retorna (backend, dicionario_de_metricas)."""
    backend = detectar_backend()
    if backend == "nvidia":
        dado = ler_nvidia()
        if dado:
            return backend, dado
    elif backend == "amd":
        dado = ler_amd()
        if dado:
            return backend, dado
    return "simulado", ler_simulado()


# ---------------------------------------------------------------------------
# Modelo empirico de consumo/eficiencia (para o benchmark)
# ---------------------------------------------------------------------------


def throughput_imgs_s(power_limit_w, tdp_w=250):
    """Throughput (imgs/s) em funcao do Power Limit.

    Modelo logistico: com PL muito baixo a GPU sofre throttling severo (pouco
    throughput); acima de ~60% do TDP o ganho satura. Por isso a eficiencia
    (throughput/potencia) tem um maximo por volta de 70-75% do TDP.
    """
    x = power_limit_w / tdp_w
    return 480.0 / (1.0 + math.exp(-6.0 * (x - 0.5)))


def consumo_medio_w(power_limit_w):
    """Consumo medio estimado: ~92% do limite configurado."""
    return power_limit_w * 0.92


def eficiencia_imgs_j(power_limit_w, tdp_w=250):
    """Eficiencia energetica = throughput / potencia media."""
    return throughput_imgs_s(power_limit_w, tdp_w) / consumo_medio_w(power_limit_w)


def timestamp():
    """Timestamp formatado para os CSVs."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
