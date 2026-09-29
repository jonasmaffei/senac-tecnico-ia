# 🐍 Aula 18 — Gestão de Fila em GPU: versão enxuta (complemento da Aula 15)

**Objetivo:** revisar os mecanismos de **exclusão mútua** e **fila com prioridade** da
**Aula 15** numa versão **enxuta**, com um **laboratório em Python cross-platform** que usa
**lock por diretório** em vez de `flock`/`systemd`.

> 📌 **Não é conteúdo novo.** Esta aula é um **complemento prático** da
> [Aula 15](../aula15/README.md). **Veja a Aula 15 primeiro.** Aqui o valor está em:
> (a) uma **demonstração enxuta no Colab** e (b) um **laboratório em Python** que resolve o
> mesmo problema **sem `flock`**, rodando no Windows.

---

## 🎯 Situação de aprendizagem

O laboratório tem **1 GPU** e **4 alunos** treinando ao mesmo tempo. Sem controle, os jobs
concorrem pela VRAM e causam **OOM**. A Aula 15 resolveu isso com `flock` + fila em Bash;
agora a equipe quer a **mesma solução em Python**, que roda em qualquer sistema —
inclusive no Windows do laboratório.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula18.html`](apresentacao_aula18.html) | Slides **só conceito** (foco na versão Python; navegue com ← →) |
| [`atividade.md`](atividade.md) | Roteiro prático e discussão |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** (demo enxuta + 5 exercícios) |
| [`laboratorio_windows/`](laboratorio_windows/README.md) | **Versão Python** (lock por diretório + fila por prioridade, **sem Bash**) |

### Estrutura da aula

```
aula18/
  apresentacao_aula18.html
  README.md
  notebook_colab/aula18_processos_fila.ipynb
  laboratorio_windows/          # 1_flock_gpu.py, 2_gpu_queue.py, 3_teste_fila.py, 4_monitor_processos_gpu.py
  atividade.md
```

> 🧩 **Bash vs. Python:** a versão **Bash** (`flock`, `gpu_queue.sh`, `systemd`) vive na
> **Aula 15** (`laboratorio_windows/`) e é a padrão para servidores Linux. O **notebook** desta
> aula demonstra os mesmos scripts no Colab (que é Linux); o **laboratório** mostra a
> alternativa **100% Python** — **lock por diretório** (`os.mkdir`, atômico) e fila por
> prioridade (ticket `prioridade_timestamp_nome`) — que roda até no Windows sem Bash.

---

## 🚀 Como usar

### No Google Colab

Abra `notebook_colab/aula18_processos_fila.ipynb` e resolva a seção **Exercícios (5)**.

### No Windows (host local)

Dê **duplo clique** em [`laboratorio_windows/iniciar.bat`](laboratorio_windows/iniciar.bat) e
escolha a opção que lança **4 jobs simultâneos** para ver a serialização por prioridade.

---

## 🔑 Conceitos-chave

- **Exclusão mútua sem `flock`** — `os.mkdir` é atômico: só um processo cria o diretório-lock.
- **Fila por prioridade** — ticket `prioridade_timestamp_nome`, ordenado por `sort`.
- **`nice`/`ionice`** — prioridade de CPU/IO, complementar à prioridade de entrada na GPU.
- **Monitoramento de processos** — `psutil` no lugar do `nvidia-smi pmon`.

---

## 🔗 Relação com o curso

- **Aula 15** é a referência do tema (versão **Bash/Linux** com `flock`/`systemd`). Esta aula
  **não substitui** — mostra a **alternativa Python cross-platform**.
- **Próxima (Aula 19):** energia — fechar o Bloco 3 otimizando o consumo das GPUs.
