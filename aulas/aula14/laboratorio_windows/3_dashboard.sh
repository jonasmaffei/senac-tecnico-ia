#!/usr/bin/env bash
# ============================================================================
# 3_dashboard.sh — gera um dashboard HTML a partir do gpu_log.csv
# ----------------------------------------------------------------------------
# Uso:  ./3_dashboard.sh [arquivo_csv]
# Ex.:  ./3_dashboard.sh gpu_log.csv
#
# Gera dashboard.html com as especificações da máquina e painéis de GPU
# (temperatura, utilização, VRAM, potência) e de sistema (CPU, RAM e, se
# disponível, temperatura da CPU) desenhados em SVG. NÃO precisa instalar nada:
# abre com duplo clique no navegador (Git Bash, WSL e Linux — sem gnuplot).
# ============================================================================

cd "$(dirname "$0")" || exit 1
source ./lib_gpu.sh

# O fuso de Brasília (BRT, UTC-3) já vem definido pela lib_gpu.sh

set -euo pipefail

CSV="${1:-$DIR_RELATORIOS/gpu_log.csv}"
HTML="$DIR_RELATORIOS/dashboard.html"

# Se o usuário passar apenas um nome (ex.: "gpu_log.csv"), busca em reports/
case "$CSV" in
    */*|*\\*) ;;                                 # já tem pasta/caminho absoluto
    *) CSV="$DIR_RELATORIOS/$CSV" ;;
esac

# Cria a pasta de relatórios, caso ainda não exista
preparar_relatorios

if [ ! -f "$CSV" ]; then
    echo "ERRO: arquivo '$CSV' nao encontrado."
    echo "Rode antes: ./1_monitorar.sh 2 gpu_log.csv 20"
    exit 1
fi

# O CSV é incremental: mostramos TODO o histórico nele.
# As amostras já vêm em ordem cronológica (são apenas acrescentadas).
#
# Para o navegador não engasgar com milhares de pontos, quando o histórico passa
# de MAX_PONTOS fazemos uma amostragem uniforme (pega 1 linha a cada N),
# preservando o formato geral das curvas e todo o período de tempo.
#
# Tudo é feito com UM único awk (normaliza os campos, amostra e formata),
# evitando milhares de chamadas a printf/tr/sed por linha — que deixariam o
# processamento lento quando o histórico cresce.
MAX_PONTOS="${MAX_PONTOS:-1500}"

# Conta as amostras (linhas de dados, sem o cabeçalho)
N_TODAS=$(awk 'NR>1 { n++ } END { print n + 0 }' "$CSV")

if [ "$N_TODAS" -eq 0 ]; then
    echo "ERRO: '$CSV' nao tem amostras (so o cabecalho)."
    echo "Rode antes: ./1_monitorar.sh 2 gpu_log.csv 20"
    exit 1
fi

# Passo da amostragem (1 = todas as amostras)
PASSO=$(( N_TODAS / MAX_PONTOS + 1 ))

# O awk devolve cada amostra como campos separados por "|":
#   ts|lbl|temp|util|vram|pot|cpu|ram|ramtot|cput|nome|vtot
# Já com espaços removidos e a RAM convertida para GB.
mapfile -t CAMPOS < <(awk -F',' -v passo="$PASSO" -v total="$N_TODAS" '
    function limpa(s) { gsub(/^ +| +$/, "", s); return s }
    function gb(v)    { return (v ~ /^[0-9]+$/) ? int(v / 1024) : v }
    NR == 1 { next }
    {
        idx = NR - 2                       # 0 = primeira amostra
        # Pega 1 a cada "passo" e SEMPRE a última amostra (mais recente)
        if (idx % passo != 0 && idx != total - 1) next
        ts = limpa($1)
        printf "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s\n", \
            ts, substr(ts, 12, 5), limpa($4), limpa($5), limpa($7), limpa($9), \
            limpa($11), gb(limpa($12)), limpa($13), limpa($14), limpa($3), limpa($8)
    }
' "$CSV")

TOTAL=${#CAMPOS[@]}

# ── Distribui os campos nas séries usadas pelo dashboard ────────────────────
TEMPS=(); UTILG=(); VRAM=(); POT=(); ROTULOS=(); CPUS=(); RAMS=(); CPUT=()
RAMS_GB=(); TS_LISTA=()
RAM_TOTAL=""; GPU_NOME=""; VRAM_TOTAL=""
for linha in "${CAMPOS[@]}"; do
    IFS='|' read -r ts lbl temp ug vram pw cpu ram ramtot cput nome vtot <<< "$linha"
    ROTULOS+=("$lbl"); TS_LISTA+=("$ts")
    TEMPS+=("$temp"); UTILG+=("$ug"); VRAM+=("$vram"); POT+=("$pw")
    CPUS+=("$cpu"); RAMS+=("$ram"); CPUT+=("$cput"); RAMS_GB+=("$ram")
    [ -z "$GPU_NOME" ] && GPU_NOME="$nome"
    [ -z "$RAM_TOTAL" ] && RAM_TOTAL="$ramtot"
    [ -z "$VRAM_TOTAL" ] && VRAM_TOTAL="$vtot"
done

# Descobre o período coberto pelo histórico (primeira e última amostra)
TS_INI="${TS_LISTA[0]:-}"
TS_FIM="${TS_LISTA[$(( TOTAL - 1 ))]:-}"

if [ "$N_TODAS" -gt "$MAX_PONTOS" ]; then
    echo "Historico com $N_TODAS amostras: grafico reduzido para $TOTAL pontos (1 a cada $PASSO)."
fi

# ── Especificações fixas da máquina (CPU, núcleos, SO) ──────────────────────
IFS='|' read -r CPU_MODELO CPU_CORES CPU_THREADS SIS_OP HOST <<< "$(specs_sistema)"
# Limpa espaços extras que a saída do Windows costuma deixar
CPU_MODELO=$(printf '%s' "$CPU_MODELO" | sed 's/^ *//; s/ *$//; s/  */ /g')
SIS_OP=$(printf '%s' "$SIS_OP" | sed 's/^ *//; s/ *$//')

