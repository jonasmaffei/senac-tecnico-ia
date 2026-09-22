# 🐳 Laboratório Realtime (Docker) — Monitoramento ao vivo com Webservice

**Desafio extra da Aula 14.** Enquanto o [`laboratorio_windows`](../laboratorio_windows/)
gera um dashboard **estático** (arquivo HTML), este laboratório sobe um **webservice em
Python** que coleta métricas continuamente e as exibe **em tempo real no navegador** —
sem recarregar a página — tudo rodando dentro de um **container Docker**.

> 👬 **Versão irmã:** [`laboratorio_realtime-windows`](../laboratorio_realtime-windows/)
> roda o MESMO webservice, mas como processo Python nativo no Windows (sem Docker).
> Escolha o Docker para portabilidade/servidores; escolha o Windows para rodar direto
> na máquina do laboratório.

> 🎯 **Pergunta que este desafio responde:** *"E se, em vez de abrir um arquivo HTML,
> eu tivesse um painel vivo, que atualiza sozinho a cada segundo, acessível de qualquer
> máquina da rede pelo navegador?"*

---

## 🧭 O que muda em relação ao laboratório anterior

| | `laboratorio_windows` | `laboratorio_realtime-docker` (este) |
| :--- | :--- | :--- |
| Linguagem | Bash + CSV + HTML | **Python** (Flask + psutil) |
| Atualização | Estática (gera o HTML e abre) | **Ao vivo** (SSE, sem recarregar) |
| Execução | Direto no Windows/Git Bash | **Docker** (isolado e portátil) |
| Acesso | Arquivo local | **Navegador** via `http://localhost:5000` |
| Histórico | CSV incremental | Memória + CSV no volume |

> 🔀 **Docker vs. Windows:** este laboratório usa Docker. Se quiser rodar o mesmo
> webservice **direto no Windows** (sem container), use a versão
> [`laboratorio_realtime-windows`](../laboratorio_realtime-windows/).

---

## 🏗️ Arquitetura da solução

```
  psutil / nvidia-smi
        │  (coleta a cada 2s)
        ▼
   coletor.py ──────────►  servidor.py (Flask)
        │                       │
        │                       ├─►  /            painel HTML
        │                       ├─►  /api/metricas JSON (histórico)
        │                       ├─►  /api/stream   SSE (tempo real)
        │                       └─►  /health       status
        │
        └─► reports/metricas.csv  (volume Docker)
                                       │
                    http://localhost:5000  ◄── navegador do Windows
```

**Por que Server-Sent Events (SSE)?** É a forma mais simples de "empurrar" dados do
servidor para o navegador: o servidor mantém a conexão HTTP aberta e envia cada nova
amostra como texto `data: {...}`. Não precisa de WebSocket nem de bibliotecas no
front-end — só `EventSource` do JavaScript.

---

## 📋 Pré-requisitos

| Item | Situação |
| :--- | :--- |
| **Docker** (Desktop no Windows ou Engine no WSL 2) | Obrigatório |
| **Navegador** (Chrome / Edge / Firefox) | Obrigatório |
| Python, Flask, psutil | ❌ **Não precisa no host** — tudo roda no container |

> 🐳 Ainda não tem Docker? Siga o
> [tutorial de instalação do Docker no WSL 2](../../../docs/07_tutorial-instalacao-docker-wsl.md)
> ou o [tutorial do WSL](../../../docs/06_tutorial-instalacao-wsl.md).

---

## 🚀 Passo a passo

### 1. Abrir o terminal na pasta

```bash
cd aulas/aula14/laboratorio_realtime-docker
```

### 2. Subir o serviço com Docker Compose

```bash
docker compose up --build
```

Na primeira vez o Docker baixa a imagem do Python e instala o Flask/psutil (leva
alguns minutos). Nas próximas, é quase instantâneo.

> 💡 Prefere rodar em segundo plano? Use `docker compose up --build -d` e acompanhe
> com `docker compose logs -f`.

### 3. Abrir no navegador

Acesse **http://localhost:5000** (no Windows, basta abrir o navegador; o Docker
expõe a porta `5000` para o host).

Você verá:
- o cartão de **especificações** (host, CPU, RAM, GPU);
- os gráficos de **GPU** (temperatura, utilização, VRAM, potência);
- os gráficos de **sistema** (CPU e RAM);
- um **ponto verde "ao vivo"** que pulsa enquanto a conexão SSE estiver ativa.

### 4. Parar o serviço

```bash
docker compose down
```

---

## 🧩 Arquivos do projeto

| Arquivo | O que faz |
| :--- | :--- |
| `app/coletor.py` | Lê **CPU e RAM reais** (psutil); **GPU simulada** no Windows (ou real via `nvidia-smi` em Linux com `--gpus all`) |
| `app/servidor.py` | Webservice Flask: thread de coleta, rotas, SSE e gravação do CSV |
| `app/templates/dashboard.html` | Painel em HTML + SVG + JavaScript que se atualiza via SSE |
| `Dockerfile` | Imagem Python 3.11-slim com Flask e psutil |
| `docker-compose.yml` | Sobe o serviço, expõe a porta 5000 e monta o volume `./reports` |
| `requirements.txt` | Dependências (Flask, psutil) |
| `.dockerignore` | Evita copiar lixo para dentro da imagem |
| `reports/` | Volume onde o CSV de histórico é gravado |

