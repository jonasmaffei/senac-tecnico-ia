# mapear_conexoes_pi.py — encontra onde a GPU ajuda no Projeto Integrador (Aula 24)
# Uso: python mapear_conexoes_pi.py [caminho_do_pi]

import os
import re
import sys
from pathlib import Path

PADROES = {
    "Loop sobre imagens/arquivos": r"for .* in .*(imagens?|arquivos?|images?|files?)",
    "Operacoes numpy pesadas":     r"np\.(dot|matmul|linalg|fft|einsum)",
    "Carregamento de modelo":      r"(load_model|from_pretrained|pickle\.load|joblib\.load)",
    "Loop de treino/inferencia":   r"for .*(epoch|batch|step)|model\.predict|\.forward",
}

PLANO = {
    "visao":            "AMP + DataLoader multi-worker + transfer learning (ResNet/ViT)",
    "pnl":              "gradient checkpointing + accumulation + tokenizacao paralela",
    "series_temporais": "LSTM/Transformer na GPU + janela vetorizada",
}


def mapear(raiz="."):
    achados = []
    for caminho in Path(raiz).rglob("*.py"):
        if any(p in str(caminho) for p in (".venv", "node_modules", "__pycache__")):
            continue
        texto = caminho.read_text(errors="ignore")
        for desc, padrao in PADROES.items():
            n = len(re.findall(padrao, texto, re.I))
            if n:
                achados.append((str(caminho), desc, n))
    return achados


def main():
    raiz = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"Analisando: {os.path.abspath(raiz)}\n")

    achados = mapear(raiz)
    if not achados:
        print("Nenhum candidato obvio encontrado. Procure loops de processamento sem GPU.")
    else:
        for caminho, desc, n in achados:
            print(f"  {desc}: {caminho} ({n}x)")

    print("\n=== Plano de ação por domínio ===")
    for dominio, acao in PLANO.items():
        print(f"  {dominio:<18} -> {acao}")


if __name__ == "__main__":
    main()
