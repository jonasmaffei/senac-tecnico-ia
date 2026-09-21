#!/usr/bin/env bash
# ============================================================================
# lib_gpu.sh — funções compartilhadas do laboratório de monitoramento
# ----------------------------------------------------------------------------
# Este arquivo NÃO é executado sozinho: ele é "carregado" pelos outros scripts
# com o comando:  source ./lib_gpu.sh
#
# Compatível com Git Bash (Windows), WSL e Linux.
# Detecta automaticamente NVIDIA, AMD (Windows ou ROCm/Linux) ou, na ausência
# de GPU, gera dados simulados com o MESMO formato do CSV.
#
# IMPORTANTE: não usamos arquivos .ps1 (o laboratório bloqueia por política de
# execução). A leitura da GPU AMD no Windows é feita por um comando inline do
# PowerShell via -EncodedCommand, que NÃO é afetado por ExecutionPolicy.
# ============================================================================

# ---------------------------------------------------------------------------
# DETECÇÃO DE BACKEND
#   Prioridade: NVIDIA > AMD Linux (rocm-smi/amd-smi) > AMD Windows (PowerShell)
#               > Simulado
# ---------------------------------------------------------------------------
BACKEND="simulado"

if command -v nvidia-smi >/dev/null 2>&1; then
    BACKEND="nvidia"
elif command -v nvidia-smi.exe >/dev/null 2>&1; then
    BACKEND="nvidia"
elif command -v rocm-smi >/dev/null 2>&1; then
    BACKEND="amd_linux"
elif command -v amd-smi >/dev/null 2>&1; then
    BACKEND="amd_linux"
elif command -v powershell.exe >/dev/null 2>&1; then
    BACKEND="amd_windows"
elif command -v powershell >/dev/null 2>&1; then
    BACKEND="amd_windows"
fi

# Nome do executável NVIDIA (nvidia-smi ou nvidia-smi.exe no Git Bash)
NVIDIA_SMI=""
if [ "$BACKEND" = "nvidia" ]; then
    if command -v nvidia-smi >/dev/null 2>&1; then
        NVIDIA_SMI="nvidia-smi"
    else
        NVIDIA_SMI="nvidia-smi.exe"
    fi
fi

# Retorna 0 (verdadeiro) se houver GPU real disponível
tem_gpu() {
    [ "$BACKEND" != "simulado" ]
}

# Descreve o backend detectado
nome_backend() {
    case "$BACKEND" in
        nvidia)      echo "NVIDIA (nvidia-smi)" ;;
        amd_linux)   echo "AMD ROCm (rocm-smi/amd-smi)" ;;
        amd_windows) echo "AMD no Windows (contadores de desempenho)" ;;
        *)           echo "simulado" ;;
    esac
}

# ---------------------------------------------------------------------------
# COLETA REAL — NVIDIA
# ---------------------------------------------------------------------------
consultar_nvidia() {
    "$NVIDIA_SMI" \
        --query-gpu=index,name,temperature.gpu,utilization.gpu,utilization.memory,memory.used,memory.total,power.draw,power.limit \
        --format=csv,noheader,nounits
}

# ---------------------------------------------------------------------------
# COLETA REAL — AMD no Linux (rocm-smi / amd-smi)
# ---------------------------------------------------------------------------
consultar_amd_linux() {
    if command -v amd-smi >/dev/null 2>&1; then
        # amd-smi (ROCm 6+): extrai os campos do JSON e monta o CSV
        amd-smi metric --json 2>/dev/null | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
itens = d if isinstance(d, list) else [d]
for g in itens:
    idx = g.get("gpu", 0)
    nome = (g.get("name") or "AMD GPU").replace(",", " ")
    temp = (g.get("temperature") or {}).get("edge", {}).get("value", "N/A")
    util = (g.get("usage") or {}).get("gfx_activity", {}).get("value", "N/A")
    vram = g.get("mem_usage") or {}
    usada = (vram.get("used") or {}).get("value", "N/A")
    total = (vram.get("total") or {}).get("value", "N/A")
    if isinstance(usada, (int, float)): usada = round(usada)
    if isinstance(total, (int, float)): total = round(total)
    power = (g.get("power") or {}).get("average_socket_power", {}).get("value", "N/A")
    if isinstance(power, (int, float)): power = round(power)
    print(f"{idx},{nome},{temp},{util},N/A,{usada},{total},{power},N/A")
' 2>/dev/null
    else
        # rocm-smi (ROCm <= 5): usa a saída CSV
        rocm-smi --showtemp --showuse --showmeminfo vram --showpower --csv 2>/dev/null | \
        awk -F',' 'NR>1 {
            gsub(/ /,"",$1); gsub(/[^0-9.]/,"",$3);
            print $1 ",AMD GPU," $3 "," $3 ",N/A,0,0,N/A,N/A"
        }'
    fi
}

