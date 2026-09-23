# 🛠️ Aula 14 — Introdução à Automação de GPUs com Bash

**Objetivo:** operar GPUs de forma **contínua e supervisionada** com Bash — extrair métricas
estruturadas do `nvidia-smi`, escrever scripts de coleta e alerta, agendar com `cron`/systemd,
gerar dashboards e integrar com o Google Sheets.

---

## 🎯 Situação de aprendizagem

Um servidor de GPUs fica ligado 24h/7d. Sem monitoramento, a placa pode **superaquecer**,
**travar silenciosamente** ou ficar **ociosa** — queimando orçamento de nuvem sem ninguém
perceber. A missão é automatizar a **coleta, o alerta e o dashboard** das métricas.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula14.html`](apresentacao_aula14.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** com explicação + **5 exercícios** |
| [`laboratorio_windows/`](laboratorio_windows/README.md) | **Experimentos com hardware real** (Git Bash / AMD) |
| [`scripts_linux/`](scripts_linux) | Scripts para **servidor Linux** (monitor, alerta, gráficos, Sheets) |
| [`laboratorio_realtime-docker/`](laboratorio_realtime-docker/README.md) | Desafio extra: webservice Flask + SSE em Docker |
| [`laboratorio_realtime-windows/`](laboratorio_realtime-windows/README.md) | Desafio extra: mesmo webservice, nativo no Windows |
| [`atividade.md`](atividade.md) | Atividade de pesquisa e discussão (tarefa de casa) |

### Estrutura da aula

```
aula14/
  apresentacao_aula14.html
  README.md
  notebook_colab/aula14_automacao_gpu_bash.ipynb
  laboratorio_windows/          # 1_monitorar.sh, 2_alertar.sh, 3_dashboard.sh, 4_agendar.sh
  scripts_linux/                # monitor_gpu.sh, alerta_gpu.sh, gerar_graficos.sh, enviar_para_sheets.py
  laboratorio_realtime-docker/  # webservice em Docker (SSE)
  laboratorio_realtime-windows/ # webservice nativo no Windows
  atividade.md
