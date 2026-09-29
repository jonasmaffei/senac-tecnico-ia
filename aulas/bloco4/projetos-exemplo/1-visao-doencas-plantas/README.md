# 👁️ Projeto Exemplo 1 — Detecção de Doenças em Plantas

> **Domínio:** Visão Computacional · **Etapa do Bloco 4:** aula 20 a 24.

## 1. Planejar (Aula 20)

| Item | Definição |
| :--- | :--- |
| Problema | Identificar a doença da planta por foto, apoiando o diagnóstico precoce |
| Dataset | PlantVillage (`plants-village/PlantVillage`) — 38 classes |
| Modelo base | ResNet-18 pré-treinado (ImageNet) + camada final para 38 classes |
| Framework | PyTorch + CUDA |
| Métrica | Accuracy e F1-score |
| Baseline | Regressão logística sobre pixels reduzidos |
| Hardware | 2× RTX 4090 ou Colab Pro (T4/V100) |

## 2. Implementar (Aula 21)

Treino com **mixed precision (AMP)** e **DataLoader** otimizado; se o batch não couber na
VRAM, usar **gradient accumulation**.

## 3. Monitorar (Aula 22)

Rodar o `monitor_treinamento.sh` junto do treino (`logs/monitor/`) e alertar acima de 82 °C.

## 4. Apresentar (Aula 23)

Pitch: Problema → Solução → Demo → Resultados → Lições + PI. Comparação:

| Métrica | CPU | GPU |
| :--- | :--- | :--- |
| Tempo por época | ~320 s | ~38 s |
| Val Accuracy | ~71% | ~87% |

## 5. Conectar ao PI (Aula 24)

- Pré-processamento de imagens do PI acelerado com `torch` na GPU.
- Monitor de GPU integrado ao treino do PI.

## ▶️ Executar

```bash
python projeto.py
```
