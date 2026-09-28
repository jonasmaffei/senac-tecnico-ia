# dashboard_metricas.py — dashboard visual das métricas de GPU do projeto
# Uso: python dashboard_metricas.py [projeto]
#
# Carrega todos os CSVs de logs/monitor/ e gera um relatório com 4 gráficos.

import glob
import os
import sys
from datetime import datetime

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def carregar_logs_gpu(log_dir="logs/monitor", projeto=None):
    """Carrega todos os CSVs de monitor e concatena em um DataFrame."""
    padrao = f"{log_dir}/{projeto or '*'}_*.csv"
    arquivos = sorted(glob.glob(padrao))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum log encontrado em {padrao}")

    dfs = []
    for arquivo in arquivos:
        df = pd.read_csv(arquivo, parse_dates=["timestamp"])
        df["arquivo"] = os.path.basename(arquivo)
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True).sort_values("timestamp")
    df["duracao_min"] = (df["timestamp"] - df["timestamp"].iloc[0]).dt.total_seconds() / 60
    return df


def gerar_dashboard(df, projeto="projeto", salvar=True):
    """Gera dashboard com 4 gráficos das métricas de GPU durante o treinamento."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle(f"Dashboard GPU — {projeto}", fontsize=14, fontweight="bold")

    # 1. Temperatura
    axes[0, 0].plot(df["duracao_min"], df["temp_c"], color="#EF4444", linewidth=1.5)
    axes[0, 0].axhline(82, color="orange", linestyle="--", linewidth=1, label="Warn 82C")
    axes[0, 0].axhline(90, color="red", linestyle="--", linewidth=1, label="Crit 90C")
    axes[0, 0].set_title("Temperatura (C)"); axes[0, 0].legend()

    # 2. Utilização
    axes[0, 1].plot(df["duracao_min"], df["util_pct"], color="#10B981", linewidth=1.5)
    axes[0, 1].set_ylim(0, 100); axes[0, 1].set_title("Utilizacao GPU (%)")

    # 3. VRAM usada
    axes[1, 0].fill_between(df["duracao_min"], df["mem_used_mb"] / 1024, alpha=0.3, color="#7E22CE")
    axes[1, 0].plot(df["duracao_min"], df["mem_used_mb"] / 1024, color="#7E22CE", linewidth=1.5)
    axes[1, 0].set_title("VRAM Usada (GB)")

    # 4. Potência
    axes[1, 1].plot(df["duracao_min"], df["power_w"], color="#F97316", linewidth=1.5)
    axes[1, 1].set_title("Potencia (W)")

    for ax in axes.flat:
        ax.set_xlabel("Tempo (min)")
        ax.grid(alpha=0.3)

    if salvar:
        os.makedirs("logs/dashboards", exist_ok=True)
        caminho = f"logs/dashboards/{projeto}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig.savefig(caminho, dpi=150, bbox_inches="tight")
        print(f"Dashboard salvo: {caminho}")
    return fig


def main():
    projeto = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        df = carregar_logs_gpu(projeto=projeto)
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        print("Execute o monitor primeiro (monitor_treinamento.sh) para gerar os CSVs.")
        return
    print(df[["temp_c", "util_pct", "mem_used_mb", "power_w"]].describe())
    gerar_dashboard(df, projeto=projeto or "projeto")


if __name__ == "__main__":
    main()
