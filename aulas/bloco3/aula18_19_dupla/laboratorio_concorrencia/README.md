# 🖥️ Laboratório Windows: Concorrência e Fila (Aula 18+19)

Este laboratório permite testar o controle de concorrência, exclusão mútua e filas por prioridade em execuções de GPU diretamente no hospedeiro Windows (sem necessitar de `flock` nativo do Linux ou permissões root de servidor).

---

## 🗂️ Estrutura da Pasta

```
laboratorio_windows/
├── iniciar.bat                  # Menu interativo do laboratório
├── requirements.txt             # Dependência (psutil)
├── train_job.py                 # Script Python de treinamento simulado
├── 1_flock_gpu.py               # Exclusão mútua atômica via lock por diretório (mkdir)
├── 2_gpu_queue.py               # Enfileiramento com suporte a prioridade (1=Alta, 2=Média, 3=Baixa)
├── 3_teste_fila.py              # Lança 4 jobs simultâneos para validar a serialização por prioridade
├── 4_monitor_processos_gpu.py   # Diagnóstico de PIDs ativos, lock e tickets na fila
└── README.md                    # Este guia
```

---

## 🚀 Como Executar

1. Dê duplo clique no `iniciar.bat`.
2. O script criará o ambiente virtual `.venv`, instalará `psutil` e exibirá o menu de opções.
3. Escolha a **Opção 3 (Testar Fila Concorrente de 4 Jobs)** para ver os jobs de prioridade 1 executando antes dos de prioridade 2 e 3 de maneira automatizada!
