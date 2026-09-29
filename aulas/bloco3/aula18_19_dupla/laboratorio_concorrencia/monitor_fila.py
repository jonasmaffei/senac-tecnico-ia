"""monitor_fila.py - Leitura do estado da GPU, do lock e da fila.

Modulo compartilhado entre o monitor (4_monitor_processos_gpu.py) e o teste de
fila (3_teste_fila.py). Como os outros arquivos comecam com numero (o que nao
pode ser importado em Python), a logica fica aqui.

Estados possiveis:
  - "OCUPADA": existe o diretorio de lock (um job esta usando a GPU).
  - "LIVRE":   ninguem esta usando a GPU no momento.

A fila e lida da pasta de tickets (reports/gpu_queue_spool), ordenada por
prioridade (o ticket e "prioridade_timestamp_nome").
"""

import os

import psutil

SPOOL_DIR = os.path.join("reports", "gpu_queue_spool")
LOCK_DIR = os.path.join("reports", "gpu_exclusive.lockdir")


def processos_ativos():
    """Lista os processos de treino/fila em execucao no host."""
    ativos = []
    for proc in psutil.process_iter(["pid", "name", "username", "cmdline"]):
        try:
            nome = (proc.info["name"] or "").lower()
            linha_cmd = " ".join(proc.info["cmdline"] or [])
            if "python" in nome and ("train_job" in linha_cmd or "gpu_queue" in linha_cmd):
                ativos.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return ativos


def lock_ativo():
    """True se a GPU esta ocupada (diretorio de lock existe)."""
    return os.path.exists(LOCK_DIR)


def fila_atual():
    """Lista os tickets aguardando, em ordem de prioridade."""
    if os.path.isdir(SPOOL_DIR):
        return sorted(os.listdir(SPOOL_DIR))
    return []


def coletar_snapshot():
    """Foto do estado atual: processos, lock e fila."""
    return {
        "processos": processos_ativos(),
        "lock": lock_ativo(),
        "fila": fila_atual(),
    }


def resumo_linha(snap):
    """Uma linha curta com o estado (para o monitoramento ao vivo)."""
    gpu = "OCUPADA" if snap["lock"] else "LIVRE"
    return (f"GPU={gpu:<7} | fila aguardando={len(snap['fila'])} "
            f"| jobs ativos={len(snap['processos'])}")
