# ⚡ Aula 21 — Implementação do Modelo no Projeto

**Objetivo:** implementar um modelo de IA com otimizações específicas para GPU —
**mixed precision** (`autocast`/`GradScaler`), **gradient checkpointing**, **gradient
accumulation** e **DataLoader** otimizado — usando **profiling** para identificar
gargalos e validando os ganhos frente ao baseline da Aula 20.

> 🧭 **Bloco 4 — Projeto Final.** Dá continuidade à [Aula 20](../aula20/README.md).

---

## 🎯 Situação de aprendizagem

O hackathon entrou na fase crítica. O plano está pronto, o repositório estruturado e o
baseline medido. Agora é implementar o modelo profundo com **aceleração GPU real** e
entregar ao final da aula um modelo treinando com pelo menos uma rodada completa registrada.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula21.html`](apresentacao_aula21.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** com explicação + **5 exercícios** |
| [`scripts/`](scripts) | Scripts de referência (`pipeline_treinamento.py`, `otimizacao_memoria.py`) |
| [`atividade.md`](atividade.md) | Roteiro prático, discussão e tarefa de casa |

### Estrutura da aula

```
aula21/
  apresentacao_aula21.html
  README.md
  notebook_colab/aula21_implementacao_modelo.ipynb
  scripts/pipeline_treinamento.py
  scripts/otimizacao_memoria.py
  atividade.md
```

---

## 🚀 Como usar

### No Google Colab
Abra `notebook_colab/aula21_implementacao_modelo.ipynb` pelo **GitHub** no Colab. Com GPU
T4, o AMP funciona de verdade; sem GPU, o notebook usa **números de referência**.

### Localmente (modo de referência)
```bash
cd aulas/bloco4/aula21/scripts
python pipeline_treinamento.py     # mostra o fluxo de uma época AMP x FP32
python otimizacao_memoria.py       # estima batch máximo e acumulação
```

---

## 🔑 Conceitos-chave

- **`autocast` / `GradScaler`** — o par que habilita mixed precision (fp16).
- **`pin_memory` + `prefetch`** — eliminam a espera CPU→GPU.
- **Gradient Checkpointing** — recomputa ativações no backward: −60% VRAM, +30% tempo.
- **Gradient Accumulation** — batch efetivo = real × N sem OOM.
- **`torch.profiler`** — mede antes de otimizar; aponta o gargalo real.
- **`set_to_none=True`** — libera buffers de gradiente (mais rápido e econômico).

---

## 📌 Tarefa de casa (para a Aula 22)

1. Executar pelo menos **10 épocas** completas com AMP e logging.
2. Rodar o monitor de GPU (Aula 14) durante o treino e salvar o CSV.
3. Comparar o throughput (imgs/s) com e sem AMP e registrar no README.
4. **Bônus:** experimentar `torch.compile(model)` e medir o impacto.
