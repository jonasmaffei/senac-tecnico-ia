#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# 1_hardware.py — Conhecer a máquina real (CPU, RAM e GPU)
# ----------------------------------------------------------------------------
# OBJETIVO: começar qualquer projeto de IA entendendo o hardware disponível —
# o mesmo primeiro passo que a aula propõe para o servidor da startup.
#
# Uso (no laboratório Windows):
#     python 1_hardware.py
# ============================================================================

import lib_hw

if __name__ == "__main__":
    print("Passo 1 do laboratório: descobrir com o que contamos.\n")
    lib_hw.imprimir_resumo()
    print()
    print("Leitura:")
    print("  - CPU: poucos nucleos, otima para tarefas sequenciais.")
    print("  - GPU: muitos nucleos em paralelo; e quem 'puxa' a IA.")
    print("  - Sem GPU acessivel, o backend cai para NumPy (SIMD na CPU).")
    print()
    print("Proximo passo: python 2_benchmark.py")
