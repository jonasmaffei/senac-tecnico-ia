# 📝 Aula 12 — Atividade: Laboratório Prático e Revisão

**Entrega:** documento curto (1 a 2 páginas) em Word/PDF, com os resultados dos experimentos.

---

## 🎯 Objetivo

Revisar, **na prática**, os conceitos das aulas 1 a 11 num único notebook interativo no Google
Colab: CPU × GPU, gargalo PCIe, tiling, VRAM e uma IA real de análise de sentimentos.

---

## 🧪 Parte 1 — Experimentos no Colab

Rode os **5 experimentos** do notebook e registre os resultados numa tabela:

| Experimento | O que mediu | Resultado | Aula relacionada |
| :--- | :--- | :--- | :--- |
| 1 — CPU × GPU | tempo CPU, tempo GPU, speedup | | 1–2 |
| 2 — PCIe | tempo de transferência × processamento | | 3 |
| 3 — Filtro de imagem | efeito escolhido e resultado | | 7–8 |
| 4 — VRAM | VRAM total / usada / livre | | 9–10 |
| 5 — Sentimento | classificação e confiança | | 11 |

> ⚙️ **Não esqueça:** ative a GPU (*Ambiente de execução ➔ Alterar tipo ➔ T4 GPU*). Vários
> experimentos dependem disso.

---

## 🔎 Parte 2 — Análise

Responda, com base nos números que você obteve:

1. **Paralelismo:** o speedup da GPU aumentou com o tamanho da matriz? Por quê?
2. **Memória:** o tempo de **transferir** ou o de **processar** dominou o Experimento 2? O que
   isso implica para um pipeline de IA?
3. **Tiling:** descreva, em uma frase, o que cada thread faz no filtro de imagem.
4. **VRAM:** se um modelo precisasse de mais VRAM do que a placa tem, o que aconteceria?
5. **Inferência:** por que o modelo de sentimentos **não** precisou ser treinado nesta aula?

---

## 💬 Parte 3 — Discussão em grupo

Em grupos de 3–4:

1. Qual experimento mais surpreendeu o grupo? Por quê?
2. Em qual situação a **CPU** seria a escolha certa, mesmo havendo GPU disponível?
3. Que cuidados devemos tomar antes de rodar um modelo grande no Colab gratuito?
4. Como os 5 experimentos se conectam ao **Projeto Integrador**?

---

## 🏁 Parte 4 — Síntese

Escreva um parágrafo (5 a 8 linhas) explicando, com suas palavras, **o fio condutor** que liga os
5 experimentos: do paralelismo à aplicação real de IA.
