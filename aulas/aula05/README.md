# 🧠 Aula 05 — Protocolos de Redes e Interação com GPUs

**Objetivo:** aplicar conceitos de redes (IPv4/IPv6, TCP/UDP) para configurar e operar
ambientes distribuídos com GPUs, garantindo comunicação eficiente em projetos de IA.

---

## 🎯 Situação de aprendizagem

A startup vai escalar o treinamento do modelo de IA para um **cluster remoto com múltiplas
GPUs**. Sua equipe precisa configurar a **rede local virtual**, entender como os dados
trafegam entre os nós (**TCP/UDP**, **IPv4/IPv6**), conectar-se remotamente via **SSH** ao
servidor de GPUs e transferir o dataset de **200 GB** de forma eficiente usando **rsync**.
Sem esse conhecimento, o treinamento distribuído simplesmente não funciona.

---

## 🗂️ Conteúdo

| Arquivo | O que é |
| :--- | :--- |
| [`apresentacao_aula05.html`](apresentacao_aula05.html) | Slides teóricos (abra no navegador, navegue com ← →) |
| [`aula05_redes.ipynb`](aula05_redes.ipynb) | Notebook do **Google Colab** (TCP/UDP, telemetria, IPv4/IPv6) |
| [`atividade.md`](atividade.md) | Atividade guiada (netcat/Wireshark, SSH/scp/rsync) + discussão |
| `scripts/` | Scripts comentados + referência de comandos de rede |

### Scripts

| Script | O que faz |
| :--- | :--- |
| [`demo_tcp_udp.py`](scripts/demo_tcp_udp.py) | TCP vs. UDP no loopback (confiabilidade × velocidade) |
| [`telemetria_tcp.py`](scripts/telemetria_tcp.py) | Servidor TCP que recebe métricas de GPU (JSON) |
| [`ipv4_ipv6.py`](scripts/ipv4_ipv6.py) | IPv4 vs. IPv6: famílias de socket e resolução de nomes |
| [`comandos_rede.sh`](scripts/comandos_rede.sh) | **Referência** comentada: `ip`, `ss`, `netcat`, `ssh`, `rsync`, netplan, ufw |

---

## 🚀 Como rodar

### No Google Colab (recomendado)

1. Abra `aula05_redes.ipynb` pelo **GitHub** no Colab
   (`https://github.com/jonasmaffei/senac-tecnico-ia`).
2. Rode as células na ordem. Tudo funciona **offline** no loopback.

> 💡 Para a atividade com `netcat` e `Wireshark`, use o **Linux/Colab** ou o
> **Google Cloud Shell** (o Wireshark não roda no Windows com capture de loopback fácil, mas
> dá para instalá-lo para estudo).

### No Windows do laboratório

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat). Ele cria o ambiente virtual (`.venv`),
instala as dependências de [`requirements.txt`](requirements.txt) e abre um **menu**:

```
[1] demo_tcp_udp.py     - TCP vs. UDP (confiabilidade x velocidade)
[2] telemetria_tcp.py   - servidor TCP que recebe metricas de GPU
[3] ipv4_ipv6.py        - IPv4 vs. IPv6 na pratica
[0] Sair
```

Quem preferir o terminal:

```bat
cd aulas\aula05
python -m venv .venv
.venv\Scripts\python.exe scripts\demo_tcp_udp.py
```

> Os scripts usam apenas a **biblioteca padrão** (`socket`, `threading`, `json`) — nada extra
> para instalar.

---

## 🔑 Conceitos-chave

### IPv4 vs. IPv6

| | IPv4 | IPv6 |
| :--- | :--- | :--- |
| Tamanho | 32 bits | 128 bits |
| Notação | `192.168.1.100` | `2001:db8::1` |
| Endereços | ~4,3 bilhões (esgotado) | ~340 undecilhões |
| Configuração | DHCP | Autoconfiguração |
| Onde | LANs (via NAT) | Data centers de IA |

### TCP vs. UDP

| | TCP | UDP |
| :--- | :--- | :--- |
| Entrega | **Garantida e ordenada** | Sem garantia |
| Conexão | Handshake de 3 vias | Sem conexão |
| Velocidade | Mais lento (overhead) | Mais rápido |
| Ideal para | SSH, datasets, modelos, APIs | Telemetria, streaming |

| Caso de uso em IA | Protocolo | Motivo |
| :--- | :--- | :--- |
| Transferir dataset (scp/rsync) | **TCP** | Dados não podem ser corrompidos |
| Monitorar GPU em tempo real | **UDP** | Velocidade > confiabilidade |
| Treinamento distribuído (NCCL) | **TCP / RDMA** | Ordem dos gradientes importa |
| Servir predições (REST API) | **TCP (HTTP)** | Resposta garantida ao cliente |
| Vídeo da câmera industrial | **UDP** | Latência baixa, perdas aceitáveis |

### Ferramentas essenciais

- **netcat (`nc`):** simula servidor/cliente TCP e UDP, transfere arquivos, faz *scan* de portas.
- **Wireshark:** captura e analisa pacotes (reveja o handshake SYN/SYN-ACK/ACK).
- **SSH:** acesso remoto, chaves (`ssh-keygen`), túnel para Jupyter (`-L`).
- **scp vs. rsync:** `scp` é simples; `rsync -avzP` é incremental e **retomável** — use para
  datasets grandes.

---

## 🧪 Atividade guiada (netcat e Wireshark)

No **Colab/Linux** (ou Cloud Shell):

```bash
# Terminal 1 (servidor TCP)
nc -lvp 9999
# Terminal 2 (cliente)
nc 127.0.0.1 9999

# Captura no Wireshark na interface lo, filtro: tcp.port == 9999
# Identifique SYN, SYN-ACK e ACK. Depois repita com UDP e compare.
```

Passo a passo completo, SSH/scp/rsync e exercícios em [`atividade.md`](atividade.md).

---

## 💬 Discussão em grupo

Em grupos de 3–4, analisem o cenário do cluster:

1. 4 nós com GPUs em Ethernet 1GbE e treino lento. É a rede? Qual *upgrade* recomendar?
2. Por que o PyTorch DDP usa TCP (e não UDP) para sincronizar gradientes?
3. Dataset de 500 GB: scp direto, rsync comprimido ou `tar` primeiro? Qual é mais rápido?
4. Na nuvem, IPv4 privado (10.x.x.x) vs. IPv6 para a comunicação interna entre nós?

---

## 📌 Tarefa de casa (opcional)

Configure uma mini rede local virtual (2 VMs no VirtualBox ou 2 instâncias na nuvem) e pratique:

- Configurar **IPs estáticos** em ambas as máquinas;
- testar conectividade com `ping` e `traceroute`;
- transferir um arquivo de modelo (`.pt`) via `scp` e `rsync`;
- criar um servidor **TCP simples em Python** que recebe métricas de GPU.

---

## 🔗 Relação com o curso

- **Aula 4** preparou os dados no host (processos/threads). Mas o *data loader* local não
  adianta se o cluster for distribuído: os dados precisam atravessar a **malha de rede** com
  resiliência a quedas (`rsync --partial`).
- **Próxima (Aula 6):** *Sistemas Operacionais Linux e GPU* — o nó remoto precisa sustentar o
  hardware e os drivers por horas: `/proc`, `/sys`, `tmux` e `cron`.
