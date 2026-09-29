# projeto_exemplo.py - exemplo simples de definicao do projeto final (Aula 20)
# Uso: python projeto_exemplo.py
#
# Mostra a configuracao central do projeto e o checklist de prontidao.

from dataclasses import dataclass, asdict


@dataclass
class ConfigProjeto:
    """Configuracao central do projeto - altere para o seu dominio."""
    nome: str = "DeteccaoDoencas"
    dominio: str = "visao"          # visao | pnl | series_temporais
    modelo_base: str = "resnet18"   # backbone pre-treinado
    batch_size: int = 32
    epochs: int = 10
    precision: str = "fp16"         # fp32 | fp16 | bf16
    num_classes: int = 38


CHECKLIST = [
    "Dominio e problema definidos",
    "Dataset escolhido (ex.: PlantVillage)",
    "Modelo base escolhido (transfer learning)",
    "Framework e GPU definidos",
    "Metrica principal e baseline definidos",
    "Repositorio criado",
]


def main():
    cfg = ConfigProjeto()
    print("=== Configuracao do projeto ===")
    for k, v in asdict(cfg).items():
        print(f"  {k:<12} = {v}")

    print("\n=== Checklist de prontidao ===")
    for item in CHECKLIST:
        print(f"  [ ] {item}")
    print("\nMarque todos antes de implementar (Aula 21).")


if __name__ == "__main__":
    main()
