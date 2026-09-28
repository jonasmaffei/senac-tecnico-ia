#!/usr/bin/env bash
# ============================================================================
# lib_gpu06.sh — funções compartilhadas do laboratório de Linux+GPU
# ----------------------------------------------------------------------------
# Este arquivo NÃO é executado sozinho: os outros scripts o carregam com
#     source ./lib_gpu06.sh
#
# Compatível com Git Bash (Windows), WSL e Linux. Ele resolve três coisas:
#   1. Cores de terminal (com fallback quando não há suporte).
#   2. Detecção do backend de GPU (NVIDIA, AMD no Windows, Linux OU simulado).
#   3. Leitura de temperatura/utilização/VRAM da GPU de forma portável.
#
# IMPORTANTE (laboratório Windows/AMD): o Git Bash NÃO tem nvidia-smi/rocm-smi,
# então a GPU AMD é lida pelos CONTADORES DE DESEMPENHO do Windows via
# PowerShell inline (sem arquivo .ps1, que o laboratório bloqueia).
# ============================================================================

# Fuso de Brasília (UTC-3). Usamos "BRT3" porque o Git Bash do Windows não
# traz a base tzdata completa ("America/Sao_Paulo" cairia para GMT).
export TZ="BRT3"

# ---------------------------------------------------------------------------
# CORES (desligadas automaticamente se o terminal não suportar)
# ---------------------------------------------------------------------------
if [ -t 1 ]; then
    VERMELHO=$'\033[0;31m'; VERDE=$'\033[0;32m'; AMARELO=$'\033[1;33m'
    AZUL=$'\033[0;34m'; SEM_COR=$'\033[0m'
else
    VERMELHO=""; VERDE=""; AMARELO=""; AZUL=""; SEM_COR=""
fi

# ---------------------------------------------------------------------------
# DETECÇÃO DE BACKEND
# ---------------------------------------------------------------------------
# Permite forçar o backend para testes:  GPU06_BACKEND=simulado bash 2_status_gpu.sh
# (útil para testar o alerta de temperatura sem nenhuma GPU).
BACKEND="${GPU06_BACKEND:-auto}"

if [ "$BACKEND" = "auto" ]; then
    if command -v nvidia-smi >/dev/null 2>&1; then
        BACKEND="nvidia"
    elif command -v nvidia-smi.exe >/dev/null 2>&1; then
        BACKEND="nvidia"
    elif command -v rocm-smi >/dev/null 2>&1; then
        BACKEND="amd_linux"
    elif command -v powershell.exe >/dev/null 2>&1; then
        BACKEND="amd_windows"
    elif command -v powershell >/dev/null 2>&1; then
        BACKEND="amd_windows"
    else
        BACKEND="simulado"
    fi
fi

nome_backend() {
    case "$BACKEND" in
        nvidia)      echo "NVIDIA (nvidia-smi)" ;;
        amd_linux)   echo "AMD Linux (rocm-smi)" ;;
        amd_windows) echo "AMD no Windows (contadores de desempenho)" ;;
        *)           echo "simulado (nenhuma GPU acessível)" ;;
    esac
}

anunciar_backend() {
    echo "${AZUL}>> Backend de GPU:${SEM_COR} $(nome_backend)"
    if [ "$BACKEND" = "simulado" ]; then
        echo "   Nenhuma GPU detectada — usando dados SIMULADOS no mesmo formato."
    fi
    echo
}

# ---------------------------------------------------------------------------
# LEITURA DA GPU — devolve uma linha por GPU: "gpu|nome|temp|util|vram_usada|vram_total"
# ---------------------------------------------------------------------------
ler_gpu() {
    case "$BACKEND" in
        nvidia)      _gpu_nvidia ;;
        amd_linux)   _gpu_amd_linux ;;
        amd_windows) _gpu_amd_windows ;;
        *)           _gpu_simulado ;;
    esac
}

_gpu_nvidia() {
    local smi="nvidia-smi"
    command -v nvidia-smi >/dev/null 2>&1 || smi="nvidia-smi.exe"
    # Um único comando traz tudo; separamos com '|' para ficar fácil de ler.
    "$smi" --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total \
           --format=csv,noheader,nounits 2>/dev/null | \
    awk -F',' '{gsub(/ /,""); print $1"|"$2"|"$3"|"$4"|"$5"|"$6}'
}

_gpu_amd_linux() {
    # rocm-smi --csv traz uma linha por GPU; extraímos uso e VRAM.
    rocm-smi --showtemp --showuse --showmeminfo vram --csv 2>/dev/null | \
    awk -F',' 'NR>1 {
        gsub(/[^0-9.]/,"",$3); gsub(/[^0-9.]/,"",$4);
        print $1"|AMD GPU|"$3"|"$4"|N/A|N/A
    }'
}

_gpu_amd_windows() {
    # Sem nvidia-smi: lemos os contadores de desempenho do Windows via
    # PowerShell inline. A "temperatura" não é exposta de forma simples no
    # Windows, então mostramos 'N/A' (honesto) em vez de um valor falso.
    local ps="powershell.exe"
    command -v powershell.exe >/dev/null 2>&1 || ps="powershell"

    local script_ps
    script_ps='
$ErrorActionPreference = "SilentlyContinue"
$util = 0
$e = Get-CimInstance Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine
if ($e) {
    $s = ($e | Where-Object { $_.Name -like "*engtype_3D*" } |
          Measure-Object UtilizationPercentage -Sum).Sum
    if ($s) { $util = [math]::Round($s, 0) }
}
if ($util -gt 100) { $util = 100 }
$mem = 0; $tot = 0
$m = Get-CimInstance Win32_PerfFormattedData_GPUPerformanceCounters_GPUAdapterMemory
if ($m) {
    $b = ($m | Measure-Object DedicatedUsage -Sum).Sum
    if ($b) { $mem = [math]::Round($b / 1MB, 0) }
}
$base = "HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
Get-ChildItem $base -ErrorAction SilentlyContinue | ForEach-Object {
    $p = Get-ItemProperty $_.PSPath -ErrorAction SilentlyContinue
    if ($p."HardwareInformation.qwMemorySize") {
        $tot = [math]::Round([uint64]$p."HardwareInformation.qwMemorySize" / 1MB, 0)
    }
}
if ($tot -eq 0) { $tot = "N/A" }
Write-Output "0|AMD GPU (Windows)|N/A|$util|$mem|$tot"
'
    local enc
    enc=$(printf '%s' "$script_ps" | iconv -f UTF-8 -t UTF-16LE 2>/dev/null | base64 | tr -d '\n')
    [ -z "$enc" ] && return 0
    "$ps" -NoProfile -EncodedCommand "$enc" 2>/dev/null | tr -d '\r'
}

_gpu_simulado() {
    # Mesmo formato das GPU reais, para a aula funcionar sem hardware.
    echo "0|GPU simulada (Tesla T4)|54|37|3200|15360"
}

# ---------------------------------------------------------------------------
# INSpeção de hardware (vale para qualquer SO)
# ---------------------------------------------------------------------------
listar_pci_gpu() {
    if command -v lspci >/dev/null 2>&1; then
        lspci 2>/dev/null | grep -iE 'vga|3d|display|nvidia|amd|radeon'
    else
        echo "(lspci não existe no Git Bash — no Linux ele lista a placa no barramento)"
    fi
}
