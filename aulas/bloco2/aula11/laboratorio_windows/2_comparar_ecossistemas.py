# -*- coding: utf-8 -*-
# ============================================================================
# 2_comparar_ecossistemas.py - NVIDIA (CUDA) x AMD (ROCm) + custo (TCO)
# ----------------------------------------------------------------------------
# OBJETIVO: apoiar a decisao de compra comparando os dois ecossistemas e
# simulando o custo anual de alugar GPUs na nuvem.
#
# COMO RODAR:
#   duplo clique em iniciar.bat   (opcao [2])
# ou:
#   python 2_comparar_ecossistemas.py
# ============================================================================

import lib_treino


def tabela_criterios():
    """Diferencas que pesam na escolha entre NVIDIA e AMD."""
    print("=" * 70)
    print("  COMPARATIVO DE ECOSSISTEMAS: NVIDIA x AMD")
    print("=" * 70)
    criterios = [
        ("Ecossistema",     "maduro (CUDA)",        "em crescimento (ROCm)"),
        ("Facilidade",      "exemplos abundantes",  "setup mais trabalhoso"),
        ("Custo/hora",      "mais caro",            "tende a ser menor"),
        ("Portabilidade",   "preso ao CUDA",        "PyTorch via HIP"),
        ("Mao de obra",     "facil contratar",      "equipe se adapta"),
    ]
    print(f"{'Criterio':<16} {'NVIDIA':<22} {'AMD'}")
    print("-" * 70)
    for nome, nv, amd in criterios:
        print(f"{nome:<16} {nv:<22} {amd}")
    print("=" * 70)


def simular_tco(preco_nvidia_hora, preco_amd_hora, horas_dia=8, dias=365):
    """Estima o custo anual de alugar cada tipo de GPU na nuvem."""
    custo_nvidia = preco_nvidia_hora * horas_dia * dias
    custo_amd = preco_amd_hora * horas_dia * dias
    print()
    print("=" * 70)
    print("  SIMULADOR DE CUSTO (TCO) - 1 ANO")
    print("=" * 70)
    print(f"  Preco hora NVIDIA : US$ {preco_nvidia_hora:.2f}")
    print(f"  Preco hora AMD    : US$ {preco_amd_hora:.2f}")
    print(f"  Uso               : {horas_dia} h/dia x {dias} dias")
    print("-" * 70)
    print(f"  Custo anual NVIDIA (CUDA): US$ {custo_nvidia:,.0f}")
    print(f"  Custo anual AMD    (ROCm): US$ {custo_amd:,.0f}")
    print(f"  Economia bruta da AMD    : US$ {custo_nvidia - custo_amd:,.0f}")
    print("=" * 70)
    print("Pergunta-chave: essa economia paga o tempo de adaptacao da equipe?")


def main():
    lib_treino.cabecalho_ascii()

    # Passo 1: contexto tecnico.
    tabela_criterios()

    # Passo 2: contexto financeiro (edite os precos com a SUA pesquisa).
    simular_tco(preco_nvidia_hora=1.00, preco_amd_hora=0.80)

    # Passo 3: lembrete de onde o benchmark entra nessa decisao.
    print()
    print("Lembre-se: a GPU mais RAPIDA nao e sempre a melhor escolha.")
    print("O benchmark da opcao [1] mostra o throughput real de cada modo.")


if __name__ == "__main__":
    main()
