# Atividade Guiada: Aula 4 — Fundamentos de Processos e Threads

## Parte 1 — Atividade guiada: medir o paralelismo

O objetivo é **ver** o efeito do GIL e o ganho do paralelismo real, com números. Rode no
**Colab** (ou no terminal do laboratório) e registre os resultados.

### Passo 1 — CPU-bound: threading vs. multiprocessing

```bash
python scripts/processos_threads.py
```

Anote os três tempos (Sequencial, Threading, Multiprocessing) e os speedups.

### Passo 2 — I/O-bound: threading

```bash
python scripts/io_bound.py
```

Compare o tempo sequencial com o tempo com threads. Por que aqui o threading **ajuda**?

### Passo 3 — Kernels CUDA (se houver GPU NVIDIA)

```bash
python scripts/kernels_cuda.py
```

Observe como o tempo varia conforme `threads_por_bloco`. Qual configuração foi mais rápida?

### Passo 4 — Enxergar processos e threads

No **Colab/Linux**, rode o benchmark numa aba e o monitor noutra:

```bash
sudo apt-get install htop nvtop -y
htop     # tecle H para mostrar as threads; observe os núcleos
nvtop    # observe a GPU e os processos
```

No **Windows**, use `python scripts/monitor_processos.py`.

### Exercício de fixação

1. O `threading` acelerou a tarefa **CPU-bound**? Por quê? (Cite o GIL.)
2. O `threading` acelerou a tarefa **I/O-bound**? Por quê?
3. No benchmark de CPU, o speedup do multiprocessing chegou perto do número de núcleos?
   Se não, o que explica a diferença (overhead de criação, memória, etc.)?

> 💡 A lição: **CPU-bound → processos; I/O-bound → threads.** O GIL só libera o interpretador
> durante esperas de I/O.

---

## Parte 2 — Discussão em grupo (3 a 4 pessoas)

Com base no cenário da startup (pipeline de reconhecimento facial):

1. No pipeline de treinamento, o pré-processamento de imagens (CPU) é um gargalo. Você
   usaria **threading ou multiprocessing** para paralelizar? Por quê?
2. Se um warp da GPU tem 32 threads e 16 delas entram no `if` e 16 no `else`, como a GPU
   executa isso? Qual o impacto?
3. Por que o PyTorch usa **múltiplos processos** (*workers*) no DataLoader em vez de threads?
4. Qual a vantagem de usar **256 threads/bloco** em vez de 1024 numa GPU?

---

## Parte 3 — Pesquisa (tarefa de casa, opcional)

Implemente um pipeline de pré-processamento de imagens paralelo usando
`multiprocessing.Pool` e compare com a versão sequencial:

- Use **100 imagens sintéticas** (numpy random) de **512×512**;
- aplique **conversão para escala de cinza** em cada imagem;
- compare o tempo sequencial vs. **2, 4 e 8 processos**;
- plote o gráfico de ***speedup*** com Matplotlib.

> Dica: para medir o speedup, calcule `tempo_sequencial / tempo_paralelo`. O ideal teórico
> é igual ao número de processos; acima disso há *overhead* de comunicação/criação.
