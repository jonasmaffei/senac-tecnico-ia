#!/usr/bin/env bash
# ============================================================================
# 3_dashboard.sh — gera um dashboard HTML (4 gráficos) a partir do gpu_log.csv
# ----------------------------------------------------------------------------
# Uso:  ./3_dashboard.sh [arquivo_csv]
# Ex.:  ./3_dashboard.sh gpu_log.csv
#
# Gera dashboard.html com 4 painéis (temperatura, utilização, VRAM, potência)
# desenhados em SVG. NÃO precisa instalar nada: abre com duplo clique no
# navegador (funciona no Git Bash, WSL e Linux — sem gnuplot, sem Python).
# ============================================================================

cd "$(dirname "$0")" || exit 1

# Força o fuso horário de Brasília no Git Bash
export TZ="America/Sao_Paulo"

set -euo pipefail

CSV="${1:-gpu_log.csv}"
HTML="dashboard.html"

if [ ! -f "$CSV" ]; then
    echo "ERRO: arquivo '$CSV' nao encontrado."
    echo "Rode antes: ./1_monitorar.sh 2 gpu_log.csv 20"
    exit 1
fi

# Lê até 300 amostras (suficiente para os gráficos e mantém o HTML leve)
mapfile -t LINHAS < <(tail -n +2 "$CSV" | tail -n 300)
TOTAL=${#LINHAS[@]}

if [ "$TOTAL" -eq 0 ]; then
    echo "ERRO: '$CSV' nao tem dados."
    exit 1
fi

# ── Vetores de dados (colunas: 4=temp 5=util_gpu 6=util_mem 7=vram 9=pot 10=lim) ──
TEMPS=(); UTILG=(); VRAM=(); POT=(); ROTULOS=()
for linha in "${LINHAS[@]}"; do
    IFS=',' read -r ts idx nome temp ug um vram vtot pw plim <<< "$linha"
    
    # Remove apenas espaços no início/fim, preservando o espaço entre data e hora
    ts=$(printf '%s' "$ts" | sed 's/^ *//; s/ *$//')
    ROTULOS+=("${ts:11:5}")            # captura exatamente HH:MM
    
    TEMPS+=("$(printf '%s' "$temp" | tr -d ' ')")
    UTILG+=("$(printf '%s' "$ug" | tr -d ' ')")
    VRAM+=("$(printf '%s' "$vram" | tr -d ' ')")
    POT+=("$(printf '%s' "$pw" | tr -d ' ')")
done

# ── Função que constrói um gráfico SVG de linha a partir de uma série ────────
# $1=título  $2=cor  $3=valor máximo do eixo Y  $4...=valores
gerar_svg() {
    local titulo="$1" cor="$2" ymax="$3"; shift 3
    local valores=("$@")
    local w=560 h=220 pad=34
    local n=${#valores[@]}
    local plotw=$(( w - 2 * pad ))
    local ploth=$(( h - 2 * pad ))

    if [ "$ymax" -le 0 ]; then ymax=1; fi

    local pontos="" i=0 ultimo=0
    for v in "${valores[@]}"; do
        if [[ "$v" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
            ultimo="$v"
        else
            v="$ultimo"
        fi
        if [ "$n" -le 1 ]; then
            x=$(( pad + plotw / 2 ))
        else
            x=$(( pad + i * plotw / (n - 1) ))
        fi
        y=$(( h - pad - ( v * ploth / ymax ) ))
        pontos+="$x,$y "
        i=$(( i + 1 ))
    done

    # Captura as horas (início, meio e fim) do array global ROTULOS
    local lbl_ini="${ROTULOS[0]:-}"
    local lbl_meio="${ROTULOS[$(( n / 2 ))]:-}"
    local lbl_fim="${ROTULOS[$(( n - 1 ))]:-}"

    cat <<EOF
    <div class="card">
      <h3>$titulo</h3>
      <svg viewBox="0 0 $w $h" preserveAspectRatio="xMidYMid meet">
        <rect x="0" y="0" width="$w" height="$h" fill="#0f172a"/>
        <!-- Eixos X e Y -->
        <line x1="$pad" y1="$(( h - pad ))" x2="$(( w - pad ))" y2="$(( h - pad ))" stroke="#334155"/>
        <line x1="$pad" y1="$pad" x2="$pad" y2="$(( h - pad ))" stroke="#334155"/>
        <!-- Rótulo do Y máximo -->
        <text x="$pad" y="$(( pad - 8 ))" fill="#94a3b8" font-size="12">max $ymax</text>
        
        <!-- Timeline (Tempo no Eixo X) em Brasília -->
        <text x="$pad" y="$(( h - pad + 15 ))" fill="#94a3b8" font-size="10">$lbl_ini</text>
        <text x="$(( pad + plotw / 2 ))" y="$(( h - pad + 15 ))" fill="#94a3b8" font-size="10" text-anchor="middle">$lbl_meio</text>
        <text x="$(( w - pad ))" y="$(( h - pad + 15 ))" fill="#94a3b8" font-size="10" text-anchor="end">$lbl_fim</text>
        
        <!-- Linha do Gráfico -->
        <polyline fill="none" stroke="$cor" stroke-width="2.5" points="$pontos"/>
      </svg>
    </div>
EOF
}

# ── Escalas (máximos) ───────────────────────────────────────────────────────
max_de() { local m=0; for x in "$@"; do [[ "$x" =~ ^[0-9]+$ ]] || continue; [ "$x" -gt "$m" ] && m=$x; done; echo "$m"; }

Y_TEMP=100
Y_UTIL=110
Y_VRAM=$(max_de "${VRAM[@]}"); [ "$Y_VRAM" -lt 100 ] && Y_VRAM=100
Y_POT=$(max_de "${POT[@]}");  [ "$Y_POT" -lt 20 ] && Y_POT=20

TITULO="GPU Monitoring Dashboard — Aula 14"
SUBTITULO="$TOTAL amostras de $CSV · gerado em $(date '+%Y-%m-%d %H:%M:%S')"

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
  .tag { display:inline-block; font-size:.75rem; color:#94a3b8; margin-top:10px; }
  @media (max-width:900px){ .grid{ grid-template-columns:1fr; } }
</style>
</head>
<body>
  <h1>$TITULO</h1>
  <div class="sub">$SUBTITULO</div>
  <div class="grid">
EOF

gerar_svg "🌡️ Temperatura GPU (°C) — limite 80 °C" "#ef4444" "$Y_TEMP" "${TEMPS[@]}"
gerar_svg "⚙️ Utilização GPU (%)" "#10b981" "$Y_UTIL" "${UTILG[@]}"
gerar_svg "💾 Memória VRAM usada (MB)" "#a855f7" "$Y_VRAM" "${VRAM[@]}"
gerar_svg "⚡ Potência (W)" "#f97316" "$Y_POT" "${POT[@]}"

cat <<EOF
  </div>
  <div class="tag">Abra este arquivo no navegador. Gerado por 3_dashboard.sh sem dependências externas.</div>
</body>
</html>
EOF
} > "$HTML"

echo "Dashboard gerado: $HTML"
echo "Abra no navegador (duplo clique) ou rode: start $HTML"