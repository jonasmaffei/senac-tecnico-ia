# Trilha de Aprendizado (Timeline): Do Silício à Computação Heterogênea
## A Cadeia Causal da Engenharia de Infraestrutura para I.A.

> **Filosofia da Trilha:** Em Inteligência Artificial, código ineficiente não é apenas lento — ele queima orçamento de nuvem, desperdiça energia e trava a escala do negócio. Cada aula resolve o gargalo deixado pela anterior, formando um encadeamento lógico inevitável do silício ao ecossistema multi-vendor.

---

## O Fluxo Contínuo de Dependência Técnica

```text
BLOCO 1 — FUNDAMENTOS (o hardware e o host)
A1 Von Neumann/Harvard ─> A2 SIMD/MIMD/RISC/CISC ─> A3 Memória (VRAM/PCIe)
   ─> A4 Processos/Threads ─> A5 Redes (TCP/UDP, SSH, rsync) ─> A6 Linux + GPU

BLOCO 2 — PROGRAMAÇÃO E OTIMIZAÇÃO (o código na GPU)
A6 ─> A7 Kernels CUDA ─> A8 Tiling & Coalescing ─> A9 OpenCL (multi-vendor)
   ─> A10 ROCm/HIP (AMD + Docker) ─> A11 CNN NVIDIA vs. AMD
   ─> A12 Lab Colab + Projeto Integrador ─> A13 Modelo Paralelo (síntese do Bloco 2)

BLOCO 3 — AUTOMAÇÃO (a operação contínua)
A13 ─> A14 Monitoramento 24/7 (cron, dashboard) ─> A15 Fila e concorrência na GPU

Legenda: cada seta (─>) representa a resolução do gargalo que a aula anterior
deixou em aberto — a cadeia causal está detalhada nas seções abaixo.
```

---

## Detalhamento Sequencial da Trilha

### Aula 1: Introdução às Arquiteturas de Computadores e GPUs
* **Conceito/Fundamento:** Von Neumann compartilha memória para dados e instruções (gargalo no barramento); Harvard separa as memórias para acesso simultâneo. CPU focada em tarefas sequenciais complexas (poucos núcleos); GPU focada em paralelismo massivo (milhares de núcleos para matrizes e IA).
* **O que se aprende:** O gargalo estrutural de Von Neumann vs. Harvard, e a divisão de papéis entre a CPU (general sequencial) e a GPU (exército massivo matricial); no Colab, consulta a GPU real via `nvidia-smi` e mede o speedup de operações matriciais (sequencial vs. vetorizado).
* **Indicador:** Reconhece modelos aplicados em arquitetura de computadores e GPU.
* **Situação de aprendizagem:** Startup de reconhecimento facial em tempo real precisa decidir entre CPU e GPU para rodar o modelo.
* **O problema que fica em aberto:** Sabemos *que* a GPU processa matrizes em massa, mas *como* os dados e instruções se movem e se organizam dentro do chip?
* **Impacto de negócio:** Impede a contratação cega de instâncias caras de nuvem sem saber se o workload é matricial ou sequencial.

### Aula 2: Modelos de Processamento (SIMD, MIMD, RISC, CISC)
* **Conceito/Fundamento:** SIMD aplica uma instrução a múltiplos dados simultaneamente (GPUs, NumPy); MIMD executa múltiplas instruções em múltiplos dados (CPUs multi-core). RISC foca em instruções simples e fixas (baixo consumo, ARM); CISC foca em instruções complexas e variáveis (x86).
* **O que se aprende:** Taxonomia de Flynn (SIMD vetorizado vs. MIMD multi-core) e o balanço energético de instruções (RISC fixo/baixo consumo em ARM vs. CISC complexo em x86); medição do ganho do SIMD (sequencial vs. NumPy) e de um estudo de caso de imagem (SIMD dentro do *warp* + MIMD entre blocos da GPU).
* **Indicador:** Reconhece modelos aplicados em arquitetura de computadores e GPU.
* **Situação de aprendizagem:** Escolha entre Raspberry Pi (ARM/RISC) e NVIDIA Jetson (ARM + GPU) para visão computacional embarcada em tempo real.
* **Conexão com a Aula 1:** Explica o *mecanismo de execução* da GPU (SIMD expandido em massa) e justifica por que dispositivos de borda (câmeras, edge) escolhem RISC.
* **O problema que fica em aberto:** O dado chega vetorizado, mas quanto tempo ele gasta para ser buscado na hierarquia de armazenamento?

