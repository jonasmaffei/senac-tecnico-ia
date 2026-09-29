# 🌙 Aula dupla 18 + 19 — Concorrência e Energia na GPU

**Formato:** aula **dupla**, condensada para **uma única noite** (≈120 min).
**Objetivo:** operar a GPU com **justiça** (1 job por vez + fila com prioridade) e com
**eficiência** (medir e limitar a energia).

> ⏱️ **Para quem tem só uma noite.** Esta pasta junta o essencial das
> [Aula 18](../aula18/README.md) (concorrência) e [Aula 19](../aula19/README.md) (energia)
> num material único. As aulas completas continuam existindo para quem tiver mais tempo.

---

## 🎯 Situação de aprendizagem

O data center consome **40% mais energia** que o projetado **e** os jobs disputam a mesma GPU
causando **CUDA OOM**. Os dois problemas têm a mesma raiz: **falta de controle sobre a GPU**.
Vamos resolver ambos: primeiro a **concorrência**, depois a **energia**.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula18_19.html`](apresentacao_aula18_19.html) | Slides **só conceito** (11 slides; navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook único no **Google Colab** (concorrência + energia) + **Exercícios (5)** |
| [`atividade.md`](atividade.md) | Roteiro da noite, discussão e entrega |

### Estrutura da pasta

```
aula18_19_dupla/
  apresentacao_aula18_19.html
  README.md
  notebook_colab/aula18_19_concorrencia_energia.ipynb
  atividade.md
```

---

## 🚀 Como usar na noite

### No Google Colab (recomendado)

1. Abra `notebook_colab/aula18_19_concorrencia_energia.ipynb` pelo **GitHub** no Colab.
2. Rode as células na ordem. **Sem GPU NVIDIA**, tudo roda em **modo simulado** — os conceitos
   valem igual.

### No Windows (laboratório)

Use os laboratórios das aulas originais (a mesma máquina):

- **Concorrência:** [`../aula18/laboratorio_windows/`](../aula18/laboratorio_windows/README.md)
  (`iniciar.bat` → lança 4 jobs e mostra a serialização por prioridade).
- **Energia:** [`../aula19/laboratorio_windows/`](../aula19/laboratorio_windows/README.md)
  (`iniciar.bat` → monitor térmico, alerta, benchmark de eficiência e Power Limit).

---

## 🧭 Roteiro da noite (≈120 min)

| Tempo | Bloco |
| :---: | :--- |
| 10 min | Abertura: os dois problemas (OOM + energia) |
| 25 min | **Parte 1** — race condition, lock e fila com prioridade |
| 25 min | **Prática 1** — 4 jobs disputando a GPU (serialização) |
| 25 min | **Parte 2** — TDP, throttling, Power Limit e NVML |
| 25 min | **Prática 2** — benchmark de eficiência (imgs/J) |
| 10 min | Síntese: integrar as duas partes |

---

## 🔑 Conceitos-chave

- **Race condition** — jobs concorrentes corrompem a VRAM → OOM.
- **Lock / exclusão mútua** — `flock` (Linux) ou **lock por diretório** (`mkdir` atômico).
- **Fila por prioridade** — ticket `prioridade_timestamp_nome`, com **aging** contra starvation.
- **TDP / TGP** e **thermal throttling** — por que GPUs gastam mais do que o esperado.
- **Power Limit** — reduzir 20–30% custa ~5–10% de throughput; melhora muito o consumo.
- **Eficiência (imgs/J)** — throughput ÷ potência; ótimo em **~60–75% do TDP**.

---

## 🔗 Relação com o curso

- **Aulas 14/17** (automação) e **15/18** (concorrência) preparam o terreno; aqui usamos o
  lock e a fila como base para **medir energia sem contaminação**.
- **Aula 19** aprofunda o tema de energia; esta aula dupla resume o suficiente para **uma noite**.
