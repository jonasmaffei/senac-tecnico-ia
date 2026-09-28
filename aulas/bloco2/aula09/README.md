# 🧠 Aula 09 — Alternativas ao CUDA: OpenCL

**Objetivo:** reconhecer o OpenCL como alternativa multiplataforma ao CUDA, compreender seu
modelo de execução heterogêneo e implementar kernels portáveis que rodam em GPUs de qualquer
fabricante (NVIDIA, AMD, Intel) e CPUs.

---

## 🎯 Situação de aprendizagem

A startup recebeu um novo cliente cujo datacenter usa GPUs **AMD e Intel** — incompatíveis com
CUDA. O código das Aulas 7 e 8 não vai rodar. O CTO pediu para você reescrever o pipeline de
processamento de áudio usando **OpenCL**, o padrão aberto do Khronos Group que roda em qualquer
hardware. Você tem **2h30** para entregar um protótipo funcional com benchmark comparativo
**CPU vs. GPU**.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula09.html`](apresentacao_aula09.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** com explicação + **5 exercícios** |
| [`laboratorio_windows/`](laboratorio_windows/README.md) | **Experimentos com hardware real** (OpenCL na GPU AMD) |
| [`atividade.md`](atividade.md) | Atividade (questões conceituais + pesquisa) e discussão |
| [`tutorials/`](tutorials) | Tutoriais bônus: rodar **LLMs locais** com Ollama e Open WebUI |

### Estrutura da aula

```
aula09/
  apresentacao_aula09.html
  README.md
  notebook_colab/aula09_opencl.ipynb
  laboratorio_windows/          # 1_listar_dispositivos.py, 2_primeiro_kernel.py, 3_benchmark_work_groups.py, lib_opencl.py
  tutorials/                    # hands-on-ollama.md, hands-on-frontend-ollama.md
  atividade.md
```

---

## 🚀 Como rodar

### No Google Colab (notebook + 5 exercícios)

1. Abra `notebook_colab/aula09_opencl.ipynb` pelo **GitHub** no Colab
   (`https://github.com/jonasmaffei/senac-tecnico-ia`).
2. Rode as células na ordem (a primeira instala o `pyopencl`).

> 💡 **Sem GPU?** O PyOpenCL costuma ter **fallback de CPU** — o kernel roda do mesmo jeito.
> Sem OpenCL, o notebook explica o conceito e mostra números de referência.

### No Windows do laboratório (GPU AMD real)

Dê **duplo clique** em [`laboratorio_windows/iniciar.bat`](laboratorio_windows/iniciar.bat):

```
[1] 1_listar_dispositivos.py    - plataformas e dispositivos OpenCL
[2] 2_primeiro_kernel.py        - primeiro kernel OpenCL (soma de vetores)
[3] 3_benchmark_work_groups.py  - CPU vs. OpenCL e escolha do work-group
[0] Sair
```

> No laboratório (**GPU AMD**), o driver expõe OpenCL 2.1 — os kernels rodam de verdade.
> Detalhes em [`laboratorio_windows/README.md`](laboratorio_windows/README.md).

---

## 🔑 Conceitos-chave

### Arquitetura OpenCL

| Componente | O que é | Equivalente CUDA |
| :--- | :--- | :--- |
| **Platform** | Drivers do fabricante | — |
| **Device** | CPU, GPU ou acelerador | a GPU escolhida |
| **Context** | Agrupa dispositivos, memória e filas | implícito |
| **Command Queue** | Envia kernels e cópias | stream |
| **Kernel (OpenCL C)** | Compilado em runtime (JIT) | `@cuda.jit` |
| **Buffer** | Memória no dispositivo (`cl.Buffer`) | device array |

### Equivalências OpenCL × CUDA

| CUDA | OpenCL |
| :--- | :--- |
| `cuda.grid(1)` | `get_global_id(0)` |
| `threadIdx.x` | `get_local_id(0)` |
| `blockIdx.x` | `get_group_id(0)` |
| `blockDim.x` | `get_local_size(0)` |
| `cuda.shared.array()` | `__local float[]` |
| `cuda.syncthreads()` | `barrier(CLK_LOCAL_MEM_FENCE)` |
| `cuda.to_device()` | `cl.Buffer(...)` |
| `copy_to_host()` | `cl.enqueue_copy(...)` |

> **Regra:** `global_size` deve ser **múltiplo** de `local_size` — por isso o kernel leva
> `if (i < n)`.

### Vantagens × desvantagens

| ✓ Vantagens | ✗ Desvantagens |
| :--- | :--- |
| Roda em qualquer GPU (NVIDIA/AMD/Intel) | Mais verboso que CUDA (~3× mais código) |
| Fallback automático para CPU | Ecossistema de IA menor |
| Padrão aberto — sem vendor lock-in | Compilação JIT: latência no início |
| Suporta FPGAs e DSPs | PyTorch/TensorFlow preferem CUDA/ROCm |

---

## 🧪 Atividade guiada

No **Colab** ou no Windows:

```bash
python scripts/listar_dispositivos.py     # o que existe no hardware?
python scripts/primeiro_kernel.py         # soma de vetores em OpenCL
python scripts/benchmark_work_groups.py   # CPU vs. GPU + work-group
```

Questões conceituais e pesquisa em [`atividade.md`](atividade.md).

---

## 💬 Discussão em grupo

Em grupos de 3–4, no cenário do cliente com GPUs AMD e Intel:

1. Cliente com AMD e startup com NVIDIA: como manter o **mesmo código-base** nas duas?
2. O JIT compila em tempo de execução. Quais as implicações para um sistema que processa áudio
   em **tempo real**?
3. O PyTorch não suporta OpenCL diretamente. Como isso afeta a decisão de **treinar** modelos?
4. Cite **3 cenários** em que OpenCL seria a melhor escolha em vez de CUDA.

---

## 📌 Tarefa de casa (opcional)

Porte o kernel de **multiplicação de matrizes com tiling** da Aula 8 para OpenCL usando memória
`__local`:

- reescreva o kernel CUDA de tiling em OpenCL C;
- use `__local float tile_A[TILE][TILE]`;
- compare os tempos: CUDA (numba) vs. OpenCL (pyopencl) para N = 256, 512, 1024;
- identifique diferenças de desempenho e explique as causas.

---

## 🔗 Relação com o curso

- **Aulas 7 e 8** ensinaram CUDA (exclusivo NVIDIA). Esta aula mostra que o **modelo mental** de
  programação paralela (kernels, hierarquia, shared memory) é o mesmo — só muda a sintaxe e a
  portabilidade multiplataforma.
- **Próxima (Aula 10):** *Introdução ao ROCm e GPUs AMD* — a solução **industrial**: rodar
  PyTorch existente em GPUs AMD via HIP, sem reescrever o código.
