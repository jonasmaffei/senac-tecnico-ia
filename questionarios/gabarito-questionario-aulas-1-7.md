# Gabarito — Questionário de Revisão (Aulas 1 a 7)
## Introdução a Arquitetura de Computadores

> **Uso:** Material de conferência para o questionário da Fase 1 (já respondido em sala). As respostas abaixo são orientativas — valorize o raciocínio e a aplicação dos conceitos, não apenas a reprodução literal.

---

### Bloco 1: Fundamentos

#### Aula 1 — Quem Faz o Quê? (CPU vs. GPU)

**1. Diferença funcional entre CPU e GPU.**
A **CPU** é o "cérebro central": possui poucos núcleos potentes e é otimizada para tarefas **sequenciais e complexas** (decisões, lógica, controle). A **GPU** é a "placa de vídeo": possui **milhares de núcleos simples** e é otimizada para o **paralelismo massivo** (aplicar a mesma operação a muitos dados ao mesmo tempo, como em matrizes). Em IA, a CPU coordena o fluxo e a GPU executa os cálculos pesados em paralelo.

**2. Por que a CPU sozinha não atende ao treinamento de IA.**
Porque o treinamento envolve **operações matriciais gigantes** (milhões de multiplicações e somas). Executadas de forma sequencial, levariam tempo inviável. A CPU, com poucos núcleos, não escala para esse volume; a GPU processa milhares de operações simultaneamente, tornando o treinamento viável.

**3. O que define a escolha entre CPU e GPU.**
A **natureza da carga de trabalho**: se for sequencial, com muitas decisões e pouca repetição (ex.: controle, pré-processamento leve), a CPU é suficiente e mais simples; se for **paralelizável e intensiva em dados** (matrizes, imagens, treino de redes neurais), a GPU traz ganho real. Também pesam o volume de dados, o custo, o consumo de energia e a latência de transferência entre RAM e VRAM.

---

#### Aula 2 — Como Eles Trabalham? (Organização do Trabalho)

**4. Modelo SIMD (Sincronia Total).**
No **SIMD** (*Single Instruction, Multiple Data*), **uma única instrução é aplicada a vários dados simultaneamente**. Comparando com uma equipe de trabalho: é como um instrutor que dá **um único comando** e todos os operários executam **ao mesmo tempo**, cada um sobre o seu material. A GPU usa esse modelo em escala massiva (milhares de threads). O ponto de atenção é que, se os operários precisarem de comandos diferentes (*divergência*), a sincronia quebra e o desempenho cai.

**5. Vantagem do RISC em relação ao CISC.**
O **RISC** usa instruções **simples, fixas e padronizadas**, o que simplifica o hardware, reduz o consumo de energia e permite maior frequência e pipelines eficientes. Já o **CISC** usa instruções **complexas e variáveis** (x86), mais poderosas por instrução, porém mais caras em consumo. Por isso dispositivos móveis e de borda (que priorizam eficiência energética) adotam RISC (ex.: ARM).

**6. Impacto da eficiência energética no desenvolvimento de soluções.**
A escolha por arquiteturas de baixo consumo (RISC/ARM) permite criar dispositivos de **borda (edge)** que processam IA localmente, sem depender da nuvem: menos latência, maior privacidade e menor custo de energia. Isso amplia o leque de soluções (câmeras inteligentes, celulares, sensores), mas exige adaptar bibliotecas e modelos para hardware menos potente.

---

#### Aula 3 — A Logística e a Memória (Por que a IA fica lenta?)

**7. O "gargalo da rodovia" (RAM ↔ VRAM).**
É a analogia para o **barramento PCIe**: a "rodovia" que liga a memória RAM (do sistema) à VRAM (da placa de vídeo). Mesmo com uma GPU ultrarrápida, os dados precisam **trafegar por essa via**, cuja largura de banda é limitada. Quando o volume de dados é grande ou mal planejado, a transferência se torna o gargalo — a GPU fica ociosa esperando dados. Por isso, minimizar transferências CPU↔GPU é essencial.

**8. Registradores vs. Memória Global/VRAM.**
Os **registradores** são a memória mais rápida, **privada de cada thread** (como o material "na mão do operário") — latência de ~1 ciclo, capacidade mínima. A **Memória Global/VRAM** é a maior e mais lenta, **compartilhada por todas as threads** — latência de ~500 ciclos. A hierarquia existe para equilibrar velocidade e capacidade: dados muito reutilizados sobem para camadas rápidas (shared/cache); o restante fica na VRAM.

**9. Por que a lentidão em camadas distantes prejudica a IA.**
Porque, na **Regra 90/10**, cerca de **90% do tempo de processamento em IA é gasto em acessos à memória**, não em cálculo. Se a thread busca dados na VRAM (camada distante) repetidamente, ela passa a maior parte do tempo **esperando** memória, e os núcleos ficam subutilizados. Daí a importância de técnicas como cache, tiling e coalescing.

---

#### Aula 4 — Como a Máquina Divide o Trabalho (Processos vs. Threads)

**10. Diferença entre Processo e Thread.**
Um **processo** tem **memória isolada e própria** — é mais seguro (uma falha não afeta os outros) e permite paralelismo real contornando o GIL do Python; porém é mais **pesado** (mais custo de criação e troca de contexto). Uma **thread** **compartilha a memória** do processo — é mais **leve e rápida** de criar, mas menos segura (risco de condição de corrida) e limitada pelo GIL em tarefas CPU-bound.

