#!/usr/bin/env bash
# set_power_limit.sh - configura o Power Limit da(s) GPU(s)
# Uso: ./set_power_limit.sh <watts> [gpu_idx]
#
# Requer sudo/root. Consultar limites antes:
#   nvidia-smi -q -d POWER | grep -i "power limit"

set -euo pipefail

WATTS="${1?Informe a potencia em watts: ex. 200}"
GPU_IDX="${2:-all}"    # "all" aplica em todas as GPUs

# -- Verificar limites suportados -------------------------
echo "=== Limites de potencia disponiveis ==="
nvidia-smi -q -d POWER | grep -E "(Min|Max|Default|Enforced) Power Limit"
echo ""

# -- Aplicar o limite -------------------------------------
if [ "$GPU_IDX" = "all" ]; then
  GPU_COUNT=$(nvidia-smi --query-gpu=count --format=csv,noheader | head -1)
  for i in $(seq 0 $(( GPU_COUNT - 1 ))); do
    sudo nvidia-smi -i "$i" -pl "$WATTS"
    echo "GPU$i: Power Limit definido para ${WATTS}W"
  done
else
  sudo nvidia-smi -i "$GPU_IDX" -pl "$WATTS"
  echo "GPU${GPU_IDX}: Power Limit definido para ${WATTS}W"
fi

# -- Verificacao pos-configuracao -------------------------
echo ""
echo "=== Verificacao pos-configuracao ==="
nvidia-smi --query-gpu=index,power.draw,enforced.power.limit \
           --format=csv,noheader,nounits | \
while IFS=", " read -r idx pwr plimit; do
  echo "GPU${idx}: Potencia atual=${pwr}W | Limite=${plimit}W"
done
