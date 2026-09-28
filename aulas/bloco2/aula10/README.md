# 🧠 Aula 10 — Introdução ao ROCm e GPUs AMD

**Objetivo:** configurar e executar aplicações de IA em GPUs AMD usando o ecossistema ROCm,
compreender a portabilidade via HIP e rodar modelos PyTorch em ambiente Docker, promovendo
independência de fabricante no desenvolvimento de IA.

---

## 🎯 Situação de aprendizagem

A startup adquiriu um lote de GPUs **AMD Instinct MI300X** para reduzir custos de infraestrutura
em **40%** comparado às NVIDIA A100. O problema: todo o pipeline de IA foi desenvolvido para
CUDA. O engenheiro sênior afirma que o **ROCm pode executar o código PyTorch existente sem
modificações**. Você precisa verificar essa afirmação, configurar o ambiente ROCm via **Docker**
e rodar o modelo **ResNet-18** para comparar desempenho.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula10.html`](apresentacao_aula10.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** com explicação + **5 exercícios** |
| [`laboratorio_windows/`](laboratorio_windows/README.md) | **Experimentos com PyTorch** (portabilidade CUDA/ROCm) |
| [`laboratorio_rocm-docker/`](laboratorio_rocm-docker/README.md) | **Lab industrial:** ROCm + PyTorch via Docker (GPUs AMD) |
| [`laboratorio_verificar-gpu/`](laboratorio_verificar-gpu/README.md) | Verificar acesso à GPU no container (Windows/AMD) |
| [`laboratorio_stressar-gpu/`](laboratorio_stressar-gpu/README.md) | Estressar a GPU via Vulkan/D3D12 (Windows/AMD) |
| [`atividade.md`](atividade.md) | Atividade (questões conceituais + pesquisa) e discussão |

### Estrutura da aula

```
aula10/
  apresentacao_aula10.html
  README.md
  notebook_colab/aula10_rocm.ipynb
  laboratorio_windows/          # 1_rocm_pytorch_benchmark.py, 2_diagnostico_portabilidade.py, lib_rocm.py
  laboratorio_rocm-docker/      # lab industrial (rocm/pytorch)
  laboratorio_verificar-gpu/    # verifica acesso à GPU
  laboratorio_stressar-gpu/     # estressa a GPU (Vulkan)
  atividade.md
```

---

## 🚀 Como rodar

### No Google Colab (notebook + 5 exercícios)

1. Abra `notebook_colab/aula10_rocm.ipynb` pelo **GitHub** no Colab
   (`https://github.com/jonasmaffei/senac-tecnico-ia`).
2. Rode as células na ordem. O notebook detecta CUDA (Colab) ou CPU.

> 💡 **Sem GPU?** O código roda na CPU e mostra a referência — é o **mesmo** que rodaria em
> NVIDIA (CUDA) ou AMD (ROCm).

### No Windows do laboratório (PyTorch portável)

Dê **duplo clique** em [`laboratorio_windows/iniciar.bat`](laboratorio_windows/iniciar.bat):

```
[1] 1_rocm_pytorch_benchmark.py     - diagnostico + matmul + treino (portatil)
[2] 2_diagnostico_portabilidade.py  - equivalencia CUDA x ROCm
[0] Sair
```

### Com GPU AMD de verdade (Docker)

Siga o laboratório principal: [`laboratorio_rocm-docker/README.md`](laboratorio_rocm-docker/README.md).

---

## 🔑 Conceitos-chave

### A stack ROCm

```
Aplicação (PyTorch, TensorFlow, JAX)
Framework GPU (MIOpen, rocBLAS, rocFFT)
HIP Runtime — API de portabilidade CUDA/AMD
ROCr — ROCm Runtime (HSA)
KFD — Kernel Fusion Driver (módulo do Linux)
Hardware: GPU AMD (GFX9 / RDNA2 / CDNA3)
```

### Equivalência CUDA × ROCm

| CUDA (NVIDIA) | ROCm (AMD) |
| :--- | :--- |
| `nvcc` | `hipcc` |
| cuBLAS | rocBLAS |
| cuDNN | MIOpen |
| cuFFT | rocFFT |
| nvidia-smi | rocm-smi |
| nvidia/cuda | rocm/pytorch |

### Portabilidade ("zero código")

O ROCm **emula a API CUDA** do PyTorch. O código Python é **idêntico**:

```python
device = "cuda" if torch.cuda.is_available() else "cpu"   # True no ROCm também!
modelo.to(device)
```

O que muda é só o **ambiente** (driver ROCm, `hipcc`, `rocm-smi`) e o **hardware**.

> **`hipify-clang`** converte kernels CUDA C/C++ para HIP automaticamente — útil quando você
> tem código de kernel próprio, não só PyTorch.

---

## 🧪 Atividade guiada

No **Colab** ou no Windows:

```bash
python scripts/lib_rocm.py                    # qual backend?
python scripts/diagnostico_portabilidade.py   # equivalências e ferramentas
python scripts/rocm_pytorch_benchmark.py      # benchmark portável
```

Questões conceituais e pesquisa em [`atividade.md`](atividade.md).

---

## 💬 Discussão em grupo

Em grupos de 3–4, no cenário das GPUs AMD:

1. Se o PyTorch roda CUDA em AMD via ROCm sem modificação, por que o **CUDA ainda domina**?
2. Resultados treinados com cuDNN e migrados para MIOpen são **numericamente idênticos**?
3. Docker facilita o ROCm, mas adiciona overhead. Quando seria **problemático**?
4. H100 (US$30k) vs. MI300X (US$20k): além do preço, que fatores técnicos e operacionais pesam?

---

## 📌 Tarefa de casa (opcional)

Compare o treinamento da **ResNet-50** em CUDA (Google Colab) vs. ROCm (Docker local ou AMD
Cloud) e produza um relatório técnico:

- meça **tempo por época**, **throughput** (imgs/s), **uso de VRAM** e **consumo de energia (W)**;
- use `torch.profiler` para gerar um *trace* nos dois ambientes;
- documente as diferenças de setup (CUDA vs. Docker ROCm) num README;
- calcule o **TCO** (Total Cost of Ownership) para 1 ano de treinamento em cada plataforma.

---

## 🔗 Relação com o curso

- **Aula 9** mostrou a portabilidade *manual* (reescrever em OpenCL). Esta aula entrega a
  solução **industrial de alto nível**: pipelines PyTorch escritos para CUDA rodam
  transparentemente em GPUs AMD (como a MI300X) via **HIP**, sem alterar o código Python.
- **Próxima (Aula 11):** *Aplicação de Modelos em GPUs NVIDIA e AMD* — medir, registrar com
  W&B e decidir com dados.
