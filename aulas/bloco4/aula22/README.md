# 📡 Aula 22 — Automação e Monitoramento do Projeto

**Objetivo:** integrar a **automação de monitoramento** ao ciclo de vida do modelo —
coleta contínua de métricas GPU em CSV, **alertas automáticos** por Slack/Telegram/e-mail,
**dashboard** em Python e registro como **serviço do sistema** — garantindo estabilidade e
rastreabilidade em treinamentos longos.

> 🧭 **Bloco 4 — Projeto Final.** Continua a [Aula 21](../aula21/README.md).

---

## 🎯 Situação de aprendizagem

O modelo está treinando e os resultados são promissores — mas o treino agora dura **horas
ou dias** no servidor com 2× RTX 4090. Ninguém ficará olhando o terminal 24h. O time precisa
de um sistema que colete métricas continuamente, dispare alertas se a temperatura ou a VRAM
passarem dos limites, gere dashboards e integre tudo ao repositório — sem intervenção manual.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula22.html`](apresentacao_aula22.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** com explicação + **5 exercícios** |
| [`scripts/`](scripts) | Scripts de referência (`monitor_treinamento.sh`, `alertas.sh`, `dashboard_metricas.py`) |
| [`atividade.md`](atividade.md) | Roteiro prático, discussão e tarefa de casa |

### Estrutura da aula

```
aula22/
  apresentacao_aula22.html
  README.md
  notebook_colab/aula22_automacao_projeto.ipynb
  scripts/monitor_treinamento.sh
  scripts/alertas.sh
  scripts/dashboard_metricas.py
  atividade.md
```

---

## 🚀 Como usar

### No Google Colab
Abra `notebook_colab/aula22_automacao_projeto.ipynb` pelo **GitHub** no Colab. Ele simula
métricas de GPU com o mesmo formato do CSV real — o pipeline de alertas e dashboard funciona
sem GPU.

### Em servidor Linux
```bash
cd aulas/bloco4/aula22/scripts
chmod +x *.sh

# 1. Iniciar o monitor junto do treino (passe o PID do train.py)
./monitor_treinamento.sh $PID_TREINO MeuProjeto

# 2. Alertas multi-canal (configurar SLACK_WEBHOOK_URL etc.)
./alertas.sh

# 3. Gerar o dashboard ao fim da sessão
python3 dashboard_metricas.py MeuProjeto
```

---

## 🔑 Conceitos-chave

- **nvidia-smi + CSV log** — coleta periódica com timestamp.
- **`subprocess.Popen`** — inicia o monitor junto do `train.py`, encerrando com o treino.
- **Slack Webhook** — canal mais rápido para alertas de time.
- **systemd service** — monitoramento contínuo, independente do treino.
- **pandas + matplotlib** — dashboard automático ao fim de cada sessão.
- **W&B API export** — combina métricas de treino com os logs de GPU.

---

## 📌 Tarefa de casa (para a Aula 23)

1. Integrar o `monitor_treinamento.sh` ao `train.py` e treinar com log CSV.
2. Gerar o **dashboard final** e salvar o PNG no repositório.
3. Configurar ao menos um **canal de alerta** e testá-lo acionando um threshold artificial.
4. Preparar o **pitch de 5 min**: problema → baseline → modelo GPU → resultados → lições.
