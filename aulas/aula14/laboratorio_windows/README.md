# 🖥️ Laboratório Windows — Monitoramento de GPU e do Sistema com Bash (Aula 14)

Pasta autocontida para rodar a **Aula 14** no laboratório com **Windows + Git Bash**,
sem precisar instalar Python, gnuplot nem qualquer dependência.

Além da GPU, o laboratório coleta o **estado da máquina**: uso da **CPU** (%),
**memória RAM** (usada/total), **temperatura da CPU** (quando o sensor existe) e um
resumo de **especificações** (modelo da CPU, núcleos/threads, SO e placa de vídeo).

**As placas do laboratório são AMD** — e este laboratório foi feito para elas:

- **GPU AMD no Windows**: o script usa os **contadores de desempenho do Windows**
  para ler **utilização e VRAM reais** da placa. Temperatura e potência são estimadas
  (veja a observação abaixo).
- **GPU AMD no Linux (ROCm)**: usa `rocm-smi`/`amd-smi` com temperatura e energia reais.
- **GPU NVIDIA**: também funciona, via `nvidia-smi`.
- **CPU e RAM**: lidas de verdade em qualquer backend (Windows via CIM, Linux via `/proc`).
- **Sem GPU**: entra em modo simulado, com o mesmo formato de CSV.

> ⚠️ **Temperatura e potência na AMD/Windows são estimadas.** O driver AMD no Windows
> não expõe esses sensores para scripts. A temperatura é calculada a partir da utilização
> (repouso ~42 °C, carga ~90 °C) apenas para a atividade de alerta funcionar. Em um
> servidor **Linux com ROCm**, o `lib_gpu.sh` lê temperatura e consumo reais via
> `rocm-smi`/`amd-smi` — exatamente como discutido na Aula 10.

---

## 📋 Pré-requisitos

