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
* **Processos vs. Threads:** Processos isolam memória (contornam o GIL do Python); Threads compartilham memória (leves, mas limitadas pelo GIL em tarefas CPU-bound). Regra: **CPU-bound → multiprocessing; I/O-bound → threading**.
* **GIL (Global Interpreter Lock):** mutex que deixa só uma thread Python rodar bytecode por vez; NumPy/PyTorch liberam o GIL nas operações nativas.
* **Hierarquia CUDA:** Threads agrupadas em Warps (32 threads SIMD, unidade de escalonamento), Blocos (compartilham SRAM, rodam em 1 SM, até 1024 threads) e Grades (problema completo). **Divergência de warp** (if/else no mesmo warp) faz a GPU serializar os dois caminhos — perda de desempenho.
* **Prática (Colab/Windows):** benchmark sequencial vs. threading vs. multiprocessing (CPU-bound) mostra que threading empata com o sequencial (GIL) e multiprocessing acelera; um cenário I/O-bound mostra threading ganhando; os kernels Numba/CUDA medem o efeito de `threads_por_bloco` (256 costuma ser o ótimo) e usam grid 2D para uma imagem.

#### Aula 5: Protocolos de Redes e Interação com GPUs
* **IPv4 vs. IPv6:** IPv4 (32 bits, `192.168.1.100`) esgotado, compensado pelo NAT; IPv6 (128 bits, `2001:db8::1`) com autoconfiguração e crescimento em data centers. Hoje as máquinas são dual stack.
* **Modelo OSI (simplificado):** Aplicação (7 — HTTP, SSH, gRPC, NCCL) → Transporte (4 — TCP/UDP) → Rede (3 — IPv4/IPv6) → Enlace (2 — Ethernet/InfiniBand).
* **TCP vs. UDP:** TCP garante entrega e ordem (handshake de 3 vias; SSH, datasets, modelos, APIs); UDP é rápido e sem confirmação (telemetria de GPU, streaming). O Wireshark mostra o handshake e a diferença de pacotes.
* **SSH, scp e rsync:** Essenciais para controle remoto de servidores de GPU e sincronização de datasets; `rsync -avzP` é incremental e retomável (ideal para datasets grandes), enquanto `scp` é simples e sem retomada. Túnel SSH (`-L`) acessa Jupyter remoto.
* **Prática (Colab/Windows):** socket TCP confirma bytes entregues enquanto UDP só dispara; um servidor de telemetria TCP recebe métricas de GPU em JSON; `getaddrinfo` revela as famílias de socket IPv4 (`AF_INET`) e IPv6 (`AF_INET6`).

#### Aula 6: Sistemas Operacionais Linux e GPU
* **Estrutura Virtual:** Uso de `/dev` (`/dev/nvidia*`), `/proc` (`/proc/driver/nvidia`, `cpuinfo`, `meminfo`) e `/sys` (`/sys/class/drm`) para interagir com o kernel e o estado das GPUs. São **pseudo-arquivos** (janela viva para o kernel, sem ocupar disco) — é deles que `htop` e `nvtop` leem.
* **Drivers:** `lspci` identifica a placa; `nvidia-smi`/`rocm-smi` confirmam o driver. Driver ausente é a causa nº 1 de falhas em ambientes de IA.
* **Automação:** `cron` para tarefas periódicas (ex.: `*/5 * * * * gpu_status.sh`) e `systemd` para serviços contínuos (reinício automático, início no boot), além de sessões persistentes com `tmux`/`screen`/`nohup` para sobreviver a quedas de SSH.
* **Prática (Colab/Windows):** `gpu_status.sh` lista GPUs (NVIDIA/AMD) e alerta acima do limite de temperatura; `monitoramento_linux.py` lê os pseudo-arquivos no Linux (ou psutil no Windows); templates de `cron` e de unit systemd comentados.

---

### Bloco 2: Programação e Otimização

