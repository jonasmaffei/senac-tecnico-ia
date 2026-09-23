# Laboratório Windows — ROCm e GPUs AMD (portabilidade CUDA ↔ ROCm)

Experimentos com o **PyTorch** da máquina do laboratório, aplicando os conceitos da Aula 10: o
mesmo código Python roda em **NVIDIA (CUDA)** e **AMD (ROCm)** sem alterações.

> ℹ️ Aqui o objetivo não é medir uma GPU AMD **real** (isso é feito no laboratório irmão
> [`../laboratorio_rocm-docker/`](../laboratorio_rocm-docker/README.md), num servidor AMD). O
> foco é provar que o **código é o mesmo** e diagnosticar o backend disponível.

---

## 🚀 Como rodar

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat):

```
[1] 1_rocm_pytorch_benchmark.py     - diagnostico + matmul + treino (portatil)
[2] 2_diagnostico_portabilidade.py  - equivalencia CUDA x ROCm
[0] Sair
```

Ou pelo terminal:

```bat
python 1_rocm_pytorch_benchmark.py
python 2_diagnostico_portabilidade.py
```

---

## 🗂️ Arquivos

| Arquivo | O que faz |
| :--- | :--- |
| `lib_rocm.py` | Detecta o backend (CUDA nativo, ROCm/HIP ou CPU) — sem quebrar sem GPU. |
| `1_rocm_pytorch_benchmark.py` | Diagnóstico + matmul (TFLOPS) + treino sintético (throughput). |
| `2_diagnostico_portabilidade.py` | Tabela de equivalência CUDA × ROCm e ferramentas instaladas. |
| `iniciar.bat` | Menu (duplo clique). |

---

## 🔎 O que observar

- **Backend detectado:** `CUDA` (NVIDIA) ou `ROCm/HIP` (AMD) — o `torch.version.hip` distingue os
  dois. Sem GPU, cai para `CPU-torch`.
- **Zero código alterado:** o mesmo `1_rocm_pytorch_benchmark.py` roda nos dois ecossistemas.
- **Fallback sem torchvision:** o treino usa uma CNN simples se a `torchvision` não existir.

> Para GPU AMD real, o laboratório principal é
> [`../laboratorio_rocm-docker/`](../laboratorio_rocm-docker/README.md) (imagem `rocm/pytorch`).

---

## 🔗 Relação com a aula

- Prova a afirmação do engenheiro sênior: o PyTorch em CUDA **roda em AMD via HIP** sem mudanças.
- Conecta aos laboratórios irmãos (Docker ROCm e diagnóstico de GPU).
- Segue o padrão de laboratório do curso (`.context.md`, §6.9 e §6.16).
