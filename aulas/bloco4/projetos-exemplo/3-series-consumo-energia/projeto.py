# projeto.py — Projeto Exemplo 3: Previsao de Consumo de Energia (Bloco 4)
# Uso: python projeto.py
#
# Percorre as 5 etapas das aulas 20 a 24 (planejar, implementar, monitorar,
# apresentar, conectar ao PI) em modo de referencia (roda sem GPU).

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- 1. Planejar (Aula 20) ----------
CONFIG = {
    "nome": "PrevisaoConsumo",
    "dominio": "series_temporais",
    "problema": "Prever consumo eletrico das proximas horas",
    "dataset": "ETT - ETTh1 (consumo)",
    "modelo": "LSTM (ou Transformer leve)",
    "metrica": "RMSE",
    "baseline": "media historica / persistencia",
    "batch_size": 64,
    "precision": "fp16",
}


def etapa1_planejar():
    print("=== 1. Planejar (Aula 20) ===")
    for k, v in CONFIG.items():
        print(f"  {k:<12} = {v}")
    print("  checklist: problema, dataset, modelo, GPU, metrica e baseline definidos.\n")


# ---------- 2. Implementar (Aula 21) ----------
def etapa2_implementar():
    print("=== 2. Implementar (Aula 21) ===")
    print("  pipeline: AMP + janela deslizante + persistent_workers=True")
    print(f"  batch={CONFIG['batch_size']} | precision={CONFIG['precision']}")
    try:
        import torch
        if torch.cuda.is_available():
            print(f"  GPU: {torch.cuda.get_device_name(0)} (treino real disponivel)")
        else:
            print("  sem GPU: modo de referencia (apenas demonstracao)")
    except ImportError:
        print("  PyTorch ausente: modo de referencia")
    print()


# ---------- 3. Monitorar (Aula 22) ----------
def etapa3_monitorar():
    print("=== 3. Monitorar (Aula 22) ===")
    print("  monitor_treinamento.sh -> logs/monitor/*.csv (intervalo ~20s)")
    print("  carga mais estavel: foco em VMEM e temperatura\n")


# ---------- 4. Apresentar (Aula 23) ----------
def etapa4_apresentar():
    print("=== 4. Apresentar (Aula 23) ===")
    metricas = {"tempo_epoca_s": (180, 12), "rmse_x100": (92, 41),
                "throughput": (120, 900)}
    print(f"  {'metrica':<18} {'CPU':>8} {'GPU':>8}")
    for nome, (cpu, gpu) in metricas.items():
        print(f"  {nome:<18} {cpu:>8} {gpu:>8}")
    print()

    cats = list(metricas.keys())
    cpu = [metricas[c][0] for c in cats]
    gpu = [metricas[c][1] for c in cats]
    fig, ax = plt.subplots(figsize=(8, 4))
    x = range(len(cats))
    ax.bar([i - 0.2 for i in x], cpu, 0.4, label="CPU", color="#94A3B8")
    ax.bar([i + 0.2 for i in x], gpu, 0.4, label="GPU", color="#7E22CE")
    ax.set_xticks(list(x)); ax.set_xticklabels(cats, fontsize=8, rotation=10)
    ax.set_title(f"Baseline x GPU - {CONFIG['nome']}")
    ax.legend(); fig.tight_layout()
    fig.savefig("relatorio.png", dpi=150)
    print("  relatorio.png salvo.\n")


# ---------- 5. Conectar ao PI (Aula 24) ----------
def etapa5_conectar():
    print("=== 5. Conectar ao PI (Aula 24) ===")
    print("  - previsao de consumo/falhas de equipamentos no PI")
    print("  - deteccao de anomalias em telemetria (IoT) na GPU\n")


def main():
    etapa1_planejar()
    etapa2_implementar()
    etapa3_monitorar()
    etapa4_apresentar()
    etapa5_conectar()
    print("Projeto concluido (exemplo).")


if __name__ == "__main__":
    main()
