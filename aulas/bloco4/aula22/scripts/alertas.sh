#!/usr/bin/env bash
# alertas.sh — sistema de alertas multi-canal para eventos críticos de GPU
# Suporta: log local | e-mail (sendmail) | webhook Slack | Telegram
#
# Configure as variáveis de ambiente antes de usar (ver .env.example).

set -uo pipefail

SLACK_WEBHOOK="${SLACK_WEBHOOK_URL:-}"
TELEGRAM_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT="${TELEGRAM_CHAT_ID:-}"
EMAIL_DEST="${ALERTA_EMAIL:-}"
HOSTNAME_SERVIDOR=$(hostname)
LOG_DIR="./logs/monitor"
mkdir -p "$LOG_DIR"

# ── Função central de alerta ──────────────────────────────
enviar_alerta() {
  local nivel="$1"   # INFO | WARN | CRITICAL
  local mensagem="$2"
  local ts
  ts=$(date '+%Y-%m-%d %H:%M:%S')
  local corpo="[$nivel] $HOSTNAME_SERVIDOR — $ts\n$mensagem"

  # 1. Log local (sempre)
  echo -e "$corpo" | tee -a "$LOG_DIR/alertas.log"

  # 2. Slack (se webhook configurado)
  if [[ -n "$SLACK_WEBHOOK" ]]; then
    local emoji="i"
    [[ "$nivel" == "WARN" ]] && emoji="!"
    [[ "$nivel" == "CRITICAL" ]] && emoji="!!"
    curl -s -X POST "$SLACK_WEBHOOK" \
      -H 'Content-type: application/json' \
      --data "{\"text\": \"${emoji} *${nivel}* — ${HOSTNAME_SERVIDOR}\n${mensagem}\"}" \
      > /dev/null
  fi

  # 3. Telegram (se token configurado)
  if [[ -n "$TELEGRAM_TOKEN" && -n "$TELEGRAM_CHAT" ]]; then
    curl -s "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
      -d "chat_id=${TELEGRAM_CHAT}" \
      -d "text=${corpo}" \
      > /dev/null
  fi

  # 4. E-mail via sendmail
  if [[ -n "$EMAIL_DEST" ]] && command -v sendmail &>/dev/null; then
    echo -e "Subject: [GPU ALERTA] $nivel\n\n$corpo" | sendmail "$EMAIL_DEST"
  fi
}

# ── Verificação periódica ─────────────────────────────────
verificar_gpu() {
  nvidia-smi --query-gpu=index,temperature.gpu,power.draw,utilization.gpu,memory.used,memory.total \
    --format=csv,noheader,nounits | while IFS=',' read -r idx temp power util mem_used mem_total; do

    temp=$(echo "$temp" | tr -d ' ')
    util=$(echo "$util" | tr -d ' ')
    mem_pct=$(( $(echo "$mem_used" | tr -d ' ') * 100 / $(echo "$mem_total" | tr -d ' ') ))

    if   [[ "$temp" -ge 90 ]]; then
      enviar_alerta "CRITICAL" "GPU${idx}: temperatura ${temp}C — RISCO DE THROTTLING"
    elif [[ "$temp" -ge 82 ]]; then
      enviar_alerta "WARN"     "GPU${idx}: temperatura ${temp}C — próximo do limite"
    fi

    if   [[ "$mem_pct" -ge 95 ]]; then
      enviar_alerta "CRITICAL" "GPU${idx}: VRAM ${mem_pct}% — risco de OOM iminente"
    elif [[ "$mem_pct" -ge 85 ]]; then
      enviar_alerta "WARN"     "GPU${idx}: VRAM ${mem_pct}% — uso elevado"
    fi

    if [[ "$util" -lt 20 ]]; then
      enviar_alerta "WARN" "GPU${idx}: utilização ${util}% — possível gargalo no DataLoader"
    fi
  done
}

# Loop de verificação
while true; do
  verificar_gpu
  sleep 30
done
