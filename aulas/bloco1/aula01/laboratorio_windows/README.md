# Laboratório Windows — Arquiteturas de Computadores e GPUs (hardware real)

Experimentos com o **hardware real** da máquina do laboratório, aplicando os conceitos da Aula
01: descobrir CPU/RAM/GPU e medir o ganho do processamento vetorizado (paralelo) sobre o
sequencial.

---

## 🚀 Como rodar

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat):

```
[1] 1_hardware.py   - descobrir CPU, RAM e GPU desta maquina
[2] 2_benchmark.py  - sequencial vs. vetorizado (medido aqui)
[0] Sair
```

Ou pelo terminal:

```bat
python 1_hardware.py
python 2_benchmark.py
python 2_benchmark.py 300     :: matriz maior (demora mais)
```

---

## 🗂️ Arquivos

| Arquivo | O que faz |
| :--- | :--- |
| `lib_hw.py` | Descobre o hardware real (CPU, RAM, GPU) e o backend de cálculo disponível. |
| `1_hardware.py` | Mostra o resumo do hardware desta máquina. |
| `2_benchmark.py` | Mede a matriz sequencial (3 loops) vs. vetorizada (NumPy/BLAS). |
| `iniciar.bat` | Menu (duplo clique). |

---

## 🔎 O que observar

- **GPU real:** o `lib_hw.py` detecta o nome da placa (ex.: `AMD Radeon RX 6700 XT`).
- **Núcleos:** a diferença entre núcleos **físicos** e **lógicos** explica o paralelismo da CPU.
- **Speedup:** a versão vetorizada (que usa SIMD e vários núcleos) é **ordens de grandeza**
  mais rápida que os 3 loops — é o "espírito" do que a GPU faz em escala massiva.

> `psutil` (no `requirements.txt`) é opcional, mas melhora a leitura de RAM e núcleos físicos.

---

## 🔗 Relação com a aula

- Põe em prática a comparação **CPU (sequencial) vs. paralelo (vetorizado/SIMD)**.
- O `lib_hw.py` antecipa a detecção de GPU que reaparece nas aulas seguintes.
- Segue o padrão de laboratório do curso (`.context.md`, §6.9 e §6.16).