**11. O que é o GIL e como ele restringe o uso de múltiplos núcleos.**
O **GIL** (*Global Interpreter Lock*) é um "cadeado" do interpretador Python que permite que **apenas uma thread execute código Python por vez**, mesmo em máquinas com vários núcleos. Em tarefas **CPU-bound** (cálculo pesado), as threads acabam se revezando e não há ganho real de desempenho. Para contornar, usa-se **`multiprocessing`** (processos separados) ou bibliotecas que liberam o GIL (como NumPy, que executa em C).

**12. Divergência em GPU.**
A GPU executa threads em **Warps de 32 threads** que devem executar **a mesma instrução** (SIMT). Quando há muitos desvios condicionais (`if/else`), threads de um mesmo warp tomam **caminhos diferentes**, e o hardware é obrigado a **serializar** os caminhos: primeiro executa o "se" (desativando as demais), depois o "senão". Resultado: **desperdício de ciclos e queda de desempenho**. Por isso se prefere código sem ramificações divergentes.

---

#### Aula 5 — A Logística e a Comunicação da I.A. (Redes e Transferência)

**13. IPv4 e a migração para IPv6.**
O **IPv4** usa endereços de 32 bits, totalizando cerca de 4,3 bilhões de endereços. Com a explosão de dispositivos (IoT, celulares, servidores, GPUs em nuvem), esse espaço **se esgotou**. O **IPv6** usa 128 bits, oferecendo um número praticamente ilimitado de endereços. Em grandes data centers, isso permite endereçar **cada máquina e dispositivo sem NAT**, simplificando roteamento, escalabilidade e conexões ponto a ponto.

**14. TCP vs. UDP — critério de escolha.**
O critério é o **trade-off entre confiabilidade e velocidade**. **TCP** garante **entrega, ordem e integridade** dos dados (com confirmações e retransmissão) — ideal para transferir **datasets e modelos**. **UDP** prioriza **baixa latência**, sem confirmar recebimento — ideal para **telemetria, streaming e métricas em tempo real**, onde perder um pacote isolado não é crítico. Escolhe-se TCP quando a integridade é indispensável; UDP quando a velocidade importa mais que a perda ocasional.

**15. Por que `rsync` é superior ao `scp` para grandes volumes.**
Porque o `rsync` faz **sincronização inteligente**: transfere apenas as **diferenças** entre origem e destino, oferece **retomada de transferências interrompidas** (`--partial`) e compressão (`-z`). Em datasets de centenas de gigabytes, se a conexão cair perto do fim, o `scp` recomeça do zero, enquanto o `rsync` continua de onde parou — economizando **tempo, banda e dinheiro** (crítico para jobs longos em nuvem).

---

#### Aula 6 — Sistemas Operacionais Linux e Gerenciamento de GPU

**16. Função de `/proc` e `/sys`.**
São **sistemas de arquivos virtuais** (pseudo-arquivos que não ocupam disco) que expõem o **estado do kernel e do hardware** em tempo real. Em `/proc` encontram-se informações de CPU (`/proc/cpuinfo`), memória (`/proc/meminfo`) e tempo ligado (`/proc/uptime`); em `/sys` ficam informações de dispositivos, inclusive GPUs (`/sys/class/drm`). Para um servidor de IA, permitem **monitorar recursos sem instalar ferramentas extras**, base para utilities como `htop`, `nvtop` e `gpustat`.

**17. Por que `screen`, `tmux` e `nohup` são essenciais.**
Porque treinamentos de IA podem durar **horas ou dias** via SSH. Se a conexão cair, o processo ligado ao terminal é encerrado e o job é perdido. `screen`/`tmux` mantêm **sessões persistentes no servidor** (o job continua rodando mesmo com a desconexão), e `nohup` permite imunes a *hangups*. Isso garante que um treino de 12 horas não seja interrompido por uma queda de rede.

**18. Utilidade de `cron` + `systemd`.**
O **`cron`** agenda **tarefas periódicas** (ex.: backup noturno, limpeza de checkpoints, download diário de datasets). O **`systemd`** gerencia **serviços contínuos** (ex.: manter uma API de inferência ou um serviço de monitoramento sempre ativo, reiniciando-o em caso de falha). Juntos, automatizam a **rotina de manutenção e operação** de um ambiente produtivo de GPUs, reduzindo intervenção manual e erros.

---

### Bloco 2: Programação

#### Aula 7 — Introdução ao Modelo CUDA

**19. O que é um *kernel* CUDA.**
É uma **função escrita para rodar na GPU**, executada em paralelo por **milhares de threads** diretamente na VRAM. Diferente de uma função comum (que roda na CPU, uma vez), o kernel é "lançado" sobre uma **grade de threads**, e cada thread executa o mesmo código sobre uma parte diferente dos dados.

**20. Como a hierarquia CUDA organiza o problema.**
A GPU organiza a execução em três níveis:
- **Grid (Grade):** o problema completo.
- **Block (Bloco):** subconjunto de threads que pode **compartilhar memória (SRAM)** e sincronizar entre si.
- **Thread:** unidade individual de execução, identificada por índices.

O índice global combina: `idx = blockIdx.x * blockDim.x + threadIdx.x`, onde `blockIdx` identifica o bloco, `blockDim` o tamanho do bloco e `threadIdx` a thread dentro do bloco. Assim, **cada thread mapeia um elemento único** dos dados.

**21. Por que `cuda.synchronize()` é obrigatório.**
Porque o lançamento de kernels é **assíncrono**: a CPU envia o trabalho e **continua** sem esperar a GPU terminar. Se a CPU tentar ler/copiar o resultado antes de a GPU concluir, obterá **dados incompletos ou incorretos**. O `cuda.synchronize()` **bloqueia a CPU até que toda a GPU finalize**, garantindo que o resultado esteja pronto antes de transferi-lo de volta à memória da CPU.
