#!/usr/bin/env bash
# benchmark_energetico.sh — mede throughput e eficiência (imgs/J) por Power Limit
# Uso: ./benchmark_energetico.sh 250 200 150 100
#
# Requer GPU NVIDIA + sudo. Faz um warm-up em cada PL e mede a potência média.

set -euo pipefail

PL_LIST=("$@")
if [ "${#PL_LIST[@]}" -eq 0 ]; then PL_LIST=(250 200 150 100); fi

DURACAO_TESTE=15   # segundos de teste por Power Limit

medir_potencia_media() {
  # Amostra a potência algumas vezes e devolve a média
  local soma=0 n=0
  for _ in $(seq 1 5); do
    v=$(nvidia-smi --query-gpu=power.draw --format=csv,noheader,nounits | head -1)
    soma=$(awk "BEGIN {print $soma + $v}")
    n=$(( n + 1 ))
    sleep 1
  done
  awk "BEGIN {printf \"%.1f\", $soma / $n}"
}

printf "%-8s %-10s %-10s %-10s\n" "PL (W)" "Pwr (W)" "Imgs/s" "Imgs/J"
echo "---------------------------------------------------"

for PL in "${PL_LIST[@]}"; do
  sudo nvidia-smi -pl "$PL"
  sleep 2   # aguarda estabilização

  # Treino sintético (substitua por seu job real de treinamento)
  IMGS=$(python3 - "$DURACAO_TESTE" <<'PY'
import sys, time, random
dur = int(sys.argv[1]); t0 = time.time(); n = 0
while time.time() - t0 < dur:
    n += 48 + random.randint(0, 8)   # batches por segundo (simulado)
    time.sleep(1)
print(n)
PY
)

  PWR=$(medir_potencia_media)
  IMGS_S=$(awk "BEGIN {printf \"%.1f\", $IMGS / $DURACAO_TESTE}")
  EFIC=$(awk "BEGIN {printf \"%.3f\", $IMGS_S / $PWR}")

  printf "%-8s %-10s %-10s %-10s\n" "$PL" "$PWR" "$IMGS_S" "$EFIC"
done

echo ""
echo "Dica: o ponto ótimo de eficiência costuma ficar em ~75% do TDP."
