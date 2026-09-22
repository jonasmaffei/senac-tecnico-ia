# ============================================================================
# servidor.py — webservice de monitoramento em tempo real (Flask + SSE)
# ----------------------------------------------------------------------------
# O que este serviço faz:
#
#   1. Roda uma thread em segundo plano que coleta métricas a cada N segundos
#      (usando o coletor.py) e guarda as últimas amostras em memória.
#   2. Expõe o painel em  http://localhost:5000/          (HTML + JavaScript)
#   3. Expõe a API JSON em http://localhost:5000/api/metricas
#   4. Expõe um fluxo em tempo real (Server-Sent Events) em
#      http://localhost:5000/api/stream  — o navegador recebe cada nova
#      amostra sem precisar recarregar a página.
#
# Server-Sent Events (SSE) é uma tecnologia simples: o servidor mantém a
# conexão HTTP aberta e envia blocos de texto "data: {...}" sempre que há
# novidade. É ideal para dashboards e não exige WebSocket.
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
# CONFIGURAÇÃO (vem de variáveis de ambiente — veja o docker-compose.yml)
# ---------------------------------------------------------------------------
INTERVALO = int(os.environ.get("INTERVALO", "2"))     # segundos entre coletas
MAX_AMOSTRAS = int(os.environ.get("MAX_AMOSTRAS", "900"))  # histórico em memória
CSV_ARQUIVO = os.environ.get("CSV_ARQUIVO", "reports/metricas.csv")

app = Flask(__name__)

# Histórico em memória. deque com maxlen descarta automaticamente as amostras
# mais antigas, mantendo o consumo de memória constante.
historico = deque(maxlen=MAX_AMOSTRAS)

# Trava para evitar que duas threads alterem o histórico ao mesmo tempo.
trava = threading.Lock()

# Contador de "assinantes" do SSE — só para mostrar no terminal quantos
# navegadores estão conectados.
ouvintes = 0


# ---------------------------------------------------------------------------
# COLETA EM SEGUNDO PLANO
# ---------------------------------------------------------------------------
def loop_coleta():
    """Thread que coleta métricas continuamente e alimenta o histórico + CSV."""
    while True:
        try:
            amostra = coletor.coletar()
            with trava:
                historico.append(amostra)
            gravar_csv(amostra)
        except Exception as erro:
            # Nunca deixa a thread morrer por causa de uma amostra com problema.
            print(f"[coletor] erro ao coletar: {erro}")
        time.sleep(INTERVALO)


def gravar_csv(amostra):
    """Acrescenta a amostra em um CSV (histórico persistente no volume)."""
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
            # Campos ausentes (ex.: temperatura da CPU) viram vazio, não "None".
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
    """Página principal: serve o HTML do dashboard."""
    return render_template(
        "dashboard.html",
        intervalo=INTERVALO,
        max_amostras=MAX_AMOSTRAS,
        backend=coletor.nome_backend(),
        specs=coletor.especificacoes(),
    )


@app.route("/api/metricas")
def api_metricas():
    """API JSON com todo o histórico em memória (para uso externo/curl)."""
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
    """Especificações fixas da máquina."""
    return jsonify(coletor.especificacoes())


@app.route("/api/stream")
def api_stream():
    """Fluxo em tempo real (SSE): envia cada nova amostra ao navegador."""
    def gerar():
        global ouvintes
        ouvintes += 1
        ultimo = 0
        try:
            # Avisa o navegador que o conteúdo é um fluxo SSE.
            yield "retry: 3000\n\n"
            while True:
                with trava:
                    dados = list(historico)
                # Envia apenas o que ainda não foi enviado.
                for amostra in dados[ultimo:]:
                    yield f"data: {json.dumps(amostra)}\n\n"
                ultimo = len(dados)
                time.sleep(1)
        finally:
            ouvintes -= 1

    return Response(gerar(), mimetype="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",   # evita buffering em proxies
    })


@app.route("/health")
def health():
    """Endpoint simples para verificar se o serviço está no ar."""
    return jsonify({"status": "ok", "hora": datetime.now().isoformat()})


# ---------------------------------------------------------------------------
# INICIALIZAÇÃO
# ---------------------------------------------------------------------------
def main():
    # Sobe a thread de coleta antes de aceitar conexões.
    thread = threading.Thread(target=loop_coleta, daemon=True)
    thread.start()

    print("=" * 60)
    print(" Monitoramento em tempo real — Aula 14")
    print(f" Backend de GPU: {coletor.nome_backend()}")
    print(f" Intervalo: {INTERVALO}s | Histórico: {MAX_AMOSTRAS} amostras")
    print(f" CSV: {CSV_ARQUIVO}")
    print(" Abra no navegador: http://localhost:5000")
    print("=" * 60)

    # host 0.0.0.0 permite acessar de fora do container (do Windows).
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)


if __name__ == "__main__":
    main()
