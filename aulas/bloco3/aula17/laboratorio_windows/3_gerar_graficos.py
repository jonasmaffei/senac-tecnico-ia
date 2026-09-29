import os
import matplotlib.pyplot as plt
import pandas as pd

def main():
    csv_file = os.path.join("reports", "gpu_log.csv")
    output_png = os.path.join("reports", "gpu_dashboard.png")

    if not os.path.exists(csv_file):
        print(f"Erro: Arquivo '{csv_file}' nao existe. Execute o monitoramento primeiro.")
        return

    try:
        df = pd.read_csv(csv_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        fig, axes = plt.subplots(2, 2, figsize=(14, 9))
        fig.suptitle("GPU & Hardware Monitoring Dashboard", fontsize=16, fontweight='bold')

        # 1. Temperatura
        axes[0, 0].plot(df['timestamp'], df['temp_c'], color='#EF4444', linewidth=2, label='Temp (C)')
        axes[0, 0].axhline(y=75, color='#F97316', linestyle='--', label='Limite 75C')
        axes[0, 0].set_title("Temperatura (C)")
        axes[0, 0].grid(True, linestyle=':', alpha=0.6)
        axes[0, 0].legend()

        # 2. Utilizacao
        axes[0, 1].plot(df['timestamp'], df['util_gpu_pct'], color='#10B981', linewidth=2, label='GPU Util %')
        axes[0, 1].plot(df['timestamp'], df['util_mem_pct'], color='#6366F1', linewidth=2, label='Mem Util %')
        axes[0, 1].set_title("Utilizacao (%)")
        axes[0, 1].grid(True, linestyle=':', alpha=0.6)
        axes[0, 1].legend()

        # 3. VRAM / RAM
        axes[1, 0].fill_between(df['timestamp'], df['mem_used_mb'], color='#7E22CE', alpha=0.3, label='Memoria Usada (MB)')
        axes[1, 0].plot(df['timestamp'], df['mem_used_mb'], color='#7E22CE', linewidth=2)
        axes[1, 0].set_title("Alocacao de Memoria (MB)")
        axes[1, 0].grid(True, linestyle=':', alpha=0.6)
        axes[1, 0].legend()

        # 4. Potencia
        axes[1, 1].plot(df['timestamp'], df['power_w'], color='#F97316', linewidth=2, label='Consumo (W)')
        axes[1, 1].plot(df['timestamp'], df['power_limit_w'], color='#EF4444', linestyle='--', label='Limite Potencia (W)')
        axes[1, 1].set_title("Potencia (Watts)")
        axes[1, 1].grid(True, linestyle=':', alpha=0.6)
        axes[1, 1].legend()

        plt.tight_layout()
        plt.savefig(output_png, dpi=150)
        plt.close()
        print(f"Sucesso! Dashboard gerado e salvo em: '{output_png}'")
    except Exception as e:
        print(f"Erro ao gerar graficos: {e}")

if __name__ == "__main__":
    main()
