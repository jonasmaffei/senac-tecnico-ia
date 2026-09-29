# 📝 Atividade — Aula 18+19 (Concorrência e Energia na GPU)

**Entrega:** documento curto (1 a 2 páginas) em Word/PDF, com os resultados das duas práticas.

---

## 🎯 Objetivo

Operar **1 GPU compartilhada** com **justiça** (1 job por vez + fila com prioridade) e com
**eficiência** (Power Limit calibrado por dados), unindo os temas de concorrência e energia.

---

## 🧪 Parte 1 — Concorrência (Prática 1)

Rode o notebook e registre:

1. **Sem lock:** com VRAM de 4 GB e 4 jobs de 2.5 GB, quantos conseguem alocar? Onde ocorre o
   **OOM**?
2. **Com lock:** descreva, em 2–3 linhas, como o **lock por diretório** (`mkdir` atômico)
   garante um job por vez.
3. **Fila:** qual foi a **ordem de execução** dos 4 jobs? Ela respeitou a **prioridade**?
4. **Starvation:** em quais situações um job de baixa prioridade pode **nunca** rodar? Como o
   **aging** resolve?

---

## 🌡️ Parte 2 — Energia (Prática 2)

1. **TDP × throttling:** acima de qual temperatura a GPU passa a reduzir o clock? O que isso
   faz com o **consumo**?
2. **Power Limit:** preencha a tabela do benchmark:

| Power Limit (W) | Throughput (imgs/s) | Potência (W) | Eficiência (imgs/J) |
| :---: | :---: | :---: | :---: |
| 100 | | | |
| 150 | | | |
| 200 | | | |
| 225 | | | |
| 250 | | | |

3. Qual Power Limit deu a **melhor eficiência**? Ele é o de **maior potência**? Explique.

---

## 🔗 Parte 3 — Integração (o ponto central)

Responda:

1. Por que **não** faz sentido calibrar o Power Limit com dois jobs ao mesmo tempo na GPU?
2. Escreva um **plano curto (5–8 linhas)** para operar **1 GPU com 3 usuários**, combinando:
   - o **lock/fila** da Parte 1;
   - o **Power Limit** da Parte 2.

---

## 💬 Discussão em grupo

1. Reduzir o PL em 20% sacrifica ~8% de throughput e economiza ~20% de energia. Você faria isso
   com um **deadline em 2 dias**? E num projeto de **3 meses**?
2. A fila por prioridade pode ser "injusta" com quem tem baixa prioridade. Como equilibrar
   **urgência** e **equidade**?
3. Se a GPU é compartilhada, quem deveria definir o **Power Limit** — cada usuário ou o
   administrador?

---

## 🏁 Entrega

Um documento com:

- os resultados das **duas práticas**;
- o **plano de operação** (1 GPU, 3 usuários);
- uma conclusão de **5–8 linhas** ligando concorrência e energia.

---

## 📝 Questionário (Aulas 14 a 19)

As **18 questões** de revisão do Bloco 3 estão em
[`questionarios/questionario-aulas-14-19.md`](../../../questionarios/questionario-aulas-14-19.md).

**Entrega:** envie as respostas por e-mail para `03049691093@senacrs.edu.br` com o assunto
`Questionario aulas 14 a 19`.
