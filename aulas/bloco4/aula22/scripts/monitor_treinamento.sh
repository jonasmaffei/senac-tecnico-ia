#!/usr/bin/env bash
# monitor_treinamento.sh — monitoramento GPU integrado ao pipeline de IA
# Executa em paralelo ao train.py, gera log CSV e alerta ao ultrapassar limites.
# Uso: ./monitor_treinamento.sh <pid_do_treinamento> <projeto>

set -euo pipefail

PID_TREINO="${1:-0}"
PROJETO="${2:-projeto_ia}"
INTERVALO=10          # segundos entre amostras
MAX_TEMP=82           # °C — threshold de alerta térmico
MAX_MEMORIA_PCT=90    # % de VRAM usada — threshold de alerta de memória
LOG_DIR="./logs/monitor"
LOG_FILE="${LOG_DIR}/${PROJETO}_$(date +%Y%m%d_%H%M%S).csv"

mkdir -p "$LOG_DIR"

# ── Cabeçalho do CSV ──────────────────────────────────────
echo "timestamp,gpu_idx,temp_c,power_w,util_pct,mem_used_mb,mem_total_mb,mem_pct,treino_ativo" > "$LOG_FILE"
echo "[Monitor] Iniciado — projeto=$PROJETO log=$LOG_FILE"
echo "[Monitor] Thresholds: temp<${MAX_TEMP}C | VRAM<${MAX_MEMORIA_PCT}%"

alertar() {
  local tipo="$1" valor="$2" limite="$3"
  echo "[ALERTA $(date '+%H:%M:%S')] $tipo = $valor (limite: $limite)" | tee -a "${LOG_DIR}/alertas.log"
  # Para notificação real, chame aqui o scripts/alertas.sh (Slack/Telegram/e-mail).
}

while true; do
  # Encerra o monitor quando o treinamento termina
  if [[ "$PID_TREINO" -gt 0 ]] && ! kill -0 "$PID_TREINO" 2>/dev/null; then
    echo "[Monitor] Treinamento PID=${PID_TREINO} finalizado. Encerrando monitor."
    break
  fi

  TREINO_ATIVO=$([[ "$PID_TREINO" -gt 0 ]] && kill -0 "$PID_TREINO" 2>/dev/null && echo "1" || echo "0")
  TS=$(date '+%Y-%m-%dT%H:%M:%S')

  # Coletar métricas via nvidia-smi (todas as GPUs)
  nvidia-smi --query-gpu=index,temperature.gpu,power.draw,utilization.gpu,memory.used,memory.total \
    --format=csv,noheader,nounits | while IFS=',' read -r idx temp power util mem_used mem_total; do

    idx=$(echo "$idx" | tr -d ' ')
    temp=$(echo "$temp" | tr -d ' ')
    power=$(echo "$power" | tr -d ' ' | cut -d. -f1)
    util=$(echo "$util" | tr -d ' ')
    mem_used=$(echo "$mem_used" | tr -d ' ')
    mem_total=$(echo "$mem_total" | tr -d ' ')
    mem_pct=$(( mem_used * 100 / mem_total ))

    echo "${TS},${idx},${temp},${power},${util},${mem_used},${mem_total},${mem_pct},${TREINO_ATIVO}" >> "$LOG_FILE"

    # Alertas automáticos
    if [[ "$temp" -ge "$MAX_TEMP" ]]; then
      alertar "TEMPERATURA GPU${idx}" "${temp}C" "${MAX_TEMP}C"
    fi
    if [[ "$mem_pct" -ge "$MAX_MEMORIA_PCT" ]]; then
      alertar "VRAM GPU${idx}" "${mem_pct}%" "${MAX_MEMORIA_PCT}%"
    fi
  done

  sleep "$INTERVALO"
done

echo "[Monitor] Encerrado. Log salvo em: $LOG_FILE"
