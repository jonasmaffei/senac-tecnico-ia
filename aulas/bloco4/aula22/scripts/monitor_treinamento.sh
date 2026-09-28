#!/usr/bin/env bash
# monitor_treinamento.sh — monitora a GPU durante o treino (Aula 22)
# Uso: ./monitor_treinamento.sh <pid_do_treino> [intervalo_s]
#
# Grava um CSV em logs/monitor/ e avisa se a temperatura passar do limite.

set -euo pipefail

PID_TREINO="${1:-0}"
INTERVALO="${2:-10}"
MAX_TEMP=82
LOG_DIR="./logs/monitor"
LOG_FILE="${LOG_DIR}/gpu_$(date +%Y%m%d_%H%M%S).csv"

mkdir -p "$LOG_DIR"
echo "timestamp,gpu_idx,temp_c,power_w,util_pct,mem_used_mb,mem_total_mb" > "$LOG_FILE"
echo "[Monitor] log=$LOG_FILE | limite=${MAX_TEMP}C"

while true; do
  # para sozinho quando o treino termina
  if [[ "$PID_TREINO" -gt 0 ]] && ! kill -0 "$PID_TREINO" 2>/dev/null; then
    echo "[Monitor] treino finalizado. Encerrando."
    break
  fi

  TS=$(date '+%Y-%m-%dT%H:%M:%S')
  nvidia-smi --query-gpu=index,temperature.gpu,power.draw,utilization.gpu,memory.used,memory.total \
    --format=csv,noheader,nounits | while IFS=',' read -r idx temp power util mem_used mem_total; do
    idx=$(echo "$idx" | tr -d ' '); temp=$(echo "$temp" | tr -d ' ')
    power=$(echo "$power" | tr -d ' '); util=$(echo "$util" | tr -d ' ')
    mem_used=$(echo "$mem_used" | tr -d ' '); mem_total=$(echo "$mem_total" | tr -d ' ')
    echo "${TS},${idx},${temp},${power},${util},${mem_used},${mem_total}" >> "$LOG_FILE"
    if [[ "$temp" -ge "$MAX_TEMP" ]]; then
      echo "[ALERTA] GPU${idx} em ${temp}C (limite ${MAX_TEMP}C)" | tee -a "$LOG_DIR/alertas.log"
    fi
  done

  sleep "$INTERVALO"
done
