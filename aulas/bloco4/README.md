# 🧱 Bloco 4 — Projeto Final: Aplicação de GPUs na IA

> Este bloco agrupa as suas aulas em `aulas/bloco4/` — cada aula fica na sua subpasta (`aulaNN/`).

O bloco de fechamento é um **hackathon interno**: em 4 semanas, cada time planeja,
implementa, monitora e apresenta uma solução de IA acelerada por GPU. A última aula conecta
tudo ao Projeto Integrador do curso.

| Aula | Tema | Recursos |
| :---: | :--- | :--- |
| **20** | Definição do Projeto Final (domínio, dataset, arquitetura) | [Guia](aula20/README.md) · [Apresentação](aula20/apresentacao_aula20.html) · [Atividade](aula20/atividade.md) · [Script](aula20/scripts/projeto_exemplo.py) |
| **21** | Implementação do Modelo (AMP, DataLoader) | [Guia](aula21/README.md) · [Apresentação](aula21/apresentacao_aula21.html) · [Atividade](aula21/atividade.md) · [Script](aula21/scripts/treino_otimizado.py) |
| **22** | Automação e Monitoramento (monitor de GPU em CSV) | [Guia](aula22/README.md) · [Apresentação](aula22/apresentacao_aula22.html) · [Atividade](aula22/atividade.md) · [Script](aula22/scripts/monitor_treinamento.sh) |
| **23** | Apresentação e Análise dos Projetos (pitch, relatório) | [Guia](aula23/README.md) · [Apresentação](aula23/apresentacao_aula23.html) · [Atividade](aula23/atividade.md) · [Script](aula23/scripts/relatorio_final.py) |
| **24** | Conexão com o Projeto Integrador (mapeamento GPU) | [Guia](aula24/README.md) · [Apresentação](aula24/apresentacao_aula24.html) · [Atividade](aula24/atividade.md) · [Script](aula24/scripts/mapear_conexoes_pi.py) |

---

## 🧭 Fio condutor do bloco

```
planejar (A20) → implementar (A21) → automatizar/monitorar (A22) → apresentar (A23) → conectar ao PI (A24)
```

> ℹ️ **Relação com o Projeto Integrador:** o [`projeto-integrador/`](../projeto-integrador/README.md)
> é uma **pesquisa** e **não exige programação**. O hackathon deste bloco é uma entrega
> **hands-on** (código, W&B, monitoramento, pitch). As duas **coexistem**: a Aula 24 conecta
> explicitamente os aprendizados de GPU à pesquisa do PI.

**Bloco anterior:** [Bloco 3 — Automação](../bloco3/README.md) ·
**Índice geral:** [README do repositório](../../README.md).

---

## 🧪 Projetos Exemplo

Três projetos **completos** (um por domínio) que percorrem as 5 etapas das aulas 20 a 24.
Cada um é um **script único que roda sem GPU** e imprime as etapas + gera o relatório:

| # | Domínio | Projeto | Dataset |
| :-: | :--- | :--- | :--- |
| 1 | Visão | [Detecção de Doenças em Plantas](projetos-exemplo/1-visao-doencas-plantas/README.md) | PlantVillage |
| 2 | PNL | [Análise de Sentimentos](projetos-exemplo/2-pnl-sentimentos/README.md) | IMDB |
| 3 | Séries Temporais | [Previsão de Consumo de Energia](projetos-exemplo/3-series-consumo-energia/README.md) | ETT |

```bash
cd aulas/bloco4/projetos-exemplo/1-visao-doencas-plantas
python projeto.py
```

As etapas que todos seguem:

| Etapa | O que fazer | Aula |
| :--- | :--- | :---: |
| **1. Planejar** | Domínio, problema, dataset, modelo e baseline | 20 |
| **2. Implementar** | Treinar com AMP (fp16) + DataLoader otimizado | 21 |
| **3. Monitorar** | Rodar o `monitor_treinamento.sh` junto do treino | 22 |
| **4. Apresentar** | Pitch de 5 min + relatório (baseline × GPU) | 23 |
| **5. Conectar** | Mapear onde a GPU ajuda no Projeto Integrador | 24 |

> 💡 Índice completo dos exemplos: [`projetos-exemplo/README.md`](projetos-exemplo/README.md).

---

**Bloco anterior:** [Bloco 3 — Automação](../bloco3/README.md) ·
**Índice geral:** [README do repositório](../../README.md).
