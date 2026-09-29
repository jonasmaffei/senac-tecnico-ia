# 💬 Projeto Exemplo 2 — Análise de Sentimentos

> **Domínio:** Processamento de Linguagem Natural · **Etapa do Bloco 4:** aula 20 a 24.

## 1. Planejar (Aula 20)

| Item | Definição |
| :--- | :--- |
| Problema | Classificar automaticamente comentários de clientes (positivo/negativo) |
| Dataset | IMDB (`imdb`) — 50k reviews |
| Modelo base | BERT pré-treinado (fine-tuning) |
| Framework | PyTorch + Transformers + CUDA |
| Métrica | F1-score |
| Baseline | Saco de palavras + regressão logística |
| Hardware | Colab Pro (V100) |

## 2. Implementar (Aula 21)

Mixed precision (AMP) + **gradient checkpointing** (BERT usa muita VRAM) e **gradient
accumulation** para batch efetivo maior.

## 3. Monitorar (Aula 22)

Monitor de GPU em CSV; o limite de VRAM é mais crítico aqui (usar ~90%).

## 4. Apresentar (Aula 23)

Pitch: Comparação:

| Métrica | CPU | GPU |
| :--- | :--- | :--- |
| Tempo por época | ~900 s | ~70 s |
| F1-score | ~78% | ~91% |

## 5. Conectar ao PI (Aula 24)

- Extração de entidades de contratos/documentos do PI.
- Inferência em lote de textos na GPU.

## ▶️ Executar

```bash
python projeto.py
```
