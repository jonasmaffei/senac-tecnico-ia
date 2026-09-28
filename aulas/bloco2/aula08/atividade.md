# Atividade Guiada: Aula 8 — Manipulação de Memória em CUDA (Tiling)

## Parte 1 — Atividade guiada: otimizando um kernel

O objetivo é **medir antes de otimizar** e entender o impacto da memória. Rode no **Google
Colab** com GPU habilitada (*Runtime ➔ Change runtime type ➔ T4 GPU*).

### Passo 1 — Coalescing

```bash
python scripts/coalescing.py
```

Compare o tempo do acesso **coalescido** com o **strided (×32)**. Anote quantas vezes mais
lento ficou.

### Passo 2 — Matmul ingênua (memória global)

```bash
python scripts/matmul_global.py
```

Guarde o tempo e confira que o erro vs. NumPy é ~0 (a resposta está certa, só é lenta).

### Passo 3 — Matmul com tiling (memória compartilhada)

```bash
python scripts/matmul_tiling.py
```

Compare com o passo 2 e calcule o speedup. Depois rode o mesmo no **Nsight Compute**:

```bash
ncu --set full python scripts/matmul_tiling.py
# no Colab: instale o ncu ou use o Nsight Systems do Google Colab
```

### Passo 4 — Medindo com eventos CUDA

```bash
python scripts/profiling_ocupacao.py
```

Observe que `cuda.event` mede o tempo **na GPU**, não na CPU.

### Exercício de fixação

1. Quantas transações de barramento um acesso não-coalescido gera no **pior caso**?
2. Por que a versão com tiling lê cada elemento da VRAM **~TILE vezes menos**?
3. O que aconteceria se você removesse **um** dos `cuda.syncthreads()`?
4. Por que `cuda.event` é mais preciso que `time.time()` para medir um kernel?

---

## Parte 2 — Discussão em grupo (3 a 4 pessoas)

No cenário do kernel lento:

1. Com tile **16×16** (256 threads), quantas vezes cada elemento de A e B é lido da
   **memória global** vs. da **memória compartilhada**?
2. Por que é obrigatório chamar `cuda.syncthreads()` **duas vezes** no kernel de tiling? O que
   acontece se você remover uma delas?
3. A memória compartilhada tem ~**48 KB por SM**. Com `TILE=32`, qual o tamanho dos dois tiles
   juntos? Cabe na shared memory?
4. Em que situações usar memória compartilhada **não** vale a pena? (Pense em kernels onde
   cada dado é lido apenas uma vez.)

---

## Parte 3 — Pesquisa (tarefa de casa, opcional)

### Engenharia e hardware

- **Coalescing:** pesquise o que acontece a nível de hardware quando threads de um warp fazem
  acessos coalescidos vs. espalhados. Quantas transações no pior caso e qual a perda estimada?
- **Shared vs. cache L1:** quais as vantagens e desvantagens de gerenciar **manualmente** o
  cache (tiling) em vez de confiar 100% no cache automático?

### Visão de negócios e infraestrutura

- **Custo do minuto de GPU:** pesquise o custo médio de instâncias com A100/H100. Se o tiling
  reduz uma época de **10 h para 2 h**, qual a economia diária para uma empresa que treina
  todo dia?
- **Eficiência energética (Green AI):** explique como reduzir acessos à VRAM lenta impacta
  diretamente o consumo de **watts** durante uma carga pesada.

### Prática extra

- Otimize a **transposta de matriz** com shared memory, adicionando **`+1`** à dimensão interna
  do tile. Explique por que isso elimina *bank conflicts*.
- Meça com `cuda.event` para N = 256, 512, 1024, 2048 e plote o **speedup × N**.

> **Dica:** o melhor engenheiro de IA não domina só a matemática dos modelos — entende a
> **física do hardware** e otimiza memória para garantir escala e viabilidade financeira.
