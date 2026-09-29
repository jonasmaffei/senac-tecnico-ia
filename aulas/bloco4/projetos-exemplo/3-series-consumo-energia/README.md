# 📈 Projeto Exemplo 3 — Previsão de Consumo de Energia

> **Domínio:** Séries Temporais · **Etapa do Bloco 4:** aula 20 a 24.

## 1. Planejar (Aula 20)

| Item | Definição |
| :--- | :--- |
| Problema | Prever o consumo elétrico das próximas horas (apoia a operação do data center) |
| Dataset | ETT (`ETDataset/ett`, ETTh1) — séries de consumo |
| Modelo base | LSTM (ou Transformer leve) |
| Framework | PyTorch + CUDA |
| Métrica | RMSE |
| Baseline | Média histórica / persistência |
| Hardware | Colab Pro (T4) |

## 2. Implementar (Aula 21)

Séries temporais usam **menos VRAM** e muitos *steps*: usar `persistent_workers=True` e
janela deslizante vetorizada. Mixed precision ainda ajuda.

## 3. Monitorar (Aula 22)

Monitor de GPU em CSV com intervalo maior (ex.: 20 s) — a carga é mais estável.

## 4. Apresentar (Aula 23)

Pitch: Comparação:

| Métrica | CPU | GPU |
| :--- | :--- | :--- |
| Tempo por época | ~180 s | ~12 s |
| RMSE | 0.92 | 0.41 |

## 5. Conectar ao PI (Aula 24)

- Previsão de consumo/falhas de equipamentos no PI.
- Detecção de anomalias em telemetria (sensores IoT) na GPU.

## ▶️ Executar

```bash
python projeto.py
```
