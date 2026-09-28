# 📝 Atividade Prática: Aula 21 — Implementação do Modelo no Projeto

---

## 🎯 Situação de Aprendizagem

O hackathon entrou na fase crítica de desenvolvimento. Os times têm o plano definido, o
repositório estruturado e o baseline medido. Agora precisam implementar o modelo profundo
com **aceleração GPU real**: escolher a precisão certa, otimizar o pipeline de dados,
garantir que o modelo cabe na VRAM e monitorar cada experimento. O objetivo é entregar um
modelo treinando corretamente com pelo menos uma rodada completa registrada.

---

## 🗂️ Roteiro de Execução

| Ambiente | Onde abrir | Como executar |
| :--- | :--- | :--- |
| **Google Colab** | [`notebook_colab/aula21_implementacao_modelo.ipynb`](notebook_colab/aula21_implementacao_modelo.ipynb) | Execute as células em sequência |
| **Local (referência)** | [`scripts/`](scripts) | `python pipeline_treinamento.py` e `python otimizacao_memoria.py` |

---

## 🚀 Parte 1 — Pipeline otimizado

1. Revise o fluxo de uma época com e sem AMP (`treinar_epoca_referencia`).
2. Configure o `DataLoader` com `num_workers`, `pin_memory` e `persistent_workers`.
3. No Colab, meça o tempo de uma época **com** e **sem** `autocast`.

---

## ⚡ Parte 2 — Mixed Precision

1. Habilite `autocast` + `GradScaler` no seu `train.py`.
2. Compare o throughput (imgs/s) e a VRAM de pico entre fp32 e fp16.
3. Registre o speedup obtido na sua GPU específica.

---

## 🧠 Parte 3 — Gestão de memória

1. Estime o batch máximo que cabe na sua GPU com AMP (`otimizacao_memoria.py`).
2. Se o batch ideal não couber, calcule os **steps de acumulação** necessários.
3. Para modelos grandes, ative o **gradient checkpointing** e compare a VRAM.

---

## 🔍 Parte 4 — Profiling

1. Rode o `torch.profiler` por ~10 iterações e exporte o trace.
2. Identifique a operação mais cara (forward/backward/otimizador).
3. Decida qual otimização ataca esse gargalo.

---

## 💬 Parte 5 — Discussão em Grupo (10 min)

Revisão cruzada de código entre as equipes:

1. Qual foi a operação mais lenta no profiler? O gargalo está onde você esperava?
2. Vocês ativaram mixed precision? Qual o speedup? Se < 1.5×, o que explica?
3. O modelo cabe na VRAM com o batch planejado?
4. Comparado ao baseline, quantas épocas faltaram para superá-lo? A GPU fica > 80% ocupada?

---

## 📌 Parte 6 — Tarefa de Casa (para a Aula 22)

1. Executar pelo menos **10 épocas completas** com AMP e logging no W&B.
2. Rodar o `monitor_gpu.sh` (Aula 14) durante o treinamento e salvar o CSV.
3. Comparar o throughput com e sem AMP e registrar no README do projeto.
4. **Bônus:** experimentar `torch.compile(model)` e medir o impacto no throughput.
