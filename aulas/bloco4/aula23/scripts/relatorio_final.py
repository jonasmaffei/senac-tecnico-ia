# relatorio_final.py — gerar o relatório final do projeto para apresentação
# Uso: python relatorio_final.py
#
# Combina métricas de treino (simuladas ou exportadas do W&B) com logs de GPU
# em um relatório de 6 gráficos. Funciona sem GPU/internet.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os

DADOS_TREINO = {
    "epoch":    list(range(1, 11)),
    "val/loss": [0.85, 0.71, 0.60, 0.51, 0.44, 0.39, 0.35, 0.33, 0.32, 0.34],
    "val/acc":  [0.58, 0.66, 0.72, 0.78, 0.81, 0.84, 0.86, 0.87, 0.876, 0.875],
}

# Comparação baseline CPU × GPU (substitua pelos dados reais)
COMPARACAO = {
    "categorias":  ["Tempo/epoca (s)", "Val Acc (%)", "Throughput (imgs/s)", "VRAM (GB)"],
    "baseline":    [320, 71.2, 48, 0],
    "gpu":         [38, 87.6, 410, 9.4],
}


def gerar_log_gpu(n=40, seed=42):
    """Gera um log de GPU simulado (substitua pelo CSV real de logs/monitor/)."""
    rng = np.random.default_rng(seed)
    return {
        "duracao_min": np.linspace(0, 35, n),
        "temp_c":      70 + 12 * np.sin(np.linspace(0, 6, n)) + rng.uniform(-2, 2, n),
        "util_pct":    np.clip(88 + rng.uniform(-8, 10, n), 0, 100),
        "mem_used_gb": 9.2 + rng.uniform(-0.2, 0.4, n),
    }


def gerar_relatorio(salvar_dir="relatorio_final"):
    os.makedirs(salvar_dir, exist_ok=True)
    gpu = gerar_log_gpu()

    fig = plt.figure(figsize=(16, 9))
    fig.suptitle("Relatorio Final - Projeto GPU", fontsize=15, fontweight="bold")
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.3)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(DADOS_TREINO["epoch"], DADOS_TREINO["val/loss"], "o-", color="#6366F1")
    ax1.set_title("Val Loss"); ax1.set_xlabel("Epoca"); ax1.grid(alpha=0.3)

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(DADOS_TREINO["epoch"], DADOS_TREINO["val/acc"], "s-", color="#10B981")
    ax2.set_title("Val Accuracy"); ax2.set_xlabel("Epoca"); ax2.grid(alpha=0.3)

    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(gpu["duracao_min"], gpu["temp_c"], color="#EF4444")
    ax3.axhline(82, color="orange", ls="--"); ax3.axhline(90, color="red", ls="--")
    ax3.set_title("Temperatura GPU (C)"); ax3.set_xlabel("Tempo (min)"); ax3.grid(alpha=0.3)

    ax4 = fig.add_subplot(gs[1, 0])
    ax4.plot(gpu["duracao_min"], gpu["util_pct"], color="#10B981")
    ax4.set_ylim(0, 100); ax4.set_title("Utilizacao GPU (%)"); ax4.set_xlabel("Tempo (min)"); ax4.grid(alpha=0.3)

    ax5 = fig.add_subplot(gs[1, 1])
    ax5.plot(gpu["duracao_min"], gpu["mem_used_gb"], color="#7E22CE")
    ax5.set_title("VRAM Usada (GB)"); ax5.set_xlabel("Tempo (min)"); ax5.grid(alpha=0.3)

    ax6 = fig.add_subplot(gs[1, 2])
    cats = COMPARACAO["categorias"]
    x = np.arange(len(cats))
    ax6.bar(x - 0.2, COMPARACAO["baseline"], 0.4, label="Baseline (CPU)", color="#94A3B8")
    ax6.bar(x + 0.2, COMPARACAO["gpu"], 0.4, label="Modelo GPU", color="#F97316")
    ax6.set_xticks(x); ax6.set_xticklabels(cats, fontsize=7, rotation=15); ax6.legend(fontsize=8)
    ax6.set_title("Baseline x GPU"); ax6.grid(axis="y", alpha=0.3)

    caminho = os.path.join(salvar_dir, "relatorio_final.png")
    fig.savefig(caminho, dpi=150, bbox_inches="tight")
    print(f"Relatorio salvo: {caminho}")
    return caminho


def main():
    print("Gerando relatorio final do projeto...")
    gerar_relatorio()
    print("\nDica: substitua DADOS_TREINO pelos numeros reais do W&B e COMPARACAO pelos do seu projeto.")


if __name__ == "__main__":
    main()
