# 🧠 Introdução a Arquitetura de Computadores

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-yellow.svg)](https://www.python.org/)
[![CUDA](https://img.shields.io/badge/CUDA-12.x-green.svg)](https://developer.nvidia.com/cuda-toolkit)
[![ROCm](https://img.shields.io/badge/ROCm-6.x-red.svg)](https://www.amd.com/en/products/software/rocm.html)

Repositório estruturado por aulas para o curso técnico de IA do Senac, cobrindo desde arquitetura de computadores e hierarquia de memória até programação CUDA, benchmarking comparativo CUDA vs ROCm e deploy de LLMs locais.

Cada aula resolve o gargalo que a anterior deixou em aberto, formando uma cadeia causal completa:

```
Silício → Modelos de Execução → Memória → Processos → Redes → Linux → CUDA → Tiling → OpenCL/LLMs → ROCm/AMD → Aplicação & Métricas → Automação → Agentes → Orquestração
```

---

## 📋 O que é usado ao longo do curso

Tudo abaixo é **opcional** (o Colab já traz a maior parte):

| Recurso | Quando aparece |
| :--- | :--- |
| **NumPy** | Todas as aulas (vetorização/SIMD) |
| **PyTorch** | Aulas 1–3 (detecção de hardware/fallback), 10 e 11 (portabilidade ROCm, treino) |
| **CuPy** | Aulas 7, 8 e 13 (FFT, benchmark e síntese do bloco) |
| **Numba** | Aulas 3, 4, 7, 8 e 13 (kernels CUDA, tiling e redução) |
| **PyOpenCL** | Aula 9 (kernels multiplataforma) |
| **psutil** | Aulas 1, 3, 4, 6, 14, 17 e 18 (monitoramento de hardware e processos) |
| **GPU NVIDIA / AMD** | Recomendada para Aulas 3, 7, 8, 9, 10, 11, 12 e 13 (há fallback para CPU) |
| **Docker / WSL 2** | Aulas 10 e 14 (AMD ROCm / PyTorch e Open WebUI/Ollama) |
| **Google Sheets API** | Aulas 14 e 17 (telemetria de GPU para planilha) |
| **nvidia-ml-py / NVML** | Aula 19 (controle programático de energia e temperatura) |
| **Agentes de código / Bash** | Aulas 16, 17 e 18 (Antigravity CLI, automação e filas) |

---

## 🚀 Como executar

**O ambiente principal do curso é o Google Colab** — não é preciso instalar nada para
acompanhar as aulas. Abra o notebook da aula e ative a GPU em
*Runtime ➔ Change runtime type ➔ T4 GPU*.

> 💡 **Sem GPU?** Os notebooks e scripts detectam a ausência dela e entram em **modo
> simulado** (ou usam o SIMD da própria CPU), então a aula continua funcionando.

Para rodar **localmente** (ex.: laboratório Windows com GPU AMD), instale apenas o que a
aula pede — em geral só o NumPy:

```bash
pip install numpy
```

O arquivo [`requirements.txt`](requirements.txt) é opcional e reúne tudo o que o curso
usa ao longo das aulas (incluindo `torch`, `numba` e clientes do Google). Instale-o só
se quiser o ambiente completo:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

> **Nota sobre GPU:** `torch` com CUDA e `cupy` exigem instalação específica para o seu
> driver — veja [pytorch.org/get-started](https://pytorch.org/get-started). Sem isso, os
> scripts usam o fallback (CPU/NumPy).

---

## 📚 Índice das Aulas

> 📂 Visão geral da pasta: [`aulas/README.md`](aulas/README.md). Cada bloco também tem um **índice próprio**: [Bloco 1](aulas/bloco1/README.md) · [Bloco 2](aulas/bloco2/README.md) · [Bloco 3](aulas/bloco3/README.md) · [Bloco 4](aulas/bloco4/README.md).

### Bloco 1 — Fundamentos de Hardware e Infraestrutura

> 📑 [Índice do Bloco 1](aulas/bloco1/README.md)

| Aula | Tema | Scripts / Recursos |
| :---: | :--- | :--- |
| **01** | Introdução às Arquiteturas de Computadores e GPUs (Von Neumann/Harvard, CPU vs GPU) | [Notebook](aulas/bloco1/aula01/notebook_colab/aula01_arquiteturas_cpu_gpu.ipynb), [Apresentação](aulas/bloco1/aula01/apresentacao_aula01.html), [Atividade](aulas/bloco1/aula01/atividade.md), [Laboratório Windows](aulas/bloco1/aula01/laboratorio_windows/README.md), [Guia da Aula](aulas/bloco1/aula01/README.md) |
| **02** | Modelos de Processamento (SIMD/MIMD, RISC/CISC) | [Notebook](aulas/bloco1/aula02/notebook_colab/aula02_modelos_processamento.ipynb), [Apresentação](aulas/bloco1/aula02/apresentacao_aula02.html), [Atividade](aulas/bloco1/aula02/atividade.md), [Laboratório Windows](aulas/bloco1/aula02/laboratorio_windows/README.md), [`scripts/lib_backend.py`](aulas/bloco1/aula02/scripts/lib_backend.py), [Guia da Aula](aulas/bloco1/aula02/README.md) |
| **03** | Estrutura de Memória em GPUs (Hierarquia, RAM vs VRAM, PCIe) | [Notebook](aulas/bloco1/aula03/notebook_colab/aula03_memoria_gpu.ipynb), [Apresentação](aulas/bloco1/aula03/apresentacao_aula03.html), [Atividade](aulas/bloco1/aula03/atividade.md), [Laboratório Windows](aulas/bloco1/aula03/laboratorio_windows/README.md), [Guia da Aula](aulas/bloco1/aula03/README.md) |
| **04** | Fundamentos de Processos e Threads (GIL, warps/blocos/grade) | [Notebook](aulas/bloco1/aula04/notebook_colab/aula04_processos_threads.ipynb), [Apresentação](aulas/bloco1/aula04/apresentacao_aula04.html), [Atividade](aulas/bloco1/aula04/atividade.md), [Laboratório Windows](aulas/bloco1/aula04/laboratorio_windows/README.md), [Guia da Aula](aulas/bloco1/aula04/README.md) |
| **05** | Protocolos de Redes e Interação com GPUs (IPv4/IPv6, TCP/UDP, SSH, rsync) | [Notebook](aulas/bloco1/aula05/notebook_colab/aula05_redes.ipynb), [Apresentação](aulas/bloco1/aula05/apresentacao_aula05.html), [Atividade](aulas/bloco1/aula05/atividade.md), [Laboratório Windows](aulas/bloco1/aula05/laboratorio_windows/README.md), [Guia da Aula](aulas/bloco1/aula05/README.md) |
| **06** | Sistemas Operacionais Linux e GPU (/proc, /sys, drivers, cron, systemd) | [Notebook](aulas/bloco1/aula06/notebook_colab/aula06_linux_gpu.ipynb), [Apresentação](aulas/bloco1/aula06/apresentacao_aula06.html), [Atividade](aulas/bloco1/aula06/atividade.md), [Laboratório Windows](aulas/bloco1/aula06/laboratorio_windows/README.md), [`scripts/`](aulas/bloco1/aula06/scripts) ([`gpu_status.sh`](aulas/bloco1/aula06/scripts/gpu_status.sh), [`cron_exemplos.sh`](aulas/bloco1/aula06/scripts/cron_exemplos.sh), [`gpu-monitor.service`](aulas/bloco1/aula06/scripts/gpu-monitor.service)), [Guia da Aula](aulas/bloco1/aula06/README.md) |

### Bloco 2 — Programação, Otimização e Computação Heterogênea

> 📑 [Índice do Bloco 2](aulas/bloco2/README.md)

| Aula | Tema | Scripts / Recursos |
| :---: | :--- | :--- |
| **07** | Introdução ao Modelo CUDA (Kernels, índice global, CuPy FFT) | [Notebook](aulas/bloco2/aula07/notebook_colab/aula07_cuda.ipynb), [Apresentação](aulas/bloco2/aula07/apresentacao_aula07.html), [Atividade](aulas/bloco2/aula07/atividade.md), [`scripts/`](aulas/bloco2/aula07/scripts) ([`indice_global.py`](aulas/bloco2/aula07/scripts/indice_global.py), [`primeiro_kernel.py`](aulas/bloco2/aula07/scripts/primeiro_kernel.py), [`fft_benchmark.py`](aulas/bloco2/aula07/scripts/fft_benchmark.py)), [Guia da Aula](aulas/bloco2/aula07/README.md) |
| **08** | Manipulação de Memória em CUDA (Tiling, Coalescing, Profiling) | [Notebook](aulas/bloco2/aula08/notebook_colab/aula08_tiling.ipynb), [Apresentação](aulas/bloco2/aula08/apresentacao_aula08.html), [Atividade](aulas/bloco2/aula08/atividade.md), [`scripts/`](aulas/bloco2/aula08/scripts) ([`matmul_tiling.py`](aulas/bloco2/aula08/scripts/matmul_tiling.py), [`matmul_global.py`](aulas/bloco2/aula08/scripts/matmul_global.py), [`coalescing.py`](aulas/bloco2/aula08/scripts/coalescing.py), [`profiling_ocupacao.py`](aulas/bloco2/aula08/scripts/profiling_ocupacao.py)), [Guia da Aula](aulas/bloco2/aula08/README.md) |
| **09** | Alternativas ao CUDA: OpenCL (+ LLMs locais) | [Notebook](aulas/bloco2/aula09/notebook_colab/aula09_opencl.ipynb), [Apresentação](aulas/bloco2/aula09/apresentacao_aula09.html), [Atividade](aulas/bloco2/aula09/atividade.md), [Laboratório Windows](aulas/bloco2/aula09/laboratorio_windows/README.md), [Tutoriais Ollama/WebUI](aulas/bloco2/aula09/tutorials), [Guia da Aula](aulas/bloco2/aula09/README.md) |
| **10** | Introdução ao ROCm e GPUs AMD (HIP, PyTorch & Docker) | [Notebook](aulas/bloco2/aula10/notebook_colab/aula10_rocm.ipynb), [Apresentação](aulas/bloco2/aula10/apresentacao_aula10.html), [Atividade](aulas/bloco2/aula10/atividade.md), [Laboratório Windows](aulas/bloco2/aula10/laboratorio_windows/README.md), [Lab ROCm/Docker](aulas/bloco2/aula10/laboratorio_rocm-docker/README.md), [Guia da Aula](aulas/bloco2/aula10/README.md) |
| **11** | Aplicação de Modelos em GPUs NVIDIA e AMD (CNN, Mixed Precision/AMP, TCO) | [Notebook](aulas/bloco2/aula11/notebook_colab/aula11_aplicacao_modelos.ipynb), [Apresentação](aulas/bloco2/aula11/apresentacao_aula11.html), [Atividade](aulas/bloco2/aula11/atividade.md), [Laboratório Windows](aulas/bloco2/aula11/laboratorio_windows/README.md), [Guia da Aula](aulas/bloco2/aula11/README.md) |
| **12** | Laboratório Prático e Revisão Interativa (5 experimentos) | [Notebook](aulas/bloco2/aula12/notebook_colab/aula12_pratica_colab.ipynb), [Apresentação](aulas/bloco2/aula12/apresentacao_aula12.html), [Atividade](aulas/bloco2/aula12/atividade.md), [Guia da Aula](aulas/bloco2/aula12/README.md), [Projeto Integrador](aulas/projeto-integrador/README.md) |
| **13** | Implementação de um Modelo Paralelo Simples (Síntese Bloco 2) | [Notebook](aulas/bloco2/aula13/notebook_colab/aula13_implementacao_modelo_paralelo.ipynb), [Apresentação](aulas/bloco2/aula13/apresentacao_aula13.html), [Atividade](aulas/bloco2/aula13/atividade.md), [Guia da Aula](aulas/bloco2/aula13/README.md) |

### Bloco 3 — Automação

> 📑 [Índice do Bloco 3](aulas/bloco3/README.md)

| Aula | Tema | Scripts / Recursos |
| :---: | :--- | :--- |
| **14** | Introdução à Automação de GPUs com Bash (nvidia-smi, cron, gnuplot, Sheets) | [Notebook](aulas/bloco3/aula14/notebook_colab/aula14_automacao_gpu_bash.ipynb), [Apresentação](aulas/bloco3/aula14/apresentacao_aula14.html), [Atividade](aulas/bloco3/aula14/atividade.md), [Scripts Linux](aulas/bloco3/aula14/scripts_linux/) ([`monitor_gpu.sh`](aulas/bloco3/aula14/scripts_linux/monitor_gpu.sh), [`alerta_gpu.sh`](aulas/bloco3/aula14/scripts_linux/alerta_gpu.sh), [`gerar_graficos.sh`](aulas/bloco3/aula14/scripts_linux/gerar_graficos.sh), [`enviar_para_sheets.py`](aulas/bloco3/aula14/scripts_linux/enviar_para_sheets.py)), [Laboratório Windows (AMD)](aulas/bloco3/aula14/laboratorio_windows/README.md), [Realtime Docker](aulas/bloco3/aula14/laboratorio_realtime-docker/README.md), [Realtime Windows](aulas/bloco3/aula14/laboratorio_realtime-windows/README.md), [Guia da Aula](aulas/bloco3/aula14/README.md) |
| **15** | Gestão de Processos e Carga de Trabalho (flock, filas com prioridade, systemd) | [Notebook](aulas/bloco3/aula15/notebook_colab/aula15_processos_fila.ipynb), [Apresentação](aulas/bloco3/aula15/apresentacao_aula15.html), [Atividade](aulas/bloco3/aula15/atividade.md), [Laboratório Windows](aulas/bloco3/aula15/laboratorio_windows/README.md), [Guia da Aula](aulas/bloco3/aula15/README.md) |
| **16** | Agentes de Código: Harness, RAG, Skills e Vibe Coding (Antigravity CLI) | [Apresentação](aulas/bloco3/aula16/apresentacao_aula16.html), [Atividade](aulas/bloco3/aula16/atividade.md), [Laboratório Monitoramento](aulas/bloco3/aula16/laboratorio_monitoramento/README.md), [Guia da Aula](aulas/bloco3/aula16/README.md) |
| **17** | Automação de GPUs — *versão enxuta / complemento da A14* | [Notebook](aulas/bloco3/aula17/notebook_colab/aula17_automacao_gpu_bash.ipynb), [Apresentação](aulas/bloco3/aula17/apresentacao_aula17.html), [Atividade](aulas/bloco3/aula17/atividade.md), [Laboratório Python](aulas/bloco3/aula17/laboratorio_windows/README.md), [Guia da Aula](aulas/bloco3/aula17/README.md) |
| **18+19** | **Concorrência + Energia na GPU** (aula dupla, 1 noite) | [Guia](aulas/bloco3/aula18_19_dupla/README.md), [Apresentação](aulas/bloco3/aula18_19_dupla/apresentacao_aula18_19.html), [Notebook](aulas/bloco3/aula18_19_dupla/notebook_colab/aula18_19_concorrencia_energia.ipynb), [Atividade](aulas/bloco3/aula18_19_dupla/atividade.md), [Lab concorrência](aulas/bloco3/aula18_19_dupla/laboratorio_concorrencia/README.md), [Lab energia](aulas/bloco3/aula18_19_dupla/laboratorio_energia/README.md), [Scripts Linux](aulas/bloco3/aula18_19_dupla/scripts_linux/) |

### Bloco 4 — Projeto Final (Aplicação de GPUs na IA)

> 📑 [Índice do Bloco 4](aulas/bloco4/README.md)

| Aula | Tema | Scripts / Recursos |
| :---: | :--- | :--- |
| **20** | Definição do Projeto Final (domínio, dataset, arquitetura) | [Apresentação](aulas/bloco4/aula20/apresentacao_aula20.html), [Atividade](aulas/bloco4/aula20/atividade.md), [Script](aulas/bloco4/aula20/scripts/projeto_exemplo.py), [Guia da Aula](aulas/bloco4/aula20/README.md) |
| **21** | Implementação do Modelo (AMP, DataLoader) | [Apresentação](aulas/bloco4/aula21/apresentacao_aula21.html), [Atividade](aulas/bloco4/aula21/atividade.md), [Script](aulas/bloco4/aula21/scripts/treino_otimizado.py), [Guia da Aula](aulas/bloco4/aula21/README.md) |
| **22** | Automação e Monitoramento (monitor de GPU em CSV) | [Apresentação](aulas/bloco4/aula22/apresentacao_aula22.html), [Atividade](aulas/bloco4/aula22/atividade.md), [Script](aulas/bloco4/aula22/scripts/monitor_treinamento.sh), [Guia da Aula](aulas/bloco4/aula22/README.md) |
| **23** | Apresentação e Análise dos Projetos (pitch, relatório) | [Apresentação](aulas/bloco4/aula23/apresentacao_aula23.html), [Atividade](aulas/bloco4/aula23/atividade.md), [Script](aulas/bloco4/aula23/scripts/relatorio_final.py), [Guia da Aula](aulas/bloco4/aula23/README.md) |
| **24** | Conexão com o Projeto Integrador (mapeamento GPU) | [Apresentação](aulas/bloco4/aula24/apresentacao_aula24.html), [Atividade](aulas/bloco4/aula24/atividade.md), [Script](aulas/bloco4/aula24/scripts/mapear_conexoes_pi.py), [Guia da Aula](aulas/bloco4/aula24/README.md), [Projeto Integrador](aulas/projeto-integrador/README.md) |

---


## 📖 Documentação


| Sequência | Documento | Descrição |
| :---: | :--- | :--- |
| **01** | [`01_timeline-engenharia.md`](docs/01_timeline-engenharia.md) | Blueprint causal de engenharia: por que cada aula existe e como se conectam |
| **02** | [`02_resumos.md`](docs/02_resumos.md) | Resumos teóricos consolidados de todas as aulas (Aulas 1 a 24) |
| **03** | [`03_git.md`](docs/03_git.md) | Guia completo de Git e GitHub: configuração de usuário/e-mail, criação de repositórios na UI e envio de projetos |
| **05** | [`05_materiais-complementares.md`](docs/05_materiais-complementares.md) | Curadoria de links, playlists e cursos externos |
| **06** | [`06_tutorial-instalacao-wsl.md`](docs/06_tutorial-instalacao-wsl.md) | Guia de instalação e configuração do WSL 2 no Windows 10 e 11 |
| **07** | [`07_tutorial-instalacao-docker-wsl.md`](docs/07_tutorial-instalacao-docker-wsl.md) | Guia de instalação e uso do Docker Engine nativo no WSL 2 (Ubuntu) |
| **08** | [`08_tutorial-google-sheets-api-gpu.md`](docs/08_tutorial-google-sheets-api-gpu.md) | Guia de configuração da Google Sheets API e Service Account para telemetria de GPU |

---


## 📝 Questionários

Os questionários de revisão ficam na pasta [`questionarios/`](questionarios/README.md), organizados por fase:

| Fase | Período | Questões | Entrega |
| :---: | :--- | :---: | :--- |
| **1** | Aulas 1 a 7 | 21 | Já respondido em sala |
| **2** | Aulas 8 a 13 | 18 | Por e-mail para `03049691093@senacrs.edu.br` — assunto `Questionario aulas 8 a 13` |

---

## 🗂️ Estrutura do Repositório

```
senac-tecnico-ia/
├── README.md
├── requirements.txt
├── .gitignore
├── aulas/
│   ├── README.md                            → índice geral da pasta de aulas
│   ├── bloco1/                              → Bloco 1 · Fundamentos (aulas 01–06)
│   │   ├── README.md                        → índice do bloco
│   │   ├── aula01/ ... aula06/              → cada aula: apresentacao_*.html, README.md,
│   │   │                                      notebook_colab/, atividade.md, laboratorio_windows/
│   ├── bloco2/                              → Bloco 2 · Programação GPU (aulas 07–13)
│   │   ├── README.md
│   │   └── aula07/ ... aula13/              → apresentacao_*.html, README.md, notebook_colab/,
│   │                                          atividade.md, laboratorio_windows/ ou scripts/
│   ├── bloco3/                              → Bloco 3 · Automação (aulas 14–19)
│   │   ├── README.md
│   │   ├── aula14/ ... aula17/              → notebook_colab/, laboratorio_windows/, scripts_linux/
│   │   └── aula18_19_dupla/                 → concorrência + energia: notebook, labs e scripts_linux
│   ├── bloco4/                              → Bloco 4 · Projeto Final (aulas 20–24)
│   │   ├── README.md
│   │   ├── aula20/ ... aula24/              → apresentação, atividade e 1 script de exemplo
│   │   └── projetos-exemplo/                → 6 exemplos (3 de código + 3 de pesquisa)
│   └── projeto-integrador/
│       └── README.md                        → pesquisa (não exige código)
├── questionarios/
│   ├── README.md                              → Índice e regras de entrega
│   ├── questionario-aulas-1-7.md              → Fase 1 (já respondida em sala)
│   ├── gabarito-questionario-aulas-1-7.md     → Gabarito da Fase 1
│   └── questionario-aulas-8-13.md             → Fase 2 (entrega por e-mail)
└── docs/
    ├── 01_timeline-engenharia.md            → Blueprint causal do curso
    ├── 02_resumos.md                        → Resumos teóricos consolidados
    ├── 03_git.md                            → Guia de clonar o repo e atualizar com pull
    ├── 05_materiais-complementares.md       → Links e leituras recomendadas
    ├── 06_tutorial-instalacao-wsl.md        → Guia de instalação do WSL no Windows 10/11
    ├── 07_tutorial-instalacao-docker-wsl.md → Guia de instalação do Docker no WSL 2 Ubuntu
    └── 08_tutorial-google-sheets-api-gpu.md → Guia de configuração da Google Sheets API e Service Account
```

