#!/usr/bin/env bash
# ============================================================================
# monitor_gpu.sh — coleta métricas de GPU com nvidia-smi e salva em CSV
# ----------------------------------------------------------------------------
# Uso: ./monitor_gpu.sh [intervalo_segundos] [arquivo_saida] [duracao_segundos]
# Ex.: ./monitor_gpu.sh 5 gpu_log.csv 3600
# ============================================================================

# 'set -euo pipefail' torna o script rigoroso:
#   -e = para no primeiro erro
#   -u = erro se usar variável não definida
#   -o pipefail = erro se qualquer comando de um pipe falhar
set -euo pipefail

# ── Parâmetros (com valores padrão caso não sejam informados) ───────────────
INTERVALO="${1:-5}"                              # segundos entre coletas
SAIDA="${2:-gpu_log_$(date +%Y%m%d_%H%M%S).csv}" # arquivo CSV de saída
DURACAO="${3:-3600}"                             # duração total em segundos

# Calcula quantas amostras cabem na duração informada (evita divisão por zero)
if [ "$INTERVALO" -gt 0 ]; then
    MAX_AMOSTRAS=$(( DURACAO / INTERVALO ))
else
    MAX_AMOSTRAS=720
fi

# ── Cabeçalho do CSV ────────────────────────────────────────────────────────
CABECALHO="timestamp,gpu_index,gpu_name,temp_c,util_gpu_pct,"
CABECALHO+="util_mem_pct,mem_used_mb,mem_total_mb,power_w,power_limit_w,"
CABECALHO+="clock_graphics_mhz,clock_mem_mhz"

echo "$CABECALHO" > "$SAIDA"
echo "Iniciando monitoramento -> $SAIDA"
echo "Intervalo: ${INTERVALO}s | Duracao: ${DURACAO}s | Amostras: ${MAX_AMOSTRAS}"

# ── Loop de coleta ──────────────────────────────────────────────────────────
AMOSTRA=0
while [ "$AMOSTRA" -lt "$MAX_AMOSTRAS" ]; do
    TS=$(date +"%Y-%m-%d %H:%M:%S")  # Timestamp da coleta

    # nvidia-smi --query-gpu devolve UMA LINHA POR GPU (CSV sem cabeçalho/unidades)
    DADOS=$(nvidia-smi \
        --query-gpu=index,name,temperature.gpu,utilization.gpu,\
utilization.memory,memory.used,memory.total,\
power.draw,power.limit,clocks.current.graphics,clocks.current.memory \
        --format=csv,noheader,nounits)

    # Prefixa o timestamp em cada linha (cada GPU vira uma linha do CSV)
    while IFS= read -r linha; do
        echo "$TS,$linha" >> "$SAIDA"
    done <<< "$DADOS"

    AMOSTRA=$(( AMOSTRA + 1 ))
    echo -ne "  Amostra $AMOSTRA/$MAX_AMOSTRAS\r"
    sleep "$INTERVALO"
done

echo ""
echo "Coleta concluida. Arquivo: $SAIDA"
