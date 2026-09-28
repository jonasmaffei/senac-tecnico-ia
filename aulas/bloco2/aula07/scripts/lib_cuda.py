# -*- coding: utf-8 -*-
# ============================================================================
# lib_cuda.py — Detecção do ambiente CUDA (numba) com fallback seguro
# ----------------------------------------------------------------------------
# Aulas de CUDA precisam de uma GPU NVIDIA. Como nem todo laboratório tem uma
# (o nosso usa GPU AMD), este módulo centraliza a detecção e permite que os
# scripts mostrem o CONCEITO e números de referência mesmo sem GPU.
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
    """Numba está instalado? (necessário para escrever kernels CUDA em Python)."""
    try:
        import numba  # noqa: F401
        return True
    except ImportError:
        return False


def tem_cuda():
    """Existe uma GPU NVIDIA acessível pelo numba.cuda?"""
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
    """Imprime um cabeçalho dizendo se há CUDA e qual a GPU."""
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
    """Mensagem didática padrão para quando não há CUDA."""
    print("Numba/CUDA indisponível — sem GPU NVIDIA acessível aqui.")
    print("Os números abaixo são de REFERÊNCIA (Tesla T4) para você comparar.")
    print("Para medir de verdade: Runtime > Change runtime type > T4 GPU.")


def cabecalho_ascii():
    """No console do Windows (cp1252), força UTF-8 e evita erro de encoding."""
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