```

---

## 🚀 Opção 1: Abrir Direto via GitHub (Mais Rápido e Recomendado)

1. Acesse o site do [Google Colab](https://colab.research.google.com/).
2. Faça login com a sua conta Google (Gmail).
3. Na janela pop-up que abrir, selecione a aba **GitHub**.
4. No campo de busca, cole a URL do repositório da turma:
   ```text
   https://github.com/jonasmaffei/senac-tecnico-ia
   ```
5. O Colab irá listar os arquivos do repositório. Clique em:
   `aulas/aula14/notebook_colab/aula14_automacao_gpu_bash.ipynb`
6. Pronto! O notebook abrirá na sua tela.

---

## 💻 Opção 2: Fazer Download do Arquivo e Subir no Colab (Upload)

1. Acesse o site do [Google Colab](https://colab.research.google.com/).
2. Na janela inicial, clique na aba **Fazer upload** (ou **Upload**).
3. Clique em **Escolher arquivo** e selecione o arquivo `aula14_automacao_gpu_bash.ipynb`.
4. Aguarde o carregamento e o notebook abrirá automaticamente.

---

## ⚙️ PASSO CRÍTICO: Ativar a GPU no Google Colab

Por padrão, o Colab roda apenas com **CPU**. Para coletar métricas reais com `nvidia-smi`:

1. No menu superior, clique em **Ambiente de execução** (*Runtime*).
2. Clique em **Alterar tipo de ambiente de execução** (*Change runtime type*).
3. Em **Acelerador de hardware**, mude para **T4 GPU** (ou GPU disponível).
4. Clique em **Salvar**.
5. Confirme no canto superior direito o ícone verde de **RAM / GPU**.

> 💡 **Não conseguiu GPU?** O notebook detecta a ausência do `nvidia-smi` e entra em
> **modo simulado**, gerando métricas sintéticas com o mesmo formato do CSV real.
> Toda a aula (dashboard, alertas e integração) continua funcionando.

---

## 🧩 O que funciona (e o que muda) no Colab

| Tecnologia | No Colab | Observação |
| :--- | :--- | :--- |
| `nvidia-smi` | ✅ funciona | Alguns campos vêm `N/A` no T4 (`fan.speed`, às vezes `power.limit`) |
| Scripts Bash (`monitor_gpu.sh`) | ✅ funciona | Executados com `!` ou `%%writefile` no notebook |
| **cron / systemd** | ❌ **não existem** | Runtime efêmero sem init; simulamos com loop Python e mostramos a sintaxe do crontab |
| `gnuplot` | ⚠️ instalável | `apt-get install gnuplot`; usamos **Matplotlib** por ser mais confiável |
| Google Sheets API | ✅ funciona | Requer **service account** + JSON enviado ao Colab (não commitar) |

---

## 🟢 Conteúdo do Notebook da Aula 14

No notebook `notebook_colab/aula14_automacao_gpu_bash.ipynb`, você encontrará:

1. **Verificação do Ambiente** (detecção de GPU e `nvidia-smi`).
2. **Teoria: `nvidia-smi`** — queries, formatos e campos úteis.
3. **Demo: `monitor_gpu.sh`** — coleta de métricas com timestamp em CSV.
4. **Teoria: `cron` e `systemd timers`** — agendamento e comparativo.
5. **Alertas** — `alerta_gpu.sh` com verificação de limites e notificação.
6. **Atividade: Dashboard** — 4 gráficos (temperatura, utilização, VRAM, potência).
7. **Integração com o Google Sheets** — template via service account.
8. **Discussão em grupo**, **Exercícios (5)** e **síntese**.

---

## 📂 Scripts para servidor Linux (`scripts_linux/`)

Scripts prontos para servidores Linux reais:

- [`monitor_gpu.sh`](scripts_linux/monitor_gpu.sh) — coleta métricas de GPU em CSV.
- [`alerta_gpu.sh`](scripts_linux/alerta_gpu.sh) — verifica limites e notifica (Slack/e-mail).
- [`gerar_graficos.sh`](scripts_linux/gerar_graficos.sh) — dashboard de 4 gráficos com gnuplot.
- [`enviar_para_sheets.py`](scripts_linux/enviar_para_sheets.py) — publica o CSV no Google
  Sheets (sem credenciais, apenas valida e avisa, sem falhar).

---

## 🖥️ Laboratório Windows (Git Bash) — placas AMD

A pasta [`laboratorio_windows/`](laboratorio_windows/) é uma versão **autocontida** da aula
para rodar no **laboratório com Windows + Git Bash**, sem instalar Python nem gnuplot.

- Detecta automaticamente **GPU AMD** (via contadores de desempenho do Windows) e
  também **NVIDIA** (`nvidia-smi`) ou o modo simulado.
- Coleta **utilização e VRAM reais** da AMD; temperatura/potência são estimadas no
  Windows (no **Linux com ROCm**, `rocm-smi`/`amd-smi` fornecem valores reais).
- Gera dashboard em **HTML** (abre no navegador) — sem dependências.

Comece por: [`laboratorio_windows/README.md`](laboratorio_windows/README.md).

```bash
cd aulas/aula14/laboratorio_windows
chmod +x *.sh
./rodar_tudo.sh
```

---

## ⚡ Desafio extra: Monitoramento em Tempo Real (Docker)

Duas versões do **webservice em Python** que coleta métricas continuamente e as exibe
**ao vivo no navegador** (sem recarregar a página), em `http://localhost:5000`:

**[`laboratorio_realtime-docker/`](laboratorio_realtime-docker/)** — roda em container
Docker (ideal para servidores Linux e para a GPU NVIDIA real com `--gpus all`):

```bash
cd aulas/aula14/laboratorio_realtime-docker
docker compose up --build
```

**[`laboratorio_realtime-windows/`](laboratorio_realtime-windows/)** — roda como
processo Python **nativo no Windows** (sem Docker), lendo a GPU AMD pelos contadores
do Windows enquanto o processo estiver ativo:

```bash
cd aulas/aula14/laboratorio_realtime-windows
python servidor.py
```

Ambos usam **Flask + Server-Sent Events (SSE)**, **CPU e RAM reais** com `psutil` e
gravam o histórico em `reports/metricas.csv`.

---

## 📌 Tarefa de Casa

1. Adapte `monitor_gpu.sh` para coletar **10 minutos** com intervalo de **3 s**.
2. Crie o dashboard (gnuplot ou Matplotlib) com os **4 gráficos** da aula.
3. Configure um **cron job** que execute o monitoramento **todo dia às 08h**.
4. **Bônus:** implemente o alerta de temperatura com envio para **webhook Slack ou Discord**.
