# 🏁 Aula 20 — Definição do Projeto Final

**Objetivo:** planejar o projeto de IA acelerado por GPU — escolher o domínio e o problema,
definir dataset, modelo base e métrica, e montar o checklist de prontidão.

> 🧭 **Bloco 4 — Projeto Final.** Complementa o [`projeto-integrador/`](../../projeto-integrador/README.md) (pesquisa).

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula20.html`](apresentacao_aula20.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`scripts/projeto_exemplo.py`](scripts/projeto_exemplo.py) | Exemplo de configuração + checklist de prontidão |
| [`atividade.md`](atividade.md) | Roteiro e tarefa de casa |

---

## 🚀 Como usar

```bash
cd aulas/bloco4/aula20/scripts
python projeto_exemplo.py
```

---

## 🔑 Conceitos-chave

- **Domínio** — visão, PNL ou séries temporais.
- **Transfer Learning** — reutilizar modelo pré-treinado (ex.: ResNet-18).
- **Baseline** — solução simples para comparar com o modelo profundo.
- **Métrica principal** — accuracy, F1 ou RMSE.
- **Checklist de prontidão** — o que precisa estar pronto antes de implementar.

---

## 🔀 Outra trilha: pesquisa (sem código)

O projeto final pode ser feito de **duas formas**: implementando código (o script desta aula)
ou como um **trabalho de pesquisa**, no estilo do
[`projeto-integrador/`](../../projeto-integrador/README.md). Na trilha de pesquisa, esta etapa
(planejar) define o **problema real**, a **pergunta central**, as **fontes** e as
**alternativas de arquitetura** (ex.: CUDA vs ROCm).

📚 Exemplos de pesquisa prontos:
[Diagnóstico por Imagem](../projetos-exemplo/4-pesquisa-diagnostico-imagem/README.md) ·
[Green AI](../projetos-exemplo/5-pesquisa-green-ai/README.md) ·
[Agricultura de Precisão](../projetos-exemplo/6-pesquisa-agricultura-precisao/README.md).


## 📌 Tarefa de casa (para a Aula 21)

1. Completar o checklist e criar o repositório GitHub do projeto.
2. Testar o carregamento do dataset.
3. Implementar o **baseline** e medir a métrica principal.
