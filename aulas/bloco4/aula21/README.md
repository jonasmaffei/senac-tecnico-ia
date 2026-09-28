# ⚡ Aula 21 — Implementação do Modelo

**Objetivo:** implementar o treino com as otimizações de GPU que mais impactam — **mixed
precision (AMP)** e **DataLoader otimizado** — e validar o ganho frente ao baseline.

> 🧭 **Bloco 4 — Projeto Final.** Continua a [Aula 20](../aula20/README.md).

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula21.html`](apresentacao_aula21.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`scripts/treino_otimizado.py`](scripts/treino_otimizado.py) | Exemplo de época com AMP |
| [`atividade.md`](atividade.md) | Roteiro e tarefa de casa |

---

## 🚀 Como usar

```bash
cd aulas/bloco4/aula21/scripts
python treino_otimizado.py
```

---

## 🔑 Conceitos-chave

- **Mixed precision (AMP)** — `autocast` + `GradScaler`: ~2× mais rápido, ~45% menos VRAM.
- **DataLoader otimizado** — `num_workers` + `pin_memory`.
- **`set_to_none=True`** — libera os gradientes em vez de zerá-los.
- **Gradient accumulation** — batch efetivo maior sem estourar a VRAM.

---

## 📌 Tarefa de casa (para a Aula 22)

1. Treinar pelo menos **10 épocas** com AMP e logging.
2. Comparar o throughput (imgs/s) com e sem AMP.
