#!/usr/bin/env bash
# ============================================================================
# teste_fila.sh — prova a serialização: lança 4 jobs e mostra a ordem real
# ----------------------------------------------------------------------------
# Uso:  ./teste_fila.sh
#
# Os 4 jobs são lançados em paralelo (em segundo plano), mas o lock da GPU faz
# com que executem UM POR VEZ. A prioridade decide quem passa primeiro:
#   Job-Alta-A (1), Job-Baixa-B (3), Job-Media-C (2), Job-Alta-D (1)
# => ordem esperada: Alta-A, Alta-D, Media-C, Baixa-B
# ============================================================================

cd "$(dirname "$0")" || exit 1
source ./lib_gpu15.sh

set -euo pipefail
preparar_dirs
mkdir -p "$DIR_FILA"

# Limpa fila/lock de execuções anteriores
rm -f "$DIR_FILA"/* 2>/dev/null || true
rm -rf "$DIR_LOCKS"/gpu.* 2>/dev/null || true

echo "==================================================================="
echo " Teste da fila de GPU — 4 jobs, 1 GPU"
echo " Backend: $(nome_backend)"
echo "==================================================================="
echo ""
echo "Regra de prioridade: 1 = alta, 2 = média, 3 = baixa."
echo "Lançando: Alta-A(1), Baixa-B(3), Media-C(2), Alta-D(1)"
echo ""

PY="python"
command -v python >/dev/null 2>&1 || PY="python3"

# Lança os 4 jobs em paralelo (o & devolve o controle imediatamente)
./fila_gpu.sh 1 "Job-Alta-A"  "$PY train_job.py --nome Job-Alta-A  --epocas 2" &
./fila_gpu.sh 3 "Job-Baixa-B" "$PY train_job.py --nome Job-Baixa-B --epocas 1" &
./fila_gpu.sh 2 "Job-Media-C" "$PY train_job.py --nome Job-Media-C --epocas 2" &
./fila_gpu.sh 1 "Job-Alta-D"  "$PY train_job.py --nome Job-Alta-D  --epocas 1" &

# Pequena pausa para os jobs criarem seus tickets antes de mostrarmos a fila
sleep 1
echo "Jobs enfileirados: $(ls "$DIR_FILA" 2>/dev/null | wc -l)"
echo ""

# Enquanto houver tickets, mostra o estado da fila a cada 2 s
while [ "$(ls "$DIR_FILA" 2>/dev/null | wc -l)" -gt 0 ]; do
    echo "[$(date '+%H:%M:%S')] Fila: $(ls "$DIR_FILA" 2>/dev/null | sort | tr '\n' ' ')"
    sleep 2
done

echo ""
wait
echo "==================================================================="
echo " Todos os jobs concluídos!"
echo " Veja a ordem real de execução no log: $LOG_FILA"
echo "==================================================================="
