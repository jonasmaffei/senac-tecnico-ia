#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# ipv4_ipv6.py - IPv4 e IPv6 na pratica, via Python
# ----------------------------------------------------------------------------
# OBJETIVO: entender os dois protocolos de enderecamento e ver a maquina usando
# ambos ao mesmo tempo (o normal hoje em dia: "dual stack").
#
#   - IPv4: 32 bits, notacao 192.168.1.100, ~4,3 bilhoes de enderecos
#     (esgotados; NAT compensa).
#   - IPv6: 128 bits, notacao 2001:db8::1, praticamente infinito.
#
# O script NAO depende de internet: usa a resolucao de nomes local e o loopback.
#
# Uso:  python ipv4_ipv6.py
# Requer: apenas a biblioteca padrao
# ============================================================================

import socket
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def sockets_por_familia():
    """Mostra que cada protocolo tem sua propria 'familia' de socket."""
    s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # IPv4
    s6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)   # IPv6
    print("Familias de socket:")
    print(f"  IPv4 -> {s4.family.name}")
    print(f"  IPv6 -> {s6.family.name}")
    s4.close(); s6.close()


def testar_portas():
    """Verifica quais portas tipicas estao abertas no proprio host (loopback)."""
    # As portas que interessam ao trabalho com GPUs: SSH e Jupyter.
    portas = {22: "SSH", 8888: "Jupyter/Colab"}
    print("\nPortas tipicas no host local (127.0.0.1):")
    for porta, servico in portas.items():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            # connect_ex devolve 0 se a porta estiver aberta.
            aberta = s.connect_ex(("127.0.0.1", porta)) == 0
        estado = "ABERTA" if aberta else "fechada/indisponivel"
        print(f"  porta {porta:>4} ({servico:<14}) -> {estado}")


def resolver(nome="www.google.com", porta=80):
    """Resolve um nome para enderecos IPv4 e IPv6 (se a rede permitir).

    getaddrinfo devolve todas as combinacoes familia/protocolo/endereco.
    Sem internet, a funcao simplesmente nao encontra nada (nao quebra).
    """
    print(f"\nResolucao de {nome} (getaddrinfo):")
    try:
        resultados = socket.getaddrinfo(nome, porta)
    except socket.gaierror as erro:
        print(f"  Nao foi possivel resolver ({erro}).")
        print("  Sem internet? Sem problema: o resto do script ja usou o loopback.")
        return

    vistos = set()
    for familia, tipo, proto, canonico, endereco in resultados:
        ip = endereco[0]
        if ip in vistos:
            continue
        vistos.add(ip)
        print(f"  {familia.name:8s} -> {ip}")


def main():
    print("=" * 60)
    print(" IPv4 vs. IPv6 - conceitos e uso")
    print("=" * 60)

    sockets_por_familia()
    testar_portas()
    resolver()

    print()
    print("Em um datacenter de IA, os nos costumam ter IPv4 interno")
    print("(ex.: 10.0.0.5) e, cada vez mais, IPv6 (dual stack).")
    print("IPv6 dispensa NAT e simplifica a comunicacao entre muitos nos.")


if __name__ == "__main__":
    main()
