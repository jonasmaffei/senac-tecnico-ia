#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# demo_tcp_udp.py - TCP vs. UDP: confiabilidade x velocidade
# ----------------------------------------------------------------------------
# OBJETIVO: mostrar, na pratica, a diferenca entre os dois protocolos de
# transporte mais usados no treinamento de IA:
#
#   - TCP (Transmission Control Protocol): confiavel. Garante que cada byte
#     chegue, na ordem certa, com confirmacao. Mais lento pelo overhead.
#     Ideal para: SSH, HTTP, transferir datasets e modelos.
#
#   - UDP (User Datagram Protocol): rapido. Dispara sem confirmar (fire-and-
#     forget). Pode perder pacotes. Ideal para: telemetria de GPU, streaming.
#
# Roda em qualquer ambiente (usa o loopback 127.0.0.1, sem rede externa).
# Uso:  python demo_tcp_udp.py
# Requer: apenas a biblioteca padrao
# ============================================================================

import socket
import sys
import threading
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

PORTA_TCP = 65432
PORTA_UDP = 65433
MENSAGENS = 200
HOST = "127.0.0.1"   # loopback: conversa da maquina com ela mesma


# ---------------------------------------------------------------------------
# TCP - servidor e cliente (conexao com confirmacao)
# ---------------------------------------------------------------------------
def servidor_tcp(resultado):
    """Escuta conexoes TCP, recebe tudo e conta os BYTES recebidos.

    TCP e um fluxo (stream) de bytes: o sistema pode juntar varias mensagens
    num unico recv. Por isso contamos bytes, nao 'pacotes'.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reusa a porta
        s.bind((HOST, PORTA_TCP))
        s.listen()                       # comeca a aceitar conexoes
        conn, _ = s.accept()             # bloqueia ate o cliente conectar
        with conn:
            total_bytes = 0
            while True:
                dados = conn.recv(1024)  # le em blocos de 1024 bytes
                if not dados:            # 0 bytes = cliente fechou a conexao
                    break
                total_bytes += len(dados)
            # devolve ao cliente o total (prova de que os dados chegaram)
            conn.sendall(str(total_bytes).encode())
    resultado.append(total_bytes)


def cliente_tcp():
    """Conecta, envia as mensagens e espera a confirmacao do servidor."""
    time.sleep(0.2)                      # da tempo do servidor subir
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORTA_TCP))     # handshake de 3 vias (SYN/SYN-ACK/ACK)
        inicio = time.perf_counter()
        enviados = 0
        for i in range(MENSAGENS):
            dado = f"msg-{i}".encode()
            s.sendall(dado)              # sendall garante que tudo saiu
            enviados += len(dado)
        s.shutdown(socket.SHUT_WR)       # avisa que terminou de enviar
        recebidos = int(s.recv(1024).decode())
        tempo = time.perf_counter() - inicio
    print(f"  TCP: {recebidos}/{enviados} bytes entregues em {tempo*1000:.1f}ms "
          f"(garantia de entrega)")
    assert recebidos == enviados, "TCP deveria entregar TODOS os bytes!"


# ---------------------------------------------------------------------------
# UDP - servidor e cliente (disparo sem confirmacao)
# ---------------------------------------------------------------------------
def servidor_udp(resultado):
    """Escuta datagramas UDP por um tempo e conta quantos chegaram."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORTA_UDP))
        s.settimeout(1.0)                # para de esperar apos 1s de silencio
        recebidas = 0
        try:
            while True:
                s.recvfrom(1024)         # cada recvfrom = 1 datagrama
                recebidas += 1
        except socket.timeout:
            pass                          # acabou o fluxo
    resultado.append(recebidas)


def cliente_udp():
    """Dispara os datagramas sem esperar confirmacao (fire-and-forget)."""
    time.sleep(0.2)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        inicio = time.perf_counter()
        for i in range(MENSAGENS):
            s.sendto(f"msg-{i}".encode(), (HOST, PORTA_UDP))
        tempo = time.perf_counter() - inicio
    print(f"  UDP: {MENSAGENS} disparadas em {tempo*1000:.1f}ms (sem confirmar)")


def main():
    print("=" * 60)
    print(" Comparacao TCP vs. UDP (no loopback 127.0.0.1)")
    print("=" * 60)

    # -- TCP ----------------------------------------------------------------
    print("\n[TCP - Transmission Control Protocol]")
    res_tcp = []
    t_srv = threading.Thread(target=servidor_tcp, args=(res_tcp,))
    t_cli = threading.Thread(target=cliente_tcp)
    t_srv.start(); t_cli.start()
    t_srv.join(); t_cli.join()

    # -- UDP ----------------------------------------------------------------
    print("\n[UDP - User Datagram Protocol]")
    res_udp = []
    t_srv = threading.Thread(target=servidor_udp, args=(res_udp,))
    t_cli = threading.Thread(target=cliente_udp)
    t_srv.start(); t_cli.start()
    t_srv.join(); t_cli.join()
    print(f"  UDP: {res_udp[0]}/{MENSAGENS} recebidas pelo servidor")

    print()
    print("Leitura dos resultados:")
    print("  - TCP confirma cada entrega (e reenvia o que faltar).")
    print("  - UDP so dispara; aqui no loopback quase tudo chega, mas numa rede")
    print("    real pode haver perda - sem retransmissao.")
    print()
    print("  Transferir dataset/modelo (scp/rsync) -> TCP")
    print("  Telemetria de GPU em tempo real        -> UDP")


if __name__ == "__main__":
    main()