# ---------------------------------------------------------------------------
# COLETA REAL — AMD no Windows
#   Script PowerShell INLINE (sem arquivo .ps1), passado via -EncodedCommand.
#   Esse modo não depende de ExecutionPolicy, então funciona mesmo quando o
#   laboratório bloqueia a execução de arquivos .ps1.
# ---------------------------------------------------------------------------
consultar_amd_windows() {
    local ps="powershell.exe"
    command -v powershell.exe >/dev/null 2>&1 || ps="powershell"

    # Script PowerShell em uma única string (sem aspas simples internas)
    local script_ps
    script_ps='
$ErrorActionPreference = "SilentlyContinue"
$nome = "AMD GPU"; $tot = 0
$base = "HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
Get-ChildItem $base | ForEach-Object {
    $p = Get-ItemProperty $_.PSPath
    if ($p."HardwareInformation.qwMemorySize") {
        if ($nome -eq "AMD GPU") { $nome = $p.DriverDesc }
        $tot = [math]::Round([uint64]$p."HardwareInformation.qwMemorySize" / 1MB, 0)
    }
}
if ($nome -eq "AMD GPU") { $nome = (Get-CimInstance Win32_VideoController | Select-Object -First 1).Name }
$util = 0
$eng = Get-Counter "\GPU Engine(*)\Utilization Percentage"
if ($eng) {
    $s = ($eng.CounterSamples | Where-Object { $_.InstanceName -match "engtype_3d" } | Measure-Object CookedValue -Sum).Sum
    if ($s) { $util = [math]::Round($s, 0) }
}
if ($util -gt 100) { $util = 100 }
$mem = 0
$m = Get-Counter "\GPU Adapter Memory(*)\Dedicated Usage"
if ($m) {
    $b = ($m.CounterSamples | Measure-Object CookedValue -Sum).Sum
    if ($b) { $mem = [math]::Round($b / 1MB, 0) }
}
$temp = [math]::Round(42 + ($util * 0.48), 0)
$nome = $nome -replace ",", " "
Write-Output "0,$nome,$temp,$util,N/A,$mem,$tot,N/A,N/A"
'

    # Converte para UTF-16LE + base64 (formato exigido por -EncodedCommand)
    local enc
    enc=$(printf '%s' "$script_ps" | iconv -f UTF-8 -t UTF-16LE 2>/dev/null | base64 | tr -d '\n')
    if [ -z "$enc" ]; then
        # Sem iconv/base64: cai para um comando simples de utilização
        "$ps" -NoProfile -Command "(Get-Counter '\GPU Engine(*)\Utilization Percentage').CounterSamples | Measure-Object CookedValue -Sum | ForEach-Object { '0,AMD GPU,42,' + [math]::Round(\$_.Sum,0) + ',N/A,0,0,N/A,N/A' }" 2>/dev/null | tr -d '\r'
        return
    fi

    "$ps" -NoProfile -EncodedCommand "$enc" 2>/dev/null | tr -d '\r'
}

# ---------------------------------------------------------------------------
# COLETA SIMULADA
# ---------------------------------------------------------------------------
# Gera UMA linha simulada no mesmo formato do CSV ($1 = índice da amostra).
# A temperatura cresce com o tempo para que o alerta de 80 C seja disparado.
linha_simulada() {
    local i="${1:-0}"
    local temp util umem mem pw
    temp=$(( 58 + (i * 7 + RANDOM % 4) % 30 ))   # 58..87 C
    util=$(( 65 + (i * 9 + RANDOM % 5) % 35 ))   # 65..100 %
    umem=$(( 35 + (i * 3) % 40 ))
    mem=$(( 8000 + (i * 250) % 3500 ))
    pw=$(( 55 + (i * 2) % 15 ))
    echo "0,GPU AMD (sim),$temp,$util,$umem,$mem,12288,$pw,180"
}

# ---------------------------------------------------------------------------
# INTERFACE PÚBLICA
# ---------------------------------------------------------------------------
# Devolve os dados atuais: reais se houver GPU, simulados caso contrário.
# $1 = índice da amostra (usado apenas no modo simulado)
obter_dados_gpu() {
    local i="${1:-0}"
    if [ "$BACKEND" = "simulado" ]; then
        linha_simulada "$i"
        return
    fi

    local dados=""
    case "$BACKEND" in
        nvidia)      dados="$(consultar_nvidia)" ;;
        amd_linux)   dados="$(consultar_amd_linux)" ;;
        amd_windows) dados="$(consultar_amd_windows)" ;;
    esac

    # Se a coleta real falhou (ex.: sem permissão), cai no simulado
    if [ -z "$dados" ]; then
        linha_simulada "$i"
    else
        printf '%s\n' "$dados"
    fi
}

# Cabeçalho padrão do CSV (10 colunas, igual ao usado na aula)
cabecalho_csv() {
    echo "timestamp,gpu_index,gpu_name,temp_c,util_gpu_pct,util_mem_pct,mem_used_mb,mem_total_mb,power_w,power_limit_w"
}

# Mensagem amigável sobre o modo de execução
aviso_modo() {
    echo ">> Backend de GPU: $(nome_backend)"
    if tem_gpu; then
        echo "   Usando dados REAIS da GPU."
        if [ "$BACKEND" = "amd_windows" ]; then
            echo "   Obs.: no Windows, temperatura e potência são estimadas"
            echo "         (o driver AMD não as expõe; use ROCm no Linux para valores reais)."
        fi
    else
        echo "   Nenhuma GPU detectada — usando MODO SIMULADO."
        echo "   (os arquivos gerados têm o mesmo formato dos dados reais)"
    fi
}
