# 🧱 Bloco 1 — Fundamentos de Arquitetura

> Este bloco agrupa as suas aulas em `aulas/bloco1/` — cada aula fica na sua subpasta (`aulaNN/`).

Este bloco constrói a base: como o hardware computa, onde os dados vivem e como a máquina
se comunica e é operada. É o alicerce que explica **por que** a GPU existe e **quando** ela
compensa.

| Aula | Tema | Recursos |
| :---: | :--- | :--- |
| **01** | Introdução às Arquiteturas de Computadores e GPUs (Von Neumann/Harvard, CPU vs GPU) | [Guia](aula01/README.md) · [Apresentação](aula01/apresentacao_aula01.html) · [Notebook](aula01/notebook_colab/aula01_arquiteturas_cpu_gpu.ipynb) · [Atividade](aula01/atividade.md) · [Laboratório Windows](aula01/laboratorio_windows/README.md) |
| **02** | Modelos de Processamento (SIMD/MIMD, RISC/CISC) | [Guia](aula02/README.md) · [Apresentação](aula02/apresentacao_aula02.html) · [Notebook](aula02/notebook_colab/aula02_modelos_processamento.ipynb) · [Atividade](aula02/atividade.md) · [Laboratório Windows](aula02/laboratorio_windows/README.md) |
| **03** | Estrutura de Memória em GPUs (hierarquia, RAM vs VRAM, PCIe) | [Guia](aula03/README.md) · [Apresentação](aula03/apresentacao_aula03.html) · [Notebook](aula03/notebook_colab/aula03_memoria_gpu.ipynb) · [Atividade](aula03/atividade.md) · [Laboratório Windows](aula03/laboratorio_windows/README.md) |
| **04** | Fundamentos de Processos e Threads (GIL, warps/blocos/grade) | [Guia](aula04/README.md) · [Apresentação](aula04/apresentacao_aula04.html) · [Notebook](aula04/notebook_colab/aula04_processos_threads.ipynb) · [Atividade](aula04/atividade.md) · [Laboratório Windows](aula04/laboratorio_windows/README.md) |
| **05** | Protocolos de Redes e Interação com GPUs (IPv4/IPv6, TCP/UDP, SSH, rsync) | [Guia](aula05/README.md) · [Apresentação](aula05/apresentacao_aula05.html) · [Notebook](aula05/notebook_colab/aula05_redes.ipynb) · [Atividade](aula05/atividade.md) · [Laboratório Windows](aula05/laboratorio_windows/README.md) |
| **06** | Sistemas Operacionais Linux e GPU (/proc, /sys, drivers, cron, systemd) | [Guia](aula06/README.md) · [Apresentação](aula06/apresentacao_aula06.html) · [Notebook](aula06/notebook_colab/aula06_linux_gpu.ipynb) · [Atividade](aula06/atividade.md) · [Laboratório Windows](aula06/laboratorio_windows/README.md) |

---

## 🧭 Fio condutor do bloco

```
silício → modelos de execução → memória → processos → redes → sistema operacional
```

Cada aula resolve o gargalo que a anterior deixa em aberto: a arquitetura impõe o modelo de
execução; o modelo esbarra na memória; a memória e o paralelismo exigem entender processos;
o processamento precisa de rede; e tudo isso é operado no Linux.

**Próximo bloco:** [Bloco 2 — Programação e Heterogeneidade](../bloco2/README.md).
