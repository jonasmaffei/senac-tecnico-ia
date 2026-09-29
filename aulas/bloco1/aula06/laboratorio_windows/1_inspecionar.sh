#!/usr/bin/env bash
# ============================================================================
# 1_inspecionar.sh - Conhecer o hardware do servidor (passo a passo)
# ----------------------------------------------------------------------------
# OBJETIVO: reproduzir, na maquina do laboratorio, o que fariamos num servidor
# Linux novo: descobrir o hardware, ler os "pseudo-arquivos" e ver a GPU.
#
# Como rodar (Git Bash, na pasta laboratorio_windows):
#     bash 1_inspecionar.sh
# ============================================================================

# source carrega as funcoes e as cores de lib_gpu06.sh (./ = pasta atual).
source ./lib_gpu06.sh

echo "${AZUL}============================================================${SEM_COR}"
echo "${AZUL}  1) Inspecao do hardware - Aula 06${SEM_COR}"
echo "${AZUL}============================================================${SEM_COR}"
echo

# -- Sistema operacional -----------------------------------------------------
echo "${VERDE}Sistema:${SEM_COR} $(uname -s)"
echo "${VERDE}Maquina:${SEM_COR} $(uname -m)"
echo

# -- Pseudo-arquivos do Linux (so existem no Linux/Colab/WSL) ----------------
if [ -r /proc/cpuinfo ]; then
    echo "${VERDE}[/proc/cpuinfo]${SEM_COR} processador:"
    grep -m1 "model name" /proc/cpuinfo | sed 's/^/  /'
    echo "${VERDE}[/proc/meminfo]${SEM_COR} memoria:"
    grep -E "^(MemTotal|MemAvailable)" /proc/meminfo | sed 's/^/  /'
else
    echo "${AMARELO}/proc e /sys nao existem aqui (Windows).${SEM_COR}"
    echo "  No Linux, eles mostram CPU, RAM e o estado do hardware como arquivos."
fi
echo

# -- Placa no barramento PCI -------------------------------------------------
echo "${VERDE}[lspci]${SEM_COR} dispositivos graficos:"
listar_pci_gpu | sed 's/^/  /'
echo

# -- Backend e GPU -----------------------------------------------------------
anunciar_backend
echo "${VERDE}Leitura da GPU (formato: idx|nome|temp|util%|vram_usada|vram_total):${SEM_COR}"
ler_gpu | sed 's/^/  /'
echo

echo "${AZUL}------------------------------------------------------------${SEM_COR}"
echo "Proximo passo: ${AMARELO}bash 2_status_gpu.sh${SEM_COR} (status + alerta de temperatura)."
