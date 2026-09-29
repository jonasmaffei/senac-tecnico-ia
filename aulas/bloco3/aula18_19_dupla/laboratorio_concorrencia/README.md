# 🖥️ Laboratório Windows: Concorrência e Fila (Aula 18+19)

Este laboratório permite testar o controle de concorrência, exclusão mútua e filas por
prioridade na GPU diretamente no **Windows**, sem precisar do `flock` do Linux nem de
permissões de root.

---

## 🗂️ Arquivos

```
laboratorio_concorrencia/
├── iniciar.bat                    # Menu interativo (duplo clique)
├── requirements.txt               # Dependência (psutil)
├── monitor_fila.py                # Lê o estado da GPU/lock/fila (módulo compartilhado)
├── train_job.py                   # Job de "treino" simulado
├── 1_flock_gpu.py                 # Exclusão mútua: lock por diretório (mkdir atômico)
├── 2_gpu_queue.py                 # Enfileira 1 job com prioridade (1=alta, 2=média, 3=baixa)
├── 3_teste_fila.py                # Teste: 4 jobs concorrentes COM monitor ao vivo
├── 4_monitor_processos_gpu.py     # Monitor da GPU/lock/fila (foto ou ao vivo)
└── README.md                      # Este guia
```

---

## 🚀 Como executar

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat). Na primeira vez ele cria o `.venv` e
instala o `psutil`. Depois aparece o menu:

| Opção | O que faz |
| :---: | :--- |
| **1** | Testa a exclusão mútua simples (`1_flock_gpu.py`) |
| **2** | Enfileira 1 job de prioridade alta (`2_gpu_queue.py`) |
| **3** | **Teste completo:** lança 4 jobs concorrentes **e mostra a GPU/fila ao vivo** |
| **4** | Monitora GPU, lock e fila por 15 s (`4_monitor_processos_gpu.py 15 1`) |
| **5** | Sair |

> 💡 **O que ver na opção 3:** os 4 jobs são lançados ao mesmo tempo, mas executam **um de cada
> vez** (a GPU fica `OCUPADA` e a fila vai diminuindo). No fim, o script imprime a **ordem real**
> de execução: os jobs de prioridade 1 primeiro, depois 2 e por último 3.

---

## 🔍 Os scripts de monitoramento

- **`monitor_fila.py`** — módulo que lê: processos de treino ativos, se o lock está ativo
  (GPU ocupada) e quantos tickets há na fila.
- **`4_monitor_processos_gpu.py`** — usa esse módulo e aceita dois modos:

  ```bat
  python 4_monitor_processos_gpu.py            :: uma foto (estado atual)
  python 4_monitor_processos_gpu.py 15 1       :: monitora por 15s, 1 leitura/s
  ```

> 🧪 Para ver o monitor em ação com a fila se movendo, use a **opção 3** (que já integra os
> dois) ou rode o `4` numa janela enquanto o `3` roda em outra.

---

## 📂 Saídas (`reports/`)

- `gpu_exclusive.lockdir/` — o "lock" (pasta que indica GPU ocupada);
- `gpu_queue_spool/` — os tickets na fila;
- `gpu_queue.log` — histórico de enfileiramento e execução.

---

## 🧠 O que este laboratório demonstra

- **Exclusão mútua:** criar uma pasta (`mkdir`) é atômico — só um job "pega a chave".
- **Fila por prioridade:** o ticket `prioridade_timestamp_nome` ordena a execução.
- **Sem OOM:** com um job por vez, a VRAM não estoura.
- **Observabilidade:** dá para ver, em tempo real, quem está na GPU e quem espera.
