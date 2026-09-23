# Atividade: Aula 14 — Introdução à Automação de GPUs com Bash

## Parte 1 — Atividade guiada: automatizar o monitoramento

No **Colab**, no notebook `aula14_automacao_gpu_bash.ipynb`, ou no **laboratório Windows**
(`laboratorio_windows/`), execute e observe:

```bash
# No laboratório Windows (Git Bash)
cd aulas/aula14/laboratorio_windows
./1_monitorar.sh          # coleta métricas em CSV
./2_alertar.sh            # verifica limites e alerta
./3_dashboard.sh          # gera o dashboard HTML
```

Registre: quantas amostras foram coletadas, qual a maior temperatura e se houve algum alerta.

---

## Parte 2 — Discussão em grupo (3 a 4 pessoas)

No cenário de uma empresa que mantém GPUs ligadas 24h/7d:

1. Por que **monitorar não é opcional** numa operação de IA? O que acontece se uma GPU
   superaquece ou fica ociosa sem ninguém perceber?
2. **cron ou systemd:** qual usar para *(a)* um relatório diário, *(b)* um monitor contínuo?
3. Qual o **custo de negócio** de uma GPU ociosa 40% do tempo? Como o monitoramento reduz isso?
4. O que era diferente entre monitorar **no Colab** (efêmero) e num **servidor real**?

---

## Parte 3 — Pesquisa (tarefa de casa)

1. Adapte o `monitor_gpu.sh` para coletar **10 minutos** com intervalo de **3 s**.
2. Gere o dashboard com os **4 gráficos** (temperatura, utilização, VRAM, potência).
3. Configure um **cron job** que execute o monitoramento **todo dia às 08h**.
4. **Bônus:** implemente o alerta com envio para **webhook** (Slack/Discord) ou e-mail.

> **Dica:** prefira métricas **estruturadas** (`--query-gpu ... --format=csv,noheader`) — elas
> são parseáveis por scripts e independentes de idioma.
