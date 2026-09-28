# 🧪 Projetos Exemplo — Bloco 4 (Projeto Final)

Três exemplos **completos** de projeto final, um por domínio, seguindo as 5 etapas das aulas
20 a 24. Cada projeto é um **script único** que roda **sem GPU** (modo de referência) e mostra:

1. **Planejar** (A20) — domínio, problema, dataset, modelo e métrica.
2. **Implementar** (A21) — pipeline de treino com mixed precision.
3. **Monitorar** (A22) — coleta de métricas da GPU.
4. **Apresentar** (A23) — comparação baseline × GPU.
5. **Conectar** (A24) — onde a GPU ajuda no Projeto Integrador.

| # | Domínio | Projeto | Dataset sugerido |
| :-: | :--- | :--- | :--- |
| 1 | Visão Computacional | [`1-visao-doencas-plantas/`](1-visao-doencas-plantas/README.md) | PlantVillage (38 classes) |
| 2 | PNL | [`2-pnl-sentimentos/`](2-pnl-sentimentos/README.md) | IMDB (sentimentos) |
| 3 | Séries Temporais | [`3-series-consumo-energia/`](3-series-consumo-energia/README.md) | ETT (consumo elétrico) |

## Como usar

```bash
cd aulas/bloco4/projetos-exemplo/1-visao-doencas-plantas
python projeto.py
```

Cada script imprime as 5 etapas e salva um gráfico do relatório (A23).
