#!/usr/bin/env bash
# ============================================================================
# alerta_gpu.sh — verifica limites de temperatura/utilização e notifica
# ----------------------------------------------------------------------------
# Uso: ./alerta_gpu.sh [limite_temp] [limite_util]
# Ex.: ./alerta_gpu.sh 80 95
# ============================================================================
set -euo pipefail

LIMITE_TEMP="${1:-80}"   # °C
LIMITE_UTIL="${2:-95}"   # %
LOG_ALERTAS="/tmp/gpu_alertas.log"           # grava em /tmp (não exige root)
SLACK_WEBHOOK="${SLACK_WEBHOOK_URL:-}"       # opcional: webhook Slack/Discord

# ── Função que dispara o alerta por todos os canais disponíveis ─────────────
alerta() {
    local msg="$1"
    local ts
    ts=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$ts] ALERTA: $msg" | tee -a "$LOG_ALERTAS"

    # Slack/Discord webhook (só se a variável de ambiente estiver definida)
    if [ -n "$SLACK_WEBHOOK" ]; then
        curl -s -X POST "$SLACK_WEBHOOK" \
             -H "Content-Type: application/json" \
             -d "{\"text\": \"GPU Alert [$ts]: $msg\"}" > /dev/null
    fi

    # E-mail (só se o comando 'mail' estiver instalado)
    if command -v mail &>/dev/null; then
        echo "$msg" | mail -s "GPU ALERT: $msg" "admin@empresa.com"
    fi
}

# ── Verifica cada GPU ───────────────────────────────────────────────────────
# O separador é ', ' (vírgula + espaço) porque usamos --format=csv,noheader
while IFS=", " read -r idx nome temp util; do
    if [ "$temp" -ge "$LIMITE_TEMP" ]; then
        alerta "GPU $idx ($nome): temperatura ${temp}C >= ${LIMITE_TEMP}C"
    fi
    if [ "$util" -ge "$LIMITE_UTIL" ]; then
        alerta "GPU $idx ($nome): utilizacao ${util}% >= ${LIMITE_UTIL}%"
    fi
done < <(nvidia-smi \
    --query-gpu=index,name,temperature.gpu,utilization.gpu \
    --format=csv,noheader,nounits)

echo "Verificacao concluida: $(date)"
