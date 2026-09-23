# 🧠 Aula 04 — Fundamentos de Processos e Threads

**Objetivo:** distinguir **processos** e **threads** em ambientes CPU e GPU, e aplicar esse
conhecimento para projetar pipelines de IA eficientes, paralelos e escaláveis.

---

## 🎯 Situação de aprendizagem

A startup de reconhecimento facial está desenvolvendo um pipeline de treinamento de IA que
precisa escalar em **múltiplos núcleos de CPU** (para pré-processar imagens) e em
**milhares de threads de GPU** (para treinar o modelo). Para isso, você precisa entender a
fundo como processos e threads funcionam — tanto na CPU quanto na GPU — e como evitar
problemas como **condições de corrida**, **deadlocks** e **subutilização de hardware**.

---

## 🗂️ Conteúdo

| Arquivo | O que é |
| :--- | :--- |
| [`apresentacao_aula04.html`](apresentacao_aula04.html) | Slides teóricos (abra no navegador, navegue com ← →) |
| [`aula04_processos_threads.ipynb`](aula04_processos_threads.ipynb) | Notebook do **Google Colab** (CPU-bound, I/O-bound, kernels CUDA) |
| [`atividade.md`](atividade.md) | Atividade guiada (medir paralelismo) + discussão em grupo |
| `scripts/` | Scripts comentados que rodam no **Colab** e no **Windows** |

### Scripts

| Script | O que faz |
| :--- | :--- |
| [`processos_threads.py`](scripts/processos_threads.py) | Sequencial vs. threading vs. multiprocessing (CPU-bound) |
| [`io_bound.py`](scripts/io_bound.py) | Threading num cenário I/O-bound (onde ele ajuda) |
| [`kernels_cuda.py`](scripts/kernels_cuda.py) | Blocos/threads na GPU + grid 2D (conceito sem GPU) |
| [`monitor_processos.py`](scripts/monitor_processos.py) | Processos/threads como o htop, em Python |

---

## 🚀 Como rodar

### No Google Colab (recomendado)

1. Abra `aula04_processos_threads.ipynb` pelo **GitHub** no Colab
   (`https://github.com/jonasmaffei/senac-tecnico-ia`).
2. *Runtime ➔ Change runtime type ➔ **T4 GPU*** ➔ *Save* (para a parte de CUDA).
3. Rode as células na ordem.

> 💡 **Sem GPU?** O notebook detecta e mostra os números de referência para warps/blocos —
> as partes de CPU (threading/multiprocessing) rodam normalmente.

### No Windows do laboratório

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat). Ele cria o ambiente virtual (`.venv`),
instala as dependências de [`requirements.txt`](requirements.txt) e abre um **menu**:

```
[1] processos_threads.py  - sequencial vs. threading vs. multiprocessing
[2] io_bound.py           - quando threading ajuda (I/O)
[3] kernels_cuda.py       - blocos e threads na GPU (conceito sem GPU)
[4] monitor_processos.py  - processos/threads como o htop
[0] Sair
```

Quem preferir o terminal:

```bat
cd aulas\aula04
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe scripts\processos_threads.py
```

> Os scripts de CPU usam apenas a biblioteca padrão. `psutil` (opcional) mostra CPU e
> processos; `numba` (opcional) é usado só no exercício de kernels CUDA.

---

## 🔑 Conceitos-chave

### Processo vs. Thread

| Critério | Processo | Thread |
| :--- | :--- | :--- |
| Memória | **Isolada** por processo | **Compartilhada** |
| Criação | Lenta (*fork*) | Rápida |
| Comunicação | IPC (overhead) | Direta (risco de *race condition*) |
| Falha isolada | Sim (não afeta outros) | Não (pode derrubar o pai) |
| GIL Python | Contorna | Afeta em CPU-bound |
| Melhor para | **CPU-bound** | **I/O-bound** |

### O GIL do Python

O **Global Interpreter Lock** é um mutex que permite apenas **uma thread Python** executar
bytecode por vez — mesmo em CPUs multi-core. Por isso `threading` **não acelera tarefas
CPU-bound**. Use `multiprocessing` para isso. Bibliotecas como NumPy e PyTorch **liberam o
GIL** durante operações nativas.

### Threads na GPU: warps, blocos e grades

| Nível | O que é |
| :--- | :--- |
| **Thread** | Menor unidade de execução; 1 instância do kernel; registradores próprios |
| **Warp (NVIDIA) / Wavefront (AMD)** | 32 threads que executam **sempre a mesma instrução** (SIMD); unidade de escalonamento |
| **Bloco (Block)** | Grupo de warps; compartilha memória compartilhada; roda em 1 SM; até 1024 threads |
| **Grade (Grid)** | Conjunto de todos os blocos = o problema completo |

> **Divergência de warp:** se threads do mesmo warp tomam caminhos diferentes num `if/else`,
> a GPU executa **ambos serialmente**, desativando as threads que não correspondem — perda
> drástica de desempenho.

---

## 🧪 Atividade guiada (medir o paralelismo)

No Colab/Linux dá para **ver** o paralelismo acontecendo:

```bash
# htop — uso de cada núcleo (tecle H para mostrar threads)
sudo apt-get install htop -y && htop

# nvtop — GPU, VRAM e processos
sudo apt-get install nvtop -y && nvtop
```

Experimento: rode `python scripts/processos_threads.py` e observe no **htop** que o
`multiprocessing` acende **vários núcleos**, enquanto o `threading` mantém quase **um** só
(GIL). No **Windows**, use `python scripts/monitor_processos.py`.
Detalhes e exercícios em [`atividade.md`](atividade.md).

---

## 💬 Discussão em grupo

Em grupos de 3–4, com base no cenário da startup:

1. O pré-processamento de imagens (CPU) é um gargalo. Threading ou multiprocessing? Por quê?
2. Se um warp tem 32 threads e 16 entram no `if` e 16 no `else`, como a GPU executa?
3. Por que o PyTorch usa múltiplos **processos** (workers) no DataLoader em vez de threads?
4. Qual a vantagem de usar 256 threads/bloco em vez de 1024?

---

## 📌 Tarefa de casa (opcional)

Implemente um pipeline de pré-processamento de imagens paralelo com `multiprocessing.Pool` e
compare com a versão sequencial:

- Use 100 imagens sintéticas (numpy random) de 512×512;
- aplique conversão para escala de cinza em cada imagem;
- compare o tempo sequencial vs. 2, 4 e 8 processos;
- plote o gráfico de *speedup* com Matplotlib.

---

## 🔗 Relação com o curso

- **Aula 3** mostrou que o gargalo de VRAM é alimentado por batches preparados no host. Esta
  aula explica **quem** os prepara em paralelo: se usarmos `threading` para CPU-bound, o GIL
  satura e a GPU fica ociosa esperando o dataset.
- **Próxima (Aula 5):** *Redes e Transferência de Dados* — o dataset pré-processado agora
  precisa vir de um storage remoto, atravessando a rede com resiliência a quedas.