# ── Função que constrói um gráfico SVG de linha a partir de uma série ────────
# $1=título  $2=cor  $3=valor máximo do eixo Y  $4=unidade  $5...=valores
# Desenha: eixos com escala (0, 25%, 50%, 75% e máximo), grades horizontais,
# linha do tempo em Brasília e legenda com mín./máx./atual.
gerar_svg() {
    local titulo="$1" cor="$2" ymax="$3" unidade="$4"; shift 4
    local valores=("$@")
    local w=560 h=240
    local pad_l=52 pad_r=16 pad_t=18 pad_b=40
    local n=${#valores[@]}
    local plotw=$(( w - pad_l - pad_r ))
    local ploth=$(( h - pad_t - pad_b ))
    local base=$(( h - pad_b ))                 # linha y=0 do gráfico

    if [ "$ymax" -le 0 ]; then ymax=1; fi

    # ── Mínimo, máximo e valor atual da série (para a legenda) ──
    local vmin="" vmax="" vcorr="" i=0
    for v in "${valores[@]}"; do
        if [[ "$v" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
            vcorr="$v"
            if [ -z "$vmin" ] || [ "$v" -lt "$vmin" ]; then vmin="$v"; fi
            if [ -z "$vmax" ] || [ "$v" -gt "$vmax" ]; then vmax="$v"; fi
        fi
    done
    local sem_dados=0
    if [ -z "$vmax" ]; then
        sem_dados=1
        vmin="N/A"; vmax="N/A"; vcorr="N/A"
    fi

    # ── Linha do gráfico ──
    local pontos="" ultimo=0
    for v in "${valores[@]}"; do
        if [[ "$v" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
            ultimo="$v"
        else
            v="$ultimo"
        fi
        if [ "$n" -le 1 ]; then
            x=$(( pad_l + plotw / 2 ))
        else
            x=$(( pad_l + i * plotw / (n - 1) ))
        fi
        y=$(( base - ( v * ploth / ymax ) ))
        pontos+="$x,$y "
        i=$(( i + 1 ))
    done

    # Marcas do eixo Y: 0, 25%, 50%, 75% e 100% do máximo
    local marcas_y="" grade_y="" k
    for k in 0 25 50 75 100; do
        local yv=$(( ymax * k / 100 ))
        local yy=$(( base - ( yv * ploth / ymax ) ))
        marcas_y+="<text x=\"$(( pad_l - 6 ))\" y=\"$(( yy + 4 ))\" fill=\"#94a3b8\" font-size=\"10\" text-anchor=\"end\">$yv</text>"
        grade_y+="<line x1=\"$pad_l\" y1=\"$yy\" x2=\"$(( w - pad_r ))\" y2=\"$yy\" stroke=\"#1e293b\" stroke-width=\"1\"/>"
    done

    # Rótulos de tempo (início, meio e fim) em Brasília
    local lbl_ini="${ROTULOS[0]:-}"
    local lbl_meio="${ROTULOS[$(( n / 2 ))]:-}"
    local lbl_fim="${ROTULOS[$(( n - 1 ))]:-}"

    # Métrica indisponível neste backend (ex.: potência na AMD/Windows)
    if [ "$sem_dados" -eq 1 ]; then
        cat <<EOF
    <div class="card">
      <h3>$titulo</h3>
      <div class="vazio">Métrica não disponível neste backend.<br>
        <span>Na AMD com Windows, temperatura e potência não são expostas pelo driver —
        no Linux com ROCm esses valores são reais.</span>
      </div>
    </div>
EOF
        return
    fi

    cat <<EOF
    <div class="card">
      <h3>$titulo</h3>
      <svg viewBox="0 0 $w $h" preserveAspectRatio="xMidYMid meet">
        <rect x="0" y="0" width="$w" height="$h" fill="#0f172a"/>
        <!-- Grades horizontais + escala do eixo Y -->
        $grade_y
        $marcas_y
        <!-- Eixos X e Y -->
        <line x1="$pad_l" y1="$base" x2="$(( w - pad_r ))" y2="$base" stroke="#475569"/>
        <line x1="$pad_l" y1="$pad_t" x2="$pad_l" y2="$base" stroke="#475569"/>
        <!-- Linha do Gráfico -->
        <polyline fill="none" stroke="$cor" stroke-width="2.5" points="$pontos"/>
        <!-- Horários (fuso de Brasília, UTC-3) -->
        <text x="$pad_l" y="$(( base + 15 ))" fill="#94a3b8" font-size="10">$lbl_ini</text>
        <text x="$(( pad_l + plotw / 2 ))" y="$(( base + 15 ))" fill="#94a3b8" font-size="10" text-anchor="middle">$lbl_meio</text>
        <text x="$(( w - pad_r ))" y="$(( base + 15 ))" fill="#94a3b8" font-size="10" text-anchor="end">$lbl_fim</text>
        <text x="$(( w - pad_r ))" y="13" fill="#64748b" font-size="9" text-anchor="end">horário de Brasília (UTC-3)</text>
      </svg>
      <div class="legenda">
        <span>mín: <b>$vmin $unidade</b></span>
        <span>máx: <b>$vmax $unidade</b></span>
        <span>atual: <b style="color:$cor">$vcorr $unidade</b></span>
        <span>escala: 0–$ymax $unidade</span>
      </div>
    </div>
EOF
}

# ── Escalas (máximos) ───────────────────────────────────────────────────────
max_de() { local m=0; for x in "$@"; do [[ "$x" =~ ^[0-9]+$ ]] || continue; [ "$x" -gt "$m" ] && m=$x; done; echo "$m"; }

# Converte MB -> GB com 1 casa (ex.: 32719 -> 31.9)
mb_para_gb() {
    local mb="$1"
    [[ "$mb" =~ ^[0-9]+$ ]] || { echo "N/A"; return; }
    awk -v m="$mb" 'BEGIN { printf "%.1f", m / 1024 }'
}

Y_TEMP=100
Y_UTIL=110
Y_CPU=100
Y_VRAM=$(max_de "${VRAM[@]}"); [ "$Y_VRAM" -lt 100 ] && Y_VRAM=100
Y_POT=$(max_de "${POT[@]}");  [ "$Y_POT" -lt 20 ] && Y_POT=20
Y_RAM=$(max_de "${RAMS_GB[@]}");  [ "$Y_RAM" -lt 4 ] && Y_RAM=4
[ -n "$RAM_TOTAL" ] && [[ "$RAM_TOTAL" =~ ^[0-9]+$ ]] && [ "$(( RAM_TOTAL / 1024 ))" -gt "$Y_RAM" ] && Y_RAM=$(( RAM_TOTAL / 1024 ))
# CPU: usa o maior entre 100% e o pico observado, para os gráficos ficarem comparáveis
Y_CPU=$(max_de "${CPUS[@]}"); [ "$Y_CPU" -lt 100 ] && Y_CPU=100

# Valores atuais para o resumo (última amostra das séries)
# Observação: RAMS já está em GB (convertido no awk); RAM_TOTAL ainda em MB.
CPU_ATUAL="${CPUS[$(( TOTAL - 1 ))]:-N/A}"
RAM_ATUAL_GB="${RAMS_GB[$(( TOTAL - 1 ))]:-N/A}"
RAM_TOTAL_GB=$(mb_para_gb "$RAM_TOTAL")
RAM_PCT="N/A"
if [[ "$RAM_ATUAL_GB" =~ ^[0-9]+$ ]] && [[ "$RAM_TOTAL" =~ ^[0-9]+$ ]] && [ "$RAM_TOTAL" -gt 0 ]; then
    RAM_PCT=$(( RAM_ATUAL_GB * 1024 * 100 / RAM_TOTAL ))
fi

TITULO="System & GPU Monitoring Dashboard — Aula 14"
AMOSTRAS_TXT="$N_TODAS amostras"
[ "$TOTAL" -ne "$N_TODAS" ] && AMOSTRAS_TXT="$N_TODAS amostras ($TOTAL pontos no gráfico)"
SUBTITULO="Histórico completo: ${TS_INI} até ${TS_FIM} · $AMOSTRAS_TXT · gerado em $(date '+%Y-%m-%d %H:%M:%S')"

{
cat <<EOF
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>$TITULO</title>
<style>
  body { margin:0; background:#020617; color:#e2e8f0;
         font-family:"Segoe UI",system-ui,Arial,sans-serif; padding:28px; }
  h1 { font-size:1.4rem; margin:0 0 4px; }
  .sub { color:#94a3b8; font-size:.85rem; margin-bottom:20px; }
  .grid { display:grid; grid-template-columns:repeat(2,1fr); gap:18px; max-width:1200px; }
  .card { background:#0f172a; border:1px solid #1e293b; border-radius:12px; padding:14px 16px; }
  .card h3 { margin:0 0 10px; font-size:.98rem; }
  svg { width:100%; height:auto; border-radius:8px; }
  .legenda { display:flex; flex-wrap:wrap; gap:6px 16px; margin-top:10px;
             font-size:.78rem; color:#94a3b8; }
  .legenda b { color:#e2e8f0; }
  .vazio { display:flex; flex-direction:column; justify-content:center; align-items:center;
           text-align:center; min-height:200px; border:1px dashed #334155; border-radius:8px;
           color:#cbd5e1; font-size:.9rem; padding:16px; }
  .vazio span { display:block; margin-top:8px; color:#64748b; font-size:.78rem; max-width:360px; }
  .tag { display:inline-block; font-size:.75rem; color:#94a3b8; margin-top:10px; }
  .specs { display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
           gap:12px 20px; max-width:1200px; margin-bottom:18px; }
  .spec { background:#0f172a; border:1px solid #1e293b; border-radius:12px; padding:12px 16px; }
  .spec .rotulo { font-size:.72rem; text-transform:uppercase; letter-spacing:.05em; color:#64748b; }
  .spec .valor { font-size:.98rem; font-weight:600; margin-top:4px; word-break:break-word; }
  .spec .extra { font-size:.78rem; color:#94a3b8; margin-top:2px; }
  @media (max-width:900px){ .grid{ grid-template-columns:1fr; } }
</style>
</head>
<body>
  <h1>$TITULO</h1>
  <div class="sub">$SUBTITULO</div>

  <!-- Especificações fixas da máquina monitorada -->
  <div class="specs">
    <div class="spec">
      <div class="rotulo">Processador</div>
      <div class="valor">$CPU_MODELO</div>
      <div class="extra">${CPU_CORES:-?} núcleos · ${CPU_THREADS:-?} threads · agora ${CPU_ATUAL}%</div>
    </div>
    <div class="spec">
      <div class="rotulo">Memória RAM</div>
      <div class="valor">${RAM_TOTAL_GB} GB</div>
      <div class="extra">em uso agora: ${RAM_ATUAL_GB} GB (${RAM_PCT}%)</div>
    </div>
    <div class="spec">
      <div class="rotulo">Placa de vídeo</div>
      <div class="valor">${GPU_NOME:-GPU}</div>
      <div class="extra">VRAM total: $(mb_para_gb "${VRAM_TOTAL:-}") GB</div>
    </div>
    <div class="spec">
      <div class="rotulo">Sistema operacional</div>
      <div class="valor">${SIS_OP:-Desconhecido}</div>
      <div class="extra">máquina: ${HOST:-?}</div>
    </div>
  </div>

  <div class="grid">
EOF

gerar_svg "🌡️ Temperatura da GPU" "#ef4444" "$Y_TEMP" "°C" "${TEMPS[@]}"
gerar_svg "⚙️ Utilização da GPU" "#10b981" "$Y_UTIL" "%" "${UTILG[@]}"
gerar_svg "💾 VRAM usada" "#a855f7" "$Y_VRAM" "MB" "${VRAM[@]}"
gerar_svg "⚡ Potência da GPU" "#f97316" "$Y_POT" "W" "${POT[@]}"
gerar_svg "🧠 Utilização da CPU" "#38bdf8" "$Y_CPU" "%" "${CPUS[@]}"
gerar_svg "🧩 Memória RAM usada" "#eab308" "$Y_RAM" "GB" "${RAMS_GB[@]}"
# Temperatura da CPU: só desenha se o sensor existir (varia entre máquinas)
if ! printf '%s\n' "${CPUT[@]}" | grep -qE '^[0-9]+$'; then
    :
else
    Y_CPUT=$(max_de "${CPUT[@]}"); [ "$Y_CPUT" -lt 100 ] && Y_CPUT=100
    gerar_svg "🌡️ Temperatura da CPU" "#f43f5e" "$Y_CPUT" "°C" "${CPUT[@]}"
fi

cat <<EOF
  </div>
  <div class="tag">Abra este arquivo no navegador. Gerado por 3_dashboard.sh sem dependências externas.</div>
</body>
</html>
EOF
} > "$HTML"

echo "Dashboard gerado: $HTML"
echo "Abra no navegador (duplo clique) ou rode: start $HTML"