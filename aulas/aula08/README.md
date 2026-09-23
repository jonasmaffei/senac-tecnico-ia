# 🧠 Aula 08 — Manipulação de Memória em CUDA (Tiling)

**Objetivo:** aplicar estratégias de uso eficiente do gerenciamento de memória da GPU —
global, compartilhada e registradores — para otimizar kernels CUDA em aplicações de IA,
medindo o impacto real com profiling.

---

## 🎯 Situação de aprendizagem

O kernel CUDA que você escreveu na Aula 7 para acelerar a FFT ficou **mais lento do que o
esperado** ao processar lotes grandes. O engenheiro sênior analisou com o **NVIDIA Nsight** e
identificou o problema: os **acessos à memória global** estão causando gargalo. Sua missão é
reescrever o kernel usando **memória compartilhada** e técnicas de **tiling** para reduzir os
acessos à VRAM e atingir o desempenho esperado.

---

## 🗂️ Conteúdo

| Arquivo | O que é |
| :--- | :--- |
| [`apresentacao_aula08.html`](apresentacao_aula08.html) | Slides teóricos (abra no navegador, navegue com ← →) |
| [`aula08_tiling.ipynb`](aula08_tiling.ipynb) | Notebook do **Google Colab** (coalescing, global × tiling, profiling) |
| [`atividade.md`](atividade.md) | Atividade de pesquisa (engenharia + negócios) e discussão |
| `scripts/` | Scripts comentados (coalescing, matmul, profiling, estresse) |

### Scripts

| Script | O que faz |
| :--- | :--- |
| [`lib_cuda.py`](scripts/lib_cuda.py) | Detecta se há CUDA; permite rodar com fallback sem GPU |
| [`coalescing.py`](scripts/coalescing.py) | Acessos coalescidos vs. não-coalescidos à VRAM |
| [`matmul_global.py`](scripts/matmul_global.py) | Matmul ingênua (memória global, o kernel lento) |
| [`matmul_tiling.py`](scripts/matmul_tiling.py) | Matmul otimizada (tiling em shared memory) + cuBLAS |
| [`profiling_ocupacao.py`](scripts/profiling_ocupacao.py) | Medição com `cuda.event` + métricas do Nsight |
| [`stress_nvtop.py`](scripts/stress_nvtop.py) | Teste de estresse da GPU para ver no nvtop |

---

## 🚀 Como rodar

### No Google Colab (recomendado — **exige GPU NVIDIA**)

1. Abra `aula08_tiling.ipynb` pelo **GitHub** no Colab
   (`https://github.com/jonasmaffei/senac-tecnico-ia`).
2. *Runtime ➔ Change runtime type ➔ **T4 GPU*** ➔ *Save*.
3. Rode as células na ordem.

> ⚠️ **Sem GPU NVIDIA?** O notebook detecta e mostra o conceito e os números de referência.

### No Windows do laboratório

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat). Ele cria o ambiente virtual (`.venv`),
instala as dependências de [`requirements.txt`](requirements.txt) e abre um **menu**:

```
[1] coalescing.py         - acessos coalescidos vs. nao-coalescidos
[2] matmul_global.py      - matmul ingenua (memoria global)
[3] matmul_tiling.py      - matmul com tiling (memoria compartilhada)
[4] profiling_ocupacao.py - medir kernel + metricas do Nsight
[5] stress_nvtop.py       - teste de estresse da GPU
[6] lib_cuda.py           - detectar se ha CUDA disponivel
[0] Sair
```

> Na máquina do laboratório (**GPU AMD**), o CUDA não está disponível: os scripts mostram o
> conceito e os números de referência.

---

## 🔑 Conceitos-chave

### Hierarquia de memória CUDA

| Memória | Escopo | Latência | Uso |
| :--- | :--- | :--- | :--- |
| **Registradores** | privado por thread | ~1 ciclo | variáveis locais automáticas |
| **Compartilhada (SRAM)** | por bloco | ~5 ciclos | cache manual (tiling) |
| **Global (VRAM)** | todos | ~500 ciclos | arrays principais |

> **Regra 90/10:** ~90% do tempo de execução de kernels de IA é gasto em **acessos de
> memória**.

### Coalescing

Threads consecutivas do mesmo warp devem acessar endereços **consecutivos**:
- **coalescido** → 1 transação de 128 bytes;
- **não-coalescido** (stride) → até ~32 transações separadas (muito mais lento).

### Tiling

O bloco carrega um **tile** de A e B para a **memória compartilhada** e todos os threads do
bloco reutilizam esses dados, reduzindo os acessos à VRAM por um fator ~TILE. Exige **dois**
`cuda.syncthreads()` (barreira antes e depois do uso).

### Profiling

- **`cuda.event`** — mede o tempo na própria GPU.
- **Nsight Systems** (`nsys`) — visão macro (timeline, transferências).
- **Nsight Compute** (`ncu`) — visão micro (ocupância, roofline, bytes da DRAM).

---

## 🧪 Atividade guiada

No **Colab com GPU**:

```bash
python scripts/coalescing.py       # coalescido vs. strided
python scripts/matmul_global.py    # versão lenta
python scripts/matmul_tiling.py    # versão otimizada + cuBLAS
python scripts/profiling_ocupacao.py
```

Exercícios completos em [`atividade.md`](atividade.md).

---

## 💬 Discussão em grupo

Em grupos de 3–4, no cenário do kernel lento:

1. Com tile 16×16, quantas vezes cada elemento de A e B é lido da VRAM vs. da SRAM?
2. Por que são obrigatórios **dois** `cuda.syncthreads()` no kernel de tiling?
3. A shared memory tem ~48 KB por SM. Com TILE=32, os dois tiles cabem?
4. Em que situações usar memória compartilhada **não** vale a pena?

---

## 📌 Tarefa de casa (opcional)

Otimize o kernel de **transposta de matriz** usando memória compartilhada para evitar acessos
não-coalescidos:

- implemente a transposta ingênua (global) e a versão com shared (`TILE×TILE+1`);
- explique por que o `+1` na dimensão interna elimina *bank conflicts*;
- meça com `cuda.event` para N = 256, 512, 1024, 2048;
- plote o gráfico de speedup × N com Matplotlib.

---

## 🔗 Relação com o curso

- **Aula 7** escreveu o primeiro kernel, mas ele batia toda hora na **VRAM global lenta**.
  Esta aula reescreve o kernel com **cache manual (SRAM)** e **coalescing** para eliminar o
  gargalo de largura de banda.
- **Próxima (Aula 9):** *Alternativas ao CUDA (OpenCL) + LLMs locais* — o kernel está
  otimizado, mas e quando o hardware **não** é NVIDIA?
