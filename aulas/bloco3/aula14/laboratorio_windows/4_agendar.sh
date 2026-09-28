#!/usr/bin/env bash
# ============================================================================
# 4_agendar.sh — mostra como agendar o monitoramento (simulação do cron)
# ----------------------------------------------------------------------------
# Uso:  ./4_agendar.sh
#
# No Windows/Git Bash NÃO existe o comando "cron". Este script:
#   1. Executa o monitoramento algumas vezes em sequência para simular o cron.
#   2. Mostra as linhas de crontab prontas para copiar em um servidor Linux.
#   3. Mostra como criar a Tarefa Agendada equivalente no Windows.
# ============================================================================

cd "$(dirname "$0")" || exit 1
source ./lib_gpu.sh

set -euo pipefail

echo "==================================================================="
echo " SIMULAÇÃO DE AGENDAMENTO (o Windows/Git Bash não tem 'cron')"
echo "==================================================================="
echo ""

INTERVALO_CICLOS=1     # segundos entre execuções (na aula)
N_CICLOS=3             # número de execuções simuladas

for ciclo in $(seq 1 "$N_CICLOS"); do
    agora=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$agora] execução #$ciclo: ./2_alertar.sh 80 95"
    ./2_alertar.sh 80 95 >/dev/null 2>&1 || true
    sleep "$INTERVALO_CICLOS"
done

echo ""
echo "-------------------------------------------------------------------"
echo " EM UM SERVIDOR LINUX REAL, use o crontab (crontab -e):"
echo "-------------------------------------------------------------------"
cat <<'EOF'
# Coletar métricas a cada 5 min no horário comercial (seg-sex)
*/5 8-20 * * 1-5 /home/user/1_monitorar.sh 5 /data/logs/gpu.csv 300

# Verificar alertas a cada minuto
* * * * * /home/user/2_alertar.sh 80 95

# Gerar dashboard diariamente às 23:59
59 23 * * * /home/user/3_dashboard.sh /data/logs/gpu.csv
EOF
echo ""
echo "-------------------------------------------------------------------"
echo " NO WINDOWS (PowerShell), use o Agendador de Tarefas:"
echo "-------------------------------------------------------------------"
cat <<'EOF'
# Criar uma tarefa diária às 08h que roda o monitoramento via Git Bash:
schtasks /Create /TN "MonitorGPU" /SC DAILY /ST 08:00 ^
  /TR "\"C:\Program Files\Git\bin\bash.exe\" -lc \"cd /c/caminho/laboratorio_windows && ./1_monitorar.sh 5 gpu_log.csv 300\""

# Rodar a tarefa agora (teste):
schtasks /Run /TN "MonitorGPU"
EOF
echo ""
echo "Simulação concluída."
