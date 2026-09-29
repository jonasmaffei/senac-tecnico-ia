# -*- coding: utf-8 -*-
# ============================================================================
# 1_benchmark_treino.py - FP32 vs. FP16 (mixed precision) na GPU ou CPU
# ----------------------------------------------------------------------------
# OBJETIVO: medir o throughput (imagens/segundo) de um treino sintetico nos dois
# modos e calcular o ganho do mixed precision (FP16).
#
# COMO RODAR:
#   duplo clique em iniciar.bat   (opcao [1])
# ou:
#   python 1_benchmark_treino.py
#
# OBS.: sem GPU, o script mostra os numeros de REFERENCIA (NVIDIA T4) para que a
# atividade continue valida no laboratorio Windows/AMD.
# ============================================================================

import lib_treino


def main():
    lib_treino.cabecalho_ascii()

    # Passo 1: descobrir o dispositivo disponivel.
    info = lib_treino.diagnostico()
    lib_treino.imprimir(info)

    if info["backend"] not in ("CUDA", "ROCm/HIP"):
        # Passo 2 (sem GPU): apenas mostrar a referencia.
        print()
        print("Sem GPU CUDA/ROCm neste ambiente.")
        print("Numeros de REFERENCIA (Tesla T4) - o mesmo codigo roda numa GPU real:")
        ref = lib_treino.referencia_t4()
        print(f"  Modo FP32 (padrao) : {ref['fp32']:8.1f} imgs/s")
        print(f"  Modo FP16 (AMP)    : {ref['fp16']:8.1f} imgs/s")
        print(f"  Ganho (speedup)    : {ref['fp16'] / ref['fp32']:.2f}x")
        return

    # Passo 3 (com GPU): treinar de verdade nos dois modos.
    import torch

    print()
    print("Treinando (aguarde)...")
    v32 = lib_treino.treinar(torch.device("cuda"), usar_fp16=False)
    v16 = lib_treino.treinar(torch.device("cuda"), usar_fp16=True)

    print()
    print("=" * 64)
    print("  RESULTADO DO BENCHMARK")
    print("=" * 64)
    print(f"  Modo FP32 (padrao) : {v32:8.1f} imgs/s")
    print(f"  Modo FP16 (AMP)    : {v16:8.1f} imgs/s")
    print(f"  Ganho (speedup)    : {v16 / v32:.2f}x")
    print("=" * 64)
    print("O mixed precision usa FP16 onde da ganho e mantem FP32 onde a")
    print("precisao e critica - por isso o treino acelera sem perder qualidade.")


if __name__ == "__main__":
    main()
