# Atividade Guiada: Aula 5 — Protocolos de Redes e Interação com GPUs

## Parte 1 — Atividade guiada: simular e capturar tráfego

O objetivo é **ver** a diferença entre TCP e UDP na prática, com `netcat` e `Wireshark`.
Rode no **Colab/Linux** ou no **Google Cloud Shell**.

### Passo 1 — netcat: comunicação TCP

```bash
# Terminal 1 (servidor)
nc -lvp 9999

# Terminal 2 (cliente) — digite mensagens e veja-as aparecer no servidor
nc 127.0.0.1 9999
```

### Passo 2 — netcat: telemetria UDP

```bash
# Terminal 1 (servidor UDP)
nc -u -lvp 9999

# Terminal 2 (cliente UDP) — dispara sem confirmar
echo "GPU_TEMP=72C GPU_MEM=8GB/16GB" | nc -u 127.0.0.1 9999
```

### Passo 3 — Wireshark: ver o handshake

```bash
sudo apt install wireshark -y     # depois: sudo wireshark
```

1. Inicie a captura na interface **`lo`** (loopback).
2. Execute a comunicação TCP do Passo 1.
3. Filtre por **`tcp.port == 9999`**.
4. Identifique os pacotes **SYN**, **SYN-ACK** e **ACK** (o *3-way handshake*).
5. Repita com **UDP** e compare o **número de pacotes**.

### Passo 4 — Scripts em Python

```bash
python scripts/demo_tcp_udp.py     # TCP vs. UDP no loopback
python scripts/telemetria_tcp.py   # servidor + nó de GPU (métricas JSON)
python scripts/ipv4_ipv6.py        # famílias de socket e resolução
```

### Exercício de fixação

1. Quantos pacotes foram necessários para **abrir** uma conexão TCP? E no UDP?
2. No UDP, o servidor confirmou a recepção? O que acontece se um pacote se perder?
3. Na telemetria, por que o JSON chegou completo (sem cortes) via TCP?
4. Qual protocolo você usaria para **transferir o dataset de 200 GB**? Por quê?

---

## Parte 2 — Atividade guiada: SSH e transferência de dados

### Passo 1 — Conexão e chaves

```bash
ssh usuario@192.168.1.50                       # conexão básica
ssh-keygen -t ed25519 -C "eu@empresa.com"      # cria par de chaves
ssh-copy-id usuario@192.168.1.50               # instala a chave pública

ssh usuario@192.168.1.50 "nvidia-smi"          # verifica a GPU remota
```

### Passo 2 — Transferir arquivos

```bash
# scp: simples, sem retomada
scp dataset.zip usuario@192.168.1.50:/home/usuario/dados/
scp -r ./imagens/ usuario@192.168.1.50:/home/usuario/treino/

# rsync: incremental e retomável (ideal para datasets grandes)
rsync -avzP ./dataset/ usuario@192.168.1.50:/data/
```

### Passo 3 — Túnel SSH para Jupyter

```bash
ssh -L 8888:localhost:8888 usuario@192.168.1.50
# Acesse http://localhost:8888 no navegador local
```

### Exercício de fixação

1. Qual a diferença de **retomada** entre `scp` e `rsync`?
2. Por que `rsync -z` **comprime** os dados durante a transferência?
3. Para que serve o túnel SSH (`-L`)?

> Referência completa de comandos de rede em `scripts/comandos_rede.sh`.

---

## Parte 3 — Discussão em grupo (3 a 4 pessoas)

Analisem o cenário do cluster de GPUs:

1. O cluster tem 4 nós com GPUs conectados por **Ethernet 1GbE** e o treinamento distribuído
   está lento. Como você diagnosticaria se o gargalo é a rede e qual *upgrade* recomendaria?
2. Por que frameworks como **PyTorch DDP** usam **TCP** e não **UDP** para sincronizar
   gradientes entre GPUs?
3. Você precisa transferir um dataset de **500 GB**. Compare: `scp` direto vs. `rsync`
   comprimido vs. compactar com `tar` primeiro. Qual seria mais rápido?
4. Na nuvem, qual a diferença entre usar **IPv4 privado** (10.x.x.x) e **IPv6** para a
   comunicação interna entre nós?

---

## Parte 4 — Pesquisa (tarefa de casa, opcional)

Configure uma mini rede local virtual usando duas VMs (VirtualBox) ou duas instâncias na
nuvem e pratique:

- Configurar **IPs estáticos** em ambas as máquinas (via Netplan no Ubuntu);
- testar conectividade com `ping` e `traceroute`;
- transferir um arquivo de modelo (`.pt`) via `scp` e `rsync`;
- criar um **servidor TCP simples em Python** que recebe métricas de GPU.
