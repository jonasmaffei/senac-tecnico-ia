# 🧱 Bloco 2 — Programação, Otimização e Computação Heterogênea

> Este bloco agrupa as suas aulas em `aulas/bloco2/` — cada aula fica na sua subpasta (`aulaNN/`).

Este bloco transforma a base teórica em prática: escrever código que roda na GPU, otimizar
memória e medir ganhos reais. É onde o aluno aprende a **explorar** a GPU, não só usá-la.

| Aula | Tema | Recursos |
| :---: | :--- | :--- |
| **07** | Introdução ao Modelo CUDA (kernels, índice global, CuPy FFT) | [Guia](aula07/README.md) · [Apresentação](aula07/apresentacao_aula07.html) · [Notebook](aula07/notebook_colab/aula07_cuda.ipynb) · [Atividade](aula07/atividade.md) · [Scripts](aula07/scripts) |
| **08** | Manipulação de Memória em CUDA (tiling, coalescing, profiling) | [Guia](aula08/README.md) · [Apresentação](aula08/apresentacao_aula08.html) · [Notebook](aula08/notebook_colab/aula08_tiling.ipynb) · [Atividade](aula08/atividade.md) · [Scripts](aula08/scripts) |
| **09** | Alternativas ao CUDA: OpenCL (+ LLMs locais) | [Guia](aula09/README.md) · [Apresentação](aula09/apresentacao_aula09.html) · [Notebook](aula09/notebook_colab/aula09_opencl.ipynb) · [Atividade](aula09/atividade.md) · [Laboratório Windows](aula09/laboratorio_windows/README.md) |
| **10** | Introdução ao ROCm e GPUs AMD (HIP, PyTorch & Docker) | [Guia](aula10/README.md) · [Apresentação](aula10/apresentacao_aula10.html) · [Notebook](aula10/notebook_colab/aula10_rocm.ipynb) · [Atividade](aula10/atividade.md) · [Laboratório Windows](aula10/laboratorio_windows/README.md) |
| **11** | Aplicação de Modelos em GPUs NVIDIA e AMD (CNN, Mixed Precision/AMP, TCO) | [Guia](aula11/README.md) · [Apresentação](aula11/apresentacao_aula11.html) · [Notebook](aula11/notebook_colab/aula11_aplicacao_modelos.ipynb) · [Atividade](aula11/atividade.md) · [Laboratório Windows](aula11/laboratorio_windows/README.md) |
| **12** | Laboratório prático e revisão interativa (5 experimentos) | [Guia](aula12/README.md) · [Apresentação](aula12/apresentacao_aula12.html) · [Notebook](aula12/notebook_colab/aula12_pratica_colab.ipynb) · [Atividade](aula12/atividade.md) · [Projeto Integrador](../projeto-integrador/README.md) |
| **13** | Implementação de um Modelo Paralelo Simples (síntese do bloco) | [Guia](aula13/README.md) · [Apresentação](aula13/apresentacao_aula13.html) · [Notebook](aula13/notebook_colab/aula13_implementacao_modelo_paralelo.ipynb) · [Atividade](aula13/atividade.md) |

---

## 🧭 Fio condutor do bloco

```
kernels CUDA → tiling/coalescing → OpenCL → ROCm/AMD → treino de CNN → validação prática → síntese
```

Depois de escrever o primeiro kernel, o aluno aprende a **otimizar memória**, a **portar**
para padrões abertos (OpenCL/ROCm), a **treinar** modelos reais e, por fim, a **medir** se a
aceleração compensa (curva de speedup e limiar de compensação).

**Bloco anterior:** [Bloco 1 — Fundamentos](../bloco1/README.md) ·
**Próximo bloco:** [Bloco 3 — Automação](../bloco3/README.md).
