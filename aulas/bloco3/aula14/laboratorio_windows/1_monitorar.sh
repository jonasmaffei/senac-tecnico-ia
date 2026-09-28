#!/usr/bin/env bash
# ============================================================================
# 1_monitorar.sh — coleta métricas de GPU em CSV
# ----------------------------------------------------------------------------
# Uso:  ./1_monitorar.sh [intervalo_segundos] [arquivo_saida] [duracao_segundos]
# Ex.:  ./1_monitorar.sh 5 gpu_log.csv 3600
#
# Compatível com Git Bash (Windows), WSL e Linux. Sem GPU, usa modo simulado.
# ============================================================================

# Descobre a pasta onde este script está e entra nela (funciona em qualquer PC)
cd "$(dirname "$0")" || exit 1
source ./lib_gpu.sh

set -euo pipefail

INTERVALO="${1:-5}"                              # segundos entre coletas
SAIDA="${2:-$DIR_RELATORIOS/gpu_log.csv}"        # arquivo CSV de saída
DURACAO="${3:-3600}"                             # duração total em segundos

# Se o usuário passar apenas um nome (ex.: "gpu_log.csv"), guarda em reports/
case "$SAIDA" in
    */*|*\\*) ;;                                 # já tem pasta/caminho absoluto
    *) SAIDA="$DIR_RELATORIOS/$SAIDA" ;;
esac

# Cria a pasta de relatórios, caso ainda não exista
preparar_relatorios

# Quantas amostras cabem na duração informada (evita divisão por zero)
if [ "$INTERVALO" -gt 0 ] 2>/dev/null; then
    MAX_AMOSTRAS=$(( DURACAO / INTERVALO ))
else
    MAX_AMOSTRAS=720
fi

aviso_modo
# CSV incremental: só cria o cabeçalho se o arquivo ainda não existir.
# Assim, rodar o monitoramento de novo ACRESCENTA amostras ao histórico.
if [ -s "$SAIDA" ]; then
    ANTERIORES=$(( $(wc -l < "$SAIDA") - 1 ))
    echo "Arquivo existente: $SAIDA ($ANTERIORES amostras) — acrescentando."
else
    cabecalho_csv > "$SAIDA"
    echo "Novo arquivo: $SAIDA"
fi
echo "Iniciando monitoramento -> $SAIDA"
echo "Intervalo: ${INTERVALO}s | Duracao: ${DURACAO}s | Amostras: ${MAX_AMOSTRAS}"

AMOSTRA=0
while [ "$AMOSTRA" -lt "$MAX_AMOSTRAS" ]; do
    TS=$(date +"%Y-%m-%d %H:%M:%S")

    # No Windows, GPU + CPU + RAM vêm em UMA única chamada ao PowerShell
    COLETA_WINDOWS=""
    if [ "$BACKEND" = "amd_windows" ]; then
        COLETA_WINDOWS="$(consultar_windows_completo)"
        [ -z "$COLETA_WINDOWS" ] && COLETA_WINDOWS=""
    fi

    # Coleta CPU/RAM uma vez por amostra (o mesmo valor vai para cada GPU)
    SYS=$(obter_dados_sistema "$AMOSTRA")
    # Uma linha por GPU, já prefixada com timestamp e sufixada com CPU/RAM
    obter_dados_gpu "$AMOSTRA" | while IFS= read -r linha; do
        echo "$TS,$linha,$SYS" >> "$SAIDA"
    done

    AMOSTRA=$(( AMOSTRA + 1 ))
    printf '\r  Amostra %d/%d' "$AMOSTRA" "$MAX_AMOSTRAS"
    sleep "$INTERVALO"
done

echo ""
echo "Coleta concluida. Arquivo: $SAIDA"
