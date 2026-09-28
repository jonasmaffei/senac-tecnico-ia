# otimizacao_memoria.py — calcular batch efetivo, acumulação e VRAM
# Uso: python otimizacao_memoria.py

# VRAM aproximada por amostra, por domínio (MB) — referência didática
PERFIL_VRAM_MB = {"visao": 100.0, "pnl": 40.0, "series_temporais": 10.0}

# GPUs de referência (MB)
GPUS = {"T4 (Colab)": 15360, "V100 (Colab Pro)": 16384, "RTX 4090": 24576}


def estimar_vram_mb(batch_size, dominio="visao", amp=True, overhead=1500):
    """Estimativa de VRAM: overhead do runtime + ativações por amostra."""
    por_amostra = PERFIL_VRAM_MB.get(dominio, 6.0)
    fator = 0.5 if amp else 1.0
    return overhead + batch_size * por_amostra * fator


def calcular_acumulacao(batch_real, batch_efetivo_desejado):
    """Steps de acumulação para atingir o batch efetivo desejado."""
    if batch_real <= 0:
        return None
    return max(1, batch_efetivo_desejado // batch_real)


def maior_batch_que_cabe(dominio, vram_mb, amp=True, passo=8, limite=512):
    """Maior batch (múltiplo de `passo`) que cabe na VRAM informada."""
    melhor = passo
    for bs in range(passo, limite + 1, passo):
        if estimar_vram_mb(bs, dominio, amp) < vram_mb:
            melhor = bs
        else:
            break
    return melhor


def main():
    print("=== Técnicas de otimização de memória ===")
    tecnicas = [
        ("Mixed Precision (fp16)", "~50% menos VRAM nas ativações", "torch.amp.autocast()"),
        ("Gradient Checkpointing", "~60% menos VRAM no backward", "model.gradient_checkpointing_enable()"),
        ("set_to_none=True", "libera buffers de gradiente", "optimizer.zero_grad(set_to_none=True)"),
        ("no_grad() na validação", "sem grafo de autograd", "@torch.no_grad()"),
        ("Gradient Accumulation", "batch efetivo maior sem OOM", "loss = loss / n_steps"),
    ]
    for nome, efeito, api in tecnicas:
        print(f"  - {nome:<28} -> {efeito:<32} | {api}")

    print("\n=== Batch máximo por GPU (domínio: visão, AMP) ===")
    for gpu, vram in GPUS.items():
        bs = maior_batch_que_cabe("visao", vram, amp=True)
        print(f"  {gpu:<18} (VRAM {vram//1024} GB): batch máximo ~ {bs}")

    print("\n=== Acumulação para batch efetivo 128 ===")
    for real in (16, 32, 64):
        n = calcular_acumulacao(real, 128)
        print(f"  batch_real={real:<3} -> {n} steps")


if __name__ == "__main__":
    main()
