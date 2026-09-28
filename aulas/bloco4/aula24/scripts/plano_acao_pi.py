# plano_acao_pi.py — gerar o plano de ação de conexão GPU <-> PI por domínio
# Uso: python plano_acao_pi.py [visao|nlp|series_temporais]

import sys

PLANOS_POR_DOMINIO = {
    "visao": {
        "titulo": "Visao Computacional no PI",
        "aceleracoes": [
            ("DataLoader multi-worker", "num_workers=4, pin_memory=True - reduz gargalo de I/O em 3-8x"),
            ("Mixed Precision (AMP)", "torch.amp.autocast + GradScaler - ate 2x mais rapido"),
            ("Batch size maior", "RTX 4090: 64-128 imagens - mais throughput e gradientes estaveis"),
            ("Transfer Learning", "ResNet/ViT pre-treinado + fine-tuning - converge ~10x mais rapido"),
        ],
        "monitor_config": {"intervalo": 10, "max_temp": 83, "max_vram_pct": 88},
    },
    "nlp": {
        "titulo": "NLP / Texto no PI",
        "aceleracoes": [
            ("Gradient checkpointing", "economiza 30-40% de VRAM em BERT/GPT-2"),
            ("Gradient accumulation", "simula batch 256 com VRAM de batch 32"),
            ("Tokenizacao paralela", "tokenizer(batch, num_proc=4) - pre-processamento fora da GPU"),
            ("FP16 inference", "model.half() - 2x mais rapido, menos VRAM"),
        ],
        "monitor_config": {"intervalo": 15, "max_temp": 80, "max_vram_pct": 92},
    },
    "series_temporais": {
        "titulo": "Series Temporais no PI",
        "aceleracoes": [
            ("LSTM/Transformer na GPU", "sequencias em .cuda() - 20-50x mais rapido que CPU"),
            ("Janela vetorizada", "torch.unfold - evita loop Python"),
            ("Normalizacao na GPU", "mean/std no tensor CUDA - sem transferencia"),
            ("Workers persistentes", "persistent_workers=True - evita recriar workers por epoca"),
        ],
        "monitor_config": {"intervalo": 20, "max_temp": 82, "max_vram_pct": 85},
    },
}


def gerar_plano(dominio):
    plano = PLANOS_POR_DOMINIO.get(dominio)
    if not plano:
        print(f"Dominio '{dominio}' nao reconhecido.")
        print(f"Opcoes: {', '.join(PLANOS_POR_DOMINIO)}")
        return

    print("=" * 60)
    print(f"  PLANO DE ACAO - {plano['titulo']}")
    print("=" * 60)
    print("\nAceleracoes recomendadas (por prioridade):\n")
    for i, (tecnica, descricao) in enumerate(plano["aceleracoes"], 1):
        print(f"  {i}. {tecnica}")
        print(f"     -> {descricao}\n")

    cfg = plano["monitor_config"]
    print("Configuracao do monitor sugerida para este dominio:")
    print(f"  intervalo={cfg['intervalo']}s | max_temp={cfg['max_temp']}C | max_vram={cfg['max_vram_pct']}%")
    print("  Copie estes valores para o monitor_treinamento.sh do seu PI.")
    print("=" * 60)


def main():
    dominio = sys.argv[1] if len(sys.argv) > 1 else "visao"
    gerar_plano(dominio)
    if len(sys.argv) == 1:
        print("\nDica: rode para os outros dominios:")
        print("  python plano_acao_pi.py nlp")
        print("  python plano_acao_pi.py series_temporais")


if __name__ == "__main__":
    main()
