# -*- coding: utf-8 -*-
# ============================================================================
# lib_opencl.py — Detecção do ambiente OpenCL (PyOpenCL) com fallback seguro
# ----------------------------------------------------------------------------
# OpenCL é o padrão aberto que roda em GPUs NVIDIA, AMD, Intel e até na CPU.
# Como o PyOpenCL pode não estar instalado (ou não haver dispositivo), este
# módulo centraliza a detecção e permite que os scripts mostrem o CONCEITO
# mesmo sem OpenCL — a aula nunca quebra.
#
# Uso:
#   import lib_opencl
#   cl = lib_opencl.carregar()          # devolve o módulo pyopencl ou None
#   if cl: ...
# ============================================================================

import sys


def tem_pyopencl():
    """PyOpenCL está instalado?"""
    try:
        import pyopencl  # noqa: F401
        return True
    except ImportError:
        return False


def carregar():
    """Importa e devolve o pyopencl, ou None se não estiver disponível."""
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
    """Imprime um cabeçalho dizendo se há OpenCL e quais dispositivos existem."""
    print("=" * 64)
    cl = carregar()
    if cl is None:
        print(" PyOpenCL indisponível neste ambiente.")
        print(" Os scripts mostram o conceito e números de REFERÊNCIA.")
        print(" Instalar no Colab/local:  pip install pyopencl")
    else:
        plataformas = listar(cl)
        total = sum(len(disp) for _, disp in plataformas)
        if total:
            print(f" OpenCL disponível: {len(plataformas)} plataforma(s), {total} dispositivo(s)")
        else:
            print(" PyOpenCL instalado, mas nenhum dispositivo OpenCL encontrado.")
            print(" Neste caso, os scripts mostram o conceito e a referência.")
    print("=" * 64)


def explicar_sem_opencl():
    """Mensagem didática padrão quando não há OpenCL utilizável."""
    print("OpenCL indisponível — sem PyOpenCL ou sem dispositivo acessível.")
    print("Os números abaixo são de REFERÊNCIA (iGPU Intel / T4) para comparar.")
    print("No Colab:  !pip install pyopencl   (há fallback de CPU na maioria dos casos).")


def cabecalho_ascii():
    """No console do Windows (cp1252), força UTF-8 e evita erro de encoding."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


if __name__ == "__main__":
    cabecalho_ascii()
    resumo()
