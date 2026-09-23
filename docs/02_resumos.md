# Guia de Estudo e Resumo Consolidado
## Introdução a Arquitetura de Computadores

---

### Bloco 1: Fundamentos

#### Aula 1: Introdução às Arquiteturas de Computadores e GPUs
* **Von Neumann vs. Harvard:** Von Neumann compartilha memória para dados e instruções (gargalo no barramento); Harvard separa as memórias para acesso simultâneo. Harvard é mais rápido por ciclo, mas Von Neumann é mais simples/barata — daí dominar os PCs.
* **Gargalo de Von Neumann:** Instruções e dados disputam o mesmo barramento; quanto mais rápido o processador, maior a espera. Caches e hierarquia de memória (Aula 3) amenizam o problema.
* **CPU vs. GPU:** CPU focada em tarefas sequenciais complexas (poucos núcleos, alta frequência); GPU focada em paralelismo massivo (milhares de núcleos, alta largura de banda, ideal para matrizes e IA).
* **Prática (Colab):** `nvidia-smi` mostra modelo, VRAM, temperatura e processos da GPU; o benchmark mede a multiplicação de matrizes com 3 `for` aninhados (sequencial) vs. NumPy/BLAS (vetorizado), evidenciando o speedup do paralelismo.
* **Analogia:** CPU = chef experiente fazendo um prato complexo sozinho; GPU = mil cozinheiros fazendo o mesmo prato simples ao mesmo tempo.

#### Aula 2: Modelos de Processamento (SIMD, MIMD, RISC, CISC)
* **Taxonomia de Flynn:** classifica por instruções × dados — **SISD** (1×1, CPU sequencial), **SIMD** (1×muitos, GPU/AVX/NumPy), **MISD** (raro) e **MIMD** (muitos×muitos, multi-core/clusters).
* **SIMD:** Uma instrução aplicada a múltiplos dados simultaneamente (GPUs, NumPy). É o que dá o grande speedup em vetores, imagens e matrizes.
* **MIMD:** Múltiplas instruções em múltiplos dados (CPUs multi-core); cada núcleo faz uma tarefa diferente.
* **RISC vs. CISC:** RISC foca em instruções simples e de tamanho **fixo** (pipeline previsível, baixo consumo, ARM); CISC foca em instruções complexas de tamanho **variável** (x86). Trade-off: RISC gasta menos energia, mas o CISC tem o ecossistema de software maduro — daí x86 dominar desktops/servidores.
* **Prática (Colab/Windows):** o ganho do SIMD é medido com sequencial (Python puro) vs. NumPy; o estudo de caso converte uma imagem 1080p em tons de cinza (loop por pixel vs. vetorizado). O código detecta o backend (CuPy → PyTorch CUDA → DirectML → NumPy) e roda igual no Colab e no Windows com GPU AMD.
* **GPU = SIMD + MIMD:** dentro de um *warp* (32 threads) a instrução é a mesma (SIMD); vários blocos/SMs processam pedaços diferentes ao mesmo tempo (MIMD).

#### Aula 3: Estrutura de Memória em GPUs
* **Hierarquia:** Registradores (~1 ciclo, por thread) -> Memória Compartilhada / SRAM (~1–5 ciclos, controlada pelo programador, por bloco) -> Cache L1/L2 (~20–50 ciclos, automático) -> Memória Global / VRAM (~400–800 ciclos, 8–80 GB) -> RAM do host (milhares de ciclos, via PCIe).
* **Regra 90/10:** ~90% do tempo de processamento em IA é gasto esperando memória, não calculando — otimizar memória vale mais que otimizar contas.
* **RAM vs. VRAM:** RAM (DDR5) ~80 GB/s; VRAM (HBM3/GDDR6) ~3.35 TB/s. A VRAM é ~40× mais rápida em largura de banda, mas muito menor.
* **O Gargalo do Barramento:** Transferências CPU <-> GPU via PCIe 4.0 x16 (~32 GB/s) são ~100× mais lentas que a VRAM interna — copiar pode custar mais que calcular. Minimize o tráfego mantendo os batches na VRAM.
* **Prática (Colab/Windows):** `nvidia-smi`/`pynvml` monitoram VRAM e utilização; o benchmark mede a mesma soma na RAM (CPU) e na VRAM (GPU) mais o custo da cópia PCIe; a `hierarquia_memoria.py` mostra o degrau de largura de banda entre cache e RAM. O kernel CUDA (Numba) contrasta memória global vs. compartilhada (`cuda.shared.array` + `syncthreads`).

