# treino_otimizado.py — exemplo de treino otimizado para GPU (Aula 21)
# Uso: python treino_otimizado.py
#
# Mostra o essencial: DataLoader otimizado + mixed precision (AMP).
# Com GPU treina de verdade; sem GPU, imprime os passos (modo de referência).

try:
    import torch
    import torch.nn as nn
    TEM_TORCH = True
except ImportError:
    TEM_TORCH = False


def treinar_epoca(model, loader, criterion, optimizer, scaler, device):
    """Uma época com mixed precision (fp16) e DataLoader otimizado."""
    model.train()
    for X, y in loader:
        X, y = X.to(device, non_blocking=True), y.to(device, non_blocking=True)
        optimizer.zero_grad(set_to_none=True)          # mais econômico
        with torch.amp.autocast("cuda"):               # forward em fp16
            loss = criterion(model(X), y)
        scaler.scale(loss).backward()                  # evita underflow
        scaler.step(optimizer)
        scaler.update()


def main():
    if not TEM_TORCH or not torch.cuda.is_available():
        print("Sem GPU/PyTorch: modo de referência.\n")
        print("Pontos-chave do pipeline otimizado:")
        print("  1. DataLoader(num_workers=4, pin_memory=True)")
        print("  2. X.to(device, non_blocking=True)")
        print("  3. optimizer.zero_grad(set_to_none=True)")
        print("  4. with autocast(): ...     # mixed precision (fp16)")
        print("  5. scaler.scale(loss).backward(); scaler.step(); scaler.update()")
        print("\nGanho típico de AMP: ~2x mais rápido e ~45% menos VRAM.")
        return

    from torch.utils.data import DataLoader, TensorDataset
    device = "cuda"
    model = nn.Sequential(nn.Flatten(), nn.Linear(784, 10)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    scaler = torch.amp.GradScaler("cuda")

    # batch sintético só para demonstrar
    dados = TensorDataset(torch.randn(256, 1, 28, 28), torch.randint(0, 10, (256,)))
    loader = DataLoader(dados, batch_size=32, num_workers=2, pin_memory=True)

    print(f"GPU: {torch.cuda.get_device_name(0)} | treinando 1 época de exemplo...")
    treinar_epoca(model, loader, criterion, optimizer, scaler, device)
    print("Época concluída com AMP.")


if __name__ == "__main__":
    main()
