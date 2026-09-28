#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# listar_dispositivos.py — Descobrir plataformas e dispositivos OpenCL
# ----------------------------------------------------------------------------
# OBJETIVO: o primeiro passo de qualquer programa OpenCL é descobrir o que
# existe no hardware. A hierarquia é:
#
#   Platform (drivers do fabricante: NVIDIA, AMD, Intel, ...)
#     └── Device (CPU, GPU ou acelerador dentro da plataforma)
#
# Aqui listamos todas as plataformas e, para cada uma, os dispositivos com
# nº de compute units, memória global (VRAM) e frequência máxima.
#
# Uso:  python listar_dispositivos.py
# Requer: pyopencl (opcional — sem ele, explica o conceito)
# ============================================================================

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import lib_opencl


def main():
    lib_opencl.cabecalho_ascii()
    print("=" * 64)
    print(" OpenCL: plataformas e dispositivos disponíveis")
    print("=" * 64)

    cl = lib_opencl.carregar()
    if cl is None:
        lib_opencl.explicar_sem_opencl()
        print()
        print("Conceito da hierarquia:")
        print("  Platform = conjunto de drivers do fabricante (NVIDIA/AMD/Intel)")
        print("  Device   = CPU, GPU ou acelerador onde o kernel executa")
        print("Referência: plataforma Intel com 1 GPU integrada + 1 CPU,")
        print("ou plataforma AMD/NVIDIA com 1 GPU dedicada.")
        return

    plataformas = lib_opencl.listar(cl)
    if not plataformas:
        print("Nenhuma plataforma OpenCL encontrada neste ambiente.")
        lib_opencl.explicar_sem_opencl()
        return

    for plataforma, dispositivos in plataformas:
        print(f"\nPlataforma: {plataforma.name}")
        print(f"  Versão    : {plataforma.version}")
        if not dispositivos:
            print("  (nenhum dispositivo exposto por esta plataforma)")
            continue
        for dispositivo in dispositivos:
            tipo = cl.device_type.to_string(dispositivo.type).replace(" ", "_")
            print(f"  [{tipo}] {dispositivo.name}")
            print(f"     Compute units : {dispositivo.max_compute_units}")
            print(f"     Mem global    : {dispositivo.global_mem_size // (1024**3)} GB")
            print(f"     Frequência    : {dispositivo.max_clock_frequency} MHz")
            print(f"     Max work-group: {dispositivo.max_work_group_size}")


if __name__ == "__main__":
    main()