#### Aula 7: Introdução ao Modelo CUDA
* **Kernels:** Funções executadas em paralelo por milhares de threads diretamente na VRAM; o host (CPU) aloca, transfere (`to_device`), lança (`kernel[blocos, threads]`), sincroniza e copia de volta (`copy_to_host`).
* **Índices Globais:** `idx = blockIdx.x * blockDim.x + threadIdx.x` (atalho `cuda.grid(1)`) garante um índice único por thread; em 2D usa-se `cuda.grid(2)` (coluna, linha).
* **Sincronização:** `cuda.synchronize()` garante a conclusão dos cálculos na GPU antes de retornar os dados para a CPU. 128–256 threads/bloco (múltiplo de 32) costuma ser o ótimo.
* **Prática (Colab):** primeiros kernels com numba; FFT CPU (NumPy) vs. GPU (CuPy) mostra ~66× no caso de áudio (~1200 ms → ~18 ms). Sem GPU, os scripts mostram o conceito e números de referência.

#### Aula 8: Manipulação de Memória em CUDA (Tiling)
* **Hierarquia de memória:** Registradores (~1 ciclo, por thread) → Shared/SRAM (~5 ciclos, por bloco, cache manual) → Cache L1/L2 (~30) → Global/VRAM (~500 ciclos).
* **Regra 90/10:** 90% do tempo de processamento em I.A. é gasto em acessos à memória.
* **Tiling:** Carregar pedaços (tiles) da VRAM para a Memória Compartilhada rápida e reutilizá-los no bloco, reduzindo os acessos à global por um fator ~TILE. Exige **dois `cuda.syncthreads()`** (barreira antes e depois do uso).
* **Coalescing:** Threads consecutivas acessando endereços consecutivos são unificadas em **1 transação de 128B**; acessos espalhados (stride) geram até ~32 transações separadas.
* **Profiling:** `cuda.event` mede o kernel na GPU; **Nsight Systems** (`nsys`, macro) e **Nsight Compute** (`ncu`, micro: `sm__warps_active`, `dram__bytes`, roofline).
* **Prática (Colab):** matmul global (~120 ms) vs. tiling (~18 ms, ~6.7×) para N=512; `stress_nvtop.py` gera carga para observar no nvtop.

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
* **Prática (Colab/Windows):** `listar_dispositivos.py` descobre plataformas/dispositivos; `primeiro_kernel.py` compila e executa um kernel OpenCL (soma de vetores) — no laboratório AMD o driver expõe OpenCL 2.1; `benchmark_work_groups.py` compara CPU (NumPy) vs. OpenCL e mede com eventos. Regra: `global_size` deve ser múltiplo de `local_size`. Sem OpenCL, os scripts mostram o conceito e números de referência.

#### Aula 10: Introdução ao ROCm e GPUs AMD
* **Ecossistema ROCm:** Plataforma open-source da AMD para computação GPU (alternativa direta ao CUDA proprietário). Stack: Aplicação -> Framework (MIOpen, rocBLAS) -> HIP Runtime -> ROCr (HSA) -> KFD Driver -> Hardware (MI300X, RDNA3, CDNA).
* **Camada HIP (Portabilidade):** Permite executar código CUDA em GPUs AMD com mínimas/nulas alterações. O PyTorch emula a API `torch.cuda` via HIP transparentemente.
* **Ferramental Equivalente:**
  * `hipcc` (nvcc), `rocBLAS` (cuBLAS), `MIOpen` (cuDNN), `rocFFT` (cuFFT), `rocRAND` (cuRAND), `rocm-smi` (nvidia-smi).
  * Ferramenta `hipify-clang` converte kernels CUDA C/C++ para HIP C++.
* **Containers e Prática via Docker:** Imagens oficiais `rocm/pytorch` abstraem drivers no host. Dispositivos repassados via `--device=/dev/kfd` e `--device=/dev/dri` com permissões `video` e `render`.
* **Estratégia de Negócios:** Mitigação de *vendor lock-in*, redução de custos de infraestrutura de nuvem/hardware e análise de TCO (Total Cost of Ownership).
* **Prática (Colab/Windows/Docker):** `lib_rocm.py` detecta o backend (CUDA nativo, ROCm/HIP ou CPU); `rocm_pytorch_benchmark.py` mede matmul e o throughput de treino (ResNet-18 ou CNN de fallback) — o **mesmo código** roda em NVIDIA e AMD. Laboratórios: ROCm+Docker (`rocm/pytorch`, dispositivos `/dev/kfd` e `/dev/dri`) e versões Windows (Vulkan/D3D12 no WSL 2).

