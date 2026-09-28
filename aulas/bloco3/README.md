# 🧱 Bloco 3 — Automação e Monitoramento

> Este bloco agrupa as suas aulas em `aulas/bloco3/` — cada aula fica na sua subpasta (`aulaNN/`).

Depois de saber programar a GPU, o desafio passa a ser **operá-la com segurança**: monitorar
24h/7d, compartilhar entre vários jobs, controlar o consumo de energia e usar agentes de
código para acelerar o próprio trabalho de desenvolvimento.

| Aula | Tema | Recursos |
| :---: | :--- | :--- |
| **14** | Introdução à Automação de GPUs com Bash (nvidia-smi, cron, gnuplot, Sheets) | [Guia](aula14/README.md) · [Apresentação](aula14/apresentacao_aula14.html) · [Notebook](aula14/notebook_colab/aula14_automacao_gpu_bash.ipynb) · [Atividade](aula14/atividade.md) · [Laboratório Windows](aula14/laboratorio_windows/README.md) |
| **15** | Gestão de Processos e Carga de Trabalho (flock, filas com prioridade, systemd) | [Guia](aula15/README.md) · [Apresentação](aula15/apresentacao_aula15.html) · [Notebook](aula15/notebook_colab/aula15_processos_fila.ipynb) · [Atividade](aula15/atividade.md) · [Laboratório Windows](aula15/laboratorio_windows/README.md) |
| **16** | Agentes de Código: Harness, RAG, Skills e Vibe Coding (Antigravity CLI) | [Guia](aula16/README.md) · [Apresentação](aula16/apresentacao_aula16.html) · [Atividade](aula16/atividade.md) · [Laboratório Monitoramento](aula16/laboratorio_monitoramento/README.md) |
| **17** | Introdução à Automação de GPUs com Bash (versão Python/cross-platform) | [Guia](aula17/README.md) · [Apresentação](aula17/apresentacao_aula17.html) · [Notebook](aula17/notebook_colab/aula17_automacao_gpu_bash.ipynb) · [Atividade](aula17/atividade.md) · [Laboratório Windows](aula17/laboratorio_windows/README.md) |
| **18** | Gestão de Processos e Carga de Trabalho (versão Python/cross-platform) | [Guia](aula18/README.md) · [Apresentação](aula18/apresentacao_aula18.html) · [Notebook](aula18/notebook_colab/aula18_processos_fila.ipynb) · [Atividade](aula18/atividade.md) · [Laboratório Windows](aula18/laboratorio_windows/README.md) |
| **19** | Otimização de Processamento e Uso de Energia em GPUs (TDP, Power Limit, nvidia-ml-py) | [Guia](aula19/README.md) · [Apresentação](aula19/apresentacao_aula19.html) · [Notebook](aula19/notebook_colab/aula19_energia_gpu.ipynb) · [Atividade](aula19/atividade.md) · [Laboratório Windows](aula19/laboratorio_windows/README.md) |

---

## 🧭 Fio condutor do bloco

```
telemetria (A14) → concorrência (A15) → agentes (A16) → telemetria em Python (A17)
→ concorrência em Python (A18) → energia (A19)
```

> ℹ️ **Nota didática:** as aulas **17 e 18** revisitam os temas de **14 e 15** numa
> implementação alternativa (Python cross-platform, sem depender de `flock`/`systemd` do
> Linux). As duas abordagens têm conteúdo próprio — recomenda-se ver a versão Bash primeiro
> e a versão Python depois.

**Bloco anterior:** [Bloco 2 — Programação](../bloco2/README.md) ·
**Próximo bloco:** [Bloco 4 — Projeto Final](../bloco4/README.md).
