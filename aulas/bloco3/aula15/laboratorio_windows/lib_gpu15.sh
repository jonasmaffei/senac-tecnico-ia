#!/usr/bin/env bash
# ============================================================================
# lib_gpu15.sh — funções compartilhadas do laboratório de Gestão de Processos
# ----------------------------------------------------------------------------
# Este arquivo NÃO é executado sozinho: é "carregado" pelos outros scripts com:
#     source ./lib_gpu15.sh
#
# Compatível com Git Bash (Windows), WSL e Linux. Junta três responsabilidades:
#   1. LOCK  — exclusão mútua portable (flock quando existe, senão mkdir).
#   2. GPU   — leitura de processos/utilização da GPU (AMD/Windows, NVIDIA ou simulado).
#   3. FS    — pastas de trabalho (fila, locks, logs) dentro de ./reports.
#
# IMPORTANTE (Windows): o Git Bash NÃO tem o comando flock nem nvidia-smi.
# Por isso o lock usa a operação atômica `mkdir` (que é universal) e a GPU é
# lida pelos contadores de desempenho do Windows via PowerShell inline (sem .ps1).
# ============================================================================

# Força o fuso de Brasília (BRT, UTC-3). Usamos "BRT3" e não "America/Sao_Paulo"
# porque o Git Bash do Windows não traz a base tzdata completa.
export TZ="BRT3"

# ---------------------------------------------------------------------------
# PASTAS DE TRABALHO (tudo dentro de ./reports, para não sujar a raiz)
# ---------------------------------------------------------------------------
export DIR_RELATORIOS="${DIR_RELATORIOS:-./reports}"
export DIR_FILA="${DIR_FILA:-$DIR_RELATORIOS/fila}"
export DIR_LOCKS="${DIR_LOCKS:-$DIR_RELATORIOS/locks}"
export LOG_FILA="${LOG_FILA:-$DIR_RELATORIOS/fila.log}"

preparar_dirs() {
    mkdir -p "$DIR_RELATORIOS" "$DIR_FILA" "$DIR_LOCKS"
}

# ---------------------------------------------------------------------------
# DETECÇÃO DE BACKEND DE GPU
# ---------------------------------------------------------------------------
BACKEND="simulado"

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
fi

nome_backend() {
    case "$BACKEND" in
        nvidia)      echo "NVIDIA (nvidia-smi)" ;;
        amd_linux)   echo "AMD ROCm (rocm-smi)" ;;
        amd_windows) echo "AMD no Windows (contadores de desempenho)" ;;
        *)           echo "simulado" ;;
    esac
}

aviso_backend() {
    echo ">> Backend de GPU: $(nome_backend)"
    if [ "$BACKEND" = "simulado" ]; then
        echo "   Nenhuma GPU detectada — usando dados SIMULADOS."
    fi
}

# ===========================================================================
# LOCK PORTÁVEL — exclusão mútua
# ---------------------------------------------------------------------------
# O lock é um DIRETÓRIO. Criar diretório é uma operação ATÔMICA no sistema de
# arquivos: se dois processos tentam ao mesmo tempo, só um consegue. É o mesmo
# princípio do flock -x, mas funciona também no Git Bash do Windows.
#
# Dentro do diretório-guarda guardamos o arquivo "pid" com o PID dono do lock.
# Se o dono morreu (job interrompido), o lock fica obsoleto e é limpo.
# ===========================================================================

# Tenta adquirir o lock. Devolve 0 se conseguiu, 1 se já estava ocupado.
# NÃO espera (non-blocking), igual ao `flock -n`.
lock_tentar() {
    local nome="${1:-gpu}"
    local dir="$DIR_LOCKS/${nome}.lock"
    if mkdir "$dir" 2>/dev/null; then
        echo "$$" > "$dir/pid"
        date +"%Y-%m-%d %H:%M:%S" > "$dir/inicio"
        return 0
    fi
    return 1
}

