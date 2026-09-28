import csv
import datetime
import os
import sys

def main():
    limite_temp = int(sys.argv[1]) if len(sys.argv) > 1 else 75
    limite_util = int(sys.argv[2]) if len(sys.argv) > 2 else 90

    csv_file = os.path.join("reports", "gpu_log.csv")
    log_file = os.path.join("reports", "alertas.log")

    if not os.path.exists(csv_file):
        print(f"Erro: Arquivo '{csv_file}' não encontrado. Execute o script 1_monitor_gpu primeiro.")
        return

    alertas_gerados = 0
    with open(csv_file, "r", encoding="utf-8") as f_in, open(log_file, "a", encoding="utf-8") as f_out:
        reader = csv.DictReader(f_in)
        for row in reader:
            try:
                temp = float(row["temp_c"])
                util = float(row["util_gpu_pct"])
                ts = row["timestamp"]
                gpu_name = row["gpu_name"]
                gpu_idx = row["gpu_index"]

                if temp >= limite_temp:
                    msg = f"[{ts}] ALERTA TEMPERATURA: GPU {gpu_idx} ({gpu_name}) atingiu {temp}°C (Limite: {limite_temp}°C)\n"
                    print(msg.strip())
                    f_out.write(msg)
                    alertas_gerados += 1

                if util >= limite_util:
                    msg = f"[{ts}] ALERTA UTILIZAÇÃO: GPU {gpu_idx} ({gpu_name}) atingiu {util}% (Limite: {limite_util}%)\n"
                    print(msg.strip())
                    f_out.write(msg)
                    alertas_gerados += 1
            except (ValueError, KeyError):
                continue

    print(f"\nVerificação concluída. Total de alertas registrados em '{log_file}': {alertas_gerados}")

if __name__ == "__main__":
    main()
