#!/usr/bin/env bash
# gpu_queue.sh - Fila de jobs com prioridade e logging
# Uso: ./gpu_queue.sh <prioridade> <nome_job> <script.py> [args...]
# Prioridades: 1=alta, 2=media, 3=baixa

set -euo pipefail

PRIORIDADE="${1:-2}"
NOME_JOB="${2:-job_$$}"
SCRIPT="${3:-train_job.py}"
shift 3 2>/dev/null || true

QUEUE_DIR="gpu_queue_spool"
LOCK_FILE="gpu_queue.lock"
LOG_FILE="gpu_queue.log"

mkdir -p "$QUEUE_DIR"

# -- Registrar job na fila ---------------------------------
TICKET="${PRIORIDADE}_$(date +%Y%m%d_%H%M%S_%N)_${NOME_JOB}"
echo "$SCRIPT $*" > "$QUEUE_DIR/$TICKET"
echo "[$(date '+%H:%M:%S')] Job '$NOME_JOB' (prio=${PRIORIDADE}) enfileirado: $TICKET" | tee -a "$LOG_FILE"

# -- Aguardar vez na fila ----------------------------------
while true; do
    PROXIMO=$(ls "$QUEUE_DIR" 2>/dev/null | sort | head -1 || true)
    
    if [ "$PROXIMO" = "$TICKET" ]; then
        break   # Nossa vez na fila!
    fi
    
    echo "[$(date '+%H:%M:%S')] '$NOME_JOB' aguardando vez: $PROXIMO esta na frente..."
    sleep 3
done

# -- Executar com lock exclusivo ---------------------------
(
  flock -x 200
  echo "[$(date '+%H:%M:%S')] Executando '$NOME_JOB'" | tee -a "$LOG_FILE"
  
  START=$(date +%s)
  python3 "$SCRIPT" "$@"
  EXIT_CODE=$?
  END=$(date +%s)
  
  DURACAO=$(( END - START ))
  echo "[$(date '+%H:%M:%S')] '$NOME_JOB' concluido em ${DURACAO}s (exit=${EXIT_CODE})" | tee -a "$LOG_FILE"
  
  rm -f "$QUEUE_DIR/$TICKET"
  exit $EXIT_CODE
) 200>"$LOCK_FILE"
