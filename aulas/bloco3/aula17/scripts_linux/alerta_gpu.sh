#!/usr/bin/env bash
# alerta_gpu.sh — Envia alerta se temperatura ou utilização ultrapassar limites

set -euo pipefail

LIMITE_TEMP="${1:-80}"
LIMITE_UTIL="${2:-95}"
LOG_ALERTAS="gpu_alertas.log"
SLACK_WEBHOOK="${SLACK_WEBHOOK_URL:-}"

alerta() {
    local msg="$1"
    local ts
    ts=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$ts] ALERTA: $msg" | tee -a "$LOG_ALERTAS"

    # Slack webhook (se configurado)
    if [ -n "$SLACK_WEBHOOK" ]; then
        curl -s -X POST "$SLACK_WEBHOOK" \
             -H "Content-Type: application/json" \
             -d "{\"text\": \"GPU Alert [$ts]: $msg\"}" > /dev/null || true
    fi

    # Email (se 'mail' disponível)
    if command -v mail &>/dev/null; then
        echo "$msg" | mail -s "GPU ALERT: $msg" "admin@empresa.com" || true
    fi
}

# ── Verificar cada GPU ────────────────────────────────────
if command -v nvidia-smi &>/dev/null; then
    DADOS_ENTRADA=$(nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu --format=csv,noheader,nounits)
else
    DADOS_ENTRADA="0, GPU Simulada, 85, 96"
fi

while IFS="," read -r idx nome temp util; do
    # Remover espaços em branco
    idx=$(echo "$idx" | xargs)
    nome=$(echo "$nome" | xargs)
    temp=$(echo "$temp" | xargs)
    util=$(echo "$util" | xargs)

    if [ "$temp" -ge "$LIMITE_TEMP" ]; then
        alerta "GPU $idx ($nome): temperatura ${temp}°C >= ${LIMITE_TEMP}°C"
    fi
    if [ "$util" -ge "$LIMITE_UTIL" ]; then
        alerta "GPU $idx ($nome): utilização ${util}% >= ${LIMITE_UTIL}%"
    fi
done <<< "$DADOS_ENTRADA"

echo "Verificação concluída: $(date +"%Y-%m-%d %H:%M:%S")"
