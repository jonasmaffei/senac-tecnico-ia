# 🧠 Aula 07 — Introdução ao Modelo CUDA

**Objetivo:** compreender a estrutura de programação paralela do CUDA — kernels, threads,
blocos e grades — e aplicá-la para acelerar cálculos matemáticos intensivos em IA, medindo o
speedup real vs. CPU.

---

## 🎯 Situação de aprendizagem

O pipeline de pré-processamento de **áudio** da startup precisa calcular a **Transformada de
Fourier (FFT)** de milhões de amostras de áudio por segundo para alimentar o modelo de
reconhecimento de voz. A versão CPU demora **~8 segundos** por batch — inaceitável para
produção. Você foi designado(a) para reescrever esse processamento usando **CUDA na GPU** e
alcançar latência abaixo de **100 ms**.

---

## 🗂️ Conteúdo

| Arquivo | O que é |
| :--- | :--- |
| [`apresentacao_aula07.html`](apresentacao_aula07.html) | Slides teóricos (abra no navegador, navegue com ← →) |
| [`aula07_cuda.ipynb`](aula07_cuda.ipynb) | Notebook do **Google Colab** (índice global, primeiros kernels, FFT) |
| [`atividade.md`](atividade.md) | Atividade guiada (kernels) + discussão em grupo |
| `scripts/` | Scripts comentados (detecção de CUDA, kernels, FFT) |

### Scripts

| Script | O que faz |
| :--- | :--- |
| [`lib_cuda.py`](scripts/lib_cuda.py) | Detecta se há CUDA; permite rodar com fallback sem GPU |
| [`indice_global.py`](scripts/indice_global.py) | A hierarquia CUDA e a fórmula do índice global (1D e 2D) |
| [`primeiro_kernel.py`](scripts/primeiro_kernel.py) | Fluxo host → device → host (soma de vetores, escala, média móvel) |
| [`fft_benchmark.py`](scripts/fft_benchmark.py) | FFT: CPU (NumPy) vs. GPU (CuPy) |

---

## 🚀 Como rodar

### No Google Colab (recomendado — **exige GPU NVIDIA**)

1. Abra `aula07_cuda.ipynb` pelo **GitHub** no Colab
   (`https://github.com/jonasmaffei/senac-tecnico-ia`).
2. *Runtime ➔ Change runtime type ➔ **T4 GPU*** ➔ *Save*.
3. Rode as células na ordem.

> ⚠️ **Sem GPU NVIDIA?** O notebook detecta e mostra o conceito e os números de referência —
> a aula roda do começo ao fim. Para medir de verdade, é preciso uma GPU NVIDIA (CUDA).

### No Windows do laboratório

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat). Ele cria o ambiente virtual (`.venv`),
instala as dependências de [`requirements.txt`](requirements.txt) e abre um **menu**:

```
[1] indice_global.py    - hierarquia CUDA e o indice global
[2] primeiro_kernel.py  - fluxo host -> device -> host
[3] fft_benchmark.py    - FFT: CPU (NumPy) vs. GPU (CuPy)
[4] lib_cuda.py         - detectar se ha CUDA disponivel
[0] Sair
```

> Na máquina do laboratório (**GPU AMD**), o CUDA não está disponível: os scripts mostram o
> conceito e os números de referência. O `fft_benchmark.py` mede a FFT na **CPU** normalmente.

---

## 🔑 Conceitos-chave

### Host × Device

| | **Host (CPU)** | **Device (GPU)** |
| :--- | :--- | :--- |
| Papel | Aloca, transfere, lança kernels, coleta | Executa o kernel em N threads |
| Memória | RAM | VRAM |

### O fluxo CUDA

1. `cuda.to_device()` — CPU aloca arrays na VRAM;
2. `kernel[blocos, threads](...)` — CPU lança o kernel;
3. GPU executa N threads em paralelo;
4. `cuda.synchronize()` — CPU espera a GPU terminar;
5. `copy_to_host()` — CPU copia o resultado de volta.

### A hierarquia e o índice global

| Identificador | O que é |
| :--- | :--- |
| `threadIdx` | Índice da thread **dentro** do bloco |
| `blockIdx` | Índice do bloco **dentro** da grade |
| `blockDim` | Nº de threads por bloco |
| `gridDim` | Nº de blocos na grade |

**Fórmula (1D):** `idx = blockIdx.x * blockDim.x + threadIdx.x` → atalho `cuda.grid(1)`.
Em 2D: `col, row = cuda.grid(2)`.

> **Regra de ouro:** use **múltiplos de 32** threads por bloco (tamanho do warp). **128–256** é
> o ponto ótimo na maioria dos kernels; o máximo é **1024**.

---

## 🧪 Atividade guiada

No **Colab com GPU**:

```bash
# 1) Há CUDA?
python scripts/lib_cuda.py

# 2) Hierarquia e índice global
python scripts/indice_global.py

# 3) Fluxo completo de um kernel
python scripts/primeiro_kernel.py

# 4) FFT CPU vs. GPU
python scripts/fft_benchmark.py
```

Exercícios completos em [`atividade.md`](atividade.md).

---

## 💬 Discussão em grupo

Em grupos de 3–4, no cenário da startup de áudio:

1. 10M de amostras com 256 threads/bloco: quantos blocos? O que acontece com as threads
   "extras" além dos 10M?
2. Por que é necessário chamar `cuda.synchronize()` antes de copiar o resultado de volta?
3. Em que situações um kernel CUDA simples **não** teria speedup vs. a CPU?
4. O CuPy dá 66× de speedup na FFT. Como você usaria isso no pipeline de áudio da startup?

---

## 📌 Tarefa de casa (opcional)

Implemente um kernel CUDA que calcula o **produto escalar** de dois vetores de 1 milhão de
elementos e compare com NumPy:

- escreva o kernel com `numba.cuda` e a versão CPU com NumPy;
- meça o speedup para N = 1K, 10K, 100K, 1M, 10M;
- plote o gráfico de speedup × N com Matplotlib;
- identifique o ponto em que a GPU começa a superar a CPU.

---

## 🔗 Relação com o curso

- **Bloco 1** preparou o terreno: arquiteturas, memória (VRAM/PCIe), threads CPU/GPU e Linux.
  Agora começamos o **Bloco 2**: programação paralela com **CUDA**, OpenCL e ROCm.
- **Próxima (Aula 8):** *Manipulação de Memória em CUDA* — o kernel funciona, mas bate
  demais na VRAM lenta; vamos usar **memória compartilhada** e **tiling**.
