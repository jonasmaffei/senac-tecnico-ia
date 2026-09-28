# 📝 Atividade Prática: Aula 22 — Automação e Monitoramento do Projeto

---

## 🎯 Situação de Aprendizagem

O modelo está treinando e os primeiros resultados são promissores. Mas os treinamentos
agora duram **horas ou dias**. Ninguém ficará olhando o terminal 24h por dia. O time precisa
de um sistema de automação que: colete métricas da GPU continuamente, dispare alertas
automáticos se a temperatura ou a VRAM passarem dos limites, gere dashboards de desempenho
e integre tudo ao repositório do projeto — sem intervenção manual.

---

## 🗂️ Roteiro de Execução

| Ambiente | Onde abrir | Como executar |
| :--- | :--- | :--- |
| **Google Colab** | [`notebook_colab/aula22_automacao_projeto.ipynb`](notebook_colab/aula22_automacao_projeto.ipynb) | Execute as células em sequência |
| **Servidor Linux** | [`scripts/`](scripts) | `./monitor_treinamento.sh <pid> <projeto>` |

---

## 🚀 Parte 1 — Monitor integrado ao pipeline

1. Execute o `monitor_treinamento.sh` apontando para o PID do seu `train.py`.
2. Verifique o CSV gerado em `logs/monitor/<projeto>_<data>.csv`.
3. Confirme que o monitor **encerra sozinho** quando o treino termina.

---

## 📄 Parte 2 — Integração via subprocess

1. No `train.py`, inicie o monitor com `subprocess.Popen` antes do loop.
2. Garanta o encerramento no bloco `finally:`.
3. Force um erro no meio do treino e confirme que o monitor foi encerrado.

---

## 🚨 Parte 3 — Alertas automáticos

1. Configure ao menos um canal (log local já funciona; Slack/Telegram são opcionais).
2. Ajuste os thresholds (`MAX_TEMP`, `MAX_MEMORIA_PCT`) do script.
3. Acione um alerta artificialmente (baixe o threshold) e verifique o registro.

---

## 📊 Parte 4 — Dashboard

1. Colete um log de GPU representativo.
2. Gere o dashboard com `python3 dashboard_metricas.py <projeto>`.
3. Salve o PNG em `logs/dashboards/` e commite junto dos resultados.

---

## 💬 Parte 5 — Discussão em Grupo (10 min)

1. O monitor encerrou corretamente ao fim do treino? Se não, o que causou?
2. Qual threshold de temperatura vocês definiram? Já houve alerta real? O que aconteceu?
3. O dashboard mostrou alguma anomalia (pico de temperatura, queda de utilização, VRAM
   crescendo)? O que esse padrão indica?
4. Cruzando os logs de GPU com o W&B: a GPU estava maximamente usada justamente nas épocas
   em que o `val/loss` caiu mais? Há correlação entre utilização e velocidade de convergência?

---

## 📌 Parte 6 — Tarefa de Casa (para a Aula 23)

1. Integrar o monitor ao `train.py` e executar um treinamento completo com log CSV.
2. Gerar o **dashboard final** e salvar o PNG no repositório.
3. Configurar ao menos um **canal de alerta** e testá-lo acionando um threshold artificial.
4. Preparar o **pitch de 5 min**: problema → baseline → modelo GPU → resultados → lições.
