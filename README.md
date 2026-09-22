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

## 📋 Pré-requisitos

| Requisito | Detalhes |
| :--- | :--- |
| **Python** | 3.10 ou superior |
| **NumPy** | Obrigatório (todas as aulas) |
| **PyTorch** | Aulas 3, 10 e 11 (benchmarks, portabilidade e treinamento de ResNet) |
| **CuPy** | Aulas 7 e 8 (FFT e estresse de GPU) |
| **Numba** | Aula 8 (kernels CUDA com Tiling) |
| **Weights & Biases** | Aula 11 (registro e monitoramento de experimentos em ML) |
| **GPU NVIDIA / AMD** | Recomendada para Aulas 3, 7, 8, 10 e 11 (scripts têm fallback para CPU) |
| **Docker / WSL 2** | Aulas 9 e 10 (Open WebUI e AMD ROCm / PyTorch) |

---

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/jonasmaffei/senac-tecnico-ia.git
cd senac-tecnico-ia

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt
```

> **Nota sobre GPU:** O PyTorch com CUDA deve ser instalado separadamente via [pytorch.org/get-started](https://pytorch.org/get-started). O CuPy também requer versão compatível com seu CUDA (`pip install cupy-cuda12x`).

---

## 📚 Índice das Aulas

### Bloco 1 — Fundamentos de Hardware e Infraestrutura

| Aula | Tema | Scripts / Recursos |
| :---: | :--- | :--- |
| **01** | Arquitetura de Computadores (Von Neumann, CPU vs GPU) | [`arquitetura_cpu_gpu.py`](aulas/aula01/arquitetura_cpu_gpu.py) |
| **02** | Modelos de Processamento (SIMD, RISC vs CISC) | [`simd_numpy.py`](aulas/aula02/simd_numpy.py) |
| **03** | Hierarquia de Memória (RAM vs VRAM, PCIe) | [`benchmark_ram_vram.py`](aulas/aula03/benchmark_ram_vram.py) |
| **04** | Processos e Threads (GIL, Multiprocessing) | [`processos_threads.py`](aulas/aula04/processos_threads.py) |
| **05** | Redes e Transferência de Dados (TCP/UDP, SSH, rsync) | [`demo_tcp_udp.py`](aulas/aula05/demo_tcp_udp.py), [`comandos_transferencia.sh`](aulas/aula05/comandos_transferencia.sh) |
| **06** | Linux e GPUs (/proc, /sys, tmux, cron) | [`monitoramento_linux.py`](aulas/aula06/monitoramento_linux.py), [`gpu_status.sh`](aulas/aula06/gpu_status.sh) |

### Bloco 2 — Programação, Otimização e Computação Heterogênea

| Aula | Tema | Scripts / Recursos |
| :---: | :--- | :--- |
| **07** | Introdução ao CUDA (Kernels, CuPy FFT) | [`fft_benchmark.py`](aulas/aula07/fft_benchmark.py) |
| **08** | Tiling e Otimização de Memória (Shared Memory) | [`tiling_benchmark.py`](aulas/aula08/tiling_benchmark.py), [`stress_nvtop.py`](aulas/aula08/stress_nvtop.py), [`atividade.md`](aulas/aula08/atividade.md) |
| **09** | Alternativas ao CUDA (OpenCL) + LLMs Locais | [`atividades.md`](aulas/aula09/atividades.md), [Tutorial Ollama](aulas/aula09/hands-on-ollama.md), [Tutorial Open WebUI](aulas/aula09/hands-on-frontend-ollama.md) |
| **10** | Introdução ao ROCm e GPUs AMD (HIP, PyTorch & Docker) | [`rocm_pytorch_benchmark.py`](aulas/aula10/rocm_pytorch_benchmark.py), [`Atividades.md`](aulas/aula10/Atividades.md), [`verificar-gpu-container/`](aulas/aula10/verificar-gpu-container), [`stressar-gpu-container/`](aulas/aula10/stressar-gpu-container) |
| **11** | Aplicação de Modelos em GPUs NVIDIA e AMD (ResNet, W&B, AMP) | [`atividade_aula11.py`](aulas/aula11/atividade_aula11.py), [Guia da Aula](aulas/aula11/README.md) |
| **12** | Prática no Colab e Projeto Final do Módulo | [`aula12_pratica_colab.ipynb`](aulas/aula12/aula12_pratica_colab.ipynb), [Guia Colab](aulas/aula12/README.md), [Projeto Integrador](aulas/projeto-integrador/README.md) |
| **13** | Implementação de um Modelo Paralelo Simples (Síntese Bloco 2) | [`aula13_implementacao_modelo_paralelo.ipynb`](aulas/aula13/aula13_implementacao_modelo_paralelo.ipynb), [Guia Colab](aulas/aula13/README.md) |

### Bloco 3 — Automação

| Aula | Tema | Scripts / Recursos |
| :---: | :--- | :--- |
| **14** | Introdução à Automação de GPUs com Bash (nvidia-smi, cron, gnuplot, Sheets) | [`aula14_automacao_gpu_bash.ipynb`](aulas/aula14/aula14_automacao_gpu_bash.ipynb), [`monitor_gpu.sh`](aulas/aula14/monitor_gpu.sh), [`alerta_gpu.sh`](aulas/aula14/alerta_gpu.sh), [`gerar_graficos.sh`](aulas/aula14/gerar_graficos.sh), [`enviar_para_sheets.py`](aulas/aula14/enviar_para_sheets.py), [Laboratório Windows (AMD)](aulas/aula14/laboratorio_windows/README.md), [Realtime Docker](aulas/aula14/laboratorio_realtime-docker/README.md), [Realtime Windows](aulas/aula14/laboratorio_realtime-windows/README.md), [Apresentação](aulas/aula14/apresentacao_aula14.html), [Guia Colab](aulas/aula14/README.md) |

---

## 📖 Documentação

| Sequência | Documento | Descrição |
| :---: | :--- | :--- |
| **01** | [`01_timeline-engenharia.md`](docs/01_timeline-engenharia.md) | Blueprint causal de engenharia: por que cada aula existe e como se conectam |
| **02** | [`02_resumos.md`](docs/02_resumos.md) | Resumos teóricos consolidados de todas as aulas (Aulas 1 a 14) |
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
│   │   └── arquitetura_cpu_gpu.py
│   ├── aula02/
│   │   └── simd_numpy.py
│   ├── aula03/
│   │   └── benchmark_ram_vram.py
│   ├── aula04/
│   │   └── processos_threads.py
│   ├── aula05/
│   │   ├── comandos_transferencia.sh
│   │   └── demo_tcp_udp.py
│   ├── aula06/
│   │   ├── gpu_status.sh
│   │   └── monitoramento_linux.py
│   ├── aula07/
│   │   └── fft_benchmark.py
│   ├── aula08/
│   │   ├── atividade.md
│   │   ├── stress_nvtop.py
│   │   └── tiling_benchmark.py
│   ├── aula09/
│   │   ├── atividades.md
│   │   ├── hands-on-frontend-ollama.md
│   │   └── hands-on-ollama.md
│   ├── aula10/
│   │   ├── Atividades.md
│   │   ├── rocm_pytorch_benchmark.py
│   │   ├── stressar-gpu-container/
│   │   └── verificar-gpu-container/
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
│   │   ├── aula14_automacao_gpu_bash.ipynb
│   │   ├── apresentacao_aula14.html
│   │   ├── alerta_gpu.sh
│   │   ├── enviar_para_sheets.py
│   │   ├── gerar_graficos.sh
│   │   ├── monitor_gpu.sh
│   │   ├── laboratorio_windows/            → versão Windows/Git Bash (AMD e NVIDIA)
│   │   ├── laboratorio_realtime-docker/    → webservice Python (Flask + SSE) em Docker
│   │   ├── laboratorio_realtime-windows/   → webservice Python nativo no Windows
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
    ├── 05_materiais-complementares.md       → Links e leituras recomendadas
    ├── 06_tutorial-instalacao-wsl.md        → Guia de instalação do WSL no Windows 10/11
    └── 07_tutorial-instalacao-docker-wsl.md → Guia de instalação do Docker no WSL 2 Ubuntu
```