#### Aula 4: Fundamentos de Processos e Threads
* **Processos vs. Threads:** Processos isolam memória (contornam o GIL do Python); Threads compartilham memória (leves, mas limitadas pelo GIL em tarefas CPU-bound).
* **Hierarquia CUDA:** Threads agrupadas em Warps (32 threads SIMD), Blocos (compartilham SRAM) e Grades (problema completo).

#### Aula 5: Protocolos de Redes e Interação com GPUs
* **IPv4 vs. IPv6:** Esgotamento do IPv4 impulsionou o IPv6 com endereçamento massivo.
* **TCP vs. UDP:** TCP garante entrega confiável (transferência de dados); UDP prioriza velocidade sem confirmação (telemetria).
* **SSH e Rsync:** Essenciais para controle remoto de servidores de GPU e sincronização de datasets.

#### Aula 6: Sistemas Operacionais Linux e GPU
* **Estrutura Virtual:** Uso de `/dev`, `/proc` e `/sys` para interagir com o kernel e estado das GPUs.
* **Automação:** Uso combinado de `cron` para tarefas agendadas e `systemd` para serviços contínuos, além de sessões persistentes com `tmux` e `screen`.

---

### Bloco 2: Programação e Otimização

#### Aula 7: Introdução ao Modelo CUDA
* **Kernels:** Funções executadas em paralelo por milhares de threads diretamente na VRAM.
* **Índices Globais:** Combinação de `blockIdx`, `blockDim` e `threadIdx` para mapear dados unicamente.
* **Sincronização:** `cuda.synchronize()` garante a conclusão dos cálculos na GPU antes de retornar os dados para a CPU.

#### Aula 8: Manipulação de Memória em CUDA (Tiling)
* **Regra 90/10:** 90% do tempo de processamento em I.A. é gasto em acessos à memória.
* **Tiling:** Técnica de carregar pedaços de dados da VRAM para a Memória Compartilhada rápida, permitindo reutilização e eliminando o gargalo de largura de banda.
* **Coalescing:** Acessos consecutivos à memória unificados em transações eficientes.

#### Aula 9: Alternativas ao CUDA: OpenCL
##### 1. Contextualização e Suporte
* **Objetivo:** Viabilizar computação paralela multiplataforma e heterogênea.
* **Cenário de Negócio:** Atender clientes com datacenters baseados em GPUs AMD e Intel (incompatíveis com CUDA).
* **Suporte por Fabricante:**
  * **NVIDIA:** OpenCL 3.0 (suportado, mas com preferência por CUDA).
  * **AMD:** OpenCL 3.0 (suportado nativamente via ROCm).
  * **Intel:** OpenCL 3.0 (CPU, GPU integrada e Arc).
  * **Apple:** OpenCL 1.2 (*deprecated* / descontinuado em favor do Metal).
  * **Qualcomm:** OpenCL 2.0 (GPUs mobile / Snapdragon).

##### 2. Arquitetura e Componentes do OpenCL
* **Platform:** Conjunto de drivers do fabricante do hardware.
* **Device:** Unidade física de processamento (CPU, GPU, FPGA, DSP).
* **Context:** Gerenciador que agrupa dispositivos, buffers de memória e filas.
* **Command Queue:** Fila de despacho de operações (kernels e cópias de dados).
* **Kernel OpenCL:** Função escrita em C99 compilada em tempo de execução (*JIT*).
* **Buffer:** Área de memória alocada explicitamente no dispositivo (`cl.Buffer`).

##### 3. Mapeamento Lógico (CUDA vs. OpenCL)
| Conceito | CUDA (NVIDIA) | OpenCL (Khronos) |
| :--- | :--- | :--- |
| **Unidade de Execução** | `thread` | `work-item` |
| **Grupo de Execução** | `block` | `work-group` |
| **Conjunto Completo** | `grid` | `NDRange` |
| **ID Local** | `threadIdx.x` | `get_local_id(0)` |
| **ID do Grupo** | `blockIdx.x` | `get_group_id(0)` |
| **ID Global** | `cuda.grid(1)` | `get_global_id(0)` |
| **Tamanho do Grupo** | `blockDim.x` | `get_local_size(0)` |
| **Memória Compartilhada**| `cuda.shared.array()` | `__local float[]` |
| **Sincronização** | `cuda.syncthreads()` | `barrier(CLK_LOCAL_MEM_FENCE)` |
| **Memória Constante** | `__constant__` | `__constant` |

