# 🎛️ Aula 15 — Gestão de Processos e Carga de Trabalho

**Objetivo:** gerenciar execuções concorrentes em GPU com Bash, usando **exclusão
mútua** (`flock`/lock), **filas com prioridade**, **monitoramento de processos em
tempo real** e **agendamento** — garantindo uso justo e eficiente da GPU em ambientes
multiusuário, sem depender de Slurm ou Kubernetes.

---

## 🎯 Situação de aprendizagem

O laboratório tem **1 GPU** e **4 alunos** que precisam treinar modelos ao mesmo tempo.
Sem controle, os jobs concorrem pelo mesmo recurso, **corrompem resultados** e causam
**OOM** (Out of Memory). A solução é uma **fila automatizada com prioridade**: jobs de
alta prioridade executam primeiro, os demais aguardam — tudo com **Bash** e um **lock**
de exclusão mútua.

```
[08:00:00] Job-A inicia — aloca 6 GB VRAM
[08:00:01] Job-B inicia — aloca 6 GB VRAM
[08:00:02] Job-A: CUDA OOM — apenas 2 GB livres!
[08:00:02] Job-B: CUDA OOM — crash silencioso
[08:00:10] Com o lock: jobs executam 1 por vez, sem conflito
```

---

## 🗂️ Conteúdo

| Arquivo | O que é |
| :--- | :--- |
| [`apresentacao_aula15.html`](apresentacao_aula15.html) | Slides teóricos da aula (abra no navegador, navegue com ← →) |
| [`laboratorio_windows/README.md`](laboratorio_windows/README.md) | Laboratório prático em **Windows + Git Bash** (adaptado à GPU AMD) |

---

## 🚀 Laboratório (Windows + Git Bash)

```bash
cd aulas/aula15/laboratorio_windows
chmod +x *.sh
./teste_fila.sh          # lança 4 jobs e mostra a fila serializando por prioridade
./monitor_gpu_proc.sh    # (outro terminal) monitora GPU, processos e fila em tempo real
```

Detalhes, tabela de scripts e solução de problemas em
[`laboratorio_windows/README.md`](laboratorio_windows/README.md).

---

## 🔑 Conceitos-chave

- **Race condition** — múltiplos jobs competindo pela mesma VRAM/GPU → OOM e resultados corrompidos.
- **Mutex / Lock** — `flock` (Linux) ou **lock por diretório** (portátil): 1 job por vez.
- **Fila FIFO** — tickets ordenados por `prioridade_timestamp_nome`.
- **Prioridade de job** — `1` alta, `2` média, `3` baixa; empates em FIFO.
- **nice / ionice** — ajuste de prioridade de CPU/IO no Linux.
- **systemd** — isolamento, logging e restart automático (produção).

### `flock` — flags principais

| Flag | Significado | Uso típico |
| :--- | :--- | :--- |
| `-x` | Lock exclusivo (padrão) | Acesso exclusivo à GPU |
| `-s` | Lock compartilhado | Leitura simultânea de métricas |
| `-n` | Non-blocking (falha rápida) | Verificar se a GPU está livre |
| `-w N` | Timeout em N segundos | Desistir se demorar muito |
| `-u` | Liberar lock manualmente | Cleanup em `trap` de sinal |

### flock vs. systemd

| | `flock` | `systemd` |
| :--- | :--- | :--- |
| Melhor para | Scripts ad-hoc, laboratório | Produção, multiusuário |
| Vantagens | Sem root, setup em 5 min | Logging, restart, cgroups, auditoria |

---

## 💡 Síntese

- **`flock -x`**: exclusão mútua — base do controle de concorrência em Bash.
- **Fila por arquivo**: `ticket = prioridade + timestamp` → ordenação automática.
- **`nvidia-smi pmon`**: monitora processos e VRAM por PID em tempo real.
- **`nice` / `ionice`**: prioridade de CPU e I/O de um processo.
- **systemd unit**: isolamento com logging e restart por job.
- **starvation**: jobs de baixa prioridade que nunca executam — exige **aging**.

---

## 📌 Tarefa de casa

1. Execute `teste_fila.sh` com 4 jobs e observe a ordem por prioridade.
2. Adicione um 5º job de **prioridade 1 depois de 30 s** e verifique se ele "passa à
   frente" dos de prioridade 2 e 3.
3. Integre o monitor (`monitor_gpu_proc.sh`) ao sistema de fila da Aula 14.
4. **Bônus:** implemente **aging** — jobs aguardando mais de 10 minutos sobem de
   prioridade automaticamente.
