#!/usr/bin/env bash
# ============================================================================
# fila_gpu.sh — fila de jobs com prioridade + exclusão mútua da GPU
# ----------------------------------------------------------------------------
# Uso:  ./fila_gpu.sh <prioridade> <nome_job> <comando...>
# Ex.:  ./fila_gpu.sh 1 Job-Alta "python train_job.py --nome Job-Alta --epocas 3"
#
# Prioridades: 1 = alta, 2 = média, 3 = baixa.
# Jobs de mesma prioridade executam por ordem de chegada (FIFO).
#
# COMO FUNCIONA
#   1. Cada job cria um "ticket" na pasta da fila com o nome:
#          <prioridade>_<timestamp>_<nome>
#      Como a ordenação é alfabética, o menor número (maior prioridade) vem
#      primeiro; empates são desempatados pelo timestamp (FIFO).
#   2. O job espera até o seu ticket ser o primeiro da lista.
#   3. Quando chega a vez, ele adquire o lock da GPU (1 job por vez) e executa.
#   4. Ao terminar, remove o ticket e libera o lock.
# ============================================================================

cd "$(dirname "$0")" || exit 1
source ./lib_gpu15.sh

set -euo pipefail
preparar_dirs

PRIORIDADE="${1:-2}"
NOME_JOB="${2:-job_$$}"
shift 2 2>/dev/null || true
COMANDO="$*"

if [ -z "$COMANDO" ]; then
    echo "ERRO: informe o comando a executar." >&2
    echo "Uso: ./fila_gpu.sh <prioridade> <nome_job> <comando...>" >&2
    exit 1
fi

# Ticket = prioridade + timestamp + nome. %N (nanossegundos) garante unicidade
# quando vários jobs entram na fila no mesmo segundo.
TICKET="${PRIORIDADE}_$(date +%Y%m%d_%H%M%S_%N)_${NOME_JOB}"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILA"; }

# ── 1. Entra na fila ────────────────────────────────────────────────────────
echo "$COMANDO" > "$DIR_FILA/$TICKET"
log "Job '$NOME_JOB' (prio=$PRIORIDADE) enfileirado: $TICKET"

# Garante a limpeza do ticket e do lock mesmo se o job for interrompido (Ctrl+C)
finalizar() {
    rm -f "$DIR_FILA/$TICKET" 2>/dev/null || true
    lock_liberar "gpu"
}
trap finalizar EXIT INT TERM

# ── 2. Espera a vez (é o primeiro da fila?) ─────────────────────────────────
while true; do
    PROXIMO=$(ls "$DIR_FILA" 2>/dev/null | sort | head -1)
    [ "$PROXIMO" = "$TICKET" ] && break
    log "Aguardando na fila: '${PROXIMO:-?}' está à frente de '$NOME_JOB'"
    sleep 2
done

# ── 3. Adquire o lock da GPU e executa ──────────────────────────────────────
log "Vez de '$NOME_JOB' — aguardando o lock da GPU..."
lock_adquirir "gpu"
log "GPU adquirida por '$NOME_JOB' (PID $$) — executando."

INICIO=$(date +%s)
if bash -c "$COMANDO"; then
    STATUS=0
else
    STATUS=$?
fi
FIM=$(date +%s)
DURACAO=$(( FIM - INICIO ))

log "'$NOME_JOB' concluído em ${DURACAO}s (exit=$STATUS)"

# ── 4. Sai da fila e libera o lock ──────────────────────────────────────────
rm -f "$DIR_FILA/$TICKET"
lock_liberar "gpu"
trap - EXIT INT TERM
exit "$STATUS"