# Remove um lock obsoleto (dono já morreu). Devolve 0 se removeu algo.
lock_limpar_obsoleto() {
    local nome="${1:-gpu}"
    local dir="$DIR_LOCKS/${nome}.lock"
    [ -d "$dir" ] || return 1
    local dono
    dono=$(cat "$dir/pid" 2>/dev/null || echo "")
    # kill -0 testa se o processo ainda existe sem enviar sinal.
    if [ -n "$dono" ] && kill -0 "$dono" 2>/dev/null; then
        return 1   # dono vivo: o lock é legítimo
    fi
    echo "[$(date '+%H:%M:%S')] Lock obsoleto de PID '${dono:-?}' removido." >&2
    rm -rf "$dir"
    return 0
}

# Libera o lock (só se formos o dono).
lock_liberar() {
    local nome="${1:-gpu}"
    # Versão flock: o descritor 200 é fechado, liberando o lock automaticamente.
    if command -v flock >/dev/null 2>&1; then
        exec 200>&- 2>/dev/null || true
        rm -f "$DIR_LOCKS/${nome}.pid"
        return 0
    fi
    # Versão por diretório
    local dir="$DIR_LOCKS/${nome}.lock"
    local dono
    dono=$(cat "$dir/pid" 2>/dev/null || echo "")
    if [ "$dono" = "$$" ]; then
        rm -rf "$dir"
    fi
}

# Adquire o lock, esperando a vez. Timeout opcional em segundos (0 = infinito).
# Uso: lock_adquirir "gpu" [timeout_s]
#
# Onde existe `flock` (Linux/WSL), usamos o próprio; no Git Bash do Windows,
# caímos no lock por diretório (mkdir atômico). Ambos bloqueiam até conseguir.
lock_adquirir() {
    local nome="${1:-gpu}"
    local timeout="${2:-0}"

    if command -v flock >/dev/null 2>&1; then
        # Abre o descritor de arquivo 200 apontando para o arquivo de lock e
        # pede o lock exclusivo. Como o `exec` roda no shell atual, o descritor
        # permanece aberto e o lock é mantido até o script terminar.
        local arq="$DIR_LOCKS/${nome}.flock"
        exec 200>"$arq"
        if [ "$timeout" -gt 0 ]; then
            flock -x -w "$timeout" 200 || return 1
        else
            flock -x 200 || return 1
        fi
        echo "$$" > "$DIR_LOCKS/${nome}.pid"
        return 0
    fi

    # Fallback portátil (Windows/Git Bash): lock por diretório + limpeza de órfãos
    local inicio
    inicio=$(date +%s)
    while true; do
        if lock_tentar "$nome"; then
            return 0
        fi
        lock_limpar_obsoleto "$nome" || true
        if [ "$timeout" -gt 0 ] && [ $(( $(date +%s) - inicio )) -ge "$timeout" ]; then
            echo "Timeout ao esperar o lock '$nome' (${timeout}s)." >&2
            return 1
        fi
        sleep 1
    done
}

# ===========================================================================
# LEITURA DA GPU
# ===========================================================================

# Processos usando a GPU: devolve linhas "pid|usuario|nome|vram_mb|util_pct".
listar_processos_gpu() {
    case "$BACKEND" in
        nvidia)      _proc_nvidia ;;
        amd_windows) _proc_amd_windows ;;
        amd_linux)   _proc_amd_linux ;;
        *)           _proc_simulado ;;
    esac
}

_proc_nvidia() {
    local smi="nvidia-smi"
    command -v nvidia-smi >/dev/null 2>&1 || smi="nvidia-smi.exe"
    "$smi" --query-compute-apps=pid,process_name,used_gpu_memory \
           --format=csv,noheader,nounits 2>/dev/null | \
    while IFS=',' read -r pid nome mem; do
        pid=$(printf '%s' "$pid" | tr -d ' ')
        nome=$(printf '%s' "$nome" | sed 's/^ *//; s/ *$//')
        mem=$(printf '%s' "$mem" | tr -d ' ')
        [ -z "$pid" ] && continue
        echo "$pid|?|$nome|$mem|?"
    done
}

