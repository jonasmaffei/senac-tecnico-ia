#!/usr/bin/env bash
# ============================================================================
# flock_gpu.sh — exclusão mútua simples (1 job por vez na GPU)
# ----------------------------------------------------------------------------
# Uso:  ./flock_gpu.sh "python train_job.py --nome X --epocas 3"
#
# Este é o exemplo mínimo da teoria: pega o lock da GPU, executa UM comando e
# libera. Outros que chamarem ao mesmo tempo esperam automaticamente na fila.
#
# O nome "flock" ficou por causa do comando Linux homônimo. No Git Bash do
# Windows ele não existe, então o lib_gpu15.sh usa um lock por diretório
# (mkdir atômico) com o MESMO efeito. Em Linux/WSL o flock real é usado.
# ============================================================================

cd "$(dirname "$0")" || exit 1
source ./lib_gpu15.sh

set -euo pipefail
preparar_dirs

COMANDO="${1:-python train_job.py --nome Job --epocas 3}"

echo "[$(date '+%H:%M:%S')] PID $$ aguardando o lock da GPU..."
lock_adquirir "gpu"
echo "[$(date '+%H:%M:%S')] PID $$ adquiriu a GPU — iniciando: $COMANDO"

if bash -c "$COMANDO"; then
    STATUS=0
else
    STATUS=$?
fi

lock_liberar "gpu"
echo "[$(date '+%H:%M:%S')] PID $$ liberou a GPU (exit=$STATUS)"
exit "$STATUS"
