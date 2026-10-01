# 📚 Aulas — Introdução a Arquitetura de Computadores

Esta pasta reúne o material das aulas do curso, **agrupadas por bloco**. Cada bloco tem o seu
próprio índice e as aulas ficam em subpastas `aulaNN/`.

> 🧭 **Percurso:** [Bloco 1](#-bloco-1--fundamentos) → [Bloco 2](#-bloco-2--programação-gpu) →
> [Bloco 3](#-bloco-3--automação) → [Bloco 4](#-bloco-4--projeto-final)

---

## 🗂️ Visão geral

```
aulas/
├── README.md                 ← este arquivo (índice geral)
├── bloco1/                   Bloco 1 · Fundamentos            (aulas 01–06)
├── bloco2/                   Bloco 2 · Programação GPU        (aulas 07–13)
├── bloco3/                   Bloco 3 · Automação              (aulas 14–19)
├── bloco4/                   Bloco 4 · Projeto Final          (aulas 20–24)
├── bloco4-teorico/           Bloco 4 · Pesquisa (sem código)  (aulas 21–22)
└── projeto-integrador/       Trabalho de pesquisa da UC
```

Cada aula (`aulaNN/`) segue o padrão: `apresentacao_aulaNN.html`, `README.md`, `atividade.md` e,
quando há material prático, `notebook_colab/` (com 5 exercícios) e/ou `laboratorio_windows/`,
`scripts/` ou `scripts_linux/`. As aulas do **Bloco 4** (Projeto Final) são mais enxutas: um
script de exemplo por aula.

---

## 🧱 Bloco 1 — Fundamentos

| Aula | Tema |
| :---: | :--- |
| **01** | Introdução às Arquiteturas de Computadores e GPUs (Von Neumann/Harvard, CPU vs GPU) |
| **02** | Modelos de Processamento (SIMD/MIMD, RISC/CISC) |
| **03** | Estrutura de Memória em GPUs (hierarquia, RAM vs VRAM, PCIe) |
| **04** | Fundamentos de Processos e Threads (GIL, warps/blocos/grade) |
| **05** | Protocolos de Redes e Interação com GPUs (IPv4/IPv6, TCP/UDP, SSH, rsync) |
| **06** | Sistemas Operacionais Linux e GPU (/proc, /sys, drivers, cron, systemd) |

📑 Índice completo: [`bloco1/README.md`](bloco1/README.md)

## 🧱 Bloco 2 — Programação GPU

| Aula | Tema |
| :---: | :--- |
| **07** | Introdução ao Modelo CUDA (kernels, índice global, CuPy FFT) |
| **08** | Manipulação de Memória em CUDA (tiling, coalescing, profiling) |
| **09** | Alternativas ao CUDA: OpenCL (+ LLMs locais) |
| **10** | Introdução ao ROCm e GPUs AMD (HIP, PyTorch & Docker) |
| **11** | Aplicação de Modelos em GPUs NVIDIA e AMD (CNN, Mixed Precision/AMP, TCO) |
| **12** | Prática no Colab e Projeto Integrador |
| **13** | Implementação de um Modelo Paralelo Simples (síntese do bloco) |

📑 Índice completo: [`bloco2/README.md`](bloco2/README.md)

## 🧱 Bloco 3 — Automação

| Aula | Tema |
| :---: | :--- |
| **14** | Introdução à Automação de GPUs com Bash (nvidia-smi, cron, gnuplot, Sheets) |
| **15** | Gestão de Processos e Carga de Trabalho (flock, filas com prioridade, systemd) |
| **16** | Agentes de Código: Harness, RAG, Skills e Vibe Coding (Antigravity CLI) |
| **17** | Introdução à Automação de GPUs com Bash (versão Python/cross-platform) |
| **18** | Gestão de Processos e Carga de Trabalho (versão Python/cross-platform) |
| **19** | Otimização de Processamento e Uso de Energia em GPUs (TDP, Power Limit, nvidia-ml-py) |

📑 Índice completo: [`bloco3/README.md`](bloco3/README.md)

## 🧱 Bloco 4 — Projeto Final

| Aula | Tema |
| :---: | :--- |
| **20** | Definição do Projeto Final (domínio, dataset, arquitetura, W&B) |
| **21** | Implementação do Modelo (AMP, checkpointing, accumulation, profiling) |
| **22** | Automação e Monitoramento do Projeto (subprocess, alertas, dashboard, systemd) |
| **23** | Apresentação e Análise dos Projetos (pitch, relatório, rubrica) |
| **24** | Conexão com o Projeto Integrador (mapeamento GPU, plano de ação) |

📑 Índice completo: [`bloco4/README.md`](bloco4/README.md)

## 🔬 Bloco 4 Teórico — Pesquisa Aplicada

Trilha **teórica / sem código** (**trabalho individual**), dois dias de aula, no estilo do Projeto Integrador. Cada aluno trabalha o **seu tema**; os 3 projetos de pesquisa de [`bloco4/projetos-exemplo/`](bloco4/projetos-exemplo/README.md) (4 — Saúde, 5 — Energia, 6 — Agricultura) servem de **exemplo de estrutura**:

| Aula | Tema |
| :---: | :--- |
| **21** | Método de Pesquisa e Fundamentação da Arquitetura |
| **22** | Análise Crítica, Relatório e Apresentação da Pesquisa |

📑 Índice completo: [`bloco4-teorico/README.md`](bloco4-teorico/README.md)

---

## 📋 Projeto Integrador

[`projeto-integrador/README.md`](projeto-integrador/README.md) — trabalho de **pesquisa**
aplicada que amarra a UC. **Não exige programação**; a aceleração por GPU (Bloco 4) é um
complemento opcional.

---

> 🔗 Voltar para o [README do repositório](../README.md) · Documentação em [`../docs/`](../docs).
