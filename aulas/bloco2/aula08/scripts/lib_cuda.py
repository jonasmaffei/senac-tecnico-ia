# -*- coding: utf-8 -*-
# ============================================================================
# lib_cuda.py - Deteccao do ambiente CUDA (numba) com fallback seguro
# ----------------------------------------------------------------------------
# Mesmo padrao da Aula 07. Como o laboratorio usa GPU AMD (sem CUDA), este
# modulo permite que os scripts da Aula 08 mostrem o CONCEITO e numeros de
# referencia mesmo quando nao ha GPU NVIDIA.
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
        print(f" CUDA disponivel: {nome_gpu()}")
        print(" Kernels via numba.cuda serao executados na GPU.")
    else:
        print(" CUDA indisponivel neste ambiente (sem GPU NVIDIA).")
        print(" Os scripts mostram o conceito e numeros de REFERENCIA.")
        print(" No Google Colab com T4 GPU, o mesmo codigo roda na GPU.")
    print("=" * 64)


def explicar_sem_gpu():
    print("Numba/CUDA indisponivel - sem GPU NVIDIA acessivel aqui.")
    print("Os numeros abaixo sao de REFERENCIA (Tesla T4) para voce comparar.")
    print("Para medir de verdade: Runtime > Change runtime type > T4 GPU.")


def cabecalho_ascii():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


if __name__ == "__main__":
    cabecalho_ascii()
    resumo()
