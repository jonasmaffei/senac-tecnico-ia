# 🌙 Aula 18 + 19 — Concorrência e Energia na GPU

**Objetivo:** operar a GPU com **justiça** (1 job por vez + fila com prioridade) e com
**eficiência** (medir e limitar a energia).

> 📌 Reúne **concorrência + energia** num único material, com apresentação, notebook e os dois
> laboratórios. A concorrência apoia-se na [Aula 15](../aula15/README.md), que apresenta o
> tema com `flock`/`systemd`.

---

## 🎯 Situação de aprendizagem

O data center consome **40% mais energia** que o projetado **e** os jobs disputam a mesma GPU
causando **CUDA OOM**. Os dois problemas têm a mesma raiz: **falta de controle sobre a GPU**.
Vamos resolver ambos: primeiro a **concorrência**, depois a **energia**.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula18_19.html`](apresentacao_aula18_19.html) | Slides **só conceito** (11 slides; navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook único no **Google Colab** (concorrência + energia) + **Exercícios (5)** |
| [`laboratorio_concorrencia/`](laboratorio_concorrencia/README.md) | **Lab Python** (Windows): lock por diretório + fila por prioridade |
| [`laboratorio_energia/`](laboratorio_energia/README.md) | **Lab Windows:** monitor térmico, alerta, benchmark de eficiência e Power Limit |
| [`scripts_linux/`](scripts_linux) | Scripts para **servidor Linux + NVIDIA** (monitorar, definir PL, benchmark, alerta) |
| [`atividade.md`](atividade.md) | Roteiro das práticas, discussão e entrega |

### Estrutura da pasta

```
aula18_19_dupla/
  apresentacao_aula18_19.html
  README.md
  notebook_colab/aula18_19_concorrencia_energia.ipynb
  laboratorio_concorrencia/     # 1_flock_gpu.py, 2_gpu_queue.py, 3_teste_fila.py, 4_monitor_processos_gpu.py
  laboratorio_energia/          # lib_energia.py + 1_monitor_thermal, 2_alerta, 3_benchmark, 4_controle_pl
  scripts_linux/                # monitor_thermal.sh, set_power_limit.sh, benchmark_energetico.sh, alerta_termico.sh
  atividade.md
```

---

## 🚀 Como usar

### No Google Colab (recomendado)

1. Abra `notebook_colab/aula18_19_concorrencia_energia.ipynb` pelo **GitHub** no Colab.
2. Rode as células na ordem. **Sem GPU NVIDIA**, tudo roda em **modo simulado** — os conceitos
   valem igual.

### No Windows (laboratório)

Dê **duplo clique** no `iniciar.bat` de cada laboratório:

- **Concorrência:** [`laboratorio_concorrencia/iniciar.bat`](laboratorio_concorrencia/iniciar.bat)
  → lança 4 jobs e mostra a serialização por prioridade.
- **Energia:** [`laboratorio_energia/iniciar.bat`](laboratorio_energia/iniciar.bat)
  → monitor térmico, alerta, benchmark de eficiência e Power Limit.

### Em servidor Linux (produção)

Os scripts de energia estão em [`scripts_linux/`](scripts_linux):

```bash
cd aulas/bloco3/aula18_19_dupla/scripts_linux
chmod +x *.sh
./monitor_thermal.sh 5 60          # coleta temp/potência por 60 s
sudo ./set_power_limit.sh 200      # define PL=200W
./benchmark_energetico.sh 250 200 150 100
```

---

## 🔑 Conceitos-chave

- **Race condition** — jobs concorrentes corrompem a VRAM → OOM.
- **Lock / exclusão mútua** — `flock` (Linux) ou **lock por diretório** (`mkdir` atômico).
- **Fila por prioridade** — ticket `prioridade_timestamp_nome`, com **aging** contra starvation.
- **TDP / TGP** e **thermal throttling** — por que GPUs gastam mais do que o esperado.
- **Power Limit** — reduzir 20–30% custa ~5–10% de throughput; melhora muito o consumo.
- **Eficiência (imgs/J)** — throughput ÷ potência; ótimo em **~60–75% do TDP**.

---

## 🔗 Relação com o curso

- **Aula 15** (Bash) é a referência conceitual de concorrência; aqui o **laboratório de
  concorrência** traz a versão **Python** (lock por diretório), e o notebook exercita lock +
  fila.
- **Aula 14/17** (automação) preparam a telemetria; aqui ela ganha as colunas de **energia**.
- Encerra o Bloco 3: a GPU passa a ser operada com **justiça** e **eficiência**.

---

## 📝 Questionário de Consolidação (Aulas 14 a 19)

As **18 questões** de revisão do Bloco 3 estão em
[`questionarios/questionario-aulas-14-19.md`](../../../questionarios/questionario-aulas-14-19.md).

**Entrega:** envie as respostas por e-mail para `03049691093@senacrs.edu.br` com o assunto
`Questionario aulas 14 a 19`.
