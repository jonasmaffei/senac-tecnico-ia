#!/usr/bin/env bash
# ============================================================================
# comandos_rede.sh — Comandos de rede no Linux (referência comentada)
# ----------------------------------------------------------------------------
# OBJETIVO: reunir, num só lugar, os comandos que você vai usar para
# configurar e diagnosticar a rede de um servidor de GPUs.
#
# Este arquivo é uma REFERÊNCIA: NÃO é para "rodar tudo de uma vez" — são
# comandos de consulta/configuração do sistema. Rode-os um a um no terminal
# (Colab/Linux/Cloud Shell).
#
# Uso:  bash comandos_rede.sh   (ou copie os comandos que precisar)
# ============================================================================

# ── 1. Ver interfaces e endereços ───────────────────────────────────────────
# ip addr show      # todos os endereços (IPv4 e IPv6) de cada interface
# ip -4 addr show   # somente IPv4
# ip -6 addr show   # somente IPv6
# ip link show      # estado físico das interfaces (UP/DOWN)

# ── 2. Roteamento ───────────────────────────────────────────────────────────
# ip route show          # tabela de rotas
# ip route get 8.8.8.8   # qual rota a máquina usa para chegar nesse IP

# ── 3. Configurar IP estático temporário (some ao reiniciar) ─────────────────
# sudo ip addr add 192.168.1.100/24 dev eth0
# sudo ip route add default via 192.168.1.1

# ── 4. Sockets e portas abertas ─────────────────────────────────────────────
# ss -tulnp    # TCP + UDP (-t -u), escutando (-l), números (-n), processo (-p)
# ss -s        # resumo das estatísticas de sockets
# netstat -tulnp   # alternativa legada (pacote net-tools)

# ── 5. Testar conectividade ─────────────────────────────────────────────────
# ping -c 4 8.8.8.8              # 4 pings e para
# ping6 ::1                     # loopback IPv6
# traceroute 8.8.8.8            # caminho (saltos) até o destino
# mtr 8.8.8.8                   # ping + traceroute combinados, ao vivo

# ── 6. IPv4 vs. IPv6 de um serviço ──────────────────────────────────────────
# curl -4 https://ipv4.google.com   # força IPv4
# curl -6 https://ipv6.google.com   # força IPv6

# ── 7. Netcat: simular TCP e UDP ────────────────────────────────────────────
# Terminal 1 (servidor TCP):        nc -lvp 9999
# Terminal 2 (cliente TCP):         nc 127.0.0.1 9999
# Servidor UDP:                     nc -u -lvp 9999
# Cliente UDP (telemetria):         echo "GPU_TEMP=72C" | nc -u 127.0.0.1 9999
# Scan de porta:                    nc -zv <ip> 22

# ── 8. SSH e transferência para o servidor de GPUs ──────────────────────────
# ssh usuario@192.168.1.50                       # conexão básica
# ssh-keygen -t ed25519 -C "eu@empresa.com"      # cria par de chaves
# ssh-copy-id usuario@192.168.1.50               # instala a chave pública
# ssh usuario@192.168.1.50 "nvidia-smi"          # roda comando remoto
# scp dataset.zip usuario@192.168.1.50:/dados/   # copia arquivo (simples)
# rsync -avzP ./dataset/ usuario@192.168.1.50:/data/   # RETOMÁVEL (grande)
# ssh -L 8888:localhost:8888 usuario@192.168.1.50       # túnel p/ Jupyter

# ── 9. Configuração persistente com Netplan (Ubuntu 18.04+) ─────────────────
# Arquivo: /etc/netplan/01-network-manager-all.yaml
#
# network:
#   version: 2
#   renderer: networkd
#   ethernets:
#     eth0:
#       dhcp4: no
#       addresses: [192.168.1.100/24]
#       gateway4: 192.168.1.1
#       nameservers:
#         addresses: [8.8.8.8, 8.8.4.4]
#
# Aplicar:  sudo netplan apply

# ── 10. Firewall (ufw) num servidor de GPUs ─────────────────────────────────
# Mantenha só o necessário: SSH (22) e as portas do treino distribuído.
# sudo ufw allow 22/tcp
# sudo ufw allow 29500/tcp     # ex.: PyTorch DDP
# sudo ufw enable

echo "Consulte os comentários deste arquivo e rode os comandos um a um."