##### 4. Trade-offs (Portabilidade vs. Ecossistema)
* **Vantagens:** 
  * Portabilidade multi-vendor (NVIDIA, AMD, Intel, CPUs, FPGAs).
  * Eliminação de *vendor lock-in*.
  * Fallback nativo para CPU.
* **Desvantagens:** 
  * Código mais verboso (~3× mais longo).
  * Compilação JIT gera latência na inicialização.
  * Ecossistema de alto nível para Deep Learning (PyTorch/TensorFlow/cuDNN) fortemente acoplado à NVIDIA.

#### Aula 10: Introdução ao ROCm e GPUs AMD
* **Ecossistema ROCm:** Plataforma open-source da AMD para computação GPU (alternativa direta ao CUDA proprietário). Stack: Aplicação -> Framework (MIOpen, rocBLAS) -> HIP Runtime -> ROCr (HSA) -> KFD Driver -> Hardware (MI300X, RDNA3, CDNA).
* **Camada HIP (Portabilidade):** Permite executar código CUDA em GPUs AMD com mínimas/nulas alterações. O PyTorch emula a API `torch.cuda` via HIP transparentemente.
* **Ferramental Equivalente:**
  * `hipcc` (nvcc), `rocBLAS` (cuBLAS), `MIOpen` (cuDNN), `rocFFT` (cuFFT), `rocRAND` (cuRAND), `rocm-smi` (nvidia-smi).
  * Ferramenta `hipify-clang` converte kernels CUDA C/C++ para HIP C++.
* **Containers e Prática via Docker:** Imagens oficiais `rocm/pytorch` abstraem drivers no host. Dispositivos repassados via `--device=/dev/kfd` e `--device=/dev/dri` com permissões `video` e `render`.
* **Estratégia de Negócios:** Mitigação de *vendor lock-in*, redução de custos de infraestrutura de nuvem/hardware e análise de TCO (Total Cost of Ownership).

#### Aula 11: Aplicação de Modelos de IA em GPUs NVIDIA e AMD
* **Treinamento Unificado CUDA vs. ROCm:** O PyTorch abstrai a execução de treinos em hardware NVIDIA e AMD sem necessidade de alteração no código Python (`torch.cuda` é emulado via HIP no ROCm).
* **Métricas Objetivas de Comparação:**
  * **Throughput (imagens/s):** Métrica primordial de produtividade em treinamento.
  * **VRAM Alocada (MB/GB):** Consumo de memória durante os passos de *forward* e *backward*.
  * **Tempo por Época & Custo (US$/h):** Fundamentais para a modelagem de TCO (Total Cost of Ownership).
* **Mixed Precision (AMP FP16/BF16):** Uso de `torch.cuda.amp.autocast()` e `GradScaler` para reduzir VRAM em ~50% e aumentar throughput em até 2–3× em ambas as plataformas.
* **Weights & Biases (W&B):** Rastreamento de experimentos de ML em dashboards comparativos unificados via tags/configurações do backend (`CUDA` vs `ROCm`).
* **Matriz de Trade-offs para Decisão Técnica:**
  * **NVIDIA (CUDA):** Ecossistema extremamente maduro, ecossistema cuDNN/cuBLAS consolidado, menor tempo de setup, porém maior custo por GPU.
  * **AMD (ROCm):** 100% open-source, maior densidade de VRAM por chip (ex: MI300X com 192GB), melhor relação custo/desempenho (~30% mais barato), exigindo suporte via contêineres Docker recomendados.

#### Aula 12: Prática no Colab e Projeto Final do Módulo
* **Laboratório Prático:** Exploração interativa no Google Colab de multiplicação de matrizes CPU vs GPU, latência de barramento PCIe na transferência RAM ➔ VRAM e aplicação de filtros em imagens por meio de Tiling simulado.
* **Prototipagem Rápida:** Uso de widgets e formulários interativos do Colab para modificar dinamicamente parâmetros de execução.

