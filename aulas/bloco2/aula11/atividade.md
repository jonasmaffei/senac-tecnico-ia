# 📝 Aula 11 — Atividade: Aplicação de Modelos de IA (NVIDIA vs AMD)

**Entrega:** relatório simples (1 a 2 páginas) em Word/PDF, em duplas ou trios.

---

## 🎯 Cenário da empresa

A startup **"IA Entregas"** precisa contratar servidores de placa de vídeo na nuvem para
treinar seus modelos pelos próximos **3 anos**. O diretor financeiro quer saber se deve
escolher placas **NVIDIA** ou **AMD**.

Você é o **consultor de tecnologia**. A decisão deve ser tomada com **dados** — não com
opinião.

---

## 🧪 Parte 1 — Prática (no Colab ou no laboratório)

Rode o treino comparativo (FP32 vs. FP16) e registre:

| Métrica | FP32 (padrão) | FP16 (mixed precision) |
| :--- | :--- | :--- |
| Throughput (imgs/s) | | |
| VRAM usada (MB) | | |
| Speedup | — | |

> 💡 Sem GPU? Use os números de **referência** mostrados pelo script e explique por que seriam
> diferentes numa T4 real.

---

## 🔎 Parte 2 — Pesquisa de custo

1. **Nuvem — NVIDIA:** pesquise o valor por hora de uma GPU **NVIDIA T4** (ou A10G) no Google
   Cloud ou AWS.
2. **Nuvem — AMD:** pesquise o preço de uma **AMD Instinct (ex.: MI300X)** ou placas AMD na
   nuvem.
3. **Comparação:** qual das marcas costuma ter o **aluguel por hora** mais baixo?

---

## ⚖️ Parte 3 — Facilidade de uso × economia

A NVIDIA usa o ecossistema **CUDA** (muito popular e fácil de instalar). A AMD usa o **ROCm**.

1. Se a equipe técnica já é habituada ao ecossistema NVIDIA, qual é o **desafio operacional**
   de migrar para AMD?
2. O preço mais baixo da AMD **compensa** a necessidade de adaptação da equipe? Justifique.

---

## 📊 Parte 4 — Análise dos resultados

1. No modo **Otimizado (FP16)**, o que aconteceu com a velocidade (imgs/s)?
2. Por que usar **mixed precision** é importante **antes** de gastar dinheiro comprando mais
   placas de vídeo?

---

## 🏁 Parte 5 — Recomendação (tarefa principal)

Escreva um texto curto (1 a 2 páginas) respondendo:

> *"Se você fosse o gerente de tecnologia, qual marca de placa de vídeo recomendaria comprar
> para a sua empresa hoje e por quê?"*

**Sua resposta deve citar, no mínimo:**

- **um número** medido na prática (throughput, VRAM ou speedup);
- **um número** da pesquisa de custo (preço/hora ou economia anual);
- **um fator qualitativo** (facilidade de uso, mão de obra ou risco de migração).

---

## 💬 Discussão em grupo

1. O FP16 deu ganho grande. Por que **não** treinamos tudo em FP16?
2. A AMD tem preço/hora menor. Que **custos escondidos** podem aparecer ao trocar?
3. Otimizar o software antes de comprar mais GPUs pode sair mais barato? Dê um exemplo.
4. Se o mesmo código roda em CUDA e ROCm, o que ainda prende as empresas à NVIDIA?