_proc_amd_windows() {
    local ps="powershell.exe"
    command -v powershell.exe >/dev/null 2>&1 || ps="powershell"

    local script_ps
    script_ps='
$ErrorActionPreference = "SilentlyContinue"
$vram = @{}
$m = Get-CimInstance Win32_PerfFormattedData_GPUPerformanceCounters_GPUAdapterMemory
# Mapa pid -> VRAM dedicada usada (quando disponivel)
$eng = Get-CimInstance Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine
$eng | Where-Object { $_.Name -match "pid_(\d+)" -and $_.Name -like "*engtype_3D*" -and $_.UtilizationPercentage -gt 0 } | ForEach-Object {
    $procId = [regex]::Match($_.Name, "pid_(\d+)").Groups[1].Value
    $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
    if ($proc) {
        Write-Output "$procId|$env:USERNAME|$($proc.ProcessName)|N/A|$($_.UtilizationPercentage)"
    }
}
'
    local enc
    enc=$(printf '%s' "$script_ps" | iconv -f UTF-8 -t UTF-16LE 2>/dev/null | base64 | tr -d '\n')
    if [ -z "$enc" ]; then return 0; fi
    "$ps" -NoProfile -EncodedCommand "$enc" 2>/dev/null | tr -d '\r'
}

_proc_amd_linux() {
    # rocm-smi (ROCm <= 5) lista os PIDs; a VRAM por processo não é trivial.
    rocm-smi --showpids 2>/dev/null | awk '/ /{print $1"|?|AMD|N/A|?"}' | head -20
}

_proc_simulado() {
    # Descobre por conta própria quem está segurando o lock e mostra esse PID.
    local dir="$DIR_LOCKS/gpu.lock"
    if [ -d "$dir" ]; then
        local dono
        dono=$(cat "$dir/pid" 2>/dev/null || echo "?")
        echo "$dono|$USER|python(treino simulado)|N/A|95"
    fi
}

# Resumo por GPU/placa: devolve "gpu|util|vram_usada|vram_total"
resumo_gpu() {
    case "$BACKEND" in
        nvidia)      _resumo_nvidia ;;
        amd_windows) _resumo_amd_windows ;;
        amd_linux)   _resumo_amd_linux ;;
        *)           _resumo_simulado ;;
    esac
}

_resumo_nvidia() {
    local smi="nvidia-smi"
    command -v nvidia-smi >/dev/null 2>&1 || smi="nvidia-smi.exe"
    "$smi" --query-gpu=index,name,utilization.gpu,memory.used,memory.total \
           --format=csv,noheader,nounits 2>/dev/null | \
    awk -F',' '{print $1"|"$3"|"$4"|"$5}'
}

_resumo_amd_windows() {
    local ps="powershell.exe"
    command -v powershell.exe >/dev/null 2>&1 || ps="powershell"

    local script_ps
    script_ps='
$ErrorActionPreference = "SilentlyContinue"
$util = 0
$e = Get-CimInstance Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine
if ($e) {
    $s = ($e | Where-Object { $_.Name -like "*engtype_3D*" } | Measure-Object UtilizationPercentage -Sum).Sum
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
Write-Output "0|$util|$mem|$tot"
'
    local enc
    enc=$(printf '%s' "$script_ps" | iconv -f UTF-8 -t UTF-16LE 2>/dev/null | base64 | tr -d '\n')
    [ -z "$enc" ] && return 0
    "$ps" -NoProfile -EncodedCommand "$enc" 2>/dev/null | tr -d '\r'
}

_resumo_amd_linux() {
    # Formato simples a partir do rocm-smi --csv
    rocm-smi --showuse --showmeminfo vram --csv 2>/dev/null | awk -F',' 'NR>1 {
        gsub(/[^0-9.]/,"",$3); print $1"|"$3"|N/A|N/A"
    }'
}

_resumo_simulado() {
    # Gera um resumo estável para a aula funcionar sem GPU.
    local util=0
    if [ -d "$DIR_LOCKS/gpu.lock" ]; then util=87; else util=3; fi
    echo "0|$util|2048|12272"
}
