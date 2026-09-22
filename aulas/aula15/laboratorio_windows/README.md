# 🖥️ Laboratório Windows — Gestão de Processos e Fila de GPU (Aula 15)

Pasta autocontida para rodar a **Aula 15** no laboratório com **Windows + Git Bash**,
sem instalar Docker, Slurm nem Kubernetes. Reproduz o cenário: **1 GPU e vários jobs
concorrendo** — com fila por prioridade e exclusão mútua.

> 🎯 **Situação de aprendizagem:** o laboratório tem **1 GPU** e **4 alunos** que
> precisam treinar ao mesmo tempo. Sem controle, os jobs competem pela VRAM, corrompem
> resultados e causam **OOM**. A solução é uma **fila com prioridade** usando só Bash.

---

## ⚠️ Ajuste para Windows (importante)

O material original da aula usa comandos **Linux** (`flock`, `systemd`, `nvidia-smi`).
Eles **não existem no Git Bash do Windows**. Este laboratório adapta a aula **sem
perder os conceitos**:

| Conceito | No Linux | Aqui (Windows/Git Bash) |
| :--- | :--- | :--- |
| Exclusão mútua | `flock -x` | **lock por diretório** (`mkdir` atômico) — e usa `flock` real quando existe |
| Monitor de GPU | `nvidia-smi` | **contadores de desempenho do Windows** (GPU AMD) via PowerShell inline |
| Agendamento | `cron` / `systemd` | **Agendador de Tarefas** do Windows (+ crontab mostrado como referência) |
| Prioridade | `nice` / `ionice` | mostrados como teoria; a prioridade aqui é **na fila de jobs** |

> ✅ **Apenas arquivos `.sh`.** Nada de `.ps1`: a leitura da GPU é um comando
> **inline** do PowerShell (`-EncodedCommand`), imune à `ExecutionPolicy` do laboratório.

---

## 📋 Pré-requisitos

