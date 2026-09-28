# 🏁 Aula 20 — Definição do Projeto Final

**Objetivo:** planejar um projeto de IA com uso estratégico de GPU — escolher o
**domínio** e o **problema real**, definir o **dataset**, a **arquitetura** e o
**framework**, configurar o **repositório** com boas práticas e integrar o
**monitoramento GPU** dos blocos anteriores, fechando o **checklist de prontidão**
para o hackathon.

> 🧭 **Bloco 4 — Projeto Final.** As aulas 20 a 24 guiam a **implementação** de uma
> solução de IA acelerada por GPU. Elas **complementam** o [`projeto-integrador/`](../../projeto-integrador/README.md)
> (que é uma **pesquisa** e não exige programação).

---

## 🎯 Situação de aprendizagem

A empresa organizou um **hackathon interno de 4 semanas**: cada time deve desenvolver
uma solução de IA acelerada por GPU para um problema real. Há acesso a um servidor com
**2× RTX 4090** e ao **Google Colab Pro**. O desafio é estruturar o projeto do zero:
escolher o domínio (visão, PNL ou séries temporais), identificar o problema, selecionar o
dataset e planejar a arquitetura.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula20.html`](apresentacao_aula20.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** com explicação + **5 exercícios** |
| [`scripts/`](scripts) | Scripts de referência (`arquitetura_projeto.py`, `checklist_projeto.py`) — rodam sem GPU |
| [`atividade.md`](atividade.md) | Roteiro prático, discussão e tarefa de casa |

### Estrutura da aula

```
aula20/
  apresentacao_aula20.html
  README.md
  notebook_colab/aula20_definicao_projeto.ipynb
  scripts/arquitetura_projeto.py
  scripts/checklist_projeto.py
  atividade.md
```

---

## 🚀 Como usar

### No Google Colab
Abra `notebook_colab/aula20_definicao_projeto.ipynb` pelo **GitHub** no Colab e siga as
células. Sem GPU, o notebook roda em **modo simulado** — o foco é **planejar**, não treinar.

### Localmente (modo de referência)
```bash
cd aulas/bloco4/aula20/scripts
python arquitetura_projeto.py     # mostra config e pipeline (PyTorch opcional)
python checklist_projeto.py       # exibe o checklist de prontidão
```

---

## 🔑 Conceitos-chave

- **Transfer Learning** — reutilizar pesos pré-treinados (ImageNet/HF Hub): converge ~10× mais rápido.
- **Mixed Precision** — `fp16`/`bf16` reduz VRAM à metade e aumenta throughput.
- **W&B / MLflow** — rastreamento de experimentos (métricas, configs e GPU).
- **Baseline vs Target** — solução simples primeiro; o alvo é superá-la.
- **Checkpointing** — salvar o melhor modelo durante o treino.
- **DataLoader GPU** — `num_workers` + `pin_memory` eliminam o gargalo CPU→GPU.

---

## 🔗 Integração com os blocos anteriores

O projeto final **reaproveita** os scripts de automação já construídos:

| Bloco 3 | O que reutilizar |
| :--- | :--- |
| Aula 14 (Automação) | Monitor de GPU com log CSV durante o treino |
| Aula 15 (Processos) | Fila de experimentos por prioridade |
| Aula 19 (Energia) | Calibração de Power Limit para treinos longos |

---

## 📌 Tarefa de casa (para a Aula 21)

1. Completar o `checklist_projeto.py` com **100%** dos itens.
2. Criar o repositório GitHub com a estrutura definida e compartilhar o link.
3. Testar o carregamento do dataset no Colab e medir o tempo.
4. Implementar o **baseline mais simples** e medir a métrica principal.
