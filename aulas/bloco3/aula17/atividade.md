# 📝 Atividade Prática: Aula 17 — Introdução à Automação de GPUs com Bash

---

## 🎯 Situação de Aprendizagem

O servidor de treinamento da empresa ficou travado durante a madrugada — a GPU atingiu **95°C** e o job falhou silenciosamente. Ninguém percebeu até a manhã seguinte. O time precisa de um sistema de monitoramento automático **24h/7d** que colete métricas a cada 5 segundos, salve em CSV, gere alertas de temperatura e publique um dashboard diário no Google Sheets — tudo via scripts Bash agendados com `cron`.

---

## 🗂️ Roteiro de Execução

Você pode realizar esta atividade no **Google Colab** ou localmente no **Windows Host**.

| Ambiente | Onde abrir | Como executar |
| :--- | :--- | :--- |
| **Google Colab** | [`notebook_colab/aula17_automacao_gpu_bash.ipynb`](notebook_colab/aula17_automacao_gpu_bash.ipynb) | Execute as células em sequência no Colab |
| **Windows Host** | [`laboratorio_windows/iniciar.bat`](laboratorio_windows/iniciar.bat) | Dê duplo clique no `iniciar.bat` no seu computador |

---

## 🚀 Parte 1 — Coleta e Alertas de Métricas

1. Execute o script de coleta por 30 segundos:
   - No Colab: `!./monitor_gpu.sh 5 gpu_log.csv 30`
   - No Windows: opção 1 do menu `iniciar.bat`
2. Abra o arquivo CSV gerado (`gpu_log.csv`) e verifique se as colunas `timestamp`, `temp_c`, `util_gpu_pct`, `mem_used_mb` e `power_w` foram preenchidas corretamente.
3. Teste o script de alertas ajustando o limiar de temperatura para $70^\circ\text{C}$:
   - Observe os registros adicionados em `gpu_alertas.log`.

---

## 📊 Parte 2 — Geração de Dashboards

1. Gere o dashboard visual contendo os 4 painéis de gráficos (Temperatura, Utilização %, VRAM Usada, Potência em Watts):
   - No Colab: via `gnuplot` / `matplotlib` (imagem renderizada na tela).
   - No Windows Host: opção 3 do menu (`reports/gpu_dashboard.png`).

---

## 🌐 Parte 3 — Integração Remota (Google Sheets API)

1. Teste a execução do script `enviar_para_sheets.py`.
2. Em modo simulação, o script validará o número de registros prontos para envio.
3. Se possuir uma Service Account do Google Cloud e uma planilha, defina `SHEETS_ID` no ambiente para efetuar a publicação real.

---

## 💬 Parte 4 — Discussão em Grupo (10 min)

Em grupos de 3 a 4 alunos, discutam:

1. O script coleta a cada 5s no mesmo servidor. Se o disco encher, o monitoramento para. Como tornar o sistema mais robusto e independente do job de treinamento?
2. `cron` e `systemd` são soluções de servidor único. Para um cluster com 50 nós GPU, qual seria a arquitetura ideal? (Pesquise sobre Prometheus, Grafana e NVIDIA DCGM).
3. O alerta está configurado em 80°C mas a GPU aguenta 95°C. Qual o limiar ideal? Quais outros indicadores (`fan.speed`, *power throttle*) deveriam acionar alertas?
4. O Google Sheets tem limitações de quota e latência. Para produção real, quais ferramentas substituiriam essa integração? Compare com InfluxDB + Grafana.

---

## 📌 Parte 5 — Tarefa de Casa

Configure o sistema de monitoramento completo em um servidor ou ambiente de testes (Colab/Host):
1. Adapte `monitor_gpu.sh` para coletar por 10 minutos com intervalo de 3s.
2. Crie o dashboard com os 4 gráficos da aula.
3. Configure uma regra de agendamento (`cron`) que execute o monitoramento todo dia às 08h.
4. **Bônus:** Implemente o alerta de temperatura enviando uma notificação simulada para um Webhook de Slack ou Discord.
