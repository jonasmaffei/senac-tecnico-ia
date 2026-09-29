# 🧱 Bloco 3 — Automação e Monitoramento

> Este bloco agrupa as suas aulas em `aulas/bloco3/` — cada aula fica na sua subpasta (`aulaNN/`).

Depois de saber programar a GPU, o desafio passa a ser **operá-la com segurança**: monitorar
24h/7d, compartilhar entre vários jobs, controlar o consumo de energia e usar agentes de
código para acelerar o próprio trabalho de desenvolvimento.

| Aula | Tema | Recursos |
| :---: | :--- | :--- |
| **14** | Automação de GPUs com Bash (nvidia-smi, cron, gnuplot, Sheets) | [Guia](aula14/README.md) · [Apresentação](aula14/apresentacao_aula14.html) · [Notebook](aula14/notebook_colab/aula14_automacao_gpu_bash.ipynb) · [Atividade](aula14/atividade.md) · [Laboratório Windows](aula14/laboratorio_windows/README.md) |
| **15** | Gestão de Processos e Carga de Trabalho (flock, filas com prioridade, systemd) | [Guia](aula15/README.md) · [Apresentação](aula15/apresentacao_aula15.html) · [Notebook](aula15/notebook_colab/aula15_processos_fila.ipynb) · [Atividade](aula15/atividade.md) · [Laboratório Windows](aula15/laboratorio_windows/README.md) |
| **16** | Agentes de Código: Harness, RAG, Skills e Vibe Coding (Antigravity CLI) | [Guia](aula16/README.md) · [Apresentação](aula16/apresentacao_aula16.html) · [Atividade](aula16/atividade.md) · [Laboratório Monitoramento](aula16/laboratorio_monitoramento/README.md) |
| **17** | Automação de GPUs — *versão enxuta / complemento da A14* | [Guia](aula17/README.md) · [Apresentação](aula17/apresentacao_aula17.html) · [Notebook](aula17/notebook_colab/aula17_automacao_gpu_bash.ipynb) · [Atividade](aula17/atividade.md) · [Laboratório Python](aula17/laboratorio_windows/README.md) |
| **18+19** | **Concorrência + Energia na GPU** (aula dupla, 1 noite) | [Guia](aula18_19_dupla/README.md) · [Apresentação](aula18_19_dupla/apresentacao_aula18_19.html) · [Notebook](aula18_19_dupla/notebook_colab/aula18_19_concorrencia_energia.ipynb) · [Lab concorrência](aula18_19_dupla/laboratorio_concorrencia/README.md) · [Lab energia](aula18_19_dupla/laboratorio_energia/README.md) · [Scripts Linux](aula18_19_dupla/scripts_linux) |

---

## 🧭 Fio condutor do bloco

```
telemetria (A14) → concorrência (A15) → agentes (A16)
      ↓ versão enxuta
   A17 (automação) ──► A18+19 (concorrência + energia)
```

> ℹ️ **Nota didática:** a **A17** é um complemento enxuto da A14. A **A18+19** é a aula
> oficial de **concorrência + energia**, reunindo apresentação, notebook e os **laboratórios**
> (concorrência e energia). A base conceitual de concorrência vem da **A15** (Bash).

**Bloco anterior:** [Bloco 2 — Programação](../bloco2/README.md) ·
**Próximo bloco:** [Bloco 4 — Projeto Final](../bloco4/README.md).
