#!/usr/bin/env bash
# monitor_thermal.sh - monitora temperatura, potencia, clock e utilizacao da GPU
# Uso: ./monitor_thermal.sh [intervalo_segundos] [duracao_segundos]
#
# Salva CSV em gpu_thermal_<data>.csv e exibe ao vivo no terminal.

set -euo pipefail

INTERVALO="${1:-5}"
DURACAO="${2:-3600}"
LOG_FILE="gpu_thermal_$(date +%Y%m%d).csv"

if [ "$INTERVALO" -le 0 ]; then INTERVALO=5; fi
MAX_AMOSTRAS=$(( DURACAO / INTERVALO ))

# -- Cabecalho CSV (somente na primeira execucao) ---------
if [ ! -f "$LOG_FILE" ]; then
  echo "timestamp,gpu_idx,temp_c,power_w,power_limit_w,gpu_util_pct,mem_util_pct,clock_sm_mhz,clock_mem_mhz" > "$LOG_FILE"
fi

echo "Monitorando GPUs a cada ${INTERVALO}s - Ctrl+C para parar"
echo "Log: $LOG_FILE"
echo ""

AMOSTRA=0
while [ "$AMOSTRA" -lt "$MAX_AMOSTRAS" ]; do
  TS=$(date '+%Y-%m-%d %H:%M:%S')

  # --query-gpu devolve uma linha por GPU no formato CSV
  nvidia-smi \
    --query-gpu=index,temperature.gpu,power.draw,enforced.power.limit,utilization.gpu,utilization.memory,clocks.sm,clocks.mem \
    --format=csv,noheader,nounits | \
  while IFS=", " read -r idx temp pwr plimit util_gpu util_mem clk_sm clk_mem; do
    echo "${TS},${idx},${temp},${pwr},${plimit},${util_gpu},${util_mem},${clk_sm},${clk_mem}" >> "$LOG_FILE"
    printf "[%s] GPU%s | Temp: %sC | Pwr: %sW/%sW | GPU: %s%% | Mem: %s%% | SMclk: %sMHz\n" \
      "$TS" "$idx" "$temp" "$pwr" "$plimit" "$util_gpu" "$util_mem" "$clk_sm"
  done

  AMOSTRA=$(( AMOSTRA + 1 ))
  sleep "${INTERVALO}"
done

echo ""
echo "Coleta concluida. Arquivo: $LOG_FILE"
