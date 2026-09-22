# 🪟 Laboratório Realtime (Windows) — Monitoramento ao vivo com Webservice

**Desafio extra da Aula 14.** Este é um **programa Python que roda direto no Windows**
(sem Docker): enquanto o processo estiver ativo, ele coleta métricas do PC e da GPU e
as publica **ao vivo no navegador** em `http://localhost:5000` — sem recarregar a página.

> 👬 **Versão irmã:** [`laboratorio_realtime-docker`](../laboratorio_realtime-docker/)
> roda o mesmo webservice dentro de um **container Docker** (mais portátil, ideal para
> servidores Linux e GPU NVIDIA real). Escolha esta versão Windows para rodar **na
> própria máquina do laboratório**, lendo a **GPU AMD de verdade**.

---

## 🧭 Comparação das versões

| | `laboratorio_windows` | **`laboratorio_realtime-windows`** (esta) | `laboratorio_realtime-docker` |
| :--- | :--- | :--- | :--- |
| Linguagem | Bash + CSV + HTML | **Python** (Flask + psutil) | Python (Flask + psutil) |
| Atualização | Estática | **Ao vivo** (SSE) | Ao vivo (SSE) |
| Execução | Git Bash | **Python nativo no Windows** | Container Docker |
| GPU AMD | Contadores do Windows | **Contadores do Windows** | Simulada |
| GPU NVIDIA | `nvidia-smi` | `nvidia-smi` | `nvidia-smi` (com `--gpus all`) |

---

## 🏗️ Como funciona

```
psutil (CPU/RAM)  +  contadores do Windows (GPU AMD)
        │  coleta a cada 2s
        ▼
   coletor.py ──────►  servidor.py (Flask)
        │                   │
        │                   ├─►  /            painel HTML
        │                   ├─►  /api/metricas JSON
        │                   ├─►  /api/stream   SSE (tempo real)
        │                   └─►  /health       status
        │
        └─► reports/metricas.csv  (histórico em disco)
                                     │
               http://localhost:5000  ◄── navegador
```

Enquanto a janela do programa estiver aberta, a **thread de coleta** continua
rodando. Ao fechar (ou `Ctrl+C`), o monitoramento para.

---

## 📋 Pré-requisitos

| Item | Situação |
| :--- | :--- |
| **Python 3.10+** (com "Add Python to PATH") | Obrigatório — [python.org/downloads](https://www.python.org/downloads/) |
| **Navegador** (Chrome / Edge / Firefox) | Obrigatório |
| Docker | ❌ não precisa (use a [versão Docker](../laboratorio_realtime-docker/) se preferir) |

---

## 🚀 Passo a passo

### Opção A — Atalho (mais fácil)

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat). Ele cria o ambiente virtual,
instala as dependências e abre o navegador automaticamente.

### Opção B — Manual (Prompt de Comando / PowerShell)

```bat
cd aulas\aula14\laboratorio_realtime-windows

REM (só na primeira vez) criar ambiente virtual e instalar dependências
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt

REM rodar o monitoramento
.venv\Scripts\python.exe app\servidor.py
```

Depois abra **http://localhost:5000** no navegador.

> 💡 Para encerrar, pressione `Ctrl+C` no terminal ou feche a janela.

---

## 🧩 Arquivos do projeto

| Arquivo | O que faz |
| :--- | :--- |
| `app/coletor.py` | Lê **CPU/RAM reais** (psutil) e a **GPU AMD real** (contadores do Windows via PowerShell/CIM) |
| `app/servidor.py` | Webservice Flask: thread de coleta, rotas, SSE e gravação do CSV |
| `app/templates/dashboard.html` | Painel em HTML + SVG que se atualiza via SSE |
| `iniciar.bat` | Atalho que cria o venv, instala dependências e abre o navegador |
| `requirements.txt` | Dependências (Flask, psutil) |
| `reports/` | Onde o histórico `metricas.csv` é gravado |

