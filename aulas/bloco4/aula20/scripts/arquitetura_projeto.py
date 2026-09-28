# arquitetura_projeto.py — template de arquitetura e configuração do Projeto Final
# Uso: python arquitetura_projeto.py
#
# Concentra os hiperparâmetros em uma dataclass e monta o pipeline (modelo,
# otimizador, scheduler e mixed precision). Em modo de referência, roda sem GPU.

from dataclasses import dataclass, asdict


@dataclass
class ConfigProjeto:
    """Configuração central do projeto — altere aqui para personalizar."""
    nome: str = "MeuProjeto"
    dominio: str = "visao"          # visao | pnl | series_temporais
    device: str = "cpu"
    precision: str = "fp16"         # fp32 | fp16 | bf16
    batch_size: int = 32
    epochs: int = 10
    lr: float = 1e-3
    weight_decay: float = 1e-4
    num_classes: int = 10
    input_size: int = 224
    save_dir: str = "./checkpoints"
    log_dir: str = "./logs"


def detectar_device():
    """Retorna 'cuda' se houver GPU PyTorch disponível, senão 'cpu'."""
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"


def descrever_pipeline(cfg):
    """Monta a descrição do pipeline e (se houver PyTorch) cria o modelo."""
    print(f"Projeto '{cfg.nome}' | dominio={cfg.dominio} | device={cfg.device}")
    print(f"Precision: {cfg.precision} | batch={cfg.batch_size} | epochs={cfg.epochs}")

    try:
        import torch
        import torch.nn as nn

        # Exemplo: backbone pré-treinado para visão (transfer learning)
        if cfg.dominio == "visao":
            from torchvision.models import resnet18, ResNet18_Weights
            modelo = resnet18(weights=ResNet18_Weights.DEFAULT)
            modelo.fc = nn.Linear(modelo.fc.in_features, cfg.num_classes)
            desc = "ResNet-18 (pré-treinado ImageNet) + FC ajustada"
        else:
            desc = "Modelo específico do domínio (defina em models/model.py)"
            modelo = None

        if modelo is not None:
            n_params = sum(p.numel() for p in modelo.parameters())
            print(f"Modelo: {desc} | parâmetros: {n_params:,}")

        # Mixed precision só faz sentido em CUDA
        if cfg.device == "cuda" and cfg.precision == "fp16":
            print("Mixed precision: habilitado (torch.cuda.amp.autocast + GradScaler)")
        else:
            print("Mixed precision: desabilitado (sem CUDA) — rodando em modo de referência")

        optimizer = "AdamW(lr=1e-3, weight_decay=1e-4)"
        scheduler = "ReduceLROnPlateau(patience=2, factor=0.5)"
        print(f"Optimizer: {optimizer}")
        print(f"Scheduler: {scheduler}")
    except ImportError:
        print("[Modo de referência] PyTorch não instalado — apenas os conceitos são exibidos.")


def main():
    cfg = ConfigProjeto(nome="DeteccaoDoencas", dominio="visao", num_classes=38)
    cfg.device = detectar_device()
    print("=== Configuração do Projeto ===")
    for k, v in asdict(cfg).items():
        print(f"  {k:<14} = {v}")
    print("\n=== Pipeline ===")
    descrever_pipeline(cfg)


if __name__ == "__main__":
    main()
