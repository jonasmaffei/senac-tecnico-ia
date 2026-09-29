# -*- coding: utf-8 -*-
# ============================================================================
# lib_opencl.py - Deteccao do ambiente OpenCL (PyOpenCL) com fallback seguro
# ----------------------------------------------------------------------------
# OpenCL e o padrao aberto que roda em GPUs NVIDIA, AMD, Intel e ate na CPU.
# Como o PyOpenCL pode nao estar instalado (ou nao haver dispositivo), este
# modulo centraliza a deteccao e permite que os scripts mostrem o CONCEITO
# mesmo sem OpenCL - a aula nunca quebra.
#
# Uso:
#   import lib_opencl
#   cl = lib_opencl.carregar()          # devolve o modulo pyopencl ou None
#   if cl: ...
# ============================================================================

import sys


def tem_pyopencl():
    """PyOpenCL esta instalado?"""
    try:
        import pyopencl  # noqa: F401
        return True
    except ImportError:
        return False


def carregar():
    """Importa e devolve o pyopencl, ou None se nao estiver disponivel."""
    try:
        import pyopencl as cl
        return cl
    except ImportError:
        return None


def listar(cl):
    """Devolve [(plataforma, [dispositivos])] para cada plataforma OpenCL."""
    resultado = []
    for plataforma in cl.get_platforms():
        try:
            dispositivos = plataforma.get_devices()
        except Exception:
            dispositivos = []
        resultado.append((plataforma, dispositivos))
    return resultado


def resumo():
    """Imprime um cabecalho dizendo se ha OpenCL e quais dispositivos existem."""
    print("=" * 64)
    cl = carregar()
    if cl is None:
        print(" PyOpenCL indisponivel neste ambiente.")
        print(" Os scripts mostram o conceito e numeros de REFERENCIA.")
        print(" Instalar no Colab/local:  pip install pyopencl")
    else:
        plataformas = listar(cl)
        total = sum(len(disp) for _, disp in plataformas)
        if total:
            print(f" OpenCL disponivel: {len(plataformas)} plataforma(s), {total} dispositivo(s)")
        else:
            print(" PyOpenCL instalado, mas nenhum dispositivo OpenCL encontrado.")
            print(" Neste caso, os scripts mostram o conceito e a referencia.")
    print("=" * 64)


def explicar_sem_opencl():
    """Mensagem didatica padrao quando nao ha OpenCL utilizavel."""
    print("OpenCL indisponivel - sem PyOpenCL ou sem dispositivo acessivel.")
    print("Os numeros abaixo sao de REFERENCIA (iGPU Intel / T4) para comparar.")
    print("No Colab:  !pip install pyopencl   (ha fallback de CPU na maioria dos casos).")


def cabecalho_ascii():
    """No console do Windows (cp1252), forca UTF-8 e evita erro de encoding."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


if __name__ == "__main__":
    cabecalho_ascii()
    resumo()
