#!/usr/bin/env bash
# ============================================================================
# 2_status_gpu.sh — Status das GPUs + alerta de temperatura
# ----------------------------------------------------------------------------
# OBJETIVO: mostrar o status de cada GPU e emitir um ALERTA quando a
# temperatura passar do limite (padrão 80°C). É a lógica de produção aplicada
# ao hardware do laboratório.
#
# Uso:
#   bash 2_status_gpu.sh                 # limite padrão: 80°C
#   LIMITE_TEMP=60 bash 2_status_gpu.sh  # força o alerta (útil p/ testar)
# ============================================================================

source ./lib_gpu06.sh

LIMITE_TEMP="${LIMITE_TEMP:-80}"   # temperatura máxima aceitável (°C)

echo "${AZUL}============================================================${SEM_COR}"
echo "${AZUL}  2) Status das GPUs — $(date '+%Y-%m-%d %H:%M:%S')${SEM_COR}"
echo "${AZUL}============================================================${SEM_COR}"
echo
anunciar_backend

TEMPERATURA_ALTA=0
QUANTIDADE=0

# Lê uma GPU por linha e quebra os campos em variáveis (IFS='|').
while IFS='|' read -r idx nome temp util vram_usada vram_total; do
    QUANTIDADE=$((QUANTIDADE + 1))
    echo "  GPU ${idx}: ${AMARELO}${nome}${SEM_COR}"
    echo "    Temperatura : ${temp} °C"
    echo "    Utilização  : ${util} %"
    echo "    VRAM        : ${vram_usada} / ${vram_total} MB"

    # O alerta só faz sentido quando a temperatura é um número (não 'N/A').
    if [ "$temp" != "N/A" ]; then
        # Comparação numérica inteira (o valor pode vir com casas decimais).
        TEMP_INT=${temp%.*}
        if [ "$TEMP_INT" -gt "$LIMITE_TEMP" ] 2>/dev/null; then
            echo "    ${VERMELHO}ALERTA: temperatura acima de ${LIMITE_TEMP}°C!${SEM_COR}"
            TEMPERATURA_ALTA=1
        fi
    else
        echo "    ${AMARELO}(temperatura não exposta neste backend)${SEM_COR}"
    fi
    echo
done < <(ler_gpu)

echo "${AZUL}------------------------------------------------------------${SEM_COR}"
echo "GPUs encontradas: ${QUANTIDADE}"

# Código de saída: 0 = tudo normal, 1 = houve alerta.
# Isso permite encadear o script em automações (ex.: enviar e-mail se falhar).
if [ "$TEMPERATURA_ALTA" -eq 1 ]; then
    echo "${VERMELHO}Resultado: ALERTA ativo.${SEM_COR} Encerrando com código 1."
    exit 1
fi
echo "${VERDE}Resultado: todas as temperaturas dentro do limite.${SEM_COR}"
exit 0