| Item | Situação |
| :--- | :--- |
| **Git para Windows** (traz o Git Bash) | Baixe em [git-scm.com/download/win](https://git-scm.com/download/win) |
| **GPU AMD** (Radeon / Instinct) | Usada de verdade via contadores do Windows |
| GPU NVIDIA | Opcional — também suportada via `nvidia-smi` |
| Python / gnuplot / outras libs | ❌ **Não precisa** |

> Durante a instalação do Git, mantenha a opção padrão que instala o **Git Bash**.

---

## 🚀 Passo a passo

### 1. Abrir o Git Bash na pasta

No **Explorer**, entre na pasta `aulas\aula14\laboratorio_windows`, clique com o botão
direito em um espaço vazio e escolha **"Open Git Bash here"**
(ou **"Abrir Git Bash aqui"**).

Se essa opção não aparecer, abra o Git Bash pelo Menu Iniciar e navegue até a pasta:

```bash
cd /c/caminho/para/senac-tecnico-ia/aulas/aula14/laboratorio_windows
```

> 💡 No Git Bash, o disco `C:` é acessado como `/c/`. Exemplo:
> `cd /c/Users/Jonas/Documents/repos/senac-tecnico-ia/aulas/aula14/laboratorio_windows`

### 2. Dar permissão de execução (só na primeira vez)

```bash
chmod +x *.sh
```

### 3. Rodar o fluxo completo

```bash
./rodar_tudo.sh
```

Esse comando executa os 3 passos: **coleta → alertas → dashboard**.

Todos os arquivos gerados vão para a pasta **`reports/`** (criada automaticamente).

Ao final, abra o arquivo **`reports/dashboard.html`** (duplo clique). Ele traz um
resumo de **especificações da máquina** e gráficos de **GPU** (temperatura, utilização,
VRAM, potência) e de **sistema** (utilização da CPU, RAM usada e, se disponível,
temperatura da CPU).

> Na primeira execução, o script imprime o backend detectado, por exemplo:
> `>> Backend de GPU: AMD no Windows (contadores de desempenho)`

---

## 🧩 Scripts disponíveis

| Script | O que faz | Exemplo |
| :--- | :--- | :--- |
| `rodar_tudo.sh` | Executa o fluxo completo (coleta + alerta + dashboard) | `./rodar_tudo.sh` |
| `1_monitorar.sh` | Coleta métricas e salva em CSV | `./1_monitorar.sh 5 gpu_log.csv 3600` |
| `2_alertar.sh` | Verifica limites de temperatura/utilização | `./2_alertar.sh 80 95` |
| `3_dashboard.sh` | Gera `reports/dashboard.html` com os gráficos de GPU e sistema (sem dependências) | `./3_dashboard.sh gpu_log.csv` |
| `4_agendar.sh` | Simula o cron e mostra como agendar no Windows/Linux | `./4_agendar.sh` |
| `lib_gpu.sh` | Funções internas de detecção de GPU e coleta do sistema (não rodar sozinho) | — |

> ✅ **Só arquivos `.sh`.** Não há nenhum `.ps1` nem outro tipo de arquivo executável,
> então as **políticas de segurança do laboratório não bloqueiam** nada. A leitura da GPU
> AMD no Windows é feita por um comando **inline** do PowerShell (`-EncodedCommand`),
> que não depende de ExecutionPolicy e não usa arquivo de script.

### Parâmetros do `1_monitorar.sh`

```bash
./1_monitorar.sh [intervalo_segundos] [arquivo_saida] [duracao_segundos]
```

- `intervalo_segundos` — tempo entre coletas (padrão: `5`)
- `arquivo_saida` — nome do CSV, salvo dentro de `reports/` (padrão: `reports/gpu_log.csv`)
- `duracao_segundos` — quanto tempo coletar (padrão: `3600`)

**Exemplo — coletar por 1 minuto, a cada 3 segundos** (tarefa de casa):

```bash
./1_monitorar.sh 3 gpu_log.csv 60
```

### Coleta incremental (o CSV só cresce)

O `reports/gpu_log.csv` é **incremental**: se já existir, as novas amostras são
**acrescentadas** ao final, preservando o histórico. O cabeçalho só é criado quando
o arquivo ainda não existe. Para começar do zero, apague o arquivo:

```bash
rm reports/gpu_log.csv
```

O dashboard lê **todo o histórico** do CSV. Se houver muitas amostras (milhares), ele
faz uma redução automática de pontos (1 a cada N) para o navegador não travar — o
período de tempo e o formato das curvas são mantidos. Ajuste com a variável
`MAX_PONTOS` (padrão: `1500`):

```bash
MAX_PONTOS=3000 ./3_dashboard.sh gpu_log.csv
```

---

## 📂 Arquivos gerados

Todos ficam dentro da pasta **`reports/`** (criada automaticamente na primeira execução):

| Arquivo | Descrição |
| :--- | :--- |
| `reports/gpu_log.csv` | Métricas coletadas, **incremental** (timestamp + uma linha por GPU + colunas de CPU/RAM) |
| `reports/alertas.log` | Registro dos alertas disparados (só é criado se houver alerta) |
| `reports/dashboard.html` | Painel com specs da máquina + gráficos de GPU e sistema |

> Esses arquivos são gerados localmente e **não precisam ser enviados ao Git**.

### Colunas do CSV

Cada linha é prefixada com o `timestamp` e, em seguida, traz os **10 campos da GPU**
e os **4 campos do sistema**:

```
timestamp,gpu_index,gpu_name,temp_c,util_gpu_pct,util_mem_pct,mem_used_mb,
mem_total_mb,power_w,power_limit_w,cpu_pct,ram_used_mb,ram_total_mb,cpu_temp_c
```

Quando a máquina tem mais de uma GPU, cada uma gera uma linha por amostra (os campos
de sistema repetem). Campos sem sensor aparecem como `N/A` (ex.: potência na
AMD/Windows).

O `reports/dashboard.html` mostra:

- um bloco de **especificações** (CPU, núcleos/threads, RAM total, placa de vídeo, SO);
- gráficos de **GPU** (temperatura, utilização, VRAM, potência);
- gráficos de **sistema** (utilização da CPU, RAM usada em GB e temperatura da CPU
  quando o sensor existe).

Em cada gráfico: eixo Y com escala e unidades, linhas de grade, os horários **no fuso
de Brasília (BRT, UTC-3)** e uma legenda com os valores **mínimo, máximo e atual**.
Quando uma métrica não existe no backend (ex.: potência na AMD/Windows), o card aparece
como **"Métrica não disponível"** em vez de desenhar uma reta enganosa em zero.

> ⏰ O fuso de Brasília é forçado via `TZ=BRT3`. Usamos `BRT3` (e não
> `America/Sao_Paulo`) porque o Git Bash no Windows não traz a base `tzdata`
> completa: com o nome da cidade, o horário caía silenciosamente para GMT.

---

## 🌡️ Alertas e webhook (bônus)

O `2_alertar.sh` dispara alerta quando a temperatura ou a utilização ultrapassam os
limites informados. Para enviar também a um **webhook do Slack/Discord**, defina a
variável de ambiente antes de rodar:

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/SEU/WEBHOOK/AQUI"
./2_alertar.sh 80 95
```

No Discord, acrescente `/slack` ao final da URL do webhook para aceitar o formato JSON.

---

## ⏰ Agendamento no Windows (equivalente ao cron)

No Git Bash **não existe `cron`**. O script `4_agendar.sh` simula as execuções e mostra
as opções. Para agendar de verdade no Windows, use o **Agendador de Tarefas** via
PowerShell (fora do Git Bash):

```powershell
schtasks /Create /TN "MonitorGPU" /SC DAILY /ST 08:00 ^
  /TR "\"C:\Program Files\Git\bin\bash.exe\" -lc \"cd /c/caminho/laboratorio_windows && ./1_monitorar.sh 5 gpu_log.csv 300\""
```

> Ajuste `/c/caminho/laboratorio_windows` para a pasta real na sua máquina.

---

## 🔧 Solução de problemas

| Problema | Causa provável | Solução |
| :--- | :--- | :--- |
| `Permission denied` ao rodar | Falta permissão de execução | `chmod +x *.sh` |
| `bash: ./x.sh: /bin/bash^M: bad interpreter` | Arquivo salvo com CRLF (Windows) | Converta com `sed -i 's/\r$//' *.sh` |
| `nvidia-smi: command not found` | Sem GPU NVIDIA — **normal nas máquinas AMD** | O script detecta AMD automaticamente; nada a fazer |
| Backend aparece como `simulado` numa máquina AMD | Interop do PowerShell indisponível no Git Bash | Reabra o **Git Bash** (não o WSL); ele executa `powershell.exe` |
| `powershell.exe: cannot execute binary file` | Você está no **WSL**, não no Git Bash | Use o **Git Bash** para interop com o Windows |
| Mensagens de "execução de scripts desabilitada" | Política de ExecutionPolicy do laboratório | Não usamos `.ps1`: o script é inline via `-EncodedCommand`, imune a essa política |
| Temperatura/potência como `N/A` | Driver AMD no Windows não expõe sensores | Esperado — temperatura é estimada; no Linux/ROCm são reais |
| `cd: no such file or directory` | Caminho incorreto no Git Bash | Use `/c/...`, não `C:\...` |
| Dashboard sem dados | `gpu_log.csv` vazio ou inexistente | Rode `./1_monitorar.sh 2 gpu_log.csv 20` antes |
| Nenhum alerta aparece | Amostras não passaram do limite | Rode `./1_monitorar.sh 1 gpu_log.csv 15` e depois `./2_alertar.sh 80 95` |

---

## 🐧 AMD com ROCm (Linux) — temperatura e potência reais

No laboratório (Windows) a temperatura é estimada. Em uma máquina **Linux com ROCm**
instalado, o `lib_gpu.sh` usa `rocm-smi`/`amd-smi` automaticamente e passa a registrar
**temperatura e consumo reais** — o mesmo ecossistema estudado na Aula 10.

```bash
# Verificar se o ROCm está presente (Linux)
rocm-smi          # ou: amd-smi metric
```

Para testar este laboratório via **WSL 2 com ROCm**, siga o
[tutorial de instalação do WSL](../../../docs/06_tutorial-instalacao-wsl.md) e o
[tutorial de Docker no WSL](../../../docs/07_tutorial-instalacao-docker-wsl.md).

---

## 🎓 Relação com a aula

Este laboratório reproduz, em Windows + Git Bash, o mesmo pipeline da aula:

```
nvidia-smi --query-gpu  →  monitor_gpu.sh  →  gpu_log.csv
   (AMD: amd-smi /          (loop Bash)      (armazenamento)
    contadores Windows)                           │
                                                  ▼
            3_dashboard.sh      ←        cron / systemd
            (visualização)              (agendamento automático)
```

- **`nvidia-smi --query-gpu`** → usado em `lib_gpu.sh`. Em máquinas **AMD**, o mesmo
  papel é feito por `amd-smi`/`rocm-smi` (Linux) ou pelos contadores do Windows.
- **`monitor_gpu.sh`** → equivalente em `1_monitorar.sh`.
- **`alerta_gpu.sh`** → equivalente em `2_alertar.sh`.
- **`gnuplot`** → substituído por `3_dashboard.sh` (HTML/SVG, sem instalar nada).
- **`cron`/`systemd`** → simulados em `4_agendar.sh`; no Windows, via Agendador de Tarefas.

> 🔎 **Ligação com a Aula 10 (ROCm):** o `rocBLAS`/`MIOpen`/`rocm-smi` são as peças AMD
> equivalentes ao ecossistema CUDA. Aqui, `rocm-smi` assume o papel do `nvidia-smi`.

Para a versão em nuvem (Google Colab), veja o notebook
[`aula14_automacao_gpu_bash.ipynb`](../aula14_automacao_gpu_bash.ipynb) e o
[guia do Colab](../README.md).