#### Aula 13: Implementação de um Modelo Paralelo Simples (Síntese do Bloco 2)
* **Comparativo Quádruplo:** Implementação e medição das 4 abordagens para soma vetorial e produto escalar (Python Puro, CPU NumPy, GPU CUDA Numba e GPU CuPy).
* **Redução Paralela em Shared Memory:** Implementação de *Tree Reduction* dentro do bloco CUDA para produto escalar em Numba com acúmulo via `cuda.atomic.add`.
* **Análise de Speedup & Overhead:** Diagnóstico empírico demonstrando que para $N < 100K$ o overhead de transferência PCIe e lançamento de kernels torna a GPU mais lenta que a CPU ($<1\times$), enquanto para $N \ge 10M$ o speedup atinge ganhos expressivos ($>20\times$).

#### Aula 14: Introdução à Automação de GPUs com Bash (Bloco 3 — Automação)
* **Monitoramento com `nvidia-smi`:** A opção `--query-gpu` extrai métricas estruturadas (`temperature.gpu`, `utilization.gpu`, `utilization.memory`, `memory.used`, `power.draw`, `power.limit`, clocks e `fan.speed`). A flag `--format=csv,noheader,nounits` produz saída ideal para scripts.
* **Scripts Bash:** `monitor_gpu.sh` coleta métricas em loop, com timestamp e uma linha por GPU, salvando em CSV; `alerta_gpu.sh` compara cada GPU com limites de temperatura/utilização e notifica via webhook (Slack/Discord) ou e-mail. Ambos usam `set -euo pipefail`.
* **Agendamento:** `cron` (sintaxe `* * * * * comando`, `crontab -e`) é o agendador clássico e simples; `systemd timer` é a alternativa moderna com logging via `journald`, dependências (`After=`) e execução após boot (`Persistent=true`).
* **Visualização:** `gnuplot` gera dashboard de 4 painéis (temperatura, utilização, VRAM, potência) direto de um CSV, sem Python; no Colab, `pandas + matplotlib` produz o equivalente.
* **Integração com Google Sheets:** Via Service Account (`google-auth` + `google-api-python-client`), o CSV é anexado a uma planilha (`values().append`), permitindo acompanhar as GPUs sem SSH. Credenciais ficam em variáveis de ambiente e fora do repositório.
* **Operação em Colab:** O notebook detecta `nvidia-smi` e, sem GPU, gera métricas simuladas com o mesmo schema do CSV real; cron/systemd não existem no Colab e são simulados com loop Python.

#### Aula 15: Gestão de Processos e Carga de Trabalho (Bloco 3 — Automação)
* **Race condition em GPU:** Quando vários jobs usam a mesma placa, competem por VRAM e capacidade de processamento → `CUDA OOM`, *crashes* silenciosos e resultados corrompidos. A correção é garantir **um job por vez** (exclusão mútua) + **fila com prioridade**.
* **`flock` (exclusão mútua):** Cria um *lock* de arquivo; enquanto um processo o mantém, os demais bloqueiam. Flags: `-x` (exclusivo), `-s` (compartilhado), `-n` (*non-blocking*), `-w N` (*timeout*), `-u` (liberar). Em Windows/Git Bash, onde não há `flock`, o mesmo efeito é obtido com **lock por diretório** (`mkdir` é atômico).
* **Fila com prioridade:** O *ticket* é um arquivo nomeado `prioridade_timestamp_nome`. A ordenação lexicográfica (`sort`) coloca prioridade 1 antes de 2 antes de 3; o *timestamp* garante FIFO e unicidade dentro da mesma prioridade.
* **Monitoramento de processos:** `nvidia-smi --query-compute-apps` lista PID/processo/VRAM por GPU e `nvidia-smi pmon` acompanha ao vivo; no Windows, os contadores `Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine` mapeiam PID→utilização.
* **Prioridade de processo:** `nice`/`renice` ajustam a prioridade de CPU e `ionice` a de I/O (`ionice -c 3` = *idle*).
* **`systemd` (produção):** Units `gpu-job@.service` dão isolamento com `MemoryMax`, `CPUWeight`, `IOWeight`, *restart* automático (`Restart=on-failure`) e logging via `journald`. `flock` é para laboratório/scripts ad-hoc; `systemd` é para produção multiusuário.
* **Starvation e aging:** Jobs de baixa prioridade podem nunca executar se os de alta ocuparem a GPU continuamente; a solução clássica é *aging* — aumentar a prioridade conforme o tempo de espera.