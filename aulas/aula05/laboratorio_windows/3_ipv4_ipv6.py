#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# ipv4_ipv6.py — IPv4 e IPv6 na prática, via Python
# ----------------------------------------------------------------------------
# OBJETIVO: entender os dois protocolos de endereçamento e ver a máquina usando
# ambos ao mesmo tempo (o normal hoje em dia: "dual stack").
#
#   - IPv4: 32 bits, notação 192.168.1.100, ~4,3 bilhões de endereços
#     (esgotados; NAT compensa).
#   - IPv6: 128 bits, notação 2001:db8::1, praticamente infinito.
#
# O script NÃO depende de internet: usa a resolução de nomes local e o loopback.
#
# Uso:  python ipv4_ipv6.py
# Requer: apenas a biblioteca padrão
# ============================================================================

import socket
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def sockets_por_familia():
    """Mostra que cada protocolo tem sua própria 'família' de socket."""
    s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # IPv4
    s6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)   # IPv6
    print("Famílias de socket:")
    print(f"  IPv4 -> {s4.family.name}")
    print(f"  IPv6 -> {s6.family.name}")
    s4.close(); s6.close()


def testar_portas():
    """Verifica quais portas típicas estão abertas no próprio host (loopback)."""
    # As portas que interessam ao trabalho com GPUs: SSH e Jupyter.
    portas = {22: "SSH", 8888: "Jupyter/Colab"}
    print("\nPortas típicas no host local (127.0.0.1):")
    for porta, servico in portas.items():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            # connect_ex devolve 0 se a porta estiver aberta.
            aberta = s.connect_ex(("127.0.0.1", porta)) == 0
        estado = "ABERTA" if aberta else "fechada/indisponível"
        print(f"  porta {porta:>4} ({servico:<14}) -> {estado}")


def resolver(nome="www.google.com", porta=80):
    """Resolve um nome para endereços IPv4 e IPv6 (se a rede permitir).

    getaddrinfo devolve todas as combinações família/protocolo/endereço.
    Sem internet, a função simplesmente não encontra nada (não quebra).
    """
    print(f"\nResolução de {nome} (getaddrinfo):")
    try:
        resultados = socket.getaddrinfo(nome, porta)
    except socket.gaierror as erro:
        print(f"  Não foi possível resolver ({erro}).")
        print("  Sem internet? Sem problema: o resto do script já usou o loopback.")
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
    print(" IPv4 vs. IPv6 — conceitos e uso")
    print("=" * 60)

    sockets_por_familia()
    testar_portas()
    resolver()

    print()
    print("Em um datacenter de IA, os nós costumam ter IPv4 interno")
    print("(ex.: 10.0.0.5) e, cada vez mais, IPv6 (dual stack).")
    print("IPv6 dispensa NAT e simplifica a comunicação entre muitos nós.")


if __name__ == "__main__":
    main()
