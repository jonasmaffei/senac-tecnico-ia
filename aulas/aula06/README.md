# 🧠 Aula 06 — Sistemas Operacionais Linux e GPU

**Objetivo:** utilizar comandos e estruturas do Linux para gerenciar sistemas com GPUs,
preparando e automatizando o ambiente para execução de cargas de trabalho de IA.

---

## 🎯 Situação de aprendizagem

Você foi designado(a) para manter o **servidor Linux** da startup que hospeda as GPUs usadas
no treinamento dos modelos de IA. Na segunda-feira, você recebe o acesso pela primeira vez —
precisa verificar quais GPUs estão instaladas, se os drivers estão corretos, monitorar o uso
de recursos e criar um **script de automação que envia alertas quando a temperatura das GPUs
ultrapassa 80°C**. Tudo isso via linha de comando Linux.

---

## 🗂️ Conteúdo

| Arquivo | O que é |
| :--- | :--- |
| [`apresentacao_aula06.html`](apresentacao_aula06.html) | Slides teóricos (abra no navegador, navegue com ← →) |
| [`aula06_linux_gpu.ipynb`](aula06_linux_gpu.ipynb) | Notebook do **Google Colab** (pseudo-arquivos, drivers, alerta, cron) |
| [`atividade.md`](atividade.md) | Atividade guiada (script Bash, cron/systemd) + discussão |
| `scripts/` | Scripts comentados e templates de automação |

### Scripts

| Arquivo | O que faz |
| :--- | :--- |
| [`gpu_status.sh`](scripts/gpu_status.sh) | Lista GPUs (NVIDIA/AMD) com temperatura, uso e **alerta** acima do limite |
| [`monitoramento_linux.py`](scripts/monitoramento_linux.py) | Lê `/proc` e `/sys` (Linux) ou o equivalente no Windows (psutil) |
| [`cron_exemplos.sh`](scripts/cron_exemplos.sh) | **Referência** comentada de linhas de crontab para servidores de GPU |
| [`gpu-monitor.service`](scripts/gpu-monitor.service) | Template de unit systemd para monitor contínuo |

---

## 🚀 Como rodar

### No Google Colab (recomendado)

1. Abra `aula06_linux_gpu.ipynb` pelo **GitHub** no Colab
   (`https://github.com/jonasmaffei/senac-tecnico-ia`).
2. Rode as células na ordem. As células com `!` usam o shell do Linux.

> 💡 **Sem GPU?** As células caem para exemplos simulados e explicam cada comando.

### No Windows do laboratório

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat). Ele cria o ambiente virtual (`.venv`),
instala as dependências de [`requirements.txt`](requirements.txt) e abre um **menu**:

```
[1] monitoramento_linux.py  - pseudo-arquivos e hardware (CPU/GPU)
[2] gpu_status.sh           - status das GPUs (Git Bash, se houver)
[0] Sair
```

Quem preferir o terminal:

```bat
cd aulas\aula06
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe scripts\monitoramento_linux.py
```

> No Windows, `monitoramento_linux.py` usa `psutil` para mostrar o equivalente de
> `/proc/cpuinfo` e `/proc/meminfo`. O `gpu_status.sh` roda no **Git Bash/WSL**.

---

## 🔑 Conceitos-chave

### Estrutura de diretórios relevante para GPUs

| Caminho | O que contém |
| :--- | :--- |
| `/dev/nvidia*` | Arquivos de dispositivo das GPUs NVIDIA (`nvidia0`, `nvidiactl`) |
| `/proc/driver/nvidia/` | Info do driver em tempo real (versão, GPUs, clients) |
| `/sys/class/drm/` | Interface sysfs para GPUs via DRM (vendor, classe) |
| `/usr/lib/...` | Bibliotecas do sistema (`libcuda.so`, `libnvidia*.so`) |
| `/etc/modprobe.d/` | Configuração de módulos do kernel (blacklist, opções) |
| `/var/log/` | Logs: `syslog`, `kern.log`, `nvidia-installer.log` |

> **Pseudo-arquivos:** `/proc` e `/sys` não ocupam disco — são uma janela viva para o kernel.
> `htop` e `nvtop` leem exatamente daí.

### Verificar drivers

```bash
lspci | grep -i 'vga|3d|display'   # a placa existe no barramento?
nvidia-smi -L                      # NVIDIA: GPUs e driver
rocminfo / rocm-smi                # AMD (ROCm)
```

### Automação: cron × systemd

| | **cron** | **systemd** |
| :--- | :--- | :--- |
| Tipo | Periódico (agenda) | Contínuo (serviço) |
| Reinicia sozinho | Não | **Sim** |
| Inicia no boot | Não | **Sim** |
| Exemplo | Relatório 08:00 | Monitor de GPU sempre ativo |

### Sessões persistentes

`screen`, `tmux` e `nohup` mantêm processos longos (treinos) vivos após você **desconectar o
SSH**.

---

## 🧪 Atividade guiada

No **Colab/Linux** (ou Cloud Shell):

```bash
# 1) Ver as GPUs e o driver
lspci | grep -i nvidia
nvidia-smi -L

# 2) Rodar o monitor
bash scripts/gpu_status.sh

# 3) Ler os pseudo-arquivos
cat /proc/cpuinfo | grep "model name" | head -1
cat /proc/meminfo | head -5
```

Passo a passo completo, script Bash e automação em [`atividade.md`](atividade.md).

---

## 💬 Discussão em grupo

Em grupos de 3–4, no cenário do servidor da startup:

1. O treino rodava há 12h quando o SSH caiu. Como evitar isso? Quais ferramentas usar?
2. Dois cientistas querem usar as mesmas 4 GPUs. Como gerenciar acesso e recursos?
3. O script mostra 85°C numa GPU. Próximos passos? Como automatizar o alerta por e-mail?
4. Por que `/proc` e `/sys` são chamados de "sistemas de arquivos virtuais"?

---

## 📌 Tarefa de casa (opcional)

Expanda o `gpu_status.sh` para incluir:

- envio de e-mail automático quando a temperatura &gt; 80°C (via `mail` ou webhook);
- log estruturado em CSV com timestamp, temperatura e utilização;
- relatório da utilização média das últimas 24h;
- agendamento via cron a cada 5 minutos.

---

## 🔗 Relação com o curso

- **Aula 5** entregou o acesso remoto (SSH/rede). Mas o job de treino longo precisa
  **sobreviver a desconexões** e auditar temperatura/recursos via terminal — é o que esta aula
  resolve com `tmux/screen`, `cron` e `systemd`.
- **Próxima (Aula 7):** *Introdução ao CUDA* — o ambiente está estável; agora vamos escrever
  **kernels** que rodam direto na VRAM.
