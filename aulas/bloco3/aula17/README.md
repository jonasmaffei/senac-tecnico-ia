# 🤖 Aula 17 — Introdução à Automação de GPUs com Bash

**Objetivo:** automatizar o monitoramento de GPUs usando scripts Bash com `nvidia-smi`, agendando a coleta de métricas via `cron`/`systemd`, gerando dashboards com `gnuplot`/`matplotlib` e integrando com a Google Sheets API para garantir operação contínua 24h/7d em ambientes de IA.

---

## 🎯 Situação de Aprendizagem

O servidor de treinamento da empresa ficou travado durante a madrugada — a GPU atingiu **95°C** e o job falhou silenciosamente. Ninguém percebeu até a manhã seguinte. O time precisa de um sistema de monitoramento automático **24h/7d** que colete métricas a cada 5 segundos, salve em CSV, gere alertas de temperatura e publique um dashboard diário no Google Sheets — tudo via scripts Bash agendados com `cron`.

---

## 🗂️ Conteúdo da Aula

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula17.html`](apresentacao_aula17.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`atividade.md`](atividade.md) | Roteiro prático, tópicos de discussão em grupo e tarefa de casa |
| [`notebook_colab/aula17_automacao_gpu_bash.ipynb`](notebook_colab/aula17_automacao_gpu_bash.ipynb) | Notebook Google Colab com 5 exercícios práticos |
| [`laboratorio_windows/`](laboratorio_windows/) | Laboratório local para executar no host Windows via `iniciar.bat` |
| [`scripts_linux/`](scripts_linux/) | Scripts Bash e Python para servidores Linux (`monitor_gpu.sh`, `alerta_gpu.sh`, `gerar_graficos.sh`, `enviar_para_sheets.py`) |

---

## 🗂️ Estrutura da Pasta

```
aula17/
├── apresentacao_aula17.html
├── README.md
├── atividade.md
├── notebook_colab/
│   └── aula17_automacao_gpu_bash.ipynb
├── laboratorio_windows/
│   ├── 1_monitor_gpu.py
│   ├── 2_alerta_gpu.py
│   ├── 3_gerar_graficos.py
│   ├── 4_enviar_sheets.py
│   ├── iniciar.bat
│   ├── requirements.txt
│   └── README.md
└── scripts_linux/
    ├── alerta_gpu.sh
    ├── enviar_para_sheets.py
    ├── gerar_graficos.sh
    └── monitor_gpu.sh
```

---

## 🚀 Como Usar

### Option A — No Google Colab
Abra o notebook em [`notebook_colab/aula17_automacao_gpu_bash.ipynb`](notebook_colab/aula17_automacao_gpu_bash.ipynb), execute a demonstração e resolva a seção **7. Exercícios Práticos (5)**.

### Option B — No Windows Host (Local)
Navegue até a pasta `laboratorio_windows/` e dê duplo clique no arquivo `iniciar.bat`. O script criará o ambiente `.venv`, instalará as dependências e abrirá o menu interativo de execução.

---

## 🔑 Conceitos-chave

- **`nvidia-smi --query-gpu`** — Padrão da indústria para extração de métricas de GPU em formato CSV limpo.
- **Limiares de Alerta (Thresholds)** — Monitoria de temperatura (°C) e utilização (%) para prevenir *thermal throttling*.
- **Agendadores (cron / systemd timers)** — Garantia de execução recorrente autônoma 24h/7d.
- **Dashboards Visuais** — Geração de relatórios com 4 gráficos via `gnuplot` / `matplotlib`.
- **Integração Cloud** — Publicação de métricas na Google Sheets API para acompanhamento remoto.
