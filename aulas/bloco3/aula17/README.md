# 🐍 Aula 17 — Automação de GPUs: versão enxuta (complemento da Aula 14)

**Objetivo:** revisar o pipeline de automação de telemetria da **Aula 14** numa versão
**enxuta e reproduzível**, com um **laboratório em Python cross-platform** — sem depender de
`cron`, `systemd` ou `gnuplot` do Linux.

> 📌 **Não é conteúdo novo.** Esta aula é um **complemento prático** da
> [Aula 14](../aula14/README.md). **Veja a Aula 14 primeiro.** Aqui o valor está em:
> (a) uma **demonstração enxuta no Colab** (os scripts Bash rodam no Linux do Colab) e
> (b) um **laboratório em Python** que faz o mesmo **sem Bash**, no Windows.

---

## 🎯 Situação de aprendizagem

O servidor de treinamento caiu de madrugada: a GPU passou de **95 °C** e o job falhou
silenciosamente. O time precisa de monitoramento **24h/7d**, mas **nem toda a equipe roda
Linux**. A missão é montar o mesmo sistema de telemetria em **Python**, que funciona no
Windows do laboratório e no Colab.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula17.html`](apresentacao_aula17.html) | Slides **só conceito** (foco na versão Python; navegue com ← →) |
| [`atividade.md`](atividade.md) | Roteiro prático e discussão |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** (demo enxuta + 5 exercícios) |
| [`laboratorio_windows/`](laboratorio_windows/README.md) | **Versão Python** dos scripts (roda no Windows, **sem Bash**) |

### Estrutura da aula

```
aula17/
  apresentacao_aula17.html
  README.md
  notebook_colab/aula17_automacao_gpu_bash.ipynb
  laboratorio_windows/          # 1_monitor_gpu.py, 2_alerta_gpu.py, 3_gerar_graficos.py, 4_enviar_sheets.py
  atividade.md
```

> 🧩 **Bash vs. Python:** a versão **Bash** (`monitor_gpu.sh`, `alerta_gpu.sh`, …) vive na
> **Aula 14** (`scripts_linux/`) e é a padrão para servidores Linux. O **notebook** desta aula
> demonstra esses mesmos scripts no Colab (que é Linux); o **laboratório** mostra a alternativa
> **100% Python**, que roda até no Windows sem Bash.

---

## 🚀 Como usar

### No Google Colab

Abra `notebook_colab/aula17_automacao_gpu_bash.ipynb` e resolva a seção **Exercícios (5)**.

### No Windows (host local)

Dê **duplo clique** em [`laboratorio_windows/iniciar.bat`](laboratorio_windows/iniciar.bat):
ele cria o `.venv`, instala as dependências e abre o menu.

---

## 🔑 Conceitos-chave

- **`nvidia-smi --query-gpu`** — métricas em CSV limpo (mesmo princípio da Aula 14).
- **Python `subprocess`** — chamar o `nvidia-smi` de dentro do Python.
- **Agendamento portátil** — loop Python no lugar do `cron` (que não existe no Windows/Colab).
- **Dashboards** — `matplotlib` no lugar do `gnuplot`.
- **Google Sheets** — publicar a telemetria sem depender de SSH.

---

## 🔗 Relação com o curso

- **Aula 14** é a referência do tema (versão **Bash/Linux**). Esta aula **não substitui** —
  ela mostra a **alternativa Python cross-platform**.
- **Próxima (Aula 18):** a mesma relação, mas para **concorrência/filas** (versão Python da
  Aula 15).
