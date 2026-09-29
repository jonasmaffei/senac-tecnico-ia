#!/usr/bin/env bash
# ============================================================================
# cron_exemplos.sh - Referencia de agendamento com cron (NAO executar direto)
# ----------------------------------------------------------------------------
# OBJETIVO: reunir os exemplos de crontab usados num servidor de IA, comentados.
# Este arquivo e uma REFERENCIA: copie as linhas que precisar para `crontab -e`.
#
# Formato de uma linha do cron:
#   +-------- minuto (0-59)
#   | +------ hora (0-23)
#   | | +---- dia do mes (1-31)
#   | | | +-- mes (1-12)
#   | | | | + dia da semana (0-7, 0 e 7 = domingo)
#   | | | | |
#   * * * * * comando_a_executar
# ============================================================================

# -- Comandos de gestao do crontab -------------------------------------------
# crontab -e    # edita o crontab do usuario atual
# crontab -l    # lista o crontab atual
# crontab -r    # remove o crontab (cuidado!)

# -- Exemplos uteis num servidor de GPU --------------------------------------

# Monitorar a GPU a cada 5 minutos e anexar ao log
# */5 * * * * /home/usuario/scripts/gpu_status.sh >> /var/log/gpu_monitor.log 2>&1

# Limpar logs antigos todo domingo a meia-noite (mais de 7 dias)
# 0 0 * * 0 find /var/log -name "gpu_*.log" -mtime +7 -delete

# Enviar relatorio diario as 08:00 por e-mail
# 0 8 * * * /home/usuario/scripts/gpu_status.sh | mail -s "GPU Status" admin@empresa.com

# Apagar checkpoints de modelo mais antigos que 30 dias, todo dia as 03:00
# 0 3 * * * find /dados/checkpoints -name "*.pt" -mtime +30 -delete

# Reiniciar o servico de inferencia toda segunda-feira as 06:00
# 0 6 * * 1 systemctl restart inferencia

echo "Este arquivo e uma REFERENCIA. Copie as linhas desejadas para 'crontab -e'."