### Aula 3: Estrutura de Memória em GPUs
* **Conceito/Fundamento:** A hierarquia vai de Registradores (mais rápidos, por thread) ➔ Memória Compartilhada / SRAM (cache manual por bloco) ➔ Cache L1/L2 ➔ Memória Global / VRAM (alta capacidade, latência alta). Transferências CPU ⟷ GPU via PCIe são o gargalo principal e devem ser minimizadas.
* **O que se aprende:** A pirâmide de latência (Registradores 1 ciclo -> SRAM Compartilhada 5 ciclos -> VRAM Global 500 ciclos) e o gargalo estrangulador do barramento PCIe.
* **Conexão com a Aula 2:** Descobrimos o verdadeiro vilão de performance: notória falta de largura de banda de entrega de dados pela rodovia PCIe/VRAM, e não falta de cálculo no SIMD.
* **O problema que fica em aberto:** A VRAM está ali, mas quem despacha os lotes de dados do sistema operacional para o barramento sem travar o processador?

### Aula 4: Fundamentos de Processos e Threads
* **Conceito/Fundamento:** Processos isolam memória (contornam o GIL do Python); Threads compartilham memória (leves, mas limitadas pelo GIL em tarefas CPU-bound). Hierarquia CUDA agrupa threads em Warps (32 threads SIMD), Blocos (compartilham SRAM) e Grades (problema completo).
* **O que se aprende:** Isolamento de memória via `multiprocessing` (contornando o GIL do Python no Data Loader) vs. levezas de threads limitadas a I/O.
* **Conexão com a Aula 3:** O gargalo de VRAM é alimentado por batches preparados em paralelo no host; se usarmos `threading` em CPU-bound, o GIL satura e a GPU fica ociosa esperando o dataset.
* **O problema que fica em aberto:** O dataset foi preparado pelo host, mas e quando ele está em um storage remoto de 200 GB fora da máquina local?

### Aula 5: Protocolos de Redes e Interação com GPUs
* **Conceito/Fundamento:** IPv4 lida com esgotamento de endereços impulsionando o IPv6 massivo; TCP garante entrega confiável (transferência de dados) enquanto UDP prioriza velocidade sem confirmação (telemetria). SSH e Rsync são essenciais para controle remoto de servidores de GPU e sincronização de datasets.
* **O que se aprende:** IPv4/IPv6, TCP (confiável/ordenado para datasets/modelos via `scp`/`rsync`) vs. UDP (rápido/sem confirmação para telemetria), e túneis SSH seguros.
* **Conexão com a Aula 4:** O data loader local da A4 não adianta se o cluster for distribuído; os dados precisam atravessar a malha de rede com resiliência a quedas (`rsync --partial`).
* **O problema que fica em aberto:** Os dados chegaram via rede ao nó remoto, mas o SO subjacente precisa sustentar o hardware e os drivers de vídeo por 12 horas seguidas.

### Aula 6: Sistemas Operacionais Linux e GPU
* **Conceito/Fundamento:** Uso de `/dev`, `/proc` e `/sys` para interagir com o kernel e estado das GPUs. Automação combinada de `cron` para tarefas agendadas e `systemd` para serviços contínuos, além de sessões persistentes com `tmux` e `screen`.
* **O que se aprende:** O kernel Linux como gestor de silício via `/dev/nvidia*`, `/proc`, `/sys`, resiliência contra queda SSH via `tmux`/`screen` e automação com `cron`/`systemd`.
* **Conexão com a Aula 5:** A rede entregou o arquivo, o SSH conectou, mas o job de treino longo precisa sobreviver a desconexões e auditar temperatura/recursos via terminal.
* **O problema que fica em aberto:** O ambiente está estável, seguro e monitorado, mas o código executado (Python puro/PyTorch padrão) ainda não espreme o máximo de eficiência do silício da VRAM.

