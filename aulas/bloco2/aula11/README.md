# 🧠 Aula 11 — Aplicação de Modelos de IA (NVIDIA vs AMD)

**Objetivo:** treinar um modelo de visão computacional e comparar o desempenho entre GPUs
**NVIDIA** (CUDA) e **AMD** (ROCm), medindo **throughput**, **VRAM** e o ganho do
*mixed precision* (FP16), para apoiar uma decisão de infraestrutura baseada em **dados**.

---

## 🎯 Situação de aprendizagem

A startup **"IA Entregas"** precisa alugar GPUs na nuvem para treinar seus modelos pelos
próximos **3 anos**. O diretor financeiro quer saber se deve escolher placas **NVIDIA** ou
**AMD**. Você é o **consultor de tecnologia**: roda o benchmark, lê os números e recomenda a
melhor escolha técnica e financeira.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula11.html`](apresentacao_aula11.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** com explicação + **5 exercícios** |
| [`laboratorio_windows/`](laboratorio_windows/README.md) | **Experimentos portáveis** (FP32/FP16 + custo TCO) |
| [`atividade.md`](atividade.md) | Atividade de pesquisa (engenharia + negócios) e discussão |

### Estrutura da aula

```
aula11/
  apresentacao_aula11.html
  README.md
  notebook_colab/aula11_aplicacao_modelos.ipynb
  laboratorio_windows/          # iniciar.bat, lib_treino.py, 1_benchmark_treino.py, 2_comparar_ecossistemas.py
  atividade.md
```

> ℹ️ **Não há `scripts/` separado:** o laboratório é autocontido (`lib_treino.py` local). Como o
> laboratório não tem GPU NVIDIA, ele roda em **modo de referência** — o mesmo código treina de
> verdade no Colab (T4).

---

## 🚀 Como rodar

### No Google Colab (recomendado — treino real)

1. Abra `notebook_colab/aula11_aplicacao_modelos.ipynb` pelo **GitHub** no Colab
   (`https://github.com/jonasmaffei/senac-tecnico-ia`).
2. *Ambiente de execução ➔ Alterar tipo de ambiente ➔ **T4 GPU*** ➔ *Salvar*.
3. Rode as células na ordem.

> 💡 **Sem GPU?** O notebook detecta e mostra os **números de referência** (T4) — a aula roda do
> começo ao fim.

### No Windows do laboratório (portável)

Dê **duplo clique** em [`laboratorio_windows/iniciar.bat`](laboratorio_windows/iniciar.bat):

```
[1] 1_benchmark_treino.py       - FP32 vs. FP16 (throughput)
[2] 2_comparar_ecossistemas.py  - NVIDIA x AMD + custo (TCO)
[0] Sair
```

---

## 🔑 Conceitos-chave

### Métricas de treino

| Métrica | O que é | Analogia |
| :--- | :--- | :--- |
| **Throughput (imgs/s)** | Imagens processadas por segundo | pacotes entregues por minuto |
| **VRAM (MB)** | Memória da GPU em uso | espaço no caminhão |
| **Tempo por época (s)** | Tempo para ler todo o dataset | duração da viagem |
| **Mixed Precision (FP16)** | Cálculos com números menores | dobrar a carga útil |

### Mixed Precision (FP16)

Usa FP16 onde dá ganho e mantém FP32 onde a precisão é crítica. O **`GradScaler`** controla a
escala do gradiente para evitar *underflow*. Ganho típico numa **T4**: **~1.9×** de throughput.

### CUDA × ROCm

| Critério | NVIDIA (CUDA) | AMD (ROCm) |
| :--- | :--- | :--- |
| Ecossistema | maduro | em crescimento |
| Facilidade | exemplos abundantes | setup mais trabalhoso |
| Custo/hora na nuvem | mais caro | tende a ser menor |
| Portabilidade | código preso ao CUDA | PyTorch roda via HIP |

> A pergunta certa não é "qual é mais rápida", mas **"qual entrega o melhor resultado por real
> gasto"**, considerando a equipe que você já tem.

---

## 🧪 Atividade guiada

No **Colab** (GPU) ou no **Windows**:

```bash
python laboratorio_windows/1_benchmark_treino.py      # FP32 vs. FP16
python laboratorio_windows/2_comparar_ecossistemas.py # NVIDIA x AMD + TCO
```

Roteiro completo em [`atividade.md`](atividade.md).

---

## 💬 Discussão em grupo

Em grupos de 3–4:

1. O FP16 deu ganho grande. Por que **não** treinamos tudo em FP16?
2. A AMD tem preço/hora menor. Que **custos escondidos** podem aparecer?
3. Otimizar o software antes de comprar mais GPUs pode sair mais barato? Dê um exemplo.
4. Se o mesmo código roda em CUDA e ROCm, o que ainda prende as empresas à NVIDIA?

---

## 📌 Tarefa de casa

Relatório de 1 a 2 páginas: *"Qual marca de placa de vídeo eu recomendaria para a IA Entregas
hoje e por quê?"*, citando **um número medido**, **um número de custo** e **um fator
qualitativo**. Detalhes em [`atividade.md`](atividade.md).

---

## 🔗 Relação com o curso

- **Aula 10** mostrou a **portabilidade** CUDA → ROCm (o mesmo PyTorch roda numa GPU AMD).
  Esta aula **mede** o desempenho e transforma a comparação em **decisão de negócio**.
- **Próxima (Aula 12):** laboratório prático no Colab + início do **Projeto Integrador**.