#### Aula 11: Aplicação de Modelos de IA em GPUs NVIDIA e AMD
* **Treinamento Unificado CUDA vs. ROCm:** O PyTorch abstrai a execução de treinos em hardware NVIDIA e AMD sem alteração no código Python (`torch.cuda` é emulado via HIP no ROCm). O script detecta o backend automaticamente (`torch.version.hip` indica ROCm; caso contrário, CUDA).
* **Modelo e Métricas:** treina uma **CNN simples** (`Conv2d` → `BatchNorm`/ReLU → `AdaptiveAvgPool2d` → `Linear`, entrada 224×224, 10 classes) e mede **throughput (imgs/s)** e **tempo total**. O **warm-up** (passada invisível antes do cronômetro) e o `torch.cuda.synchronize()` são essenciais para medir corretamente.
* **Mixed Precision (AMP FP16):** uso de `torch.amp.autocast('cuda')` + `torch.amp.GradScaler` para reduzir memória e aumentar o throughput. O script compara o modo **FP32 (padrão)** com o **FP16 (otimizado)** e mostra o ganho.
* **Análise de Negócios (pesquisa):** custo por hora de aluguel de GPUs NVIDIA vs. AMD na nuvem, facilidade de uso (CUDA maduro vs. adaptação ao ROCm) e a decisão de compra considerando **custo × esforço de migração** (TCO).
* **Matriz de Trade-offs para Decisão Técnica:**
  * **NVIDIA (CUDA):** ecossistema maduro (cuDNN/cuBLAS), menor tempo de setup, porém maior custo por GPU.
  * **AMD (ROCm):** 100% open-source, maior densidade de VRAM por chip (ex.: MI300X com 192 GB), melhor relação custo/desempenho, exigindo suporte via contêineres Docker recomendados.

#### Aula 12: Prática no Colab e Projeto Integrador
* **Laboratório Interativo (5 experimentos):** notebook no Colab com formulários (`@title`) que revisita a trilha — (1) multiplicação de matrizes CPU vs GPU; (2) custo de transferir RAM ➔ VRAM (PCIe); (3) filtro de imagem paralelo (simulação visual de CUDA/tiling); (4) monitor de VRAM via `nvidia-smi`; (5) classificador de sentimentos de clientes (aplicação real de NLP). 
* **Prototipagem Rápida:** uso de widgets e formulários interativos do Colab para alterar parâmetros e ver o resultado na hora.
* **Projeto Integrador:** a aula também apresenta o trabalho final (pesquisa aplicada que amarra a UC; detalhes em `aulas/projeto-integrador/README.md`).

#### Aula 13: Implementação de um Modelo Paralelo Simples (Síntese do Bloco 2)
* **Comparativo Quádruplo:** Implementação e medição das 4 abordagens para soma vetorial e produto escalar (Python Puro, CPU NumPy, GPU CUDA Numba e GPU CuPy).
* **Redução Paralela em Shared Memory:** Implementação de *Tree Reduction* dentro do bloco CUDA para produto escalar em Numba com acúmulo via `cuda.atomic.add`.
* **Análise de Speedup & Overhead:** Diagnóstico empírico demonstrando que para $N < 100K$ o overhead de transferência PCIe e lançamento de kernels torna a GPU mais lenta que a CPU ($<1\times$), enquanto para $N \ge 10M$ o speedup atinge ganhos expressivos ($>20\times$).
* **Extras:** varredura de $N \in [10K, 100K, 1M, 10M, 100M]$, gráficos de tempo e speedup com Matplotlib, comparação `np.linalg.norm` vs. `cp.linalg.norm`, mini-relatório gerado automaticamente e fechamento com o questionário das Aulas 8 a 13.