### Aula 7: Introdução ao Modelo CUDA
* **Conceito/Fundamento:** Kernels são funções executadas em paralelo por milhares de threads diretamente na VRAM. Uso de índices globais (`blockIdx`, `blockDim`, `threadIdx`) para mapear dados unicamente, com `cuda.synchronize()` garantindo conclusão dos cálculos antes de retornar dados à CPU.
* **O que se aprende:** Escrita de *kernels* em Python/Numba, mapeamento de índice global (`blockIdx.x * blockDim.x + threadIdx.x`) e sincronização obrigatória (`cuda.synchronize()`).
* **Conexão com as Aulas 1-6:** Unimos o hardware da A1-3, a alimentação do host da A4-5 e o SO da A6 para rodar código customizado direto na VRAM da NVIDIA.
* **O problema que fica em aberto:** O kernel da A7 funciona, mas ele bate toda hora na VRAM Global lenta (A3), gerando desperdício massivo de ciclos de clock.

### Aula 8: Manipulação de Memória em CUDA (Tiling)
* **Conceito/Fundamento:** Regra 90/10 (90% do tempo de processamento em IA é gasto em acessos à memória). Tiling carrega pedaços da VRAM para a Memória Compartilhada rápida para reutilização. Coalescing une acessos consecutivos em transações eficientes.
* **O que se aprende:** A Regra 90/10, *Coalescing* (unir transações de memória global) e *Tiling* (carregar blocos de matrizes na SRAM compartilhada para reutilização local).
* **Conexão com a Aula 7:** Pegamos o kernel da A7 e o reescremos com estratégia de cache manual (SRAM da A3) para eliminar o gargalo de largura de banda da VRAM.
* **O problema que fica em aberto:** O código é hiper-otimizado para NVIDIA (CUDA/cuDNN), mas e quando o cliente corporativo exige execução em infraestrutura AMD/Intel?

### Aula 9: Alternativas ao CUDA: OpenCL
* **Conceito/Fundamento:** Viabilizar computação paralela multiplataforma e heterogênea para clientes com AMD/Intel. Suporte OpenCL 3.0 (NVIDIA/AMD/Intel), Apple deprecated 1.2 (Metal), Qualcomm 2.0 (Mobile). Arquitetura com *Platform*, *Device*, *Context*, *Command Queue*, kernel em C99 JIT e `cl.Buffer`. Mapeamento: thread/work-item, block/work-group, grid/NDRange, shared mem/`__local`, syncthreads/barrier, constant/`__constant`. Trade-offs: portabilidade multi-vendor sem vendor lock-in vs. código ~3x mais verboso, JIT cold start e ecossistema DL fraco.
* **O que se aprende:** Padrão aberto do Khronos Group, hierarquia *Platform -> Device -> Context -> Command Queue*, mapeamento de `work-items`/`work-groups` e trade-offs JIT vs AOT.
* **Conexão com a Trilha Inteira:** O aluno percebe que *não aprendeu CUDA isoladamente* — **aprendeu computação paralela de dados**. O OpenCL traduz a matriz mental de *tiling* (A8) e *kernels* (A7) para um padrão agnóstico multi-vendor.
* **O problema que fica em aberto:** O OpenCL exige reescrever o código em C99 manual. Como rodar modelos de IA prontos em PyTorch/TensorFlow no hardware AMD mantendo alta performance de nível industrial?

### Aula 10: Introdução ao ROCm e GPUs AMD
* **Conceito/Fundamento:** Configurar e executar aplicações de IA em GPUs AMD com o ecossistema ROCm, abstraindo a portabilidade via HIP e contêineres Docker para eliminar o *vendor lock-in*.
* **O que se aprende:** Arquitetura ROCm (`KFD`, `ROCr`, `HIP`), equivalência funcional (`rocBLAS`, `MIOpen`, `rocm-smi`), conversão via `hipify` e contêineres oficiais `rocm/pytorch`.
* **Conexão com a Aula 9:** O OpenCL mostrou a teoria multi-vendor; a Aula 10 entrega a solução industrial de alto nível, provando que pipelines PyTorch em CUDA rodam transparentemente via HIP em GPUs AMD (como a MI300X) sem alterar o código Python.
* **O problema que fica em aberto:** Como estruturar uma avaliação quantitativa rigorosa (throughput, VRAM, custo, energia) para guiar decisões de conselho técnico/CTO na escolha dos próximos 3 anos de infraestrutura?

