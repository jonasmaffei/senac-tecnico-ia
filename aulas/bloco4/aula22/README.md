# 📡 Aula 22 — Automação e Monitoramento

**Objetivo:** monitorar a GPU automaticamente durante treinos longos — coleta contínua em CSV
e alerta quando a temperatura passar do limite.

> 🧭 **Bloco 4 — Projeto Final.** Continua a [Aula 21](../aula21/README.md).

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula22.html`](apresentacao_aula22.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`scripts/monitor_treinamento.sh`](scripts/monitor_treinamento.sh) | Monitor de GPU em CSV com alerta de temperatura |
| [`atividade.md`](atividade.md) | Roteiro e tarefa de casa |

---

## 🚀 Como usar (servidor Linux com NVIDIA)

```bash
cd aulas/bloco4/aula22/scripts
chmod +x monitor_treinamento.sh
./monitor_treinamento.sh $PID_DO_TREINO 10
```

O monitor grava `logs/monitor/gpu_<data>.csv` e **encerra sozinho** quando o treino termina.

---

## 🔑 Conceitos-chave

- **Monitor integrado** — roda junto do treino (via `subprocess` ou outro terminal).
- **CSV estruturado** — timestamp, temperatura, potência, utilização e VRAM.
- **Alerta por limiar** — avisa quando a temperatura passa de 82 °C.
- **Auto-encerramento** — verifica o PID do treino e para sozinho.

---

## 🔀 Outra trilha: pesquisa (sem código)

Na trilha de pesquisa, o monitoramento vira **requisito da solução**: estimar custo e energia,
definir as métricas de operação (temperatura, potência, utilização) e citar as ferramentas
(`nvidia-smi`, NVML) como parte da arquitetura.


## 📌 Tarefa de casa (para a Aula 23)

1. Rodar o monitor junto de um treino e salvar o CSV.
2. Ajustar o limite de temperatura e testar o alerta.
3. Preparar o **pitch de 5 min** do projeto.
