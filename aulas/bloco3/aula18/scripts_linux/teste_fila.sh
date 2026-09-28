#!/usr/bin/env bash
# teste_fila.sh — Lançar 4 jobs simultâneos para testar a fila por prioridade

set -euo pipefail

echo "Lançando 4 jobs em paralelo — apenas 1 executará por vez na GPU"
echo "Observe a serialização automática via flock e ordenação por prioridade (1=alta, 3=baixa)"
echo ""

chmod +x gpu_queue.sh flock_gpu.sh

./gpu_queue.sh 1 "Job-Alta-A"  train_job.py --nome "Job-Alta-A"  --epocas 3 &
./gpu_queue.sh 3 "Job-Baixa-B" train_job.py --nome "Job-Baixa-B" --epocas 2 &
./gpu_queue.sh 2 "Job-Media-C" train_job.py --nome "Job-Media-C" --epocas 4 &
./gpu_queue.sh 1 "Job-Alta-D"  train_job.py --nome "Job-Alta-D"  --epocas 2 &

sleep 1
echo "Jobs na fila spool: $(ls gpu_queue_spool 2>/dev/null | wc -l)"
echo ""

while [ "$(ls gpu_queue_spool 2>/dev/null | wc -l)" -gt 0 ]; do
    echo "[$(date '+%H:%M:%S')] Estado da Fila: $(ls gpu_queue_spool 2>/dev/null | sort | tr '\n' ' ')"
    sleep 3
done

wait
echo ""
echo "Todos os jobs concluídos!"
