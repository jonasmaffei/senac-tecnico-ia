# 🤖 Aula 18 — Gestão de Processos e Carga de Trabalho em GPU

**Objetivo:** gerenciar execuções concorrentes em GPU usando `flock` para exclusão mútua, implementar sistemas de fila com prioridade, monitorar processos em tempo real com `nvidia-smi` e `systemd`, garantindo uso justo e eficiente da GPU em ambientes multiusuário.

---

## 🎯 Situação de Aprendizagem

O laboratório tem **1 GPU** e **4 alunos** que precisam treinar modelos ao mesmo tempo. Sem controle, os jobs concorrem pelo mesmo recurso, corrompem resultados e causam `CUDA Out of Memory (OOM)`. O time precisa de um sistema de fila automatizado com suporte a prioridade: jobs de alta prioridade executam primeiro, outros aguardam na fila — tudo via scripts Bash com `flock` e `systemd`, sem precisar de software externo como Slurm ou Kubernetes.

---

## 🗂️ Conteúdo da Aula

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula18.html`](apresentacao_aula18.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`atividade.md`](atividade.md) | Roteiro prático, tópicos de discussão em grupo e tarefa de casa |
| [`notebook_colab/aula18_processos_fila.ipynb`](notebook_colab/aula18_processos_fila.ipynb) | Notebook Google Colab com 5 exercícios práticos |
| [`laboratorio_windows/`](laboratorio_windows/) | Laboratório local para executar no host Windows via `iniciar.bat` |
| [`scripts_linux/`](scripts_linux/) | Scripts Bash e Python para servidores Linux (`flock_gpu.sh`, `gpu_queue.sh`, `train_job.py`, `teste_fila.sh`, `monitor_processos_gpu.sh`) |

---

## 🗂️ Estrutura da Pasta

```
aula18/
├── apresentacao_aula18.html
├── README.md
├── atividade.md
├── notebook_colab/
│   └── aula18_processos_fila.ipynb
├── laboratorio_windows/
│   ├── 1_flock_gpu.py
│   ├── 2_gpu_queue.py
│   ├── 3_teste_fila.py
│   ├── 4_monitor_processos_gpu.py
│   ├── iniciar.bat
│   ├── requirements.txt
│   ├── train_job.py
│   └── README.md
└── scripts_linux/
    ├── flock_gpu.sh
    ├── gpu_queue.sh
    ├── monitor_processos_gpu.sh
    ├── teste_fila.sh
    └── train_job.py
```

---

## 🚀 Como Usar

### Option A — No Google Colab
Abra o notebook em [`notebook_colab/aula18_processos_fila.ipynb`](notebook_colab/aula18_processos_fila.ipynb), execute a demonstração e resolva a seção **7. Exercícios Práticos (5)**.

### Option B — No Windows Host (Local)
Navegue até a pasta `laboratorio_windows/` e dê duplo clique no arquivo `iniciar.bat`. Escolha a opção **3** para disparar 4 jobs simultâneos e acompanhar a serialização por prioridade.

---

## 🔑 Conceitos-chave

- **Race Condition** — Colisão de memória e GPU quando múltiplos processos tentam alocar a VRAM ao mesmo tempo.
- **`flock` (Mutex)** — Trava de arquivo para garantir exclusão mútua simples (1 job por vez).
- **Fila com Prioridade** — Organização de tickets (`prioridade_timestamp_job`) onde números menores rodam primeiro.
- **Starvation & Aging** — Prevenção do bloqueio perpétuo de jobs de baixa prioridade.
- **`systemd units`** — Isolamento de serviços com limites de CPU, memória e relançamento automático.
