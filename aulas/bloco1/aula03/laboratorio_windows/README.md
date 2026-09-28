# Laboratório Windows — Estrutura de Memória em GPUs (hardware real)

Experimentos com o **hardware real** da máquina do laboratório, aplicando os conceitos da Aula
03: a hierarquia de memória, o custo de mover dados entre RAM e VRAM (PCIe) e o diagnóstico de
memória.

---

## 🚀 Como rodar

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat):

```
[1] 1_benchmark_ram_vram.py  - RAM (CPU) vs. VRAM (GPU) + custo do PCIe
[2] 2_hierarquia_memoria.py  - a piramide de latencia na pratica
[3] 3_monitor_memoria.py     - diagnostico de memoria (nvidia-smi/RAM)
[0] Sair
```

Ou pelo terminal:

```bat
python 1_benchmark_ram_vram.py
python 2_hierarquia_memoria.py
python 3_monitor_memoria.py
```

---

## 🗂️ Arquivos

| Arquivo | O que faz |
| :--- | :--- |
| `1_benchmark_ram_vram.py` | Mede a soma de vetores na RAM (CPU) vs. VRAM (GPU) e o custo da cópia PCIe. |
| `2_hierarquia_memoria.py` | Mostra o degrau de largura de banda entre cache e RAM (a pirâmide de latência). |
| `3_monitor_memoria.py` | Diagnóstico: `nvidia-smi`/`rocm-smi` (GPU) e a RAM do host (psutil). |
| `lib_backend.py` | Biblioteca de detecção de backend (CuPy → PyTorch CUDA → DirectML → NumPy). |
| `iniciar.bat` | Menu (duplo clique). |

---

## 🔎 O que observar

- **Sem GPU acessível:** os scripts rodam com **fallback NumPy** e explicam a lição do PCIe.
  No Colab com **T4 GPU**, o mesmo código mede a VRAM e a transferência de verdade.
- **Degrau de cache:** no script 2, veja a largura de banda cair quando o vetor deixa de caber
  em cache e passa a ser lido da RAM.
- **Custo do PCIe:** copiar RAM ↔ VRAM é ~100× mais lento que a VRAM interna — por isso os
  batches ficam na VRAM.

---

## 🔗 Relação com a aula

- Reproduz, no laboratório, a medição de **RAM × VRAM** e o **gargalo do PCIe**.
- O `3_monitor_memoria.py` mostra como diagnosticar uma GPU ociosa (o caso da startup).
- Segue o padrão de laboratório do curso (`.context.md`, §6.9 e §6.16).
