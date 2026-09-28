# checklist_apresentacao.py — verificar a prontidão do projeto antes do pitch
# Uso: python checklist_apresentacao.py

import glob
import os
import subprocess
from pathlib import Path


def check(descricao, condicao, detalhe=""):
    status = "[OK]  " if condicao else "[FALTA]"
    extra = f"  -> {detalhe}" if detalhe else ""
    print(f"{status} {descricao}{extra}")
    return bool(condicao)


def main():
    print("=" * 55)
    print("  CHECKLIST DE APRESENTACAO")
    print("=" * 55)

    itens = []

    # Repositório
    itens.append(check("README.md existe", Path("README.md").exists()))
    itens.append(check("requirements.txt existe", Path("requirements.txt").exists()))
    itens.append(check(".gitignore configurado", Path(".gitignore").exists()))
    try:
        r = subprocess.run(["git", "log", "--oneline", "-1"], capture_output=True)
        itens.append(check("Historico Git acessivel", r.returncode == 0))
    except FileNotFoundError:
        itens.append(check("Historico Git acessivel", False, "git nao encontrado"))

    # Código
    itens.append(check("train.py existe", Path("training/train.py").exists()))
    itens.append(check("config.py existe", Path("config/config.py").exists()))

    # Logs e dashboard
    logs = glob.glob("logs/monitor/*_*.csv")
    itens.append(check("Log GPU existe", len(logs) > 0, f"{len(logs)} arquivo(s)"))
    dashboards = glob.glob("logs/dashboards/*.png")
    itens.append(check("Dashboard gerado", len(dashboards) > 0, f"{len(dashboards)} imagem(ns)"))
    relatorio = glob.glob("relatorio_final/*.png")
    itens.append(check("Relatorio final gerado", len(relatorio) > 0))

    ok = sum(itens)
    print("=" * 55)
    print(f"  {ok}/{len(itens)} itens prontos", "Pronto para apresentar!" if ok == len(itens) else "Corrija os itens faltantes.")
    print("=" * 55)


if __name__ == "__main__":
    main()
