#!/usr/bin/env bash
# monitor_processos_gpu.sh - Monitorar processos em tempo real na GPU e fila de execucao

set -euo pipefail

echo "=== Processos na GPU ==="
if command -v nvidia-smi &>/dev/null; then
    nvidia-smi --query-compute-apps=pid,process_name,used_gpu_memory,gpu_uuid \
               --format=csv,noheader | \
    while IFS="," read -r pid nome mem uuid; do
        pid=$(echo "$pid" | xargs)
        cmd=$(ps -p "$pid" -o comm= 2>/dev/null || echo "N/A")
        user=$(ps -p "$pid" -o user= 2>/dev/null || echo "N/A")
        echo "  PID=$pid | USER=$user | CMD=$cmd | VRAM=${mem}MB"
    done
else
    echo "  (NVIDIA GPU nao detectada. Exibindo processos Python do host)"
    ps aux | grep "[p]ython" || echo "  Nenhum processo Python ativo."
fi

echo ""
echo "=== Utilizacao da GPU ==="
if command -v nvidia-smi &>/dev/null; then
    nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total \
               --format=csv,noheader,nounits | \
    while IFS="," read -r idx nome util mem_used mem_total; do
        pct=$(( mem_used * 100 / mem_total ))
        echo "  GPU $idx ($nome): util=${util}% | VRAM=${mem_used}/${mem_total}MB (${pct}%)"
    done
fi

echo ""
echo "=== Fila Atual (gpu_queue_spool) ==="
QUEUE_DIR="gpu_queue_spool"
if [ -d "$QUEUE_DIR" ] && [ "$(ls -A $QUEUE_DIR 2>/dev/null)" ]; then
    ls "$QUEUE_DIR" | sort | nl -w3 -s'. '
else
    echo "  Fila vazia."
fi
