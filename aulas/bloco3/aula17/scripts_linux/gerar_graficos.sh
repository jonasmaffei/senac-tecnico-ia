#!/usr/bin/env bash
# gerar_graficos.sh — Visualizar métricas de GPU com gnuplot
# Requer: sudo apt install gnuplot

CSV_FILE="${1:-gpu_log.csv}"
OUTPUT_PNG="${2:-gpu_dashboard.png}"

if [ ! -f "$CSV_FILE" ]; then
    echo "Erro: arquivo CSV '$CSV_FILE' não encontrado."
    exit 1
fi

if command -v gnuplot &>/dev/null; then
gnuplot <<EOF
set terminal png size 1400,900 enhanced font "Helvetica,11"
set output "$OUTPUT_PNG"
set multiplot layout 2,2 title "GPU Monitoring Dashboard" font "Helvetica,14"

set datafile separator ","
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set format x "%H:%M:%S"
set grid ytics lc rgb "#e0e0e0"
set key top right

# ── Gráfico 1: Temperatura ────────────────────────────────
set title "Temperatura GPU (graus C)"
set ylabel "Temperatura (C)"
set yrange [0:100]
plot "$CSV_FILE" using 1:4 with lines lw 2 lc rgb "#EF4444" title "GPU 0", \
     80 with lines lw 1 lc rgb "#F97316" dt 2 title "Limite 80C"

# ── Gráfico 2: Utilização ─────────────────────────────────
set title "Utilização GPU (%)"
set ylabel "Utilização (%)"
set yrange [0:110]
plot "$CSV_FILE" using 1:5 with lines lw 2 lc rgb "#10B981" title "GPU util", \
     "$CSV_FILE" using 1:6 with lines lw 2 lc rgb "#6366F1" title "Mem util"

# ── Gráfico 3: Memória VRAM ───────────────────────────────
set title "Memória VRAM (MB)"
set ylabel "Memória (MB)"
set yrange [0:*]
plot "$CSV_FILE" using 1:7 with filledcurve y1=0 lc rgb "#7E22CE" \
     fs transparent solid 0.3 title "VRAM used", \
     "$CSV_FILE" using 1:7 with lines lw 2 lc rgb "#7E22CE" notitle

# ── Gráfico 4: Potência ───────────────────────────────────
set title "Potência (W)"
set ylabel "Potência (W)"
set yrange [0:*]
plot "$CSV_FILE" using 1:9 with lines lw 2 lc rgb "#F97316" title "Power draw", \
     "$CSV_FILE" using 1:10 with lines lw 1 lc rgb "#EF4444" dt 2 title "Power limit"

unset multiplot
EOF
echo "Dashboard gnuplot salvo em: $OUTPUT_PNG"
else
    echo "gnuplot não instalado. Usando fallback em Python/matplotlib..."
    python3 - <<EOF
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("$CSV_FILE")
df['timestamp'] = pd.to_datetime(df['timestamp'])

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle("GPU Monitoring Dashboard (Fallback Matplotlib)", fontsize=16)

axes[0, 0].plot(df['timestamp'], df['temp_c'], color='#EF4444', label='Temp C')
axes[0, 0].axhline(y=80, color='#F97316', linestyle='--', label='Limite 80C')
axes[0, 0].set_title("Temperatura GPU (°C)")
axes[0, 0].legend()

axes[0, 1].plot(df['timestamp'], df['util_gpu_pct'], color='#10B981', label='GPU Util %')
axes[0, 1].plot(df['timestamp'], df['util_mem_pct'], color='#6366F1', label='Mem Util %')
axes[0, 1].set_title("Utilização (%)")
axes[0, 1].legend()

axes[1, 0].fill_between(df['timestamp'], df['mem_used_mb'], color='#7E22CE', alpha=0.3, label='VRAM Usada')
axes[1, 0].plot(df['timestamp'], df['mem_used_mb'], color='#7E22CE')
axes[1, 0].set_title("Memória VRAM (MB)")
axes[1, 0].legend()

axes[1, 1].plot(df['timestamp'], df['power_w'], color='#F97316', label='Power Draw')
axes[1, 1].plot(df['timestamp'], df['power_limit_w'], color='#EF4444', linestyle='--', label='Power Limit')
axes[1, 1].set_title("Potência (W)")
axes[1, 1].legend()

plt.tight_layout()
plt.savefig("$OUTPUT_PNG")
print("Dashboard Matplotlib salvo em: $OUTPUT_PNG")
EOF
fi