> ℹ️ Não há `.ps1`: a leitura da GPU usa o PowerShell **inline** (`-Command`), que não
> depende de `ExecutionPolicy` — a mesma técnica do `laboratorio_windows`.

---

## 🔌 Endpoints da API

| Rota | O que devolve |
| :--- | :--- |
| `GET /` | O painel HTML (dashboard ao vivo) |
| `GET /api/metricas` | JSON com **todo o histórico** em memória |
| `GET /api/specs` | JSON com as especificações da máquina |
| `GET /api/stream` | Fluxo **SSE** — uma amostra por mensagem |
| `GET /health` | `{"status": "ok"}` |

Teste rápido (com o programa rodando):

```bat
curl http://localhost:5000/health
curl http://localhost:5000/api/metricas
```

---

## ⚙️ Configuração (variáveis de ambiente)

| Variável | Padrão | Descrição |
| :--- | :--- | :--- |
| `INTERVALO` | `2` | Segundos entre coletas |
| `MAX_AMOSTRAS` | `900` | Quantas amostras manter em memória (900 × 2s = 30 min) |
| `CSV_ARQUIVO` | `reports/metricas.csv` | Caminho do CSV de histórico |
| `GPU_BACKEND` | `auto` | `simulado` força GPU sintética; `auto` tenta AMD/NVIDIA |

Exemplo (Prompt de Comando):

```bat
set INTERVALO=1
set MAX_AMOSTRAS=3600
.venv\Scripts\python.exe app\servidor.py
```

---

## 🎮 GPU: real vs. simulada

- **AMD no Windows:** utilização e VRAM **reais** pelos contadores de desempenho;
  a **temperatura é estimada** (o driver AMD não a expõe) e a **potência fica
  indisponível** — o painel mostra "Métrica não disponível" nesse caso.
- **NVIDIA:** todos os campos reais via `nvidia-smi`.
- **Sem GPU:** modo simulado, com o mesmo formato de dados.

---

## 🧪 Desafios propostos

1. Ajuste `INTERVALO` para 1s e veja o painel atualizar mais rápido.
2. Adicione um gráfico de **temperatura da CPU** (veja o `psutil.sensors_temperatures`).
3. Crie uma rota `/api/alertas` que devolve as amostras acima de um limite de temperatura.
4. Troque o SSE por **polling** (`setInterval` + `fetch` em `/api/metricas`) e compare.
5. Faça o gráfico **continuar de onde parou** ao reabrir, lendo `reports/metricas.csv`.
6. Compare as versões Windows e Docker: qual é mais simples de rodar? Qual é mais portátil?

---

## 🔧 Solução de problemas

| Problema | Causa provável | Solução |
| :--- | :--- | :--- |
| `python não é reconhecido` | Python fora do PATH | Reinstale marcando **"Add Python to PATH"** |
| `No module named flask` | Dependências não instaladas | `.venv\Scripts\python.exe -m pip install -r requirements.txt` |
| `porta 5000 em uso` | Outro programa usa a porta | `set INTERVALO=2` e troque a porta no `servidor.py` (ou feche o outro app) |
| GPU sempre "simulada" | Sem GPU/ driver indisponível | Normal em máquina sem GPU; em AMD verifique o driver |
| Potência "Métrica não disponível" | Driver AMD não expõe potência | Esperado no Windows; use NVIDIA/Linux para esse campo |
| Ponto vermelho "reconectando…" | O processo foi encerrado | Rode novamente o `iniciar.bat` / `servidor.py` |

---

## 🔗 Relação com a Aula 14

Mesma evolução do pipeline da aula, agora em Python nativo no Windows:

```
nvidia-smi / contadores AMD → monitor_gpu.sh → CSV → gnuplot       (aula base)
        │
        └──► coletor.py → Flask + SSE → navegador ao vivo           (este desafio)
```
