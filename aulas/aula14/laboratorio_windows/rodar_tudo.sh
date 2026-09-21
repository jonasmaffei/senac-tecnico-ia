#!/usr/bin/env bash
# ============================================================================
# rodar_tudo.sh — executa o fluxo completo do laboratório em sequência
# ----------------------------------------------------------------------------
# Uso:  ./rodar_tudo.sh
#
# 1. Coleta 20 segundos de métricas (intervalo de 2 s) em gpu_log.csv
# 2. Verifica os alertas de temperatura/utilização
# 3. Gera o dashboard.html
# 4. Mostra um resumo final
# ============================================================================

cd "$(dirname "$0")" || exit 1

set -euo pipefail

echo "==================================================================="
echo " FLUXO COMPLETO — Monitoramento de GPU (Aula 14)"
echo "==================================================================="
echo ""
echo ">>> PASSO 1/3: coletando 20 segundos de métricas..."
./1_monitorar.sh 2 gpu_log.csv 20
echo ""
echo ">>> PASSO 2/3: verificando alertas..."
./2_alertar.sh 80 95
echo ""
echo ">>> PASSO 3/3: gerando dashboard..."
./3_dashboard.sh gpu_log.csv
echo ""
echo "==================================================================="
echo " CONCLUÍDO"
echo "-------------------------------------------------------------------"
echo " Arquivos gerados nesta pasta:"
echo "   - gpu_log.csv      (métricas coletadas)"
echo "   - alertas.log      (registro de alertas, se houver)"
echo "   - dashboard.html   (abra no navegador com duplo clique)"
echo "==================================================================="
