# pipeline_treinamento.py — pipeline de treino otimizado para GPU (modo de referência)
# Uso: python pipeline_treinamento.py
#
# Demonstra: DataLoader otimizado, mixed precision (autocast + GradScaler),
# zero_grad(set_to_none=True) e transferência non_blocking. Sem GPU, imprime
# o pipeline e os conceitos.

import sys


def descrever_dataloader():
    print("=== DataLoader otimizado ===")
    print("  num_workers=4          -> paraleliza a leitura no CPU")
    print("  pin_memory=True        -> memória fixada (transferência rápida)")
    print("  prefetch_factor=2      -> pré-carrega 2 batches por worker")
    print("  persistent_workers=True-> mantém workers vivos entre épocas")
    print("  val: batch_size*2      -> sem backprop, cabe mais na VRAM")


def descrever_epoca(usar_amp=True):
    print(f"\n=== Época {'AMP (fp16)' if usar_amp else 'FP32'} ===")
    passos = [
        "X, y = X.to(device, non_blocking=True), y.to(device, non_blocking=True)",
        "optimizer.zero_grad(set_to_none=True)",
    ]
    if usar_amp:
        passos += [
            "with autocast(): logits = model(X); loss = criterion(logits, y)",
            "scaler.scale(loss).backward()",
            "scaler.unscale_(optimizer); clip_grad_norm_(..., 1.0)",
            "scaler.step(optimizer); scaler.update()",
        ]
    else:
        passos += [
            "logits = model(X); loss = criterion(logits, y)",
            "loss.backward()",
            "optimizer.step()",
        ]
    for i, p in enumerate(passos, 1):
        print(f"  {i}. {p}")


def main():
    usar_amp = True
    try:
        import torch
        usar_amp = torch.cuda.is_available() and hasattr(torch, "amp")
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("Sem GPU: modo de referência (apenas conceitos).")
    except ImportError:
        print("PyTorch não instalado: modo de referência (apenas conceitos).")

    descrever_dataloader()
    descrever_epoca(usar_amp=usar_amp)
    descrever_epoca(usar_amp=False)
    print("\nResumo: AMP reduz VRAM (~45%) e acelera o treino (1.5-2.5x) sem perda relevante de precisão.")


if __name__ == "__main__":
    sys.exit(main())
