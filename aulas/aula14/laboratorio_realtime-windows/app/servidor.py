# ============================================================================
# servidor.py — webservice de monitoramento em tempo real (versão Windows)
# ----------------------------------------------------------------------------
# Este é o programa que você executa no Windows: enquanto ele estiver rodando,
# coleta métricas continuamente e as publica em http://localhost:5000.
#
#   1. Uma thread em segundo plano coleta métricas a cada N segundos e guarda
#      as últimas amostras em memória (deque).
#   2. O painel fica em  http://localhost:5000/
#   3. A API JSON fica em http://localhost:5000/api/metricas
#   4. O fluxo em tempo real (SSE) fica em http://localhost:5000/api/stream.
#
# Feche a janela / Ctrl+C para encerrar o monitoramento.
# ============================================================================

import json
import os
import threading
import time
from collections import deque
from datetime import datetime

from flask import Flask, Response, jsonify, render_template

import coletor

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO (pode ser ajustada por variáveis de ambiente)
# ---------------------------------------------------------------------------
INTERVALO = int(os.environ.get("INTERVALO", "2"))
MAX_AMOSTRAS = int(os.environ.get("MAX_AMOSTRAS", "900"))

# A raiz do projeto é a pasta ACIMA de app/ (onde este arquivo está). Assim o
# CSV é gravado em <projeto>/reports/metricas.csv, independentemente de qual
# diretório o programa foi iniciado.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_ARQUIVO = os.environ.get("CSV_ARQUIVO", os.path.join(RAIZ, "reports", "metricas.csv"))

# A pasta do script entra no sys.path, então "import coletor" funciona mesmo
# rodando de qualquer diretório. O template é procurado em app/templates.
app = Flask(__name__)

historico = deque(maxlen=MAX_AMOSTRAS)
trava = threading.Lock()


# ---------------------------------------------------------------------------
# COLETA EM SEGUNDO PLANO
# ---------------------------------------------------------------------------
def loop_coleta():
    while True:
        try:
            amostra = coletor.coletar()
            with trava:
                historico.append(amostra)
            gravar_csv(amostra)
        except Exception as erro:
            print(f"[coletor] erro ao coletar: {erro}")
        time.sleep(INTERVALO)


def gravar_csv(amostra):
    """Acrescenta a amostra em reports/metricas.csv (histórico persistente)."""
    try:
        os.makedirs(os.path.dirname(CSV_ARQUIVO) or ".", exist_ok=True)
        novo = not os.path.exists(CSV_ARQUIVO)
        campos = [
            "timestamp", "cpu_pct", "cpu_temp_c", "ram_usada_mb", "ram_total_mb",
            "gpu_nome", "gpu_temp_c", "gpu_util_pct", "vram_usada_mb",
            "vram_total_mb", "gpu_potencia_w",
        ]
        with open(CSV_ARQUIVO, "a", encoding="utf-8") as f:
            if novo:
                f.write(",".join(campos) + "\n")
            valores = [
                "" if amostra.get(c) is None else str(amostra.get(c, ""))
                for c in campos
            ]
            f.write(",".join(valores) + "\n")
    except Exception as erro:
        print(f"[coletor] erro ao gravar CSV: {erro}")


# ---------------------------------------------------------------------------
# ROTAS
# ---------------------------------------------------------------------------
@app.route("/")
def painel():
    return render_template(
        "dashboard.html",
        intervalo=INTERVALO,
        max_amostras=MAX_AMOSTRAS,
        backend=coletor.nome_backend(),
        specs=coletor.especificacoes(),
    )


@app.route("/api/metricas")
def api_metricas():
    with trava:
        dados = list(historico)
    return jsonify({
        "intervalo_s": INTERVALO,
        "backend_gpu": coletor.nome_backend(),
        "total": len(dados),
        "amostras": dados,
    })


@app.route("/api/specs")
def api_specs():
    return jsonify(coletor.especificacoes())


@app.route("/api/stream")
def api_stream():
    def gerar():
        ultimo = 0
        yield "retry: 3000\n\n"
        while True:
            with trava:
                dados = list(historico)
            for amostra in dados[ultimo:]:
                yield f"data: {json.dumps(amostra)}\n\n"
            ultimo = len(dados)
            time.sleep(1)

    return Response(gerar(), mimetype="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok", "hora": datetime.now().isoformat()})


# ---------------------------------------------------------------------------
# INICIALIZAÇÃO
# ---------------------------------------------------------------------------
def main():
    thread = threading.Thread(target=loop_coleta, daemon=True)
    thread.start()

    print("=" * 60)
    print(" Monitoramento em tempo real (Windows) — Aula 14")
    print(f" Backend de GPU: {coletor.nome_backend()}")
    print(f" Intervalo: {INTERVALO}s | Histórico: {MAX_AMOSTRAS} amostras")
    print(f" CSV: {CSV_ARQUIVO}")
    print(" Abra no navegador: http://localhost:5000")
    print(" Pressione Ctrl+C para encerrar o monitoramento.")
    print("=" * 60)

    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)


if __name__ == "__main__":
    main()
