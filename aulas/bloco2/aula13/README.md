# 🧠 Aula 13 — Implementação de um Modelo Paralelo Simples (Síntese do Bloco 2)

**Objetivo:** implementar e comparar a **soma vetorial** e o **produto escalar** em **4 versões**
— Python puro, NumPy, Numba CUDA e CuPy — medindo o **speedup** e consolidando o Bloco 2 com
gráficos e um mini-relatório técnico.

---

## 🎯 Situação de aprendizagem

O setor pediu uma **prova técnica**: mostrar, com números, **quanto** a GPU realmente acelera um
workload simples — e a partir de qual tamanho de problema ela passa a compensar a CPU. Você vai
escrever a mesma operação em 4 níveis de abstração e compará-las.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula13.html`](apresentacao_aula13.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** com a implementação das 4 versões + **5 exercícios** |
| [`atividade.md`](atividade.md) | Roteiro de análise, mini-relatório e questionário (8–13) |

### Estrutura da aula

```
aula13/
  apresentacao_aula13.html
  README.md
  notebook_colab/aula13_implementacao_modelo_paralelo.ipynb
  atividade.md
```

> ℹ️ Esta aula **não tem `laboratorio_windows/`**: o benchmark exige **GPU** (Colab). O notebook
> detecta a ausência de GPU e mostra os números de referência.

---

## 🚀 Como rodar

### No Google Colab

1. Abra `notebook_colab/aula13_implementacao_modelo_paralelo.ipynb` pelo **GitHub** no Colab
   (`https://github.com/jonasmaffei/senac-tecnico-ia`).
2. *Ambiente de execução ➔ Alterar tipo de ambiente ➔ **T4 GPU*** ➔ *Salvar*.
3. Rode as células na ordem.

---

## 🔑 As 4 versões

| Versão | Onde roda | Característica |
| :--- | :--- | :--- |
| **Python puro** | CPU | laço interpretado — baseline lento |
| **NumPy** | CPU | vetorizado, usa BLAS |
| **Numba CUDA** | GPU | kernel explícito; controle das threads e shared memory |
| **CuPy** | GPU | API idêntica ao NumPy, rodando na VRAM |

### O que se aprende medindo

- **SIMD (CPU) × SIMT (GPU):** poucos núcleos potentes × milhares de threads simples.
- **Launch overhead + PCIe:** em N pequeno a GPU **perde**; a partir de um limiar, ela dispara.
- **Redução:** o produto escalar e a norma (`np.linalg.norm` × `cp.linalg.norm`) exigem reduzir
  muitos valores a um só — típico de workload que favorece a GPU.

---

## 🧪 Atividade guiada

Rode o notebook, preencha a tabela de tempos e responda ao roteiro em
[`atividade.md`](atividade.md). No fim, o notebook gera um **mini-relatório automático**.

---

## 💬 Discussão em grupo

Em grupos de 3–4:

1. Em que cenário real usaríamos cada uma das 4 versões?
2. Vale a pena escrever um kernel CUDA "na mão" (Numba) em vez de usar CuPy? Quando?
3. Que cuidados tomar ao comparar tempos de CPU e GPU (warm-up, sincronização)?
4. Como esse benchmark se conecta ao **Projeto Integrador**?

---

## 📝 Questionário de Consolidação (Aulas 8 a 13)

As **18 questões** de revisão estão em
[`questionarios/questionario-aulas-8-13.md`](../../../questionarios/questionario-aulas-8-13.md).

**Entrega:** envie as respostas por e-mail para `03049691093@senacrs.edu.br` com o assunto
`Questionario aulas 8 a 13`.

---

## 🔗 Relação com o curso

- **Aulas 7–10** ensinaram *como* programar a GPU (CUDA, OpenCL, ROCm). Esta aula **sintetiza**
  o bloco: implementa o mesmo problema em 4 níveis e **mede** quando vale a pena.
- **Próximo bloco (Aula 14):** automação — monitorar e agendar tarefas de GPU sem digitar
  comandos todo dia.
