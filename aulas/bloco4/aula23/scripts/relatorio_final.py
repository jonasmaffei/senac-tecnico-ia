# relatorio_final.py — relatório simples do projeto (Aula 23)
# Uso: python relatorio_final.py
#
# Gera um gráfico com a tabela baseline x GPU e as curvas de treino (dados de exemplo).
# Substitua os valores pelos reais do seu projeto.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Curvas de treino (exemplo) — troque pelos números reais do W&B
EPOCAS = list(range(1, 11))
VAL_LOSS = [0.85, 0.71, 0.60, 0.51, 0.44, 0.39, 0.35, 0.33, 0.32, 0.34]
VAL_ACC = [0.58, 0.66, 0.72, 0.78, 0.81, 0.84, 0.86, 0.87, 0.876, 0.875]

# Comparação baseline (CPU) x modelo (GPU) — troque pelos dados reais
CATEGORIAS = ["Tempo/epoca (s)", "Val Acc (%)", "Throughput (imgs/s)"]
BASELINE = [320, 71.2, 48]
GPU = [38, 87.6, 410]


def main():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle("Relatorio Final - Projeto GPU", fontweight="bold")

    axes[0].plot(EPOCAS, VAL_LOSS, "o-", color="#6366F1")
    axes[0].set_title("Val Loss"); axes[0].set_xlabel("Epoca")

    axes[1].plot(EPOCAS, VAL_ACC, "s-", color="#10B981")
    axes[1].set_title("Val Accuracy"); axes[1].set_xlabel("Epoca")

    x = np.arange(len(CATEGORIAS))
    axes[2].bar(x - 0.2, BASELINE, 0.4, label="Baseline (CPU)", color="#94A3B8")
    axes[2].bar(x + 0.2, GPU, 0.4, label="Modelo GPU", color="#F97316")
    axes[2].set_xticks(x); axes[2].set_xticklabels(CATEGORIAS, fontsize=7, rotation=15)
    axes[2].set_title("Baseline x GPU"); axes[2].legend()

    fig.tight_layout()
    fig.savefig("relatorio_final.png", dpi=150)
    print("Relatorio salvo: relatorio_final.png")


if __name__ == "__main__":
    main()
