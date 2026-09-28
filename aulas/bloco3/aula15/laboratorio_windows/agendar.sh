#!/usr/bin/env bash
# ============================================================================
# agendar.sh — mostra como agendar a fila/monitor (equivalente ao cron/systemd)
# ----------------------------------------------------------------------------
# Uso:  ./agendar.sh
#
# No Git Bash do Windows NÃO existe o comando "cron" nem o systemd. Este script:
#   1. Simula algumas execuções em sequência (para a aula ver o efeito).
#   2. Mostra as linhas de crontab prontas para um servidor Linux.
#   3. Mostra um unit systemd de exemplo (produção) e o Agendador de Tarefas
#      do Windows como alternativa nativa.
# ============================================================================

cd "$(dirname "$0")" || exit 1
source ./lib_gpu15.sh

set -euo pipefail
preparar_dirs

echo "==================================================================="
echo " AGENDAMENTO — o Windows/Git Bash não tem 'cron' nem 'systemd'"
echo "==================================================================="
echo ""

# ── 1. Simulação local ──────────────────────────────────────────────────────
echo ">>> Simulando agendamento (3 ciclos de monitoramento):"
for ciclo in $(seq 1 3); do
    echo "[$(date '+%H:%M:%S')] execução #$ciclo: ./fila_gpu.sh 2 Job-Cron \"python train_job.py --nome Job-Cron --epocas 1\""
    ./fila_gpu.sh 2 "Job-Cron-$ciclo" "python train_job.py --nome Job-Cron-$ciclo --epocas 1"
    sleep 1
done
echo ""

# ── 2. crontab (Linux) ─────────────────────────────────────────────────────
echo "-------------------------------------------------------------------"
echo " EM UM SERVIDOR LINUX REAL (crontab -e):"
echo "-------------------------------------------------------------------"
cat <<'EOF'
# Monitorar a GPU a cada 5 min no horário comercial (seg-sex)
*/5 8-20 * * 1-5  /opt/gpu/monitor_gpu_proc.sh 1 1 >> /var/log/gpu_monitor.log 2>&1

# Rodar a fila diária de treinos às 02h (baixa prioridade)
0 2 * * *  /opt/gpu/fila_gpu.sh 3 Treino-Noturno "python3 /data/train_job.py --epocas 20" >> /var/log/gpu_fila.log 2>&1
EOF
echo ""

# ── 3. systemd (Linux, produção) ───────────────────────────────────────────
echo "-------------------------------------------------------------------"
echo " EM PRODUÇÃO, ISOLAMENTO COM SYSTEMD (/etc/systemd/system/gpu-job@.service):"
echo "-------------------------------------------------------------------"
cat <<'EOF'
[Unit]
Description=GPU Training Job %i
After=network.target

[Service]
Type=simple
User=ml-user
WorkingDirectory=/data/jobs/%i
ExecStart=/usr/bin/python3 train.py
CPUWeight=50
MemoryMax=16G
IOWeight=50
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=gpu-job-%i

[Install]
WantedBy=multi-user.target
EOF
echo ""
echo "  sudo systemctl start gpu-job@experimento-01"
echo "  journalctl -u gpu-job@experimento-01 -f"
echo ""

# ── 4. Agendador de Tarefas (Windows) ──────────────────────────────────────
echo "-------------------------------------------------------------------"
echo " NO WINDOWS (PowerShell — Agendador de Tarefas):"
echo "-------------------------------------------------------------------"
cat <<'EOF'
schtasks /Create /TN "MonitorGPU15" /SC DAILY /ST 08:00 ^
  /TR "\"C:\Program Files\Git\bin\bash.exe\" -lc \"cd /c/caminho/laboratorio_windows && ./monitor_gpu_proc.sh 1 1\""
EOF
echo ""
echo "Simulação concluída."
