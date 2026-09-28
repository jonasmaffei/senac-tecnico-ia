# Laboratório Windows — OpenCL (GPU AMD real)

Experimentos com a **GPU real** da máquina do laboratório (AMD/Windows), aplicando os conceitos
da Aula 09: o OpenCL como padrão multiplataforma, kernels portáveis e a escolha do work-group.

> ✅ **Este laboratório roda de verdade no laboratório:** o driver AMD expõe **OpenCL 2.1**, e
> os kernels são executados na GPU (`gfx1031`). É a aula onde a portabilidade multi-vendor sai
> do papel.

---

## 🚀 Como rodar

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat):

```
[1] 1_listar_dispositivos.py    - plataformas e dispositivos OpenCL
[2] 2_primeiro_kernel.py        - primeiro kernel OpenCL (soma de vetores)
[3] 3_benchmark_work_groups.py  - CPU vs. OpenCL e escolha do work-group
[0] Sair
```

Ou pelo terminal:

```bat
python 1_listar_dispositivos.py
python 2_primeiro_kernel.py
python 3_benchmark_work_groups.py
```

---

## 🗂️ Arquivos

| Arquivo | O que faz |
| :--- | :--- |
| `lib_opencl.py` | Detecta o PyOpenCL e lista plataformas/dispositivos (com fallback). |
| `1_listar_dispositivos.py` | Mostra plataformas e dispositivos (compute units, VRAM, max work-group). |
| `2_primeiro_kernel.py` | Compila (JIT) e executa um kernel OpenCL de soma de vetores. |
| `3_benchmark_work_groups.py` | CPU (NumPy) vs. OpenCL + variação do `local_size` (work-group). |
| `iniciar.bat` | Menu (duplo clique). |

---

## 🔎 O que observar

- **Plataforma AMD:** `AMD Accelerated Parallel Processing`, versão **OpenCL 2.1**.
- **Dispositivo:** `gfx1031` (a GPU AMD), com ~11 GB de memória e `max_work_group = 256`.
- **Regra do OpenCL:** o `global_size` deve ser **múltiplo** do `local_size` — por isso o kernel
  leva `if (i < n)`.
- **Melhor work-group:** o script 3 marca o **melhor medido** (varia por dispositivo).

> Se o PyOpenCL não estiver instalado, os scripts mostram o conceito e números de referência.

---

## 🔗 Relação com a aula

- Prova que **o mesmo kernel OpenCL roda em GPUs de qualquer fabricante** — sem código CUDA.
- Conecta os conceitos do CUDA (Aulas 7–8) à terminologia OpenCL: `work-item`/`work-group`.
- Segue o padrão de laboratório do curso (`.context.md`, §6.9 e §6.16).