### Aula 11: Aplicação de Modelos de IA em GPUs NVIDIA e AMD
* **Conceito/Fundamento:** Rodar o treinamento de uma pequena rede convolucional (CNN simples: `Conv2d` → ReLU → `AdaptiveAvgPool` → `Linear`, entrada 224×224) e comparar o comportamento em **NVIDIA (CUDA)** e **AMD (ROCm)**, medindo throughput e o ganho do Mixed Precision. O código é agnóstico de hardware (`dispositivo = "cuda" if torch.cuda.is_available() else "cpu"`).
* **O que se aprende:** Métricas objetivas de treino (throughput em imgs/s, tempo total), detecção automática do backend (`torch.version.hip` distingue ROCm de CUDA), otimização com Mixed Precision (`torch.amp.autocast('cuda')` + `torch.amp.GradScaler`), importância do **warm-up** e do `torch.cuda.synchronize()` para medir corretamente, e análise de negócios (custo de aluguel na nuvem, facilidade de uso vs. economia, TCO).
* **Conexão com a Aula 10:** Consolida o Bloco 2. Coloca em prática a execução do **mesmo** modelo PyTorch nos dois ecossistemas, fundamentando a decisão executiva com dados empíricos de desempenho e custo.
* **O problema que fica em aberto:** Já sabemos medir um treino real; mas onde, afinal, o ganho da GPU **compensa** — e onde o overhead a torna pior que a CPU?

### Aula 12: Prática no Colab e Projeto Integrador
* **Conceito/Fundamento:** Laboratório prático interativo no Google Colab, em 5 experimentos com formulários (`@title`), revisitando toda a trilha: (1) multiplicação de matrizes CPU vs GPU; (2) custo de transferir RAM ➔ VRAM (PCIe); (3) filtro de imagem paralelo (simulação visual de CUDA/tiling); (4) monitor de VRAM via `nvidia-smi`; (5) classificador de sentimentos de clientes (aplicação real).
* **O que se aprende:** Uso de widgets/formulários interativos do Colab, medição de latência PCIe, prototipagem rápida e introdução ao Projeto Integrador (pesquisa aplicada).
* **Conexão com a Aula 11:** Valida interativamente, num só notebook, os conceitos de todo o curso antes do encerramento do Bloco 2.
* **O problema que fica em aberto:** A prática mostrou o "como"; falta a **medição rigorosa** que quantifica o ponto exato em que a GPU vence a CPU.

### Aula 13: Implementação de um Modelo Paralelo Simples (Síntese do Bloco 2)
* **Conceito/Fundamento:** Desenvolvimento e benchmark de 4 implementações (Python Puro, CPU NumPy, GPU CUDA Numba, GPU CuPy) para soma vetorial e produto escalar, com redução paralela (*tree reduction*) em memória compartilhada e `cuda.atomic.add` no fechamento.
* **O que se aprende:** Paralelismo SIMT vs. SIMD, varredura de N (10K a 100M), limiar de compensação da GPU, overhead de transferência PCIe/kernel launch, gráficos de tempo e speedup com Matplotlib e mini-relatório técnico gerado automaticamente. Inclui a comparação `np.linalg.norm` vs. `cp.linalg.norm`.
* **Conexão com todo o Bloco 2:** Síntese final e reproduzível do Bloco 2, consolidando kernels CUDA, CuPy, vetorização em CPU e análise técnica empírica — e fecha com o questionário das Aulas 8 a 13.
* **O problema que fica em aberto:** O código está otimizado e medido, mas quem garante que ele roda **sem falhar por 12 horas seguidas** num servidor de produção?

### Aula 14: Introdução à Automação de GPUs com Bash (Bloco 3 — Automação)
* **Conceito/Fundamento:** Operação contínua e supervisionada de GPUs com `nvidia-smi --query-gpu` para métricas estruturadas, scripts Bash de coleta e alerta, agendamento com `cron`/`systemd timers`, dashboard com `gnuplot`/Matplotlib e integração com o Google Sheets.
* **O que se aprende:** Extração de métricas (`temperature.gpu`, `utilization.gpu`, `power.draw`, `memory.used`), escrita de `monitor_gpu.sh`/`alerta_gpu.sh` com `set -euo pipefail`, sintaxe do crontab vs. timer systemd, limites de alerta e publicação de séries temporais via API. O **notebook do Colab** (com **5 exercícios**) simula cron/systemd e gera gráficos; o **laboratório Windows** roda os scripts reais (Git Bash + contadores AMD).
* **Conexão com o Bloco 2:** O código paralelo otimizado (A7–A13) roda em produção 24h/7d; a automação garante que a GPU não trave silenciosamente nem desperdice orçamento de nuvem.
* **O problema que fica em aberto:** Monitorar é o primeiro passo; e quando **vários jobs** disputam a mesma GPU ao mesmo tempo, como evitar contenção de recursos?

