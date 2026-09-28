#!/usr/bin/env bash
# ============================================================================
# gpu_status.sh — Lista as GPUs e o status atual (com alerta de temperatura)
# ----------------------------------------------------------------------------
# OBJETIVO: o primeiro script que você roda num servidor de IA novo: descobre
# quais GPUs existem, checa os drivers e mostra temperatura, uso e memória.
#
# Suporta:
#   - NVIDIA  -> via nvidia-smi
#   - AMD     -> via rocm-smi (Linux) — se não houver, cai no lspci
#
# Uso:
#   bash gpu_status.sh                 # execução normal
#   bash gpu_status.sh >> log.txt      # grava num log
#   LIMITE_TEMP=75 bash gpu_status.sh  # muda o limite do alerta (padrão 80)
#
# Pronto para agendar com cron:
#   */5 * * * * /caminho/gpu_status.sh >> /var/log/gpu_monitor.log 2>&1
# ============================================================================

# Cores (se o terminal não suportar, elas simplesmente aparecem como texto)
VERMELHO='\033[0;31m'; VERDE='\033[0;32m'; AMARELO='\033[1;33m'
AZUL='\033[0;34m'; SEM_COR='\033[0m'

LIMITE_TEMP="${LIMITE_TEMP:-80}"   # temperatura máxima aceitável (°C)

echo -e "${AZUL}==============================================${SEM_COR}"
echo -e "${AZUL}  Status das GPUs - $(date '+%Y-%m-%d %H:%M:%S')${SEM_COR}"
echo -e "${AZUL}==============================================${SEM_COR}"

if command -v nvidia-smi >/dev/null 2>&1; then
    # ── NVIDIA ─────────────────────────────────────────────────────────────
    echo -e "\n${VERDE}> GPUs NVIDIA detectadas:${SEM_COR}"

    # Conta quantas GPUs existem (uma linha por GPU)
    N_GPUS=$(nvidia-smi --query-gpu=name --format=csv,noheader | wc -l)
    echo -e "  Total: ${AMARELO}${N_GPUS} GPU(s)${SEM_COR}\n"

    # Lê os campos separados por vírgula; IFS=',' quebra a linha em variáveis
    nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw \
        --format=csv,noheader | while IFS=',' read -r idx nome temp util mem_usada mem_total watts; do
        echo -e "  GPU ${idx}: ${AMARELO}${nome}${SEM_COR}"
        echo -e "    Temperatura : ${temp}"
        echo -e "    Utilizacao : ${util}"
        echo -e "    Memoria     : ${mem_usada} / ${mem_total}"
        echo -e "    Consumo     : ${watts}"

        # Alerta de temperatura: remove " C" e compara como número
        TEMP_NUM=$(echo "$temp" | tr -d ' C')
        if [ "$TEMP_NUM" -gt "$LIMITE_TEMP" ] 2>/dev/null; then
            echo -e "    ${VERMELHO}ALERTA: temperatura acima de ${LIMITE_TEMP}C!${SEM_COR}"
        fi
        echo ""
    done

elif command -v rocm-smi >/dev/null 2>&1; then
    # ── AMD (ROCm) ─────────────────────────────────────────────────────────
    echo -e "\n${VERDE}> GPUs AMD detectadas (ROCm):${SEM_COR}"
    rocm-smi --showtemp --showuse --showmeminfo vram

elif command -v lspci >/dev/null 2>&1; then
    # ── Sem utilitário da GPU: ao menos identifica o hardware no barramento ─
    echo -e "\n${AMARELO}> Sem nvidia-smi/rocm-smi. GPUs no barramento PCI:${SEM_COR}"
    lspci | grep -iE 'vga|3d|display|nvidia|amd|radeon' || \
        echo "  Nenhum dispositivo grafico encontrado no lspci."

else
    # ── Nada disponível (ex.: Git Bash no Windows sem driver de terminal) ───
    echo -e "${VERMELHO}X Nenhuma GPU gerenciavel detectada.${SEM_COR}"
    echo "  Verifique se os drivers estao instalados."
    echo "  No Windows, veja a GPU real com:  python scripts/monitoramento_linux.py"
fi

echo -e "\n${AZUL}==============================================${SEM_COR}"
