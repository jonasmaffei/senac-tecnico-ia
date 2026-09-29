#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# arquitetura_instrucoes.py - RISC vs. CISC na pratica
# ----------------------------------------------------------------------------
# OBJETIVO: mostrar como a arquitetura instrucional da maquina se apresenta:
#
#   - RISC (ARM): instrucoes simples e de tamanho FIXO. Ex.: Raspberry Pi,
#     smartphones, Apple Silicon.
#   - CISC (x86/x64): instrucoes complexas e de tamanho VARIAVEL. Ex.: PCs
#     Intel/AMD e servidores.
#
# O script detecta a plataforma e explica o que voce veria em cada uma. No
# Colab/Linux (x86) ele tambem mostra as instrucoes SIMD que o Python usa.
#
# Uso:  python arquitetura_instrucoes.py
# ============================================================================

import platform
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def classificar(maquina):
    """Traduz o nome da maquina (platform.machine) em RISC, CISC ou desconhecido."""
    m = maquina.lower()
    if any(t in m for t in ("x86", "amd64", "i386", "i686")):
        return "CISC (x86/x64)", "Intel/AMD"
    if any(t in m for t in ("arm", "aarch64")):
        return "RISC (ARM)", "ARM (ex.: Raspberry Pi, smartphones, Apple Silicon)"
    return "Indefinida", "?"


def instrucoes_simd():
    """Devolve os conjuntos de instrucoes SIMD conhecidos nesta maquina.

    Tenta a API publica do NumPy primeiro e, se nao existir, cai para o
    atributo interno (compativel com versoes antigas), sem emitir aviso.
    """
    flags = []
    recursos = None
    try:
        # API publica (NumPy >= 2.0). Retorna None se nao suportado.
        from numpy.lib._utils_impl import __cpu_features__ as recursos
    except Exception:
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                from numpy._core._multiarray_umath import __cpu_features__ as recursos
        except Exception:
            recursos = None

    if not recursos:
        return flags

    for chave, descricao in (
        ("AVX512F", "AVX-512"),
        ("AVX2", "AVX2"),
        ("AVX", "AVX"),
        ("SSE42", "SSE4.2"),
        ("SSE2", "SSE2"),
        ("NEON", "NEON (ARM)"),
    ):
        if recursos.get(chave):
            flags.append(descricao)
    return flags


def main():
    maquina = platform.machine()
    sistema = platform.system()
    tipo, exemplo = classificar(maquina)

    print("=" * 64)
    print(" Arquitetura instrucional desta maquina")
    print("=" * 64)
    print(f" Plataforma   : {sistema} / {maquina}")
    print(f" Tipo         : {tipo}  ({exemplo})")

    if tipo.startswith("CISC"):
        print(" Instrucoes   : complexas e de TAMANHO VARIAVEL (1 a ~15 bytes)")
        print(" Pipeline     : menos previsivel; consome mais energia")
    elif tipo.startswith("RISC"):
        print(" Instrucoes   : simples e de TAMANHO FIXO (ex.: 32 bits)")
        print(" Pipeline     : eficiente e previsivel; baixo consumo")
    else:
        print(" Nao foi possivel classificar automaticamente esta maquina.")

    flags = instrucoes_simd()
    print()
    print(" Recursos SIMD disponiveis (que o NumPy usa):")
    if flags:
        print("   " + ", ".join(flags))
    else:
        print("   (nao detectados) - o NumPy ainda usa a melhor opcao da CPU")

    print()
    print("Como inspecionar no laboratorio (Colab/Linux):")
    print("   cat /proc/cpuinfo | grep 'model name' | head -1")
    print("   objdump -d /bin/ls | head -30   # RISC=tamanho fixo, CISC=variavel")


if __name__ == "__main__":
    main()
