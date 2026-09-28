# mapear_conexoes_pi.py — identificar onde a GPU acelera o Projeto Integrador
# Uso: python mapear_conexoes_pi.py [caminho_do_repositorio]

import os
import re
import sys
from pathlib import Path

# Padrões que indicam potencial uso de GPU
PADROES_GPU = {
    "Loop sobre imagens/arquivos": re.compile(r"for .* in .*(imagens?|arquivos?|images?|files?)", re.I),
    "Carregamento de modelo ML":   re.compile(r"(load_model|from_pretrained|pickle\.load|joblib\.load)", re.I),
    "Operacoes numpy intensivas":  re.compile(r"np\.(dot|matmul|linalg|fft|einsum)", re.I),
    "Loop de treinamento":         re.compile(r"for .*(epoch|batch|step|itera)", re.I),
    "Inferencia em loop":          re.compile(r"(model\.predict|\.forward|sess\.run)", re.I),
    "Processamento de video":      re.compile(r"(cv2\.VideoCapture|imageio\.get_reader)", re.I),
}


def analisar_repositorio(raiz="."):
    """Varre arquivos .py do repositório e identifica candidatos a GPU."""
    resultados = {padrao: [] for padrao in PADROES_GPU}

    for caminho in Path(raiz).rglob("*.py"):
        if any(p in str(caminho) for p in [".venv", "node_modules", "__pycache__"]):
            continue
        texto = caminho.read_text(errors="ignore")
        for descricao, regex in PADROES_GPU.items():
            matches = regex.findall(texto)
            if matches:
                try:
                    rel = caminho.relative_to(raiz)
                except ValueError:
                    rel = caminho
                resultados[descricao].append(f"{rel}  ({len(matches)} ocorrencia(s))")
    return resultados


def gerar_relatorio_conexoes(raiz="."):
    print("=" * 60)
    print("  ANALISE DE CONEXOES GPU <-> PI")
    print(f"  Repositorio: {os.path.abspath(raiz)}")
    print("=" * 60)

    resultados = analisar_repositorio(raiz)
    encontrados = 0

    for descricao, arquivos in resultados.items():
        if arquivos:
            encontrados += len(arquivos)
            print(f"\n  {descricao}")
            for arq in arquivos:
                print(f"    -> {arq}")

    if encontrados == 0:
        print("\n  Nenhum padrao obvio encontrado.")
        print("  Dica: procure funcoes que processam dados em loop sem GPU.")
    else:
        print("\n" + "=" * 60)
        print(f"  {encontrados} arquivo(s) com potencial de aceleracao GPU.")
        print("  Priorize os que aparecem em loops de treinamento/inferencia.")
    print("=" * 60)


if __name__ == "__main__":
    raiz = sys.argv[1] if len(sys.argv) > 1 else "."
    gerar_relatorio_conexoes(raiz)
