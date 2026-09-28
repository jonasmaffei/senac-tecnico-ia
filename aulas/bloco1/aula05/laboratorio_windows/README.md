# Laboratório Windows — Protocolos de Redes e Interação com GPUs (rede real)

Experimentos com a **rede real** da máquina do laboratório, aplicando os conceitos da Aula 05:
TCP vs. UDP, telemetria de GPU e IPv4/IPv6. Tudo roda **offline** no loopback (127.0.0.1).

---

## 🚀 Como rodar

Dê **duplo clique** em [`iniciar.bat`](iniciar.bat):

```
[1] 1_demo_tcp_udp.py    - TCP vs. UDP (confiabilidade x velocidade)
[2] 2_telemetria_tcp.py  - servidor TCP que recebe metricas de GPU
[3] 3_ipv4_ipv6.py       - IPv4 vs. IPv6 na pratica
[4] comandos_rede.sh     - referencia de comandos (Git Bash)
[0] Sair
```

Ou pelo terminal:

```bat
python 1_demo_tcp_udp.py
python 2_telemetria_tcp.py
python 3_ipv4_ipv6.py
```

---

## 🗂️ Arquivos

| Arquivo | O que faz |
| :--- | :--- |
| `1_demo_tcp_udp.py` | Mede TCP (confiável, conta bytes) vs. UDP (dispara sem confirmar). |
| `2_telemetria_tcp.py` | Servidor TCP que recebe métricas de GPU em JSON (com modo demo). |
| `3_ipv4_ipv6.py` | Famílias de socket (`AF_INET`/`AF_INET6`) e resolução de nomes. |
| `comandos_rede.sh` | **Referência** comentada: `ip`, `ss`, `netcat`, `ssh`, `rsync`, netplan, ufw. |
| `iniciar.bat` | Menu (duplo clique). |

---

## 🔎 O que observar

- **TCP:** todos os bytes chegam (o servidor confirma o total recebido).
- **UDP:** dispara sem confirmar — no loopback quase tudo chega, mas numa rede real pode haver perda.
- **IPv4/IPv6:** a máquina é **dual stack**; o `getaddrinfo` revela os endereços de cada família.

> Para a atividade com `netcat` e `Wireshark`, use o **Colab/Linux** (o `.sh` é uma referência).

---

## 🔗 Relação com a aula

- Demonstra na prática **TCP (integridade) × UDP (velocidade)** e a **telemetria de GPU**.
- O `comandos_rede.sh` reúne SSH/rsync — a base para operar GPUs remotas.
- Segue o padrão de laboratório do curso (`.context.md`, §6.9 e §6.16).