---

## 🔌 Endpoints da API

| Rota | O que devolve |
| :--- | :--- |
| `GET /` | O painel HTML (dashboard ao vivo) |
| `GET /api/metricas` | JSON com **todo o histórico** em memória |
| `GET /api/specs` | JSON com as especificações da máquina |
| `GET /api/stream` | Fluxo **SSE** — uma amostra por mensagem |
| `GET /health` | `{"status": "ok"}` — útil para monitoração |

Teste rápido sem navegador (com o serviço no ar):

```bash
curl http://localhost:5000/health
curl http://localhost:5000/api/metricas
curl -N http://localhost:5000/api/stream   # Ctrl+C para sair
```

---

## ⚙️ Configuração (variáveis de ambiente)

Definidas no `docker-compose.yml` e podem ser alteradas sem tocar no código:

| Variável | Padrão | Descrição |
| :--- | :--- | :--- |
| `INTERVALO` | `2` | Segundos entre coletas |
| `MAX_AMOSTRAS` | `900` | Quantas amostras manter em memória (900 × 2s = 30 min) |
| `CSV_ARQUIVO` | `reports/metricas.csv` | Caminho do CSV de histórico no volume |
| `GPU_BACKEND` | `auto` | `simulado` força a GPU sintética; `auto` tenta `nvidia-smi` |

Exemplo: coletar a cada 5s e guardar 1 hora de histórico:

```bash
INTERVALO=5 MAX_AMOSTRAS=720 docker compose up --build
```

---

## 🎮 GPU: simulada vs. real

No **Docker dentro do Windows (WSL 2)**, o container não acessa a GPU **AMD** — por
isso a GPU é **simulada** com valores plausíveis (a CPU e a RAM são reais, via
psutil). Isso é intencional: mantém o desafio executável em qualquer máquina.

Em um **host Linux com GPU NVIDIA**, o container pode ler a placa de verdade. Basta:

1. Ter o driver NVIDIA e o `nvidia-container-toolkit` instalados.
2. Descomentar o bloco `deploy:` no `docker-compose.yml`.
3. Remover a variável `GPU_BACKEND` do `environment`.
4. Subir com `docker compose up --build`.

O `coletor.py` detecta o `nvidia-smi` automaticamente e passa a usá-lo.

---

## 🧪 Desafios propostos (para ir além)

1. **Ajuste o intervalo** de coleta para 1s e observe o painel se atualizar mais rápido.
2. **Adicione um gráfico novo** (ex.: temperatura da CPU) no `dashboard.html`.
3. **Crie uma rota `/api/alertas`** que devolve as amostras que ultrapassaram
   um limite de temperatura, reaproveitando a lógica do `2_alertar.sh`.
4. **Troque o SSE por polling:** faça o JavaScript buscar `/api/metricas` a cada
   2s com `setInterval` + `fetch` e compare a experiência.
5. **Persistência:** carregue `reports/metricas.csv` na inicialização para o gráfico
   continuar de onde parou, mesmo após reiniciar o container.
6. **Dockerfile:** troque o servidor de desenvolvimento do Flask por um servidor
   WSGI de produção (ex.: `waitress` ou `gunicorn`).

---

## 🔧 Solução de problemas

| Problema | Causa provável | Solução |
| :--- | :--- | :--- |
| `port is already allocated` | Outra aplicação usa a porta 5000 | Troque para `"5001:5000"` no compose e acesse `localhost:5001` |
| Página não abre | Container ainda subindo | Rode `docker compose logs -f` e espere "Running on 0.0.0.0:5000" |
| Ponto vermelho "reconectando…" | Serviço parou ou reiniciou | Verifique `docker compose ps` e os logs |
| Gráficos vazios | Ainda não coletou amostras | Aguarde alguns segundos (primeira coleta leva ~1s de CPU) |
| `docker: command not found` | Docker não instalado | Veja o [tutorial do Docker no WSL 2](../../../docs/07_tutorial-instalacao-docker-wsl.md) |
| GPU sempre "simulada" em Linux | GPU não exposta ao container | Configure `--gpus all` / bloco `deploy` do compose |

---

## 🔗 Relação com a Aula 14

Este laboratório é a evolução natural do pipeline da aula:

```
nvidia-smi → monitor_gpu.sh → CSV → gnuplot/cron        (aula base)
     │
     └──► coletor.py → Flask + SSE → navegador ao vivo   (este desafio)
```

Ele conecta três ideias da aula: **coleta** (como o `monitor_gpu.sh`), **automação**
(loop em vez de `cron`) e **visualização** (painel que substitui o `gnuplot`), agora
empacotadas em um **container Docker** — o mesmo ecossistema de deploy visto nas
Aulas 9 e 10.