| Item | Situação |
| :--- | :--- |
| **Git para Windows** (traz o Git Bash) | [git-scm.com/download/win](https://git-scm.com/download/win) |
| **Python** (para o `train_job.py`) | [python.org](https://www.python.org/downloads/) — marque "Add to PATH" |
| GPU AMD / NVIDIA | Opcional — sem GPU, entra em **modo simulado** |
| Docker / systemd | ❌ não precisa |

---

## 🚀 Passo a passo

### 1. Abrir o Git Bash na pasta

No Explorer, entre em `aulas\aula15\laboratorio_windows`, clique com o botão direito e
escolha **"Open Git Bash here"**.

### 2. Dar permissão de execução (só na primeira vez)

```bash
chmod +x *.sh
```

### 3. Rodar o teste da fila (o experimento principal)

```bash
./teste_fila.sh
```

Ele lança **4 jobs em paralelo** com prioridades diferentes:

| Job | Prioridade |
| :--- | :--- |
| Job-Alta-A | 1 (alta) |
| Job-Baixa-B | 3 (baixa) |
| Job-Media-C | 2 (média) |
| Job-Alta-D | 1 (alta) |

**Ordem esperada:** `Alta-A → Alta-D → Media-C → Baixa-B`. Os jobs executam **um por
vez** (lock da GPU), e a prioridade decide quem passa primeiro — veja o log em
`reports/fila.log`.

### 4. Monitorar em tempo real

Em outro terminal Git Bash:

```bash
./monitor_gpu_proc.sh
```

Mostra a cada 3 s: quem usa a GPU, o resumo da placa, o estado da fila e o dono do lock.

---

## 🧩 Scripts disponíveis

| Script | O que faz | Exemplo |
| :--- | :--- | :--- |
| `teste_fila.sh` | Lança 4 jobs e mostra a fila serializando | `./teste_fila.sh` |
| `fila_gpu.sh` | Enfileira 1 job com prioridade (1 alta … 3 baixa) | `./fila_gpu.sh 1 MeuJob "python train_job.py --nome MeuJob --epocas 3"` |
| `flock_gpu.sh` | Exclusão mútua simples (1 comando por vez) | `./flock_gpu.sh "python train_job.py --epocas 2"` |
| `monitor_gpu_proc.sh` | Monitor de processos/GPU/fila | `./monitor_gpu_proc.sh 5 2` |
| `agendar.sh` | Simula o cron e mostra systemd/Agendador | `./agendar.sh` |
| `train_job.py` | Job de "treino" simulado (sem precisar de CUDA) | `python train_job.py --nome A --epocas 3` |
| `lib_gpu15.sh` | Funções internas (lock + leitura da GPU) | — (carregado pelos outros) |

---

## 🔑 Como funciona a fila (e o lock)

### Fila por prioridade
Cada job cria um **ticket** na pasta `reports/fila/` com o nome:

```
<prioridade>_<timestamp>_<nome>
```

Como o `sort` é alfabético, **`1_...` vem antes de `2_...` antes de `3_...`**. Dentro
da mesma prioridade, o _timestamp_ desempata (FIFO). O job espera até o seu ticket ser
o primeiro da lista.

### Exclusão mútua (lock)
O lock é um **diretório** em `reports/locks/gpu.lock`. Criar diretório é uma operação
**atômica**: se dois processos tentam juntos, só um consegue. É o mesmo princípio do
`flock -x`. Existe também **limpeza de lock obsoleto**: se o dono morreu (job
interrompido), o lock é detectado via `kill -0` e removido.

> 🐧 Em **Linux/WSL**, onde o `flock` existe, o `lib_gpu15.sh` usa o `flock` real
> automaticamente — o mesmo script roda nos dois mundos.

---

## ⚡ Controle de prioridade Linux (`nice` / `ionice`)

Quando a fila não for suficiente (ex.: jobs que já estão rodando), o Linux permite
ajustar a prioridade do processo:

```bash
nice -n 19 python3 train.py      # menor prioridade de CPU
ionice -c 3 python3 train.py     # idle I/O (não bloqueia o disco)
renice -n -5 -p PID              # aumentar a prioridade de um job em curso
```

No Windows esses comandos não existem — por isso o laboratório foca a **prioridade na
fila** (quem entra primeiro no lock).

---

## ⏰ Agendamento

No Git Bash **não há `cron`/`systemd`**. O `agendar.sh` simula as execuções e mostra:

- as linhas de **crontab** para um servidor Linux real;
- um **unit systemd** (`gpu-job@.service`) para produção;
- o comando `schtasks` para o **Agendador de Tarefas** do Windows.

---

## 📂 Arquivos gerados (em `reports/`)

| Caminho | Descrição |
| :--- | :--- |
| `reports/fila/` | Tickets dos jobs aguardando (ordem de execução) |
| `reports/locks/` | Diretório de lock da GPU |
| `reports/fila.log` | Histórico de enfileiramento e execução |

> Não precisam ir para o Git (já ignorados). Para limpar tudo: apague `reports/fila/` e
> `reports/locks/`.

---

## 🔧 Solução de problemas

| Problema | Causa provável | Solução |
| :--- | :--- | :--- |
| `Permission denied` | Falta permissão de execução | `chmod +x *.sh` |
| `bad interpreter ... ^M` | Arquivo salvo com CRLF | `sed -i 's/\r$//' *.sh` |
| `python não é reconhecido` | Python fora do PATH | Reinstale marcando "Add to PATH" |
| Fila nunca anda | Lock obsoleto de um job morto | O script limpa sozinho; se persistir, `rm -rf reports/locks/*` |
| Backend `simulado` numa máquina AMD | PowerShell indisponível | Reabra o **Git Bash** (não o WSL) |
| `flock: command not found` | É esperado no Windows | O lib usa lock por diretório automaticamente |

---

## 🎓 Relação com a aula

```
nvidia-smi / contadores AMD        fila_gpu.sh          reports/fila/
 (processos na GPU)         →      (locks + fila)  →    (ordem de execução)
        ▲                              │
        └──── monitor_gpu_proc.sh ─────┘
             (tempo real)
```

- **`flock -x`** → `lock_adquirir` (flock real ou lock por diretório).
- **`nvidia-smi pmon`** → `monitor_gpu_proc.sh` (contadores do Windows).
- **`cron`/`systemd`** → `agendar.sh` + Agendador de Tarefas.

### Desafios (tarefa de casa)
1. Adicione um 5º job com prioridade 1 **depois de 30 s** e confirme que ele "fura"
   a fila dos de prioridade 2 e 3.
2. Implemente **aging**: jobs esperando > 10 min sobem automaticamente de prioridade.
3. Integre o `monitor_gpu_proc.sh` ao pipeline de monitoramento da Aula 14.
