"""4_controle_pl.py — Controle programático do Power Limit.

Uso: python 4_controle_pl.py [watts]

Em GPU NVIDIA real, tenta aplicar o Power Limit via NVML (nvidia-ml-py);
se não houver permissão/GPU, explica o modo simulado. Também exibe as
constraints (faixa) suportadas pela placa.
"""

import sys

from lib_energia import detectar_backend


def main():
    watts = int(sys.argv[1]) if len(sys.argv) > 1 else 180
    backend = detectar_backend()
    print(f"Backend detectado: {backend}")

    try:
        import pynvml

        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)

        pl_min, pl_max = pynvml.nvmlDeviceGetPowerManagementLimitConstraints(handle)
        atual = pynvml.nvmlDeviceGetPowerManagementLimit(handle) / 1000
        print(f"Power Limit atual: {atual:.0f}W")
        print(f"Faixa suportada:   {pl_min // 1000}W - {pl_max // 1000}W")

        # Só aplica se estiver dentro da faixa suportada
        if not (pl_min // 1000 <= watts <= pl_max // 1000):
            print(f"\n{watts}W está fora da faixa suportada. Ajuste e tente novamente.")
            pynvml.nvmlShutdown()
            return

        try:
            pynvml.nvmlDeviceSetPowerManagementLimit(handle, watts * 1000)
            print(f"\nPower Limit configurado para {watts}W.")
        except pynvml.NVMLError as e:
            print(f"\nNão foi possível aplicar (precisa de root?): {e}")

        pynvml.nvmlShutdown()
    except Exception as e:
        # Sem NVML (AMD/Windows ou sem GPU): apenas demonstra o conceito
        print(f"NVML indisponível ({e}).")
        print(f"[SIMULADO] O Power Limit seria ajustado para {watts}W em uma GPU NVIDIA.")
        print("Em Linux com GPU NVIDIA, o comando equivalente seria:")
        print(f"    sudo nvidia-smi -i 0 -pl {watts}")


if __name__ == "__main__":
    main()
