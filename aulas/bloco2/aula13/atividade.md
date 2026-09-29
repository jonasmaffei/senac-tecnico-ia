# 📝 Aula 13 — Atividade: Implementação de um Modelo Paralelo

**Entrega:** documento curto (1 a 2 páginas) em Word/PDF, com o mini-relatório e o speedup.

---

## 🎯 Objetivo

Implementar e comparar a **soma vetorial** e o **produto escalar** em **4 versões** — Python
puro, NumPy, Numba CUDA e CuPy — e consolidar o Bloco 2 com dados e um mini-relatório.

---

## 🧪 Parte 1 — Execução no Colab

Ative a GPU (*Ambiente de execução ➔ Alterar tipo ➔ T4 GPU*), rode o notebook e registre:

| Versão | Soma (N=10M) | Produto escalar (N=10M) |
| :--- | :--- | :--- |
| Python puro | | |
| NumPy (CPU) | | |
| Numba CUDA (GPU) | | |
| CuPy (GPU) | | |

Preencha também a seção extra da **norma** (`np.linalg.norm` × `cp.linalg.norm`).

---

## 🔎 Parte 2 — Análise

1. **Abstrações:** ordene as 4 versões da mais lenta à mais rápida. O resultado coincide com o
   esperado?
2. **SMD × SIMT:** por que o NumPy já é muito mais rápido que o Python puro, mesmo sem GPU?
3. **Launch overhead:** em qual valor de N a GPU começou a compensar a CPU? O que explica esse
   limiar?
4. **CuPy × Numba:** qual das duas versões de GPU foi mais **simples de escrever**? E qual daria
   mais **controle**? Justifique.
5. **Norma:** quantas vezes a GPU foi mais rápida no cálculo da norma? Esse ganho é maior ou
   menor que o da soma vetorial?

---

## 💬 Parte 3 — Discussão em grupo

Em grupos de 3–4:

1. Em que cenário real usaríamos cada uma das 4 versões?
2. Vale a pena escrever um kernel CUDA "na mão" (Numba) em vez de usar CuPy? Quando?
3. Que cuidados tomar ao comparar tempos de CPU e GPU (warm-up, sincronização)?
4. Como esse benchmark se conecta ao **Projeto Integrador**?

---

## 📑 Parte 4 — Mini-relatório

Use o **mini-relatório automático** gerado pelo notebook como base e escreva uma conclusão de
5 a 8 linhas respondendo:

> *"Em que ponto vale a pena usar a GPU e a partir de qual tamanho de problema ela passa a
> compensar?"*

---

## 📝 Questionário (Aulas 8 a 13)

As **18 questões** de revisão estão em
[`questionarios/questionario-aulas-8-13.md`](../../../questionarios/questionario-aulas-8-13.md).

**Entrega:** envie as respostas por e-mail para `03049691093@senacrs.edu.br` com o assunto
`Questionario aulas 8 a 13`.
