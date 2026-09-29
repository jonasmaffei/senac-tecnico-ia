"""3_benchmark_energia.py - Benchmark energetico (simulado) por Power Limit.

Uso: python 3_benchmark_energia.py

Usa o modelo empirico de lib_energia.py para estimar throughput, consumo e
eficiencia (imgs/J) em diferentes Power Limits e identifica o ponto otimo.
Gera o grafico reports/benchmark_energia.png.
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lib_energia import consumo_medio_w, eficiencia_imgs_j, throughput_imgs_s

TDP = 250
POWER_LIMITS = [100, 125, 150, 175, 200, 225, 250]


def main():
    os.makedirs("reports", exist_ok=True)
    saida_png = os.path.join("reports", "benchmark_energia.png")

    resultados = []
    print(f"{'PL (W)':>8} {'Imgs/s':>10} {'Pwr (W)':>10} {'Imgs/J':>10}  {'% TDP':>7}")
    print("-" * 52)
    for pl in POWER_LIMITS:
        imgs = throughput_imgs_s(pl, TDP)
        pwr = consumo_medio_w(pl)
        efic = eficiencia_imgs_j(pl, TDP)
        resultados.append((pl, imgs, pwr, efic))
        print(f"{pl:>8} {imgs:>10.1f} {pwr:>10.1f} {efic:>10.3f}  {pl/TDP:>6.0%}")

    pl_otimo, _, _, efic_otimo = max(resultados, key=lambda r: r[3])
    print(f"\nPonto otimo de eficiencia: PL={pl_otimo}W "
          f"(~{pl_otimo/TDP:.0%} do TDP) -> {efic_otimo:.3f} imgs/J")

    pls = [r[0] for r in resultados]
    imgs = [r[1] for r in resultados]
    efics = [r[3] for r in resultados]

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(pls, imgs, "o-", color="#6366F1", label="Throughput (imgs/s)")
    ax1.set_xlabel("Power Limit (W)")
    ax1.set_ylabel("Throughput (imgs/s)", color="#6366F1")
    ax1.tick_params(axis="y", labelcolor="#6366F1")

    ax2 = ax1.twinx()
    ax2.plot(pls, efics, "s--", color="#10B981", label="Eficiencia (imgs/J)")
    ax2.set_ylabel("Eficiencia (imgs/J)", color="#10B981")
    ax2.tick_params(axis="y", labelcolor="#10B981")

    ax1.axvline(x=pl_otimo, color="#F97316", linestyle=":", alpha=0.7)
    ax1.set_title("Trade-off: Desempenho x Eficiencia Energetica")

    fig.tight_layout()
    fig.savefig(saida_png, dpi=150)
    print(f"Grafico salvo em '{saida_png}'.")


if __name__ == "__main__":
    main()
