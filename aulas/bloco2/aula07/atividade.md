# Atividade Guiada: Aula 7 — Introdução ao Modelo CUDA

## Parte 1 — Atividade guiada: kernels CUDA

O objetivo é dominar o **modelo de programação CUDA** na prática. Rode no **Google Colab**
com GPU habilitada (*Runtime ➔ Change runtime type ➔ T4 GPU*).

### Passo 1 — Há CUDA disponível?

```bash
python scripts/lib_cuda.py
```

Confirme o nome da GPU. Sem GPU, siga pelos conceitos (os scripts mostram a referência).

### Passo 2 — A hierarquia e o índice global

```bash
python scripts/indice_global.py
```

Observe como a fórmula `blockIdx.x * blockDim.x + threadIdx.x` distribui **um índice único**
por thread.

### Passo 3 — O fluxo completo de um kernel

```bash
python scripts/primeiro_kernel.py
```

Acompanhe as 5 etapas: alocar → lançar → executar → sincronizar → copiar.

### Passo 4 — FFT: CPU vs. GPU

```bash
python scripts/fft_benchmark.py
```

Anote o tempo da CPU (NumPy) e da GPU (CuPy) e calcule o speedup.

### Exercício de fixação

1. Para N = 10.000.000 e 256 threads/bloco, quantos blocos são lançados?
2. Por que o kernel precisa da proteção `if idx < c.shape[0]`?
3. O que aconteceria se você copiasse o resultado **sem** `cuda.synchronize()`?
4. Por que `256` threads/bloco costuma ser melhor que `1024`?

---

## Parte 2 — Discussão em grupo (3 a 4 pessoas)

No cenário da startup de áudio:

1. Se você tem 10 milhões de amostras e usa 256 threads/bloco, quantos blocos precisa? O que
   acontece com as threads "extras" além dos 10M?
2. Por que é necessário chamar `cuda.synchronize()` antes de copiar o resultado de volta para
   a CPU?
3. Em que situações um kernel CUDA simples **não** teria speedup vs. a versão CPU? (Pense em
   overhead de transferência e tamanho dos dados.)
4. O CuPy oferece 66× de speedup na FFT. Como você usaria isso no pipeline de processamento
   de áudio da startup?

---

## Parte 3 — Pesquisa (tarefa de casa, opcional)

Implemente um kernel CUDA que calcula o **produto escalar** de dois vetores de 1 milhão de
elementos e compare com NumPy:

- Escreva o kernel com `numba.cuda` e a versão CPU com NumPy;
- Meça o speedup para N = 1K, 10K, 100K, 1M, 10M;
- Plote o gráfico de **speedup × N** com Matplotlib;
- Identifique o **ponto em que a GPU começa a superar a CPU**.

> **Dica:** para N pequeno, o overhead de copiar dados pela PCIe domina e a GPU pode ficar
> *mais lenta* que a CPU. O cruzamento no gráfico mostra o tamanho mínimo em que vale a pena
> usar a GPU.
