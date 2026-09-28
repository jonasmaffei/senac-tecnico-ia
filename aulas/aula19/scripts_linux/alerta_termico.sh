#!/usr/bin/env bash
# alerta_termico.sh — alerta e AGE quando a temperatura excede o limite
# Uso: crontab -e -> */2 * * * * /opt/scripts/alerta_termico.sh
#
# Ao atingir o limite crítico, reduz o Power Limit automaticamente e notifica.
# Quando a temperatura normaliza, restaura o Power Limit de trabalho.

set -euo pipefail

TEMP_ALERTA=80      # °C — apenas alertar
TEMP_CRITICA=88     # °C — reduzir power limit automaticamente
PL_NORMAL=250       # Watts — power limit padrão
PL_REDUZIDO=150     # Watts — power limit de emergência
LOG="/var/log/gpu_alerta.log"

TS=$(date '+%Y-%m-%d %H:%M:%S')

nvidia-smi --query-gpu=index,temperature.gpu,power.draw,enforced.power.limit \
           --format=csv,noheader,nounits | \
while IFS=", " read -r idx temp pwr plimit; do

  if (( temp >= TEMP_CRITICA )); then
    echo "[${TS}] CRÍTICO GPU${idx}: ${temp}°C -> reduzindo PL para ${PL_REDUZIDO}W" | tee -a "$LOG"
    sudo nvidia-smi -i "${idx}" -pl "${PL_REDUZIDO}"
    # Notificação (exemplo com mail; troque por webhook se preferir)
    echo "GPU${idx} atingiu ${temp}°C — PL reduzido para ${PL_REDUZIDO}W" | mail -s "ALERTA GPU CRÍTICO" admin@empresa.com 2>/dev/null || true

  elif (( temp >= TEMP_ALERTA )); then
    echo "[${TS}] AVISO GPU${idx}: ${temp}°C (acima de ${TEMP_ALERTA}°C)" | tee -a "$LOG"

  else
    # Restaurar o PL normal se estava reduzido
    PLIMIT_INT=${plimit%.*}
    if (( PLIMIT_INT < PL_NORMAL )); then
      echo "[${TS}] GPU${idx}: ${temp}°C — restaurando PL para ${PL_NORMAL}W" | tee -a "$LOG"
      sudo nvidia-smi -i "${idx}" -pl "${PL_NORMAL}"
    fi
  fi

done
