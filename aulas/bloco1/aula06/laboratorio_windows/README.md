# Laboratório Windows — Linux e GPU (hardware real)

Experimentos com o **hardware real** da máquina do laboratório (AMD/Windows), aplicando os
conceitos da Aula 06: inspecionar hardware, ler o estado da GPU, criar um alerta de temperatura
e automatizar a coleta.

> Este laboratório roda no **Git Bash**. Ele usa a **GPU AMD real** do Windows através dos
> contadores de desempenho (via PowerShell inline, sem `.ps1`).

---

## 🚀 Como rodar

> **Pré-requisito do passo [4]:** o `monitoramento_linux.py` usa `psutil`. Se ele reclamar,
> instale uma vez com: `pip install psutil`. Os passos [1]–[3] usam só o Git Bash (nada a
> instalar).

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat):

```
[1] 1_inspecionar.sh  - conhecer o hardware e a GPU
[2] 2_status_gpu.sh   - status + alerta de temperatura
[3] 3_agendar.sh      - agendamento (simula o cron)
[4] monitoramento_linux.py - CPU/RAM/GPU via Python
[0] Sair
```

Ou, no terminal (Git Bash, dentro desta pasta):

```bash
bash 1_inspecionar.sh
bash 2_status_gpu.sh                 # alerta padrão: 80°C
bash 3_agendar.sh 5 1                # 5 coletas a cada 1 segundo
```

---

## 🗂️ Arquivos

| Arquivo | O que faz |
| :--- | :--- |
| `lib_gpu06.sh` | Funções compartilhadas: cores, detecção de backend e **leitura real da GPU** (AMD/Windows, NVIDIA ou simulado). |
| `1_inspecionar.sh` | Mostra SO, `/proc` (quando existe), `lspci` e a leitura da GPU. |
| `2_status_gpu.sh` | Status por GPU + **alerta** acima de `LIMITE_TEMP` (código de saída 1 se alertar). |
| `3_agendar.sh` | Coleta em vários instantes e grava histórico em `reports/historico_gpu.csv`. |
| `monitoramento_linux.py` | Versão Python: lê `/proc` e `/sys` no Linux ou o equivalente no Windows (psutil). |
| `iniciar.bat` | Menu (duplo clique). |

> Os scripts `1_…`, `2_…`, `3_…` **importam** `lib_gpu06.sh` (`source`) — a lógica de GPU fica
> num lugar só. Este laboratório é **autocontido**: tudo o que ele usa está nesta pasta.

---

## 🎛️ Forçando cenários (para testar sem depender do hardware)

| Objetivo | Comando |
| :--- | :--- |
| Simular uma GPU (com temperatura 54°C) | `GPU06_BACKEND=simulado bash 2_status_gpu.sh` |
| Forçar o alerta de temperatura | `GPU06_BACKEND=simulado LIMITE_TEMP=1 bash 2_status_gpu.sh` |

> No **Windows/AMD** a temperatura normalmente aparece como **`N/A`** — o Windows não a expõe
> de forma simples. O script **mostra `N/A` honestamente** em vez de inventar um valor. Para
> testar o alerta de verdade, use o backend simulado (acima).

---

## 🔎 O que observar

- **Backend detectado:** `AMD no Windows` nesta máquina; `NVIDIA`/`AMD Linux` no servidor.
- **VRAM em uso** e **utilização (%)** variam conforme outros programas rodam.
- O histórico em `reports/historico_gpu.csv` é **incremental** — rode o `3_agendar.sh` mais de
  uma vez e veja as linhas se acumularem.

---

## 🧹 Saídas

Tudo é gerado em `reports/` (criada automaticamente). O `.gitignore` ignora o conteúdo — só o
`.gitkeep` é versionado.

---

## 🔗 Relação com a aula

- Coloca em prática a trilha: **inspecionar → visualizar → alertar → agendar**.
- O `2_status_gpu.sh` é a versão didática do `scripts/gpu_status.sh` (mais completo, para
  servidor Linux).
- O `iniciar.bat` implementa o padrão de laboratório (`.context.md`, §6.9 e §6.16).