#### Aula 14: Introdução à Automação de GPUs com Bash (Bloco 3 — Automação)
* **Monitoramento com `nvidia-smi`:** A opção `--query-gpu` extrai métricas estruturadas (`temperature.gpu`, `utilization.gpu`, `utilization.memory`, `memory.used`, `power.draw`, `power.limit`, clocks e `fan.speed`). A flag `--format=csv,noheader,nounits` produz saída ideal para scripts.
* **Scripts Bash:** `monitor_gpu.sh` coleta métricas em loop, com timestamp e uma linha por GPU, salvando em CSV; `alerta_gpu.sh` compara cada GPU com limites de temperatura/utilização e notifica via webhook (Slack/Discord) ou e-mail. Ambos usam `set -euo pipefail`.
* **Agendamento:** `cron` (sintaxe `* * * * * comando`, `crontab -e`) é o agendador clássico e simples; `systemd timer` é a alternativa moderna com logging via `journald`, dependências (`After=`) e execução após boot (`Persistent=true`).
* **Visualização:** `gnuplot` gera dashboard de 4 painéis (temperatura, utilização, VRAM, potência) direto de um CSV, sem Python; no Colab, `pandas + matplotlib` produz o equivalente.
* **Integração com Google Sheets:** Via Service Account (`google-auth` + `google-api-python-client`), o CSV é anexado a uma planilha (`values().append`), permitindo acompanhar as GPUs sem SSH. Credenciais ficam em variáveis de ambiente e fora do repositório.
* **Operação em Colab:** O notebook detecta `nvidia-smi` e, sem GPU, gera métricas simuladas com o mesmo schema do CSV real; cron/systemd não existem no Colab e são simulados com loop Python. Fecha com a seção **Exercícios (5)**.

#### Aula 15: Gestão de Processos e Carga de Trabalho (Bloco 3 — Automação)
* **Race condition em GPU:** Quando vários jobs usam a mesma placa, competem por VRAM e capacidade de processamento → `CUDA OOM`, *crashes* silenciosos e resultados corrompidos. A correção é garantir **um job por vez** (exclusão mútua) + **fila com prioridade**.
* **`flock` (exclusão mútua):** Cria um *lock* de arquivo; enquanto um processo o mantém, os demais bloqueiam. Flags: `-x` (exclusivo), `-s` (compartilhado), `-n` (*non-blocking*), `-w N` (*timeout*), `-u` (liberar). Em Windows/Git Bash, onde não há `flock`, o mesmo efeito é obtido com **lock por diretório** (`mkdir` é atômico).
* **Fila com prioridade:** O *ticket* é um arquivo nomeado `prioridade_timestamp_nome`. A ordenação lexicográfica (`sort`) coloca prioridade 1 antes de 2 antes de 3; o *timestamp* garante FIFO e unicidade dentro da mesma prioridade.
* **Monitoramento de processos:** `nvidia-smi --query-compute-apps` lista PID/processo/VRAM por GPU e `nvidia-smi pmon` acompanha ao vivo; no Windows, os contadores `Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine` mapeiam PID→utilização.
* **Prioridade de processo:** `nice`/`renice` ajustam a prioridade de CPU e `ionice` a de I/O (`ionice -c 3` = *idle*).
* **`systemd` (produção):** Units `gpu-job@.service` dão isolamento com `MemoryMax`, `CPUWeight`, `IOWeight`, *restart* automático (`Restart=on-failure`) e logging via `journald`. `flock` é para laboratório/scripts ad-hoc; `systemd` é para produção multiusuário.
* **Starvation e aging:** Jobs de baixa prioridade podem nunca executar se os de alta ocuparem a GPU continuamente; a solução clássica é *aging* — aumentar a prioridade conforme o tempo de espera.
* **Prática (Colab/Windows):** no notebook do Colab, o **lock por diretório** e a **fila por prioridade** são simulados em Python (o Colab não tem `flock`/`systemd`); no **laboratório Windows** (`laboratorio_windows/`), `teste_fila.sh` lança 4 jobs e serializa por prioridade, `fila_gpu.sh` enfileira um job e `monitor_gpu_proc.sh` acompanha GPU/processos/fila. Fecha com a seção **Exercícios (5)**.