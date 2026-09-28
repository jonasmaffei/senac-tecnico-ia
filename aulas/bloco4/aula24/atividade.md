# 📝 Atividade Prática: Aula 24 — Conexão com o Projeto Integrador (PI)

---

## 🎯 Situação de Aprendizagem

A UC chegou ao fim. Você aprendeu a montar servidores com GPU, escrever código CUDA,
automatizar monitoramento e treinar modelos de IA reais. Agora o desafio é **não deixar esse
conhecimento isolado**: o Projeto Integrador do curso tem componentes de processamento de
dados, modelos preditivos ou análise de imagens que podem ser acelerados com GPU. Nesta aula,
o time mapeia essas conexões, integra a infraestrutura ao repositório do PI e documenta o
plano de ação.

> ℹ️ O PI é uma **pesquisa** e não exige código — a aceleração GPU é um **complemento opcional**.

---

## 🗂️ Roteiro de Execução

| Ambiente | Onde abrir | Como executar |
| :--- | :--- | :--- |
| **Google Colab** | [`notebook_colab/aula24_conexao_pi.ipynb`](notebook_colab/aula24_conexao_pi.ipynb) | Execute as células em sequência |
| **Local (referência)** | [`scripts/`](scripts) | `python mapear_conexoes_pi.py` e `python plano_acao_pi.py` |

---

## 🔍 Parte 1 — Mapear as conexões GPU ↔ PI

1. Rode `mapear_conexoes_pi.py` apontando para o repositório do seu PI.
2. Liste os pontos de alto custo computacional (loops, `np.dot`, modelos em CPU).
3. Priorize os que aparecem em **loops de treinamento/inferência**.

---

## 🧩 Parte 2 — Plano de ação por domínio

1. Gere o plano do seu domínio (`plano_acao_pi.py visao|nlp|series_temporais`).
2. Copie os thresholds sugeridos para o `monitor_treinamento.sh` do PI.

---

## ⚙️ Parte 3 — Integrar a infraestrutura ao PI

1. Crie `scripts/gpu/` no repositório do PI.
2. Copie monitor, alertas, dashboard e relatório das aulas 22–23.
3. Atualize o README do PI com a seção de monitoramento e o `.env.example`.

---

## 📈 Parte 4 — W&B e monitor no treino

1. Inicialize uma run do W&B com tags `"PI"`, `"GPU"` e o domínio.
2. Inicie o monitor de GPU junto do treino (padrão `subprocess.Popen` + `finally`).
3. Cruze as métricas de treino com as métricas de GPU por janela temporal.

---

## 💬 Parte 5 — Discussão em Grupo (10 min)

Cada time apresenta 3 conexões mapeadas (2 min) e recebe feedback:

1. Qual componente do PI mais se beneficia de GPU? Qual o ganho estimado?
2. O repositório do PI tem código numpy/sklearn/torch em CPU que poderia migrar?
3. Como o monitor de GPU pode ajudar especificamente o PI? Que thresholds fazem sentido?
4. Se o PI fosse produção com RTX 4090, quais 3 ajustes de arquitetura maximizariam a GPU?

---

## 🏁 Parte 6 — Entregas finais da UC

1. **Repositório do projeto GPU** com README, `requirements.txt` e histórico de runs no W&B.
2. **Dashboard final** em PNG commitado em `logs/dashboards/`.
3. **Monitor integrado** ao `train.py` com log CSV de pelo menos 1 treinamento completo.
4. **Documento de 1 página:** "3 conexões entre GPU/UC e o nosso PI".
5. **Slide de proposta:** "Como aplicaríamos GPU/automação no nosso PI?"
6. **Avaliação formativa** respondida individualmente.
