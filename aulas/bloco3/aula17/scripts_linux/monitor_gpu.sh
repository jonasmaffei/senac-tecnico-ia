#!/usr/bin/env bash
# monitor_gpu.sh - Coleta metricas de GPU e salva em CSV
# Uso: ./monitor_gpu.sh [intervalo_segundos] [arquivo_saida] [duracao_segundos]

set -euo pipefail

INTERVALO="${1:-5}"
SAIDA="${2:-gpu_log_$(date +%Y%m%d_%H%M%S).csv}"
DURACAO="${3:-3600}"

if [ "$INTERVALO" -le 0 ]; then
    INTERVALO=5
fi
MAX_AMOSTRAS=$(( DURACAO / INTERVALO ))

# -- Cabecalho CSV -----------------------------------------
CABECALHO="timestamp,gpu_index,gpu_name,temp_c,util_gpu_pct,"
CABECALHO+="util_mem_pct,mem_used_mb,mem_total_mb,power_w,power_limit_w,"
CABECALHO+="clock_graphics_mhz,clock_mem_mhz"

echo "$CABECALHO" > "$SAIDA"
echo "Iniciando monitoramento -> $SAIDA"
echo "Intervalo: ${INTERVALO}s | Duracao: ${DURACAO}s | Amostras: ${MAX_AMOSTRAS}"

# -- Loop de coleta ----------------------------------------
AMOSTRA=0
while [ "$AMOSTRA" -lt "$MAX_AMOSTRAS" ]; do
    TS=$(date +"%Y-%m-%d %H:%M:%S")

    if command -v nvidia-smi &>/dev/null; then
        DADOS=$(nvidia-smi \
            --query-gpu=index,name,temperature.gpu,utilization.gpu,utilization.memory,memory.used,memory.total,power.draw,power.limit,clocks.current.graphics,clocks.current.memory \
            --format=csv,noheader,nounits)
    else
        # Modo simulado caso nao haja GPU NVIDIA
        DADOS="0, GPU Simulada, $(( 45 + RANDOM % 40 )), $(( 20 + RANDOM % 75 )), $(( 10 + RANDOM % 60 )), $(( 2048 + RANDOM % 4000 )), 16384, $(( 50 + RANDOM % 100 )).0, 250.0, 1410, 5001"
    fi

    while IFS= read -r linha; do
        echo "$TS,$linha" >> "$SAIDA"
    done <<< "$DADOS"

    AMOSTRA=$(( AMOSTRA + 1 ))
    echo -ne "  Amostra $AMOSTRA/$MAX_AMOSTRAS\r"
    sleep "$INTERVALO"
done

echo ""
echo "Coleta concluida. Arquivo: $SAIDA"
