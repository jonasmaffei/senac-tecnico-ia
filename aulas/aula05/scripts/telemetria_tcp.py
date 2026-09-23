#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# telemetria_tcp.py — Servidor TCP que recebe métricas de GPU (JSON)
# ----------------------------------------------------------------------------
# OBJETIVO: simular o fluxo real de um cluster de GPUs: cada nó envia suas
# métricas (temperatura, VRAM, utilização) para um servidor central via TCP.
#
# É o mesmo padrão usado por frameworks de treinamento distribuído: o TCP
# garante que os dados cheguem completos e na ordem — obrigatório quando a
# ordem importa (ex.: sincronização de gradientes).
#
# Como rodar (loopback; em máquinas diferentes troque 127.0.0.1 pelo IP do
# servidor):
#   Terminal 1:  python telemetria_tcp.py servidor
#   Terminal 2:  python telemetria_tcp.py cliente
#
# Uso:  python telemetria_tcp.py [servidor|cliente]
# Requer: apenas a biblioteca padrão
# ============================================================================

import json
import socket
import sys
import threading
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

HOST = "127.0.0.1"
PORTA = 9999


def ler_gpu():
    """Tenta ler a GPU real (nvidia-smi). Sem GPU, devolve um exemplo simulado."""
    try:
        import shutil
        import subprocess
        if shutil.which("nvidia-smi"):
            saida = subprocess.run(
                ["nvidia-smi",
                 "--query-gpu=name,temperature.gpu,memory.used,memory.total,utilization.gpu",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True,
            ).stdout.strip().splitlines()[0]
            nome, temp, usada, total, util = [p.strip() for p in saida.split(",")]
            return {
                "nome": nome,
                "temp_c": int(temp),
                "vram_usada_gb": round(int(usada) / 1024, 1),
                "vram_total_gb": round(int(total) / 1024, 1),
                "utilizacao_pct": int(util),
            }
    except Exception:
        pass
    # Exemplo no mesmo formato (didático, quando não há GPU NVIDIA)
    return {
        "nome": "NVIDIA Tesla T4 (simulado)",
        "temp_c": 72,
        "vram_usada_gb": 11.3,
        "vram_total_gb": 16.0,
        "utilizacao_pct": 87,
    }


def servidor():
    """Escuta na porta TCP e imprime as métricas recebidas de cada nó."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORTA))
        srv.listen(5)                          # aceita até 5 conexões na fila
        print(f"Servidor de telemetria aguardando em {HOST}:{PORTA}...")
        print("(rode em outro terminal:  python telemetria_tcp.py cliente)")

        while True:
            conn, addr = srv.accept()          # bloqueia até um nó conectar
            with conn:
                dados = conn.recv(4096).decode()
                if not dados:
                    continue
                metricas = json.loads(dados)    # TCP garantiu o JSON completo
                print(f"\nConexão de {addr[0]}:{addr[1]}")
                print(f"  GPU  : {metricas['nome']}")
                print(f"  Temp : {metricas['temp_c']} C")
                print(f"  VRAM : {metricas['vram_usada_gb']:.1f}/{metricas['vram_total_gb']:.1f} GB")
                print(f"  Uso  : {metricas['utilizacao_pct']}%")


def cliente(repeticoes=3):
    """Envia as métricas da GPU para o servidor, algumas vezes."""
    for _ in range(repeticoes):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
                cli.connect((HOST, PORTA))
                cli.send(json.dumps(ler_gpu()).encode())
            print("Métricas enviadas.")
        except ConnectionRefusedError:
            print("Servidor indisponível. Rode primeiro:  python telemetria_tcp.py servidor")
            return
        time.sleep(0.5)


def demo_interna():
    """Quando ninguém passa argumento: sobe o servidor numa thread e envia 1x.

    Facilita testar tudo num único comando (útil no laboratório/Colab).
    """
    print("Modo demonstração: servidor + cliente no mesmo processo.\n")
    t = threading.Thread(target=servidor, daemon=True)  # servidor em segundo plano
    t.start()
    time.sleep(0.5)
    cliente(repeticoes=1)
    time.sleep(0.5)
    print("\n[OK] Demonstração concluída.")


if __name__ == "__main__":
    modo = sys.argv[1].lower() if len(sys.argv) > 1 else "demo"
    if modo == "servidor":
        servidor()
    elif modo == "cliente":
        cliente()
    else:
        demo_interna()
