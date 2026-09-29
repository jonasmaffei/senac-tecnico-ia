"""4_monitor_processos_gpu.py - Monitor do estado da GPU, do lock e da fila.

Uso:
    python 4_monitor_processos_gpu.py            # uma foto (estado no instante)
    python 4_monitor_processos_gpu.py 15 1       # monitora por 15s, 1 leitura/s

Dica: para ver a fila em movimento, rode o teste (3_teste_fila.py) numa janela e
este monitor em outra. Ou use a opcao do menu que faz os dois juntos.
"""

import sys
import time

import monitor_fila


def imprimir_snapshot(snap):
    print("=== Processos em Execucao no Host ===")
    if snap["processos"]:
        for p in snap["processos"]:
            print(f"  PID={p['pid']} | User={p['username']}")
            print(f"      Cmd: {' '.join(p['cmdline'] or [])}")
    else:
        print("  Nenhum job de treinamento ativo no momento.")

    print("\n=== Estado do Lock de GPU ===")
    print("  GPU OCUPADA (um job esta usando a placa)" if snap["lock"]
          else "  GPU LIVRE")

    print("\n=== Fila Atual de Jobs ===")
    if snap["fila"]:
        for i, ticket in enumerate(snap["fila"], 1):
            print(f"  {i}. {ticket}")
    else:
        print("  Fila vazia.")


def main():
    segundos = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    intervalo = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0

    if segundos <= 0:
        # Modo "foto": imprime uma vez e sai.
        print("=== Monitor da GPU (leitura unica) ===\n")
        imprimir_snapshot(monitor_fila.coletar_snapshot())
        return

    # Modo "ao vivo": atualiza a tela a cada 'intervalo' segundos.
    print(f"=== Monitor da GPU ao vivo ({segundos}s, {intervalo}s por leitura) ===")
    print("Pressione Ctrl+C para parar antes do tempo.\n")
    fim = time.time() + segundos
    try:
        while time.time() < fim:
            snap = monitor_fila.coletar_snapshot()
            # '\r' volta o cursor para o inicio da linha (atualiza sem rolar a tela)
            print("\r" + monitor_fila.resumo_linha(snap), end="", flush=True)
            time.sleep(intervalo)
        print("\n\nMonitoramento encerrado.")
    except KeyboardInterrupt:
        print("\n\nMonitoramento interrompido pelo usuario.")


if __name__ == "__main__":
    main()
