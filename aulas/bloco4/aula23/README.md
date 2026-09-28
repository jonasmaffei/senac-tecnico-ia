# 🎤 Aula 23 — Apresentação e Análise dos Projetos

**Objetivo:** comunicar de forma clara e técnica os resultados do projeto de IA acelerado
por GPU — estruturar o **pitch de 5 minutos**, gerar o **relatório final automatizado**,
apresentar para a banca e receber feedback para a conexão com o Projeto Integrador.

> 🧭 **Bloco 4 — Projeto Final.** Continua a [Aula 22](../aula22/README.md).

---

## 🎯 Situação de aprendizagem

O treinamento finalizou, os logs de GPU estão salvos e o W&B registrou todas as runs. Uma
**banca técnica** vai avaliar cada projeto: o que foi resolvido, como a GPU foi usada
estrategicamente, os ganhos reais e o que o time aprendeu. Você tem **5 minutos** — prepare
o pitch, gere o relatório final e demonstre o pipeline funcionando.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula23.html`](apresentacao_aula23.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** com explicação + **5 exercícios** |
| [`scripts/`](scripts) | Scripts de referência (`relatorio_final.py`, `checklist_apresentacao.py`) |
| [`atividade.md`](atividade.md) | Roteiro do pitch, rubrica e tarefa de casa |

### Estrutura da aula

```
aula23/
  apresentacao_aula23.html
  README.md
  notebook_colab/aula23_apresentacao_projetos.ipynb
  scripts/relatorio_final.py
  scripts/checklist_apresentacao.py
  atividade.md
```

---

## 🚀 Como usar

### No Google Colab
Abra `notebook_colab/aula23_apresentacao_projetos.ipynb` pelo **GitHub** no Colab. Gere a
tabela baseline × GPU, o relatório de 6 gráficos e avalie a rubrica.

### Localmente (modo de referência)
```bash
cd aulas/bloco4/aula23/scripts
python relatorio_final.py           # gera relatorio_final/relatorio_final.png
python checklist_apresentacao.py    # verifica a prontidão do projeto
```

---

## 🔑 Conceitos-chave

- **Pitch técnico (5 min)** — Problema → Solução → Demo → Resultados → Lições + PI.
- **Relatório automatizado** — combina W&B + logs de GPU em um PNG.
- **Baseline vs GPU** — a tabela que evidencia o valor real da aceleração.
- **Rubrica (100 pts)** — modelo, automação, apresentação e documentação.
- **W&B run export** — exportar o histórico de métricas para análise offline.
- **Conexão com o PI** — como aplicar GPU/automação no Projeto Integrador.

---

## 📊 Rubrica resumida (100 pts + bônus)

| Dimensão | Pts |
| :--- | :---: |
| Qualidade técnica do modelo | 30 |
| Automação e monitoramento | 25 |
| Qualidade da apresentação | 25 |
| Documentação e reprodutibilidade | 20 |
| **Bônus** | +10 |

---

## 📌 Tarefa de casa (para a Aula 24)

1. Incorporar o **feedback da banca** ao relatório final e commitar a versão definitiva.
2. Mapear pelo menos **3 pontos de conexão** entre o projeto de GPU e o PI.
3. Documentar no README a **lição mais importante** que o time leva para o PI.
4. Preparar 1 slide: *"Como aplicaríamos GPU/automação no nosso PI?"*
