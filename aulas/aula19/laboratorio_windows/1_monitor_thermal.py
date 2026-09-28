"""1_monitor_thermal.py — Coleta temperatura, potência e clock da GPU.

Uso: python 1_monitor_thermal.py [intervalo_s] [amostras]

Grava o histórico incremental em reports/gpu_thermal.csv (nunca apaga o
histórico). O backend (NVIDIA/AMD/SIMULADO) é detectado automaticamente.
"""

import csv
import os
import sys
import time

from lib_energia import ler_amostra, timestamp

CABECALHO = ["timestamp", "backend", "gpu_index", "gpu_name", "temp_c",
             "power_w", "power_limit_w", "util_gpu_pct",
             "clock_sm_mhz", "clock_mem_mhz"]


def main():
    intervalo = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    amostras = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    os.makedirs("reports", exist_ok=True)
    saida = os.path.join("reports", "gpu_thermal.csv")

    # Cria o cabeçalho apenas na primeira execução
    if not os.path.exists(saida):
        with open(saida, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(CABECALHO)

    print(f"Monitorando GPU a cada {intervalo}s ({amostras} amostras)")
    print(f"Saída: {saida}\n")

    with open(saida, "a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        for i in range(1, amostras + 1):
            backend, m = ler_amostra()
            linha = [
                timestamp(), backend, m["gpu_index"], m["gpu_name"],
                m["temp_c"], m["power_w"], m["power_limit_w"],
                m["util_gpu_pct"], m["clock_sm_mhz"], m["clock_mem_mhz"],
            ]
            escritor.writerow(linha)
            f.flush()
            print(f"  [{i}/{amostras}] {backend:<8} | {m['gpu_name'][:24]:<24} | "
                  f"{m['temp_c']:.0f}°C | {m['power_w']:.0f}W/{m['power_limit_w']:.0f}W | "
                  f"util {m['util_gpu_pct']:.0f}%")
            if i < amostras:
                time.sleep(intervalo)

    print(f"\nColeta concluída. Histórico em '{saida}'.")


if __name__ == "__main__":
    main()
