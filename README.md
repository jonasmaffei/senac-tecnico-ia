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
| **PyTorch** | Aulas 3, 10 e 11 (benchmarks, portabilidade e treino de ResNet) |
| **CuPy** | Aulas 7 e 8 (FFT e estresse de GPU) |
| **Numba** | Aula 8 (kernels CUDA com Tiling) |
| **Weights & Biases** | Aula 11 (registro de experimentos de ML) |
| **GPU NVIDIA / AMD** | Recomendada para Aulas 3, 7, 8, 10 e 11 (há fallback para CPU) |
| **Docker / WSL 2** | Aulas 9 e 10 (Open WebUI e AMD ROCm / PyTorch) |

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
| **01** | Introdução às Arquiteturas de Computadores e GPUs (Von Neumann/Harvard, CPU vs GPU) | [`aula01_arquiteturas_cpu_gpu.ipynb`](aulas/aula01/aula01_arquiteturas_cpu_gpu.ipynb), [Apresentação](aulas/aula01/apresentacao_aula01.html), [Atividade](aulas/aula01/atividade.md), [`scripts/arquitetura_cpu_gpu.py`](aulas/aula01/scripts/arquitetura_cpu_gpu.py), [Guia da Aula](aulas/aula01/README.md) |
| **02** | Modelos de Processamento (SIMD/MIMD, RISC/CISC) | [`aula02_modelos_processamento.ipynb`](aulas/aula02/aula02_modelos_processamento.ipynb), [Apresentação](aulas/aula02/apresentacao_aula02.html), [Atividade](aulas/aula02/atividade.md), [`scripts/`](aulas/aula02/scripts) ([`benchmark_simd.py`](aulas/aula02/scripts/benchmark_simd.py), [`estudo_imagem.py`](aulas/aula02/scripts/estudo_imagem.py), [`lib_backend.py`](aulas/aula02/scripts/lib_backend.py)), [Guia da Aula](aulas/aula02/README.md) |
| **03** | Estrutura de Memória em GPUs (Hierarquia, RAM vs VRAM, PCIe) | [`aula03_memoria_gpu.ipynb`](aulas/aula03/aula03_memoria_gpu.ipynb), [Apresentação](aulas/aula03/apresentacao_aula03.html), [Atividade](aulas/aula03/atividade.md), [`scripts/`](aulas/aula03/scripts) ([`benchmark_ram_vram.py`](aulas/aula03/scripts/benchmark_ram_vram.py), [`hierarquia_memoria.py`](aulas/aula03/scripts/hierarquia_memoria.py), [`monitor_memoria.py`](aulas/aula03/scripts/monitor_memoria.py), [`lib_backend.py`](aulas/aula03/scripts/lib_backend.py)), [Guia da Aula](aulas/aula03/README.md) |
| **04** | Fundamentos de Processos e Threads (GIL, warps/blocos/grade) | [`aula04_processos_threads.ipynb`](aulas/aula04/aula04_processos_threads.ipynb), [Apresentação](aulas/aula04/apresentacao_aula04.html), [Atividade](aulas/aula04/atividade.md), [`scripts/`](aulas/aula04/scripts) ([`processos_threads.py`](aulas/aula04/scripts/processos_threads.py), [`io_bound.py`](aulas/aula04/scripts/io_bound.py), [`kernels_cuda.py`](aulas/aula04/scripts/kernels_cuda.py), [`monitor_processos.py`](aulas/aula04/scripts/monitor_processos.py)), [Guia da Aula](aulas/aula04/README.md) |
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
| **14** | Introdução à Automação de GPUs com Bash (nvidia-smi, cron, gnuplot, Sheets) | [`aula14_automacao_gpu_bash.ipynb`](aulas/aula14/aula14_automacao_gpu_bash.ipynb), [Scripts Linux](aulas/aula14/scripts_linux/) ([`monitor_gpu.sh`](aulas/aula14/scripts_linux/monitor_gpu.sh), [`alerta_gpu.sh`](aulas/aula14/scripts_linux/alerta_gpu.sh), [`gerar_graficos.sh`](aulas/aula14/scripts_linux/gerar_graficos.sh), [`enviar_para_sheets.py`](aulas/aula14/scripts_linux/enviar_para_sheets.py)), [Laboratório Windows (AMD)](aulas/aula14/laboratorio_windows/README.md), [Realtime Docker](aulas/aula14/laboratorio_realtime-docker/README.md), [Realtime Windows](aulas/aula14/laboratorio_realtime-windows/README.md), [Apresentação](aulas/aula14/apresentacao_aula14.html), [Guia Colab](aulas/aula14/README.md) |
| **15** | Gestão de Processos e Carga de Trabalho (flock, filas com prioridade, systemd) | [Apresentação](aulas/aula15/apresentacao_aula15.html), [Laboratório Windows](aulas/aula15/laboratorio_windows/README.md), [Guia da Aula](aulas/aula15/README.md) |

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
│   │   ├── aula01_arquiteturas_cpu_gpu.ipynb
│   │   ├── apresentacao_aula01.html
│   │   ├── atividade.md
│   │   ├── scripts/arquitetura_cpu_gpu.py
│   │   └── README.md
│   ├── aula02/
│   │   ├── aula02_modelos_processamento.ipynb
│   │   ├── apresentacao_aula02.html
│   │   ├── atividade.md
│   │   ├── scripts/                         → lib_backend.py, benchmark_simd.py, estudo_imagem.py
│   │   └── README.md
│   ├── aula03/
│   │   ├── aula03_memoria_gpu.ipynb
│   │   ├── apresentacao_aula03.html
│   │   ├── atividade.md
│   │   ├── scripts/                         → lib_backend.py, benchmark_ram_vram.py, hierarquia_memoria.py, monitor_memoria.py
│   │   └── README.md
│   ├── aula04/
│   │   ├── aula04_processos_threads.ipynb
│   │   ├── apresentacao_aula04.html
│   │   ├── atividade.md
│   │   ├── scripts/                         → processos_threads.py, io_bound.py, kernels_cuda.py, monitor_processos.py
│   │   └── README.md
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
│   │   ├── scripts_linux/                  → monitor_gpu.sh, alerta_gpu.sh, gerar_graficos.sh, enviar_para_sheets.py
│   │   ├── laboratorio_windows/            → versão Windows/Git Bash (AMD e NVIDIA)
│   │   ├── laboratorio_realtime-docker/    → webservice Python (Flask + SSE) em Docker
│   │   ├── laboratorio_realtime-windows/   → webservice Python nativo no Windows
│   │   └── README.md
│   ├── aula15/
│   │   ├── apresentacao_aula15.html
│   │   ├── laboratorio_windows/            → fila de GPU com lock/prioridade (Git Bash + AMD)
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
