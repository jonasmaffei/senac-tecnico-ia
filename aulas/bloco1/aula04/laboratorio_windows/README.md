# Laboratório Windows — Fundamentos de Processos e Threads (hardware real)

Experimentos com o **hardware real** da máquina do laboratório, aplicando os conceitos da Aula
04: o **GIL** do Python, a diferença entre **processos** e **threads**, a hierarquia de threads
da GPU e o monitoramento de processos.

---

## 🚀 Como rodar

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat):

```
[1] 1_processos_threads.py  - sequencial vs. threading vs. multiprocessing
[2] 2_io_bound.py           - quando threading ajuda (I/O)
[3] 3_kernels_cuda.py       - blocos e threads na GPU (conceito sem GPU)
[4] 4_monitor_processos.py  - processos/threads como o htop
[0] Sair
```

Ou pelo terminal:

```bat
python 1_processos_threads.py
python 2_io_bound.py
python 4_monitor_processos.py
```

---

## 🗂️ Arquivos

| Arquivo | O que faz |
| :--- | :--- |
| `1_processos_threads.py` | Compara sequencial, threading (GIL) e multiprocessing numa tarefa CPU-bound. |
| `2_io_bound.py` | Mostra que threading **ajuda** em tarefas de I/O (o GIL é liberado). |
| `3_kernels_cuda.py` | Configuração de blocos/threads na GPU (Numba/CUDA) — sem GPU, mostra referência. |
| `4_monitor_processos.py` | Lista processos/threads e o uso de CPU (como o `htop`). |
| `iniciar.bat` | Menu (duplo clique). |

---

## 🔎 O que observar

- **CPU-bound:** o threading empata com o sequencial (GIL), mas o **multiprocessing acelera**
  de verdade (usa vários núcleos).
- **I/O-bound:** o threading ganha — as threads esperam em paralelo.
- **Núcleos:** o `4_monitor_processos.py` usa `psutil` (opcional) para listar os processos.

> Rode o `1_processos_threads.py` e observe no **Gerenciador de Tarefas** (aba Desempenho →
  CPU) o multiprocessing acender **vários núcleos**, enquanto o threading mantém **um** ocupado.

---

## 🔗 Relação com a aula

- Demonstra na prática a regra **CPU-bound → processos; I/O-bound → threads**.
- O `3_kernels_cuda.py` conecta à **hierarquia da GPU** (Thread → Warp → Bloco → Grid).
- Segue o padrão de laboratório do curso (`.context.md`, §6.9 e §6.16).
