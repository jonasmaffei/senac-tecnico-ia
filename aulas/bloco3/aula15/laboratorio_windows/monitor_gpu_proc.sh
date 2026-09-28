#!/usr/bin/env bash
# ============================================================================
# monitor_gpu_proc.sh — monitora processos, GPU e fila em tempo real
# ----------------------------------------------------------------------------
# Uso:  ./monitor_gpu_proc.sh [vezes] [intervalo_s]
# Ex.:  ./monitor_gpu_proc.sh          (infinito, 3 s)
#       ./monitor_gpu_proc.sh 5 2      (5 atualizações a cada 2 s)
#
# Mostra, a cada ciclo:
#   - quem está usando a GPU (PID, usuário, processo, VRAM/utilização);
#   - o resumo da placa (utilização e VRAM);
#   - o estado atual da fila (quem está executando e quem espera);
#   - o dono do lock da GPU.
# ============================================================================

cd "$(dirname "$0")" || exit 1
source ./lib_gpu15.sh

set -euo pipefail
preparar_dirs

VEZES="${1:-0}"       # 0 = fica em loop até Ctrl+C
INTERVALO="${2:-3}"

uma_volta() {
    echo "=============================================================="
    echo " Monitor de GPU — $(date '+%Y-%m-%d %H:%M:%S') (Brasília)"
    echo " Backend: $(nome_backend)"
    echo "=============================================================="

    echo "── Processos usando a GPU ──"
    local achou=0
    while IFS='|' read -r pid user nome vram util; do
        [ -z "$pid" ] && continue
        achou=1
        printf '  PID=%-8s USER=%-10s CMD=%-22s VRAM=%s MB  UTIL=%s%%\n' \
               "$pid" "$user" "$nome" "$vram" "$util"
    done < <(listar_processos_gpu)
    [ "$achou" -eq 0 ] && echo "  (nenhum processo dedicado na GPU agora)"

    echo ""
    echo "── Resumo da GPU ──"
    while IFS='|' read -r idx util mem tot; do
        [ -z "$idx" ] && continue
        if [ "$tot" != "N/A" ] && [ "$tot" -gt 0 ] 2>/dev/null; then
            local pct=$(( mem * 100 / tot ))
            echo "  GPU$idx: util=${util}% | VRAM=${mem}/${tot} MB (${pct}%)"
        else
            echo "  GPU$idx: util=${util}% | VRAM=${mem} MB"
        fi
    done < <(resumo_gpu)

    echo ""
    echo "── Fila de jobs (ordem de execução) ──"
    if [ -n "$(ls -A "$DIR_FILA" 2>/dev/null)" ]; then
        ls "$DIR_FILA" | sort | nl -w3 -s'. '
    else
        echo "  (fila vazia)"
    fi

    echo ""
    echo "── Lock da GPU ──"
    if [ -d "$DIR_LOCKS/gpu.lock" ]; then
        echo "  Ocupado por PID $(cat "$DIR_LOCKS/gpu.lock/pid" 2>/dev/null) desde $(cat "$DIR_LOCKS/gpu.lock/inicio" 2>/dev/null)"
    elif [ -f "$DIR_LOCKS/gpu.pid" ]; then
        echo "  Ocupado por PID $(cat "$DIR_LOCKS/gpu.pid" 2>/dev/null) (via flock)"
    else
        echo "  Livre"
    fi
    echo ""
}

if [ "$VEZES" -gt 0 ]; then
    for (( i = 1; i <= VEZES; i++ )); do
        uma_volta
        [ "$i" -lt "$VEZES" ] && sleep "$INTERVALO"
    done
else
    echo "Monitor contínuo (Ctrl+C para sair). Intervalo: ${INTERVALO}s"
    while true; do
        uma_volta
        sleep "$INTERVALO"
    done
fi
