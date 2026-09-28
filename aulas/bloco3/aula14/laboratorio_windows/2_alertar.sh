#!/usr/bin/env bash
# ============================================================================
# 2_alertar.sh — verifica limites de temperatura/utilização e mostra alertas
# ----------------------------------------------------------------------------
# Uso:  ./2_alertar.sh [limite_temp] [limite_util]
# Ex.:  ./2_alertar.sh 80 95
#
# Lê os dados atuais da GPU (real ou simulada). Se existir gpu_log.csv,
# usa a última amostra coletada. Registra os alertas em alertas.log.
# ============================================================================

cd "$(dirname "$0")" || exit 1
source ./lib_gpu.sh

set -euo pipefail

LIMITE_TEMP="${1:-80}"     # °C
LIMITE_UTIL="${2:-95}"     # %
LOG_ALERTAS="${LOG_ALERTAS:-$DIR_RELATORIOS/alertas.log}"

# Cria a pasta de relatórios, caso ainda não exista
preparar_relatorios

# Nome do CSV gerado pelo 1_monitorar.sh (dentro de reports/)
CSV_ENTRADA="$DIR_RELATORIOS/gpu_log.csv"

# ── Obtém uma linha no formato "index, name, temp, util" ────────────────────
obter_linha() {
    if [ -f "$CSV_ENTRADA" ]; then
        # Pega a última linha do CSV: timestamp,idx,nome,temp,util,...
        # Constrói "idx, nome, temp, util" para reaproveitar o mesmo parser.
        local ultima
        ultima=$(tail -n 1 "$CSV_ENTRADA")
        local idx nome temp util
        IFS=',' read -r _ idx nome temp util _ _ _ _ _ <<< "$ultima"
        # Remove espaços ao redor de cada campo
        idx=$(printf '%s' "$idx" | tr -d ' ')
        nome=$(printf '%s' "$nome" | sed 's/^ *//; s/ *$//')
        temp=$(printf '%s' "$temp" | tr -d ' ')
        util=$(printf '%s' "$util" | tr -d ' ')
        echo "$idx, $nome, $temp, $util"
    else
        # Sem CSV: consulta direto (real ou simulado)
        obter_dados_gpu 0 | head -n 1 | \
            cut -d',' -f1,2,3,4
    fi
}

# ── Dispara o alerta nos canais disponíveis ─────────────────────────────────
alerta() {
    local msg="$1"
    local ts
    ts=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$ts] ALERTA: $msg" | tee -a "$LOG_ALERTAS"

    # Webhook Slack/Discord (opcional; defina a variável SLACK_WEBHOOK_URL)
    if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
        curl -s -X POST "$SLACK_WEBHOOK_URL" \
             -H "Content-Type: application/json" \
             -d "{\"text\": \"GPU Alert [$ts]: $msg\"}" >/dev/null 2>&1 || true
    fi
}

# ── Verifica os limites ─────────────────────────────────────────────────────
aviso_modo
LINHA=$(obter_linha)

while IFS=',' read -r idx nome temp util; do
    idx=$(printf '%s' "$idx" | tr -d ' ')
    nome=$(printf '%s' "$nome" | sed 's/^ *//; s/ *$//')
    temp=$(printf '%s' "$temp" | tr -d ' ')
    util=$(printf '%s' "$util" | tr -d ' ')

    # Campos podem vir "N/A" (ex.: fan.speed no T4); ignoramos não numéricos
    if [[ "$temp" =~ ^[0-9]+$ ]] && [ "$temp" -ge "$LIMITE_TEMP" ]; then
        alerta "GPU $idx ($nome): temperatura ${temp}C >= ${LIMITE_TEMP}C"
    fi
    if [[ "$util" =~ ^[0-9]+$ ]] && [ "$util" -ge "$LIMITE_UTIL" ]; then
        alerta "GPU $idx ($nome): utilizacao ${util}% >= ${LIMITE_UTIL}%"
    fi
done <<< "$LINHA"

echo "Verificacao concluida: $(date). Log: $LOG_ALERTAS"
