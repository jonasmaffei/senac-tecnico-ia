#!/usr/bin/env bash
# ============================================================================
# 3_agendar.sh - Automacao: coletar o status em varios instantes
# ----------------------------------------------------------------------------
# OBJETIVO: mostrar, na pratica, o que o `cron` faz num servidor Linux: rodar
# o monitoramento DE TEMPO EM TEMPO, de forma automatica, e gravar um historico.
#
# No Git Bash do Windows nao existe cron, entao simulamos um agendamento com um
# laco (a mesma ideia: repetir a coleta a cada N segundos).
#
# Uso:
#   bash 3_agendar.sh         # 3 coletas, uma a cada 2 segundos
#   bash 3_agendar.sh 5 1     # 5 coletas, a cada 1 segundo
# ============================================================================

source ./lib_gpu06.sh

COLETAS="${1:-3}"       # quantas vezes coletar
INTERVALO="${2:-2}"     # segundos entre as coletas

DIR_RELATORIOS="./reports"
mkdir -p "$DIR_RELATORIOS"
ARQUIVO="$DIR_RELATORIOS/historico_gpu.csv"

echo "${AZUL}============================================================${SEM_COR}"
echo "${AZUL}  3) Agendamento simulado - ${COLETAS} coletas a cada ${INTERVALO}s${SEM_COR}"
echo "${AZUL}============================================================${SEM_COR}"
echo
anunciar_backend

# Cabecalho do CSV: so na primeira vez (se o arquivo nao existir).
if [ ! -f "$ARQUIVO" ]; then
    echo "data_hora,gpu,nome,temperatura_c,utilizacao_pct,vram_usada_mb,vram_total_mb" > "$ARQUIVO"
fi

# Laco que simula o disparo periodico do cron.
for i in $(seq 1 "$COLETAS"); do
    AGORA=$(date '+%Y-%m-%d %H:%M:%S')
    echo "${VERDE}Coleta ${i}/${COLETAS} - ${AGORA}${SEM_COR}"
    while IFS='|' read -r idx nome temp util vram_usada vram_total; do
        echo "  GPU ${idx}: temp=${temp}C util=${util}% vram=${vram_usada}/${vram_total} MB"
        # Anexa uma linha ao CSV (virgulas separam os campos).
        echo "${AGORA},${idx},${nome},${temp},${util},${vram_usada},${vram_total}" >> "$ARQUIVO"
    done < <(ler_gpu)
    [ "$i" -lt "$COLETAS" ] && sleep "$INTERVALO"
done

echo
echo "${AZUL}------------------------------------------------------------${SEM_COR}"
echo "Historico gravado em: ${AMARELO}${ARQUIVO}${SEM_COR}"
echo
echo "Como seria no servidor Linux (cron):"
echo "  crontab -e"
echo "  */5 * * * * /caminho/2_status_gpu.sh >> /var/log/gpu_monitor.log 2>&1"
echo "  -> roda a cada 5 minutos, sem ninguem apertar nada."
