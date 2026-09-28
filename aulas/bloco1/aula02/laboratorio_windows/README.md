# Laboratório Windows — Modelos de Processamento (hardware real)

Experimentos com o **hardware real** da máquina do laboratório, aplicando os conceitos da Aula
02: o ganho do **SIMD** (vetorização) e como identificar a arquitetura da CPU (RISC/CISC) e os
recursos SIMD disponíveis.

---

## 🚀 Como rodar

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat):

```
[1] 1_benchmark_simd.py       - sequencial vs. SIMD (NumPy/GPU)
[2] 2_estudo_imagem.py        - imagem 1080p: loop vs. vetorizado
[3] 3_arquitetura_instrucoes.py - RISC/CISC + recursos SIMD da CPU
[0] Sair
```

Ou pelo terminal:

```bat
python 1_benchmark_simd.py
python 2_estudo_imagem.py
python 3_arquitetura_instrucoes.py
```

---

## 🗂️ Arquivos

| Arquivo | O que faz |
| :--- | :--- |
| `1_benchmark_simd.py` | Compara a soma sequencial (Python puro) com a vetorizada (NumPy/SIMD). |
| `2_estudo_imagem.py` | Converte uma imagem 1080p para cinza: loop por pixel vs. vetorizado. |
| `3_arquitetura_instrucoes.py` | Identifica RISC/CISC e lista os recursos SIMD da CPU (AVX2, SSE4…). |
| `iniciar.bat` | Menu (duplo clique). |

> O `1_benchmark_simd.py` importa `../scripts/lib_backend.py` (biblioteca **compartilhada**
> com o notebook do Colab). Os outros dois usam apenas NumPy.

---

## 🔎 O que observar

- **Recursos SIMD desta CPU:** o script 3 mostra o que o NumPy usa (ex.: `AVX2, AVX, SSE4.2`).
- **Tipo de arquitetura:** CPUs Intel/AMD aparecem como **CISC (x86/x64)**.
- **Speedup:** a versão vetorizada usa SIMD por baixo dos panos — o mesmo princípio da GPU,
  em escala menor.

---

## 🔗 Relação com a aula

- Demonstra **SIMD** (1 instrução → vários dados) na prática, no hardware do aluno.
- O `3_arquitetura_instrucoes.py` conecta ao debate **RISC vs. CISC**.
- Segue o padrão de laboratório do curso (`.context.md`, §6.9 e §6.16).
