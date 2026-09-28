#!/usr/bin/env bash
# ============================================================================
# gerar_graficos.sh — dashboard de 4 gráficos a partir do CSV do monitor_gpu.sh
# ----------------------------------------------------------------------------
# Requer: sudo apt install gnuplot
# Uso: ./gerar_graficos.sh [arquivo_csv]
# ============================================================================
set -euo pipefail

CSV="${1:-gpu_log.csv}"
SAIDA_PNG="${CSV%.csv}.png"

# O bloco entre 'EOF' (com aspas) é enviado literalmente ao gnuplot
gnuplot <<EOF
set terminal png size 1400,900 enhanced font "Helvetica,11"
set output "$SAIDA_PNG"
set multiplot layout 2,2 title "GPU Monitoring Dashboard" font "Helvetica,14"

set datafile separator ","
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set format x "%H:%M"
set grid ytics lc rgb "#e0e0e0"
set key top right
set xtics rotate by -30

# ── Gráfico 1: Temperatura (CSV col 1 = timestamp, col 4 = temp_c) ─────────
set title "Temperatura GPU (graus C)"
set ylabel "Temperatura (C)"
set yrange [0:100]
plot "$CSV" using 1:4 with lines lw 2 lc rgb "#EF4444" title "GPU 0", \
     80 with lines lw 1 lc rgb "#F97316" dt 2 title "Limite 80C"

# ── Gráfico 2: Utilização (col 5 = util_gpu, col 6 = util_mem) ────────────
set title "Utilizacao GPU (%)"
set ylabel "Utilizacao (%)"
set yrange [0:110]
plot "$CSV" using 1:5 with lines lw 2 lc rgb "#10B981" title "GPU util", \
     "$CSV" using 1:6 with lines lw 2 lc rgb "#6366F1" title "Mem util"

# ── Gráfico 3: Memória VRAM (col 7 = mem_used_mb) ─────────────────────────
set title "Memoria VRAM (MB)"
set ylabel "Memoria (MB)"
set yrange [0:*]
plot "$CSV" using 1:7 with filledcurve y1=0 lc rgb "#7E22CE" \
     fs transparent solid 0.3 title "VRAM used", \
     "$CSV" using 1:7 with lines lw 2 lc rgb "#7E22CE" notitle

# ── Gráfico 4: Potência (col 9 = power_w, col 10 = power_limit_w) ─────────
set title "Potencia (W)"
set ylabel "Potencia (W)"
set yrange [0:*]
plot "$CSV" using 1:9  with lines lw 2 lc rgb "#F97316" title "Power draw", \
     "$CSV" using 1:10 with lines lw 1 lc rgb "#EF4444" dt 2 title "Power limit"

unset multiplot
EOF

echo "Dashboard salvo: $SAIDA_PNG"
