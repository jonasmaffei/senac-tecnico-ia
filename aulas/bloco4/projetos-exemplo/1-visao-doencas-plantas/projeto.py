# projeto.py - Projeto Exemplo 1: Deteccao de Doencas em Plantas (Bloco 4)
# Uso: python projeto.py
#
# Percorre as 5 etapas das aulas 20 a 24 (planejar, implementar, monitorar,
# apresentar, conectar ao PI) em modo de referencia (roda sem GPU).

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- 1. Planejar (Aula 20) ----------
CONFIG = {
    "nome": "DeteccaoDoencas",
    "dominio": "visao",
    "problema": "Identificar doenca da planta por foto",
    "dataset": "PlantVillage (38 classes)",
    "modelo": "ResNet-18 pre-treinado",
    "metrica": "accuracy",
    "baseline": "regressao logistica sobre pixels",
    "batch_size": 32,
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
    print("  pipeline: DataLoader(pin_memory) + autocast/GradScaler (AMP)")
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
    print("  monitor_treinamento.sh -> logs/monitor/*.csv (temp, potencia, VRAM)")
    print("  alerta automatico se temperatura >= 82 C\n")


# ---------- 4. Apresentar (Aula 23) ----------
def etapa4_apresentar():
    print("=== 4. Apresentar (Aula 23) ===")
    metricas = {"tempo_epoca_s": (320, 38), "val_acc_pct": (71.2, 87.6),
                "throughput": (48, 410)}
    print(f"  {'metrica':<18} {'CPU':>8} {'GPU':>8}")
    for nome, (cpu, gpu) in metricas.items():
        print(f"  {nome:<18} {cpu:>8} {gpu:>8}")
    print()

    # gera o grafico do relatorio
    cats = list(metricas.keys())
    cpu = [metricas[c][0] for c in cats]
    gpu = [metricas[c][1] for c in cats]
    fig, ax = plt.subplots(figsize=(8, 4))
    x = range(len(cats))
    ax.bar([i - 0.2 for i in x], cpu, 0.4, label="CPU", color="#94A3B8")
    ax.bar([i + 0.2 for i in x], gpu, 0.4, label="GPU", color="#F97316")
    ax.set_xticks(list(x)); ax.set_xticklabels(cats, fontsize=8, rotation=10)
    ax.set_title(f"Baseline x GPU - {CONFIG['nome']}")
    ax.legend(); fig.tight_layout()
    fig.savefig("relatorio.png", dpi=150)
    print("  relatorio.png salvo.\n")


# ---------- 5. Conectar ao PI (Aula 24) ----------
def etapa5_conectar():
    print("=== 5. Conectar ao PI (Aula 24) ===")
    print("  - pre-processamento de imagens do PI na GPU")
    print("  - monitor de GPU integrado ao treino do PI\n")


def main():
    etapa1_planejar()
    etapa2_implementar()
    etapa3_monitorar()
    etapa4_apresentar()
    etapa5_conectar()
    print("Projeto concluido (exemplo).")


if __name__ == "__main__":
    main()
