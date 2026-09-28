# -*- coding: utf-8 -*-
# ============================================================================
# lib_cuda.py — Detecção do ambiente CUDA (numba) com fallback seguro
# ----------------------------------------------------------------------------
# Mesmo padrão da Aula 07. Como o laboratório usa GPU AMD (sem CUDA), este
# módulo permite que os scripts da Aula 08 mostrem o CONCEITO e números de
# referência mesmo quando não há GPU NVIDIA.
#
# Uso:
#   import lib_cuda
#   if lib_cuda.tem_cuda():
#       from numba import cuda
#       ...
#   else:
#       lib_cuda.explicar_sem_gpu()
# ============================================================================

import sys


def tem_numba():
    try:
        import numba  # noqa: F401
        return True
    except ImportError:
        return False


def tem_cuda():
    if not tem_numba():
        return False
    try:
        from numba import cuda
        return cuda.is_available()
    except Exception:
        return False


def nome_gpu():
    try:
        from numba import cuda
        if cuda.is_available():
            return cuda.get_current_device().name.decode()
    except Exception:
        pass
    return None


def resumo():
    print("=" * 64)
    if tem_cuda():
        print(f" CUDA disponível: {nome_gpu()}")
        print(" Kernels via numba.cuda serão executados na GPU.")
    else:
        print(" CUDA indisponível neste ambiente (sem GPU NVIDIA).")
        print(" Os scripts mostram o conceito e números de REFERÊNCIA.")
        print(" No Google Colab com T4 GPU, o mesmo código roda na GPU.")
    print("=" * 64)


def explicar_sem_gpu():
    print("Numba/CUDA indisponível — sem GPU NVIDIA acessível aqui.")
    print("Os números abaixo são de REFERÊNCIA (Tesla T4) para você comparar.")
    print("Para medir de verdade: Runtime > Change runtime type > T4 GPU.")


def cabecalho_ascii():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


if __name__ == "__main__":
    cabecalho_ascii()
    resumo()
