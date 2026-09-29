#!/usr/bin/env bash
# flock_gpu.sh - Exclusao mutua para acesso a GPU usando flock
# Uso: ./flock_gpu.sh <script_python.py> [args...]

set -euo pipefail

LOCK_FILE="gpu_exclusive.lock"
PYTHON_SCRIPT="${1:-train_job.py}"
shift || true

echo "[$(date '+%H:%M:%S')] PID $$ aguardando lock da GPU..."

(
  flock -x 200
  echo "[$(date '+%H:%M:%S')] PID $$ adquiriu GPU - iniciando $PYTHON_SCRIPT"
  
  python3 "$PYTHON_SCRIPT" "$@"
  EXIT_CODE=$?
  
  echo "[$(date '+%H:%M:%S')] PID $$ liberou GPU (exit=$EXIT_CODE)"
  exit $EXIT_CODE
) 200>"$LOCK_FILE"
