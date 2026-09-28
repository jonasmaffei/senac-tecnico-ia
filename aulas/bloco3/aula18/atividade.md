# 📝 Atividade Prática: Aula 18 — Gestão de Processos e Carga de Trabalho

---

## 🎯 Situação de Aprendizagem

O laboratório tem **1 GPU** e **4 alunos** que precisam treinar modelos ao mesmo tempo. Sem controle, os jobs concorrem pelo mesmo recurso, corrompem resultados e causam `CUDA Out of Memory (OOM)`. O time precisa de um sistema de fila automatizado com suporte a prioridade: jobs de alta prioridade executam primeiro, outros aguardam na fila — tudo via scripts Bash com `flock` e `systemd`, sem precisar de software externo como Slurm ou Kubernetes.

---

## 🗂️ Roteiro de Execução

Você pode realizar esta atividade no **Google Colab** ou localmente no **Windows Host**.

| Ambiente | Onde abrir | Como executar |
| :--- | :--- | :--- |
| **Google Colab** | [`notebook_colab/aula18_processos_fila.ipynb`](notebook_colab/aula18_processos_fila.ipynb) | Execute as células no Colab para ver os jobs executando em série |
| **Windows Host** | [`laboratorio_windows/iniciar.bat`](laboratorio_windows/iniciar.bat) | Dê duplo clique no `iniciar.bat` no seu computador |

---

## 🚀 Parte 1 — Exclusão Mútua Simples com `flock`

1. Execute o script de exclusão mútua (`1_flock_gpu.py` no Windows ou `flock_gpu.sh` no Linux).
2. Tente abrir dois terminais simultâneos e lançar o script ao mesmo tempo.
3. Observe como o segundo processo aguarda a liberação do *lock* do primeiro sem causar colisões de VRAM.

---

## 📊 Parte 2 — Teste da Fila Concorrente com Prioridade

1. Execute a simulação da fila concorrente com 4 jobs simultâneos (`3_teste_fila.py` no Windows ou `./teste_fila.sh` no Linux).
2. Observe o comportamento dos 4 jobs:
   - `Job-Alta-A` (Prioridade 1)
   - `Job-Baixa-B` (Prioridade 3)
   - `Job-Media-C` (Prioridade 2)
   - `Job-Alta-D` (Prioridade 1)
3. Confirme que os jobs de prioridade 1 executam primeiro, seguidos pelos de prioridade 2 e 3, independentemente da ordem em que foram disparados.

---

## 🔍 Parte 3 — Monitoramento de Processos ao Vivo

1. Enquanto a fila estiver em execução, utilize a ferramenta de monitoramento (`4_monitor_processos_gpu.py` no Windows ou `monitor_processos_gpu.sh` no Linux).
2. Verifique os PIDs ativos, o status da GPU e os arquivos de ticket presentes na pasta de spool da fila.

---

## 💬 Parte 4 — Discussão em Grupo (10 min)

Em grupos de 3 a 4 alunos, discutam:

1. O sistema de fila com `flock` é FIFO dentro de cada prioridade. Se um job de alta prioridade demorar 8 horas, jobs de prioridade média nunca executam (*Starvation*). Como resolver?
2. `flock` funciona apenas no mesmo servidor. Para um cluster com 10 nós GPU, como você escalonaria a solução? Compare com SLURM, Kubernetes e Ray.
3. Um job malicioso pode deletar o arquivo de lock e "roubar" a GPU. Como tornar o sistema mais seguro? (Dica: pesquise sobre permissões de arquivos e grupos Linux).
4. `systemd` com `Type=simple` não detecta quando o processo Python trava em deadlock sem usar CPU. Como monitorar e agir automaticamente nesses casos?

---

## 📌 Parte 5 — Tarefa de Casa

1. Execute o `teste_fila.sh` com 4 jobs e observe a ordem de execução por prioridade.
2. Adicione um 5° job com prioridade 1 após 30 segundos — verifique se ele "passa à frente" dos jobs de prioridade 2 e 3.
3. **Bônus:** Implemente a lógica de *Aging*: jobs aguardando há mais de 10 minutos sobem automaticamente de nível de prioridade na fila.
