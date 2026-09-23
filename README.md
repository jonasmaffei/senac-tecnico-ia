# 🧠 Introdução a Arquitetura de Computadores

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-yellow.svg)](https://www.python.org/)
[![CUDA](https://img.shields.io/badge/CUDA-12.x-green.svg)](https://developer.nvidia.com/cuda-toolkit)
[![ROCm](https://img.shields.io/badge/ROCm-6.x-red.svg)](https://www.amd.com/en/products/software/rocm.html)

Repositório estruturado por aulas para o curso técnico de IA do Senac, cobrindo desde arquitetura de computadores e hierarquia de memória até programação CUDA, benchmarking comparativo CUDA vs ROCm e deploy de LLMs locais.

Cada aula resolve o gargalo que a anterior deixou em aberto, formando uma cadeia causal completa:

```
Silício → Modelos de Execução → Memória → Processos → Redes → Linux → CUDA → Tiling → OpenCL/LLMs → ROCm/AMD → Aplicação & Métricas
```

---

## 📋 O que é usado ao longo do curso

Tudo abaixo é **opcional** (o Colab já traz a maior parte):

| Recurso | Quando aparece |
| :--- | :--- |
| **NumPy** | Todas as aulas (vetorização/SIMD) |
| **PyTorch** | Aulas 10, 11 e 13 (portabilidade, treino e benchmark) |
| **CuPy** | Aulas 7, 8 e 13 (FFT, estresse de GPU e benchmark) |
| **Numba** | Aulas 3, 4, 7, 8 e 13 (kernels CUDA e tiling) |
| **PyOpenCL** | Aula 9 (kernels multiplataforma) |
| **GPU NVIDIA / AMD** | Recomendada para Aulas 3, 7, 8, 9, 10, 11 e 13 (há fallback para CPU) |
| **Docker / WSL 2** | Aulas 10 e 14 (AMD ROCm / PyTorch e Open WebUI/Ollama) |

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

### Bloco 1 — Fundamentos de Hardware e Infraestrutura

| Aula | Tema | Scripts / Recursos |
| :---: | :--- | :--- |
| **01** | Introdução às Arquiteturas de Computadores e GPUs (Von Neumann/Harvard, CPU vs GPU) | [Notebook](aulas/aula01/notebook_colab/aula01_arquiteturas_cpu_gpu.ipynb), [Apresentação](aulas/aula01/apresentacao_aula01.html), [Atividade](aulas/aula01/atividade.md), [Laboratório Windows](aulas/aula01/laboratorio_windows/README.md), [Guia da Aula](aulas/aula01/README.md) |
| **02** | Modelos de Processamento (SIMD/MIMD, RISC/CISC) | [Notebook](aulas/aula02/notebook_colab/aula02_modelos_processamento.ipynb), [Apresentação](aulas/aula02/apresentacao_aula02.html), [Atividade](aulas/aula02/atividade.md), [Laboratório Windows](aulas/aula02/laboratorio_windows/README.md), [`scripts/lib_backend.py`](aulas/aula02/scripts/lib_backend.py), [Guia da Aula](aulas/aula02/README.md) |
| **03** | Estrutura de Memória em GPUs (Hierarquia, RAM vs VRAM, PCIe) | [Notebook](aulas/aula03/notebook_colab/aula03_memoria_gpu.ipynb), [Apresentação](aulas/aula03/apresentacao_aula03.html), [Atividade](aulas/aula03/atividade.md), [Laboratório Windows](aulas/aula03/laboratorio_windows/README.md), [Guia da Aula](aulas/aula03/README.md) |
| **04** | Fundamentos de Processos e Threads (GIL, warps/blocos/grade) | [Notebook](aulas/aula04/notebook_colab/aula04_processos_threads.ipynb), [Apresentação](aulas/aula04/apresentacao_aula04.html), [Atividade](aulas/aula04/atividade.md), [Laboratório Windows](aulas/aula04/laboratorio_windows/README.md), [Guia da Aula](aulas/aula04/README.md) |
| **05** | Protocolos de Redes e Interação com GPUs (IPv4/IPv6, TCP/UDP, SSH, rsync) | [Notebook](aulas/aula05/notebook_colab/aula05_redes.ipynb), [Apresentação](aulas/aula05/apresentacao_aula05.html), [Atividade](aulas/aula05/atividade.md), [Laboratório Windows](aulas/aula05/laboratorio_windows/README.md), [Guia da Aula](aulas/aula05/README.md) |
| **06** | Sistemas Operacionais Linux e GPU (/proc, /sys, drivers, cron, systemd) | [Notebook](aulas/aula06/notebook_colab/aula06_linux_gpu.ipynb), [Apresentação](aulas/aula06/apresentacao_aula06.html), [Atividade](aulas/aula06/atividade.md), [Laboratório Windows](aulas/aula06/laboratorio_windows/README.md), [`scripts/`](aulas/aula06/scripts) ([`gpu_status.sh`](aulas/aula06/scripts/gpu_status.sh), [`cron_exemplos.sh`](aulas/aula06/scripts/cron_exemplos.sh), [`gpu-monitor.service`](aulas/aula06/scripts/gpu-monitor.service)), [Guia da Aula](aulas/aula06/README.md) |

### Bloco 2 — Programação, Otimização e Computação Heterogênea

| Aula | Tema | Scripts / Recursos |
| :---: | :--- | :--- |
| **07** | Introdução ao Modelo CUDA (Kernels, índice global, CuPy FFT) | [Notebook](aulas/aula07/notebook_colab/aula07_cuda.ipynb), [Apresentação](aulas/aula07/apresentacao_aula07.html), [Atividade](aulas/aula07/atividade.md), [`scripts/`](aulas/aula07/scripts) ([`indice_global.py`](aulas/aula07/scripts/indice_global.py), [`primeiro_kernel.py`](aulas/aula07/scripts/primeiro_kernel.py), [`fft_benchmark.py`](aulas/aula07/scripts/fft_benchmark.py)), [Guia da Aula](aulas/aula07/README.md) |
| **08** | Manipulação de Memória em CUDA (Tiling, Coalescing, Profiling) | [Notebook](aulas/aula08/notebook_colab/aula08_tiling.ipynb), [Apresentação](aulas/aula08/apresentacao_aula08.html), [Atividade](aulas/aula08/atividade.md), [`scripts/`](aulas/aula08/scripts) ([`matmul_tiling.py`](aulas/aula08/scripts/matmul_tiling.py), [`matmul_global.py`](aulas/aula08/scripts/matmul_global.py), [`coalescing.py`](aulas/aula08/scripts/coalescing.py), [`profiling_ocupacao.py`](aulas/aula08/scripts/profiling_ocupacao.py)), [Guia da Aula](aulas/aula08/README.md) |
| **09** | Alternativas ao CUDA: OpenCL (+ LLMs locais) | [Notebook](aulas/aula09/notebook_colab/aula09_opencl.ipynb), [Apresentação](aulas/aula09/apresentacao_aula09.html), [Atividade](aulas/aula09/atividade.md), [Laboratório Windows](aulas/aula09/laboratorio_windows/README.md), [Tutoriais Ollama/WebUI](aulas/aula09/tutorials), [Guia da Aula](aulas/aula09/README.md) |
| **10** | Introdução ao ROCm e GPUs AMD (HIP, PyTorch & Docker) | [Notebook](aulas/aula10/notebook_colab/aula10_rocm.ipynb), [Apresentação](aulas/aula10/apresentacao_aula10.html), [Atividade](aulas/aula10/atividade.md), [Laboratório Windows](aulas/aula10/laboratorio_windows/README.md), [Lab ROCm/Docker](aulas/aula10/laboratorio_rocm-docker/README.md), [Guia da Aula](aulas/aula10/README.md) |
| **11** | Aplicação de Modelos em GPUs NVIDIA e AMD (CNN, Mixed Precision/AMP, TCO) | [`atividade_aula11.py`](aulas/aula11/atividade_aula11.py), [Guia da Aula](aulas/aula11/README.md) |
| **12** | Prática no Colab e Projeto Integrador | [`aula12_pratica_colab.ipynb`](aulas/aula12/aula12_pratica_colab.ipynb), [Guia Colab](aulas/aula12/README.md), [Projeto Integrador](aulas/projeto-integrador/README.md) |
| **13** | Implementação de um Modelo Paralelo Simples (Síntese Bloco 2) | [`aula13_implementacao_modelo_paralelo.ipynb`](aulas/aula13/aula13_implementacao_modelo_paralelo.ipynb), [Guia Colab](aulas/aula13/README.md) |

### Bloco 3 — Automação

| Aula | Tema | Scripts / Recursos |
| :---: | :--- | :--- |
| **14** | Introdução à Automação de GPUs com Bash (nvidia-smi, cron, gnuplot, Sheets) | [Notebook](aulas/aula14/notebook_colab/aula14_automacao_gpu_bash.ipynb), [Apresentação](aulas/aula14/apresentacao_aula14.html), [Atividade](aulas/aula14/atividade.md), [Scripts Linux](aulas/aula14/scripts_linux/) ([`monitor_gpu.sh`](aulas/aula14/scripts_linux/monitor_gpu.sh), [`alerta_gpu.sh`](aulas/aula14/scripts_linux/alerta_gpu.sh), [`gerar_graficos.sh`](aulas/aula14/scripts_linux/gerar_graficos.sh), [`enviar_para_sheets.py`](aulas/aula14/scripts_linux/enviar_para_sheets.py)), [Laboratório Windows (AMD)](aulas/aula14/laboratorio_windows/README.md), [Realtime Docker](aulas/aula14/laboratorio_realtime-docker/README.md), [Realtime Windows](aulas/aula14/laboratorio_realtime-windows/README.md), [Guia da Aula](aulas/aula14/README.md) |
| **15** | Gestão de Processos e Carga de Trabalho (flock, filas com prioridade, systemd) | [Notebook](aulas/aula15/notebook_colab/aula15_processos_fila.ipynb), [Apresentação](aulas/aula15/apresentacao_aula15.html), [Atividade](aulas/aula15/atividade.md), [Laboratório Windows](aulas/aula15/laboratorio_windows/README.md), [Guia da Aula](aulas/aula15/README.md) |
| **16** | Agentes de Código: Harness, RAG, Skills e Vibe Coding (Antigravity CLI) | [Apresentação](aulas/aula16/apresentacao_aula16.html), [Atividade](aulas/aula16/atividade.md), [Guia da Aula](aulas/aula16/README.md) |

---

## 📖 Documentação

| Sequência | Documento | Descrição |
| :---: | :--- | :--- |
| **01** | [`01_timeline-engenharia.md`](docs/01_timeline-engenharia.md) | Blueprint causal de engenharia: por que cada aula existe e como se conectam |
| **02** | [`02_resumos.md`](docs/02_resumos.md) | Resumos teóricos consolidados de todas as aulas (Aulas 1 a 15) |
| **03** | [`03_git.md`](docs/03_git.md) | Guia de Git (somente leitura): clonar o repositório e atualizar com `pull` |
| **05** | [`05_materiais-complementares.md`](docs/05_materiais-complementares.md) | Curadoria de links, playlists e cursos externos |
| **06** | [`06_tutorial-instalacao-wsl.md`](docs/06_tutorial-instalacao-wsl.md) | Guia de instalação e configuração do WSL 2 no Windows 10 e 11 |
| **07** | [`07_tutorial-instalacao-docker-wsl.md`](docs/07_tutorial-instalacao-docker-wsl.md) | Guia de instalação e uso do Docker Engine nativo no WSL 2 (Ubuntu) |

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
│   ├── aula01/
│   │   ├── apresentacao_aula01.html
│   │   ├── README.md
│   │   ├── notebook_colab/aula01_arquiteturas_cpu_gpu.ipynb
│   │   ├── laboratorio_windows/             → 1_hardware.py, 2_benchmark.py, lib_hw.py
│   │   └── atividade.md
│   ├── aula02/
│   │   ├── apresentacao_aula02.html
│   │   ├── README.md
│   │   ├── notebook_colab/aula02_modelos_processamento.ipynb
│   │   ├── laboratorio_windows/             → 1_benchmark_simd.py, 2_estudo_imagem.py, 3_arquitetura_instrucoes.py
│   │   ├── scripts/lib_backend.py           → compartilhado (notebook + lab)
│   │   └── atividade.md
│   ├── aula03/
│   │   ├── apresentacao_aula03.html
│   │   ├── README.md
│   │   ├── notebook_colab/aula03_memoria_gpu.ipynb
│   │   ├── laboratorio_windows/             → 1_benchmark_ram_vram.py, 2_hierarquia_memoria.py, 3_monitor_memoria.py
│   │   └── atividade.md
│   ├── aula04/
│   │   ├── apresentacao_aula04.html
│   │   ├── README.md
│   │   ├── notebook_colab/aula04_processos_threads.ipynb
│   │   ├── laboratorio_windows/             → 1_processos_threads.py, 2_io_bound.py, 3_kernels_cuda.py, 4_monitor_processos.py
│   │   └── atividade.md
│   ├── aula05/
│   │   ├── apresentacao_aula05.html
│   │   ├── README.md
│   │   ├── notebook_colab/aula05_redes.ipynb
│   │   ├── laboratorio_windows/             → 1_demo_tcp_udp.py, 2_telemetria_tcp.py, 3_ipv4_ipv6.py, comandos_rede.sh
│   │   └── atividade.md
│   ├── aula06/
│   │   ├── apresentacao_aula06.html
│   │   ├── README.md
│   │   ├── notebook_colab/aula06_linux_gpu.ipynb
│   │   ├── laboratorio_windows/             → hardware real (iniciar.bat + 1_inspecionar.sh, 2_status_gpu.sh, 3_agendar.sh, monitoramento_linux.py)
│   │   ├── scripts/                         → gpu_status.sh, cron_exemplos.sh, gpu-monitor.service (referências servidor Linux)
│   │   └── atividade.md
│   ├── aula07/
│   │   ├── apresentacao_aula07.html
│   │   ├── README.md
│   │   ├── notebook_colab/aula07_cuda.ipynb
│   │   ├── scripts/                         → lib_cuda.py, indice_global.py, primeiro_kernel.py, fft_benchmark.py (referência)
│   │   └── atividade.md
│   ├── aula08/
│   │   ├── apresentacao_aula08.html
│   │   ├── README.md
│   │   ├── notebook_colab/aula08_tiling.ipynb
│   │   ├── scripts/                         → lib_cuda.py, coalescing.py, matmul_global.py, matmul_tiling.py, profiling_ocupacao.py, stress_nvtop.py (referência)
│   │   └── atividade.md
│   ├── aula09/
│   │   ├── apresentacao_aula09.html
│   │   ├── README.md
│   │   ├── notebook_colab/aula09_opencl.ipynb
│   │   ├── laboratorio_windows/             → 1_listar_dispositivos.py, 2_primeiro_kernel.py, 3_benchmark_work_groups.py, lib_opencl.py
│   │   ├── tutorials/                       → hands-on-ollama.md, hands-on-frontend-ollama.md
│   │   └── atividade.md
│   ├── aula10/
│   │   ├── apresentacao_aula10.html
│   │   ├── README.md
│   │   ├── notebook_colab/aula10_rocm.ipynb
│   │   ├── laboratorio_windows/             → 1_rocm_pytorch_benchmark.py, 2_diagnostico_portabilidade.py, lib_rocm.py
│   │   ├── laboratorio_rocm-docker/         → ROCm + PyTorch via Docker (industrial)
│   │   ├── laboratorio_verificar-gpu/       → verifica acesso à GPU (Windows/AMD)
│   │   ├── laboratorio_stressar-gpu/        → estressa GPU via Vulkan (Windows/AMD)
│   │   └── atividade.md
│   ├── aula11/
│   │   ├── atividade_aula11.py
│   │   └── README.md
│   ├── aula12/
│   │   ├── aula12_pratica_colab.ipynb
│   │   └── README.md
│   ├── aula13/
│   │   ├── aula13_implementacao_modelo_paralelo.ipynb
│   │   └── README.md
│   ├── aula14/
│   │   ├── apresentacao_aula14.html
│   │   ├── README.md
│   │   ├── notebook_colab/aula14_automacao_gpu_bash.ipynb
│   │   ├── atividade.md
│   │   ├── scripts_linux/                  → monitor_gpu.sh, alerta_gpu.sh, gerar_graficos.sh, enviar_para_sheets.py
│   │   ├── laboratorio_windows/            → versão Windows/Git Bash (AMD e NVIDIA)
│   │   ├── laboratorio_realtime-docker/    → webservice Python (Flask + SSE) em Docker
│   │   └── laboratorio_realtime-windows/   → webservice Python nativo no Windows
│   ├── aula15/
│   │   ├── apresentacao_aula15.html
│   │   ├── README.md
│   │   ├── notebook_colab/aula15_processos_fila.ipynb
│   │   ├── atividade.md
│   │   └── laboratorio_windows/            → fila de GPU com lock/prioridade (Git Bash + AMD)
│   ├── aula16/
│   │   ├── apresentacao_aula16.html
│   │   ├── atividade.md                    → roteiro prático da Antigravity CLI (agy)
│   │   └── README.md
│   └── projeto-integrador/
│       └── README.md
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
    └── 07_tutorial-instalacao-docker-wsl.md → Guia de instalação do Docker no WSL 2 Ubuntu
```
