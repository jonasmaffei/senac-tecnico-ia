# 📝 Atividade Prática: Aula 23 — Apresentação e Análise dos Projetos

---

## 🎯 Situação de Aprendizagem

O treinamento finalizou, os logs de GPU estão salvos e o W&B registrou todas as runs. Agora
é hora de transformar **dados técnicos em narrativa**. Uma banca de engenheiros avaliará cada
projeto: o que foi resolvido, como a GPU foi usada estrategicamente, quais foram os ganhos
reais e o que o time aprendeu. Você tem **5 minutos**.

---

## 🗂️ Roteiro de Execução

| Ambiente | Onde abrir | Como executar |
| :--- | :--- | :--- |
| **Google Colab** | [`notebook_colab/aula23_apresentacao_projetos.ipynb`](notebook_colab/aula23_apresentacao_projetos.ipynb) | Execute as células em sequência |
| **Local (referência)** | [`scripts/`](scripts) | `python relatorio_final.py` e `python checklist_apresentacao.py` |

---

## 🎤 Parte 1 — Estrutura do pitch (5 min)

Prepare os 5 blocos com tempo:
1. **Problema** (0:00–0:45): problema real e por que a GPU é necessária.
2. **Solução** (0:45–1:30): arquitetura e stack.
3. **Demo** (1:30–2:30): treino + monitor rodando.
4. **Resultados** (2:30–3:30): tabela baseline × GPU.
5. **Lições + PI** (3:30–5:00): obstáculos, aprendizados e conexão com o PI.

---

## 📊 Parte 2 — Relatório final

1. Gere o relatório com `relatorio_final.py` (ou no notebook).
2. Confira os 6 gráficos: val/loss, val/acc, temperatura, utilização, VRAM e baseline × GPU.
3. Substitua os **dados de referência** pelos reais do seu projeto.

---

## ✅ Parte 3 — Checklist antes do pitch

1. Rode `checklist_apresentacao.py` e corrija todos os itens marcados como `[FALTA]`.
2. Garanta que o repositório tem README, `requirements.txt` e commit recente.
3. Verifique se o dashboard e o relatório final estão no repositório.

---

## 💬 Parte 4 — Discussão em Grupo (10 min)

Após cada apresentação, a banca e os colegas respondem:

1. O ganho de velocidade veio de qual técnica principal? Combinaria mais de uma?
2. O monitor detectou algum evento real? Como o time reagiu?
3. O gráfico de val/loss mostrou overfitting ou underfitting? O que foi ajustado?
4. Como o tema do projeto se conecta ao Projeto Integrador?

---

## 📌 Parte 5 — Tarefa de Casa (para a Aula 24)

1. Incorporar o **feedback da banca** ao relatório final e commitar a versão definitiva.
2. Mapear pelo menos **3 pontos de conexão** entre o projeto de GPU e o PI do curso.
3. Documentar no README a **lição mais importante** para o PI.
4. Preparar 1 slide: *"Como aplicaríamos GPU/automação no nosso PI?"*