### Aula 15: Gestão de Processos e Carga de Trabalho (Bloco 3 — Automação)
* **Conceito/Fundamento:** Controle de concorrência em GPU em ambiente multiusuário: exclusão mútua com `flock` (ou lock por diretório no Windows), filas de jobs com prioridade, monitoramento de processos em tempo real (`nvidia-smi pmon` / contadores do Windows) e isolamento com `systemd`.
* **O que se aprende:** Race conditions e OOM por disputa de VRAM, semântica das flags do `flock` (`-x`, `-s`, `-n`, `-w`, `-u`), fila por *ticket* (`prioridade + timestamp` → ordenação lexicográfica), `nice`/`ionice`, units `systemd` com controle de recursos e o conceito de *starvation* (e *aging* como remédio). No **notebook do Colab** (com **5 exercícios**), o lock e a fila são **simulados em Python**; no **laboratório Windows**, `teste_fila.sh` e `monitor_gpu_proc.sh` exercitam a fila de verdade.
* **Conexão com o Bloco 2:** O código paralelo (A7–A13) e o monitoramento contínuo (A14) agora rodam de forma **justa e segura** quando vários usuários compartilham a mesma placa; a solução é feita só com Bash, sem Slurm/Kubernetes.
* **O problema que fica em aberto:** Garantir uso justo da GPU resolve a concorrência; como reduzir o **consumo de energia** da operação contínua?

---

## Matriz de Domínio por Elo da Corrente

| Elo | Pergunta Crítica Respondida | Evidência Prática no Repositório |
| :--- | :--- | :--- |
| **A1-A2** | "Preciso de CPU sequencial ou GPU massiva — e o que cada arquitetura custa em energia?" | Notebooks e scripts de Von Neumann vs. Harvard, SIMD/MIMD e RISC/CISC (`benchmark_simd.py`, `estudo_imagem.py`, `arquitetura_instrucoes.py`). |
| **A3** | "Onde os dados vivem e qual é o gargalo real de entrega?" | `benchmark_ram_vram.py`, `hierarquia_memoria.py`, `monitor_memoria.py` (VRAM, PCIe, degrau de cache). |
| **A4-A6** | "Como alimentar a GPU num cluster remoto sem perder o job de 12h?" | `multiprocessing`/`io_bound` (A4), `demo_tcp_udp`/`telemetria_tcp`/`rsync`/SSH (A5), `tmux`/`screen`/`cron`/`systemd` (A6). |
| **A7-A8** | "Como espremer 100% da VRAM da placa de vídeo?" | Kernels CUDA (A7) e matmul com *tiling*/*coalescing* + profiling `cuda.event`/Nsight (A8). |
| **A9** | "E se o cliente exigir rodar em cluster AMD/Intel?" | Tradução do paralelismo para padrão aberto agnóstico (OpenCL/PyOpenCL). |
| **A10-A11** | "Como provar com dados objetivos qual ecossistema (CUDA vs. ROCm) adotar?" | ROCm/HIP + Docker (A10) e treino de CNN comparando throughput FP32×FP16 e custo (A11). |
| **A12-A13** | "Onde o speedup da GPU compensa de fato (e quando não)?" | Lab interativo no Colab (A12) + benchmark de 4 implementações, curva de speedup e mini-relatório (A13). |
| **A14** | "Como garantir que a GPU opere 24h/7d sem falhar em silêncio?" | `monitor_gpu.sh` + `alerta_gpu.sh` via `cron`, dashboard e envio ao Google Sheets. |
| **A15** | "Como compartilhar 1 GPU entre vários jobs sem OOM?" | Fila com prioridade + `flock`/lock (`fila_gpu.sh`), monitor de processos na GPU e agendamento (`systemd`/cron). |