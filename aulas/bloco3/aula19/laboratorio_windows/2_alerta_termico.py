"""2_alerta_termico.py — Analisa o CSV e dispara alertas por limiar térmico.

Uso: python 2_alerta_termico.py [temp_alerta] [temp_critica]

Lê reports/gpu_thermal.csv, classifica cada leitura e grava um log em
reports/alertas_termicos.log. Também mostra a ação recomendada:
  - >= critica  -> reduzir o Power Limit automaticamente (emergência)
  - >= alerta   -> apenas registrar/notificar
"""

import csv
import os
import sys

from lib_energia import timestamp

TEMP_ALERTA = 80.0
TEMP_CRITICA = 88.0


def main():
    alerta = float(sys.argv[1]) if len(sys.argv) > 1 else TEMP_ALERTA
    critica = float(sys.argv[2]) if len(sys.argv) > 2 else TEMP_CRITICA

    csv_file = os.path.join("reports", "gpu_thermal.csv")
    log_file = os.path.join("reports", "alertas_termicos.log")

    if not os.path.exists(csv_file):
        print(f"Erro: '{csv_file}' não existe. Rode 1_monitor_thermal.py primeiro.")
        return

    total = 0
    with open(csv_file, encoding="utf-8") as f_in, open(log_file, "a", encoding="utf-8") as f_out:
        for linha in csv.DictReader(f_in):
            try:
                temp = float(linha["temp_c"])
            except (ValueError, KeyError):
                continue

            if temp >= critica:
                nivel, acao = "CRÍTICO", f"reduzir PL para {int(linha['power_limit_w'] * 0.6)}W"
            elif temp >= alerta:
                nivel, acao = "AVISO", "apenas registrar/notificar"
            else:
                continue  # temperatura normal: não gera log

            msg = (f"[{linha['timestamp']}] {nivel} | {linha['gpu_name']} | "
                   f"{temp:.0f}°C (limiar {alerta:.0f}/{critica:.0f}°C) -> {acao}")
            print(msg)
            f_out.write(msg + "\n")
            total += 1

    print(f"\nVerificação concluída às {timestamp()}. "
          f"Alertas registrados em '{log_file}': {total}")


if __name__ == "__main__":
    main()
