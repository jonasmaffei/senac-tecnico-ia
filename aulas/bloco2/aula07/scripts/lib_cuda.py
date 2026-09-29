# -*- coding: utf-8 -*-
# ============================================================================
# lib_cuda.py - Deteccao do ambiente CUDA (numba) com fallback seguro
# ----------------------------------------------------------------------------
# Aulas de CUDA precisam de uma GPU NVIDIA. Como nem todo laboratorio tem uma
# (o nosso usa GPU AMD), este modulo centraliza a deteccao e permite que os
# scripts mostrem o CONCEITO e numeros de referencia mesmo sem GPU.
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
    """Numba esta instalado? (necessario para escrever kernels CUDA em Python)."""
    try:
        import numba  # noqa: F401
        return True
    except ImportError:
        return False


def tem_cuda():
    """Existe uma GPU NVIDIA acessivel pelo numba.cuda?"""
    if not tem_numba():
        return False
    try:
        from numba import cuda
        return cuda.is_available()
    except Exception:
        return False


def nome_gpu():
    """Nome da primeira GPU CUDA, se houver."""
    try:
        from numba import cuda
        if cuda.is_available():
            return cuda.get_current_device().name.decode()
    except Exception:
        pass
    return None


def resumo():
    """Imprime um cabecalho dizendo se ha CUDA e qual a GPU."""
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
    """Mensagem didatica padrao para quando nao ha CUDA."""
    print("Numba/CUDA indisponivel - sem GPU NVIDIA acessivel aqui.")
    print("Os numeros abaixo sao de REFERENCIA (Tesla T4) para voce comparar.")
    print("Para medir de verdade: Runtime > Change runtime type > T4 GPU.")


def cabecalho_ascii():
    """No console do Windows (cp1252), forca UTF-8 e evita erro de encoding."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


if __name__ == "__main__":
    cabecalho_ascii()
    resumo()
    if tem_cuda():
        print("\nTestando um kernel trivial...")
        from numba import cuda
        import numpy as np

        @cuda.jit
        def preencher(arr):
            i = cuda.grid(1)
            if i < arr.shape[0]:
                arr[i] = i

        dados = np.zeros(16, dtype=np.int32)
        d = cuda.to_device(dados)
        preencher[1, 16](d)
        cuda.synchronize()
        print("Resultado:", d.copy_to_host())
    else:
        print("\nDica: teste este arquivo no Colab com GPU para ver o kernel rodar.")
