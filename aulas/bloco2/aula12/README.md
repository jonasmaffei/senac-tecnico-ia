# 🧠 Aula 12 — Laboratório Prático e Revisão Interativa

**Objetivo:** revisar, **na prática**, os conceitos das aulas 1 a 11 num único notebook
interativo do Google Colab — CPU × GPU, gargalo PCIe, tiling, VRAM e uma IA real de análise de
sentimentos.

---

## 🎯 Situação de aprendizagem

Depois de aprender os fundamentos e a programar na GPU, é hora de **juntar as peças**. Cinco
experimentos interativos (com sliders e menus) mostram os conceitos em ação, e no final um
modelo pré-treinado analisa avaliações de clientes **de verdade**.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula12.html`](apresentacao_aula12.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** com os 5 experimentos + **5 exercícios** |
| [`atividade.md`](atividade.md) | Roteiro de experimentos, análise e discussão |
| [`../../projeto-integrador/`](../../projeto-integrador/README.md) | **Projeto Integrador** (pesquisa aplicada) |

### Estrutura da aula

```
aula12/
  apresentacao_aula12.html
  README.md
  notebook_colab/aula12_pratica_colab.ipynb
  atividade.md
```

> ℹ️ Esta aula **não tem `laboratorio_windows/`**: os experimentos dependem de **GPU** (Colab).
> Sem GPU, o notebook mostra os avisos e roda o que não depende dela.

---

## 🚀 Como rodar

### No Google Colab

1. Abra `notebook_colab/aula12_pratica_colab.ipynb` pelo **GitHub** no Colab
   (`https://github.com/jonasmaffei/senac-tecnico-ia`).
2. *Ambiente de execução ➔ Alterar tipo de ambiente ➔ **T4 GPU*** ➔ *Salvar*.
3. Rode as células na ordem, mexendo nos **sliders e menus**.

---

## 🔑 Os 5 experimentos

| # | Experimento | Conceito | Aulas |
| :---: | :--- | :--- | :---: |
| 1 | Multiplicação massiva de matrizes | CPU × GPU (SIMD) | 1–2 |
| 2 | Custo de transferir dados (RAM → VRAM) | Gargalo PCIe | 3 |
| 3 | Filtro de imagem paralelo | Tiling (blocos/threads) | 7–8 |
| 4 | Monitor de VRAM (`nvidia-smi`) | VRAM / OOM | 9–10 |
| 5 | Classificador de feedbacks | Inferência com modelo pré-treinado | 11 |

> 💡 O Experimento 5 usa `transformers` (pré-instalado no Colab) e baixa um modelo multilíngue
> de análise de sentimentos da Hugging Face.

---

## 🧪 Atividade guiada

Rode os 5 experimentos e registre os resultados. Roteiro de análise em
[`atividade.md`](atividade.md).

---

## 💬 Discussão em grupo

Em grupos de 3–4:

1. Qual experimento mais surpreendeu o grupo? Por quê?
2. Em que situação a **CPU** seria a escolha certa, mesmo havendo GPU?
3. Que cuidados tomar antes de rodar um modelo grande no Colab gratuito?
4. Como os 5 experimentos se conectam ao **Projeto Integrador**?

---

## 🔗 Relação com o curso

- Esta aula **amarra** o Bloco 2: cada experimento reusa um conceito das aulas 1 a 11 num único
  ambiente interativo, servindo de **revisão** antes da síntese.
- **Próxima (Aula 13):** implementar um modelo paralelo simples — a síntese final do bloco.
