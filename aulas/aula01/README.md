# 🧠 Aula 01 — Introdução às Arquiteturas de Computadores e GPUs

**Objetivo:** compreender as arquiteturas clássicas de computadores (**Von Neumann** e
**Harvard**) e o papel diferenciado das **GPUs** na computação moderna — em especial na
Inteligência Artificial — para embasar decisões técnicas em ambientes reais de
desenvolvimento.

---

## 🎯 Situação de aprendizagem

Você é estagiário(a) numa startup que desenvolve um **sistema de reconhecimento facial
em tempo real** para controle de acesso. A equipe precisa decidir se vai usar **CPU ou
GPU** para rodar o modelo de IA. Antes de escolher o hardware, é essencial entender como
o computador funciona por dentro e por que as GPUs são tão eficazes em IA.

---

## 🗂️ Conteúdo

| Arquivo | O que é |
| :--- | :--- |
| [`apresentacao_aula01.html`](apresentacao_aula01.html) | Slides teóricos (abra no navegador, navegue com ← →) |
| [`aula01_arquiteturas_cpu_gpu.ipynb`](aula01_arquiteturas_cpu_gpu.ipynb) | Notebook do **Google Colab** (teoria + `nvidia-smi` + benchmark) |
| [`atividade.md`](atividade.md) | Atividade de pesquisa e discussão em grupo |
| [`scripts/arquitetura_cpu_gpu.py`](scripts/arquitetura_cpu_gpu.py) | Benchmark CPU (sequencial) vs. NumPy (vetorizado), comentado |

---

## 🚀 Como rodar no Google Colab

1. Acesse o [Google Colab](https://colab.research.google.com/) e faça login.
2. Aba **GitHub** → cole `https://github.com/jonasmaffei/senac-tecnico-ia` → abra
   `aulas/aula01/aula01_arquiteturas_cpu_gpu.ipynb`.
3. **Ative a GPU:** *Runtime ➔ Change runtime type ➔ **T4 GPU*** ➔ *Save*.
4. Rode as células na ordem. A primeira detecta a GPU:

```
!nvidia-smi   # mostra modelo, VRAM, temperatura e processos
```

> 💡 **Sem GPU?** O notebook detecta a ausência do `nvidia-smi` e entra em **modo
> simulado**, com os mesmos dados sintéticos. Toda a aula continua funcionando.

---

## 🔑 Conceitos-chave

- **Von Neumann** — memória compartilhada para dados e instruções; usada na maioria dos PCs.
- **Harvard** — memórias separadas; acesso simultâneo; comum em embarcados (microcontroladores, DSPs).
- **Gargalo de Von Neumann** — instruções e dados disputam o mesmo barramento → processador espera.
- **CPU** — poucos núcleos, alta frequência, ótima em tarefas sequenciais e lógica de controle.
- **GPU** — milhares de núcleos, alta largura de banda, feita para paralelismo massivo e matrizes.

### Analogia
> A **CPU** é um chef experiente que faz um prato complexo sozinho. A **GPU** são mil
> cozinheiros fazendo o mesmo prato simples ao mesmo tempo.

---

## 🧪 Atividade guiada (no notebook)

Somar **1000 números**, se cada instrução leva 1 ciclo:

| Abordagem | Conta | Resultado |
| :--- | :--- | :--- |
| **CPU (1 núcleo)** | 1000 × 1 ciclo | 1000 ciclos |
| **GPU (1000 núcleos)** | 1000 ÷ 1000 | 1 ciclo (≈ 1000× mais rápido) |

O notebook mede isso na prática: **3 loops aninhados** (sequencial) vs. **NumPy/BLAS**
(vetorizado). Matrizes de IA têm milhões de linhas — sem paralelismo, é inviável.

---

## 💬 Discussão em grupo

1. Em que aplicações a **CPU** ainda é melhor que a GPU?
2. Por que um **smartphone** usa GPU integrada?
3. Vale a pena usar GPU para um **site simples**? Por quê?
4. Como **escolher entre CPU e GPU** para um projeto de IA?

---

## 📌 Tarefa de casa (opcional)

Encontre um **caso real** (notícia, artigo, vídeo) em que a GPU acelerou significativamente
uma aplicação de IA. Temas sugeridos: Tesla Autopilot, diagnóstico médico com deep
learning, PLN (ChatGPT) e renderização de filmes em tempo real.

---

## 🔧 Recursos de apoio

- **Google Colab** — GPU gratuita + `nvidia-smi` (ambiente principal da aula).
- **CPU Sim** — simulador web de arquitetura Von Neumann (para visualizar o ciclo de instrução).
- **VS Code Online** e **Replit** — editores na nuvem para praticar.

---

## 🔗 Relação com o curso

Esta é a primeira aula do **Bloco 1 — Fundamentos**. Ela estabelece a base que as
seguintes aprofundam: modelos de processamento (Aula 2), hierarquia de memória (Aula 3)
e, mais adiante, programação em GPU (Aulas 7–13).
