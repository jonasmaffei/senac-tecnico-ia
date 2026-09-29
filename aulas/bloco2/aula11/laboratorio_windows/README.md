# 🖥️ Laboratório Windows — Aula 11 (Aplicação de Modelos de IA)

Este laboratório roda **o mesmo código** do notebook do Colab, mas como scripts Python no
Windows do laboratório. Sem GPU NVIDIA, ele mostra os **números de referência (T4)** em vez de
quebrar — a atividade continua válida.

---

## 🚀 Como rodar

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat). Na primeira vez ele cria o `.venv` e
instala as dependências (só `torch`). Depois aparece o menu:

```
[1] 1_benchmark_treino.py       - FP32 vs. FP16 (throughput)
[2] 2_comparar_ecossistemas.py  - NVIDIA x AMD + custo (TCO)
[0] Sair
```

Opção manual no terminal:

```bat
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe 1_benchmark_treino.py
```

---

## 📄 Arquivos

| Arquivo | O que faz |
| :--- | :--- |
| [`iniciar.bat`](iniciar.bat) | Menu (duplo clique): cria `.venv`, instala deps e roda |
| [`lib_treino.py`](lib_treino.py) | Detecção de backend (CUDA/ROCm/CPU) + treino portável |
| [`1_benchmark_treino.py`](1_benchmark_treino.py) | Mede throughput FP32 vs. FP16 (mixed precision) |
| [`2_comparar_ecossistemas.py`](2_comparar_ecossistemas.py) | Comparativo NVIDIA × AMD e simulador de TCO |
| [`requirements.txt`](requirements.txt) | Dependências (`torch`) |

---

## 🧪 O que observar

- **Com GPU (Colab/T4):** o script treina de verdade e mostra o throughput medido e o speedup
  do FP16.
- **Sem GPU (este laboratório):** mostra a referência T4 — FP32 ≈ 180 imgs/s, FP16 ≈ 341 imgs/s
  (≈ 1.9×).
- **Custo:** edite os preços/hora no `2_comparar_ecossistemas.py` com a **sua** pesquisa da
  nuvem e veja a economia anual da AMD.

> ℹ️ A decisão de infraestrutura não é só técnica: envolve **custo por hora**,
> **facilidade de uso** e **a equipe** que você já tem.

---

## 🔗 Relação com a aula

- A teoria (métricas, mixed precision, CUDA × ROCm) está na
  [`apresentacao_aula11.html`](../apresentacao_aula11.html).
- O passo a passo completo, com os 5 exercícios, está no notebook
  [`notebook_colab/aula11_aplicacao_modelos.ipynb`](../notebook_colab/aula11_aplicacao_modelos.ipynb).
- A atividade de pesquisa está em [`atividade.md`](../atividade.md).
