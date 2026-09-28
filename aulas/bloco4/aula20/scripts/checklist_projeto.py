# checklist_projeto.py — verificar a prontidão do projeto para o hackathon
# Uso: python checklist_projeto.py

checklist = {
    "1. Definição do problema": {
        "Domínio escolhido (visão / PNL / séries temporais)": False,
        "Problema real identificado com impacto mensurável": False,
        "Dataset público disponível e compatível com Colab": False,
    },
    "2. Arquitetura técnica": {
        "Framework definido (PyTorch / TensorFlow)": False,
        "Modelo base escolhido (pré-treinado ou custom)": False,
        "Estratégia de GPU: CUDA / ROCm / Colab T4": False,
        "Precision: fp16 / bf16 habilitado para VRAM": False,
    },
    "3. Automação e monitoramento": {
        "Script de monitoramento GPU integrado (Aula 14)": False,
        "Fila de jobs configurada se múltiplas GPUs": False,
        "W&B ou MLflow configurado para logging": False,
    },
    "4. Repositório e documentação": {
        "Estrutura de pastas criada": False,
        "README com objetivo e instruções de reprodução": False,
        "requirements.txt completo": False,
    },
    "5. Critérios de avaliação": {
        "Métrica principal definida (acc / F1 / RMSE)": False,
        "Baseline simples implementado para comparação": False,
        "Meta de desempenho estabelecida": False,
    },
}


def main():
    for categoria, itens in checklist.items():
        concluidos = sum(itens.values())
        total = len(itens)
        print(f"\n{categoria} [{concluidos}/{total}]")
        for item, status in itens.items():
            print(f"  {'[x]' if status else '[ ]'} {item}")

    total_geral = sum(len(v) for v in checklist.values())
    pct = sum(v for itens in checklist.values() for v in itens.values()) / total_geral
    print(f"\nProntidão geral: {pct*100:.0f}%")
    if pct == 1.0:
        print("Projeto pronto para a Aula 21!")
    else:
        print("Marque todos os itens antes de começar a implementação.")


if __name__ == "__main__":
    main()
