#!/usr/bin/env bash
# ============================================================================
# alerta_gpu.sh - verifica limites de temperatura/utilizacao e notifica
# ----------------------------------------------------------------------------
# Uso: ./alerta_gpu.sh [limite_temp] [limite_util]
# Ex.: ./alerta_gpu.sh 80 95
# ============================================================================
set -euo pipefail

LIMITE_TEMP="${1:-80}"   # C
LIMITE_UTIL="${2:-95}"   # %
# Log configuravel; padrao em /tmp (nao exige root e funciona no Colab).
# Em servidores reais, use LOG_ALERTAS=/var/log/gpu_alertas.log
LOG_ALERTAS="${LOG_ALERTAS:-/tmp/gpu_alertas.log}"
SLACK_WEBHOOK="${SLACK_WEBHOOK_URL:-}"       # opcional: webhook Slack/Discord

# -- Funcao que dispara o alerta por todos os canais disponiveis -------------
alerta() {
    local msg="$1"
    local ts
    ts=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$ts] ALERTA: $msg" | tee -a "$LOG_ALERTAS"

    # Slack/Discord webhook (so se a variavel de ambiente estiver definida)
    if [ -n "$SLACK_WEBHOOK" ]; then
        curl -s -X POST "$SLACK_WEBHOOK" \
             -H "Content-Type: application/json" \
             -d "{\"text\": \"GPU Alert [$ts]: $msg\"}" > /dev/null
    fi

    # E-mail (so se o comando 'mail' estiver instalado)
    if command -v mail &>/dev/null; then
        echo "$msg" | mail -s "GPU ALERT: $msg" "admin@empresa.com"
    fi
}

# -- Fonte dos dados: nvidia-smi (real) ou a ultima amostra do CSV (simulado) -
# A query devolve CSV no formato: "0, Tesla T4, 52, 87".
# Sem GPU NVIDIA, usamos a ultima linha do gpu_log.csv (se existir) ou uma
# amostra simulada - assim o alerta tambem funciona no laboratorio.
if command -v nvidia-smi >/dev/null 2>&1; then
    DADOS=$(nvidia-smi \
        --query-gpu=index,name,temperature.gpu,utilization.gpu \
        --format=csv,noheader,nounits)
elif [ -f gpu_log.csv ]; then
    ULTIMA=$(tail -n 1 gpu_log.csv)
    IFS="," read -r _ idx nome temp util _ <<< "$ULTIMA"
    DADOS="$idx, $nome, $temp, $util"
else
    DADOS="0, Tesla T4 (sim), 84, 97"
fi

# -- Verifica cada GPU -------------------------------------------------------
# Separamos por virgula (IFS=",") e removemos os espacos com tr.
# IMPORTANTE: NAO usar IFS=", " - o shell trataria virgula E espaco como
# separadores, desalinhando os campos (ex.: temp receberia "T4").
while IFS="," read -r idx nome temp util; do
    # Remove espacos em branco ao redor de cada campo
    idx=$(printf '%s' "$idx" | tr -d ' ')
    nome=$(printf '%s' "$nome" | sed 's/^ *//; s/ *$//')
    temp=$(printf '%s' "$temp" | tr -d ' ')
    util=$(printf '%s' "$util" | tr -d ' ')

    # Campos podem vir "N/A" (ex.: fan.speed no T4); ignoramos valores nao numericos
    if [[ "$temp" =~ ^[0-9]+$ ]] && [ "$temp" -ge "$LIMITE_TEMP" ]; then
        alerta "GPU $idx ($nome): temperatura ${temp}C >= ${LIMITE_TEMP}C"
    fi
    if [[ "$util" =~ ^[0-9]+$ ]] && [ "$util" -ge "$LIMITE_UTIL" ]; then
        alerta "GPU $idx ($nome): utilizacao ${util}% >= ${LIMITE_UTIL}%"
    fi
done <<< "$DADOS"

echo "Verificacao concluida: $(date)"
