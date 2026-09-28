# 🔗 Aula 24 — Conexão com o Projeto Integrador (PI)

**Objetivo:** articular os conhecimentos de arquitetura de computadores, GPU e automação
com o **Projeto Integrador** do curso — identificando pontos concretos de aceleração,
integrando a infraestrutura de monitoramento ao repositório do PI e propondo um **plano de
ação** por domínio.

> 🧭 **Bloco 4 — Projeto Final.** Última aula da UC. Conecta as aulas 20–23 ao
> [`projeto-integrador/`](../../projeto-integrador/README.md) (pesquisa).

---

## 🎯 Situação de aprendizagem

A UC chegou ao fim. Você aprendeu a montar servidores com GPU, escrever código CUDA,
automatizar monitoramento e treinar modelos reais. O desafio final é **não deixar esse
conhecimento isolado**: o PI tem componentes de processamento de dados, modelos preditivos
ou análise de imagens que podem ser acelerados com GPU. Nesta aula, o time mapeia essas
conexões, integra a infraestrutura ao repositório do PI e documenta o plano.

> ℹ️ O **PI do curso é uma pesquisa** e **não exige programação**. A aceleração GPU entra
> como **complemento opcional** que sustenta a recomendação.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula24.html`](apresentacao_aula24.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** com explicação + **5 exercícios** |
| [`scripts/`](scripts) | Scripts de referência (`mapear_conexoes_pi.py`, `plano_acao_pi.py`) |
| [`atividade.md`](atividade.md) | Roteiro, discussão e entregas finais da UC |

### Estrutura da aula

```
aula24/
  apresentacao_aula24.html
  README.md
  notebook_colab/aula24_conexao_pi.ipynb
  scripts/mapear_conexoes_pi.py
  scripts/plano_acao_pi.py
  atividade.md
```

---

## 🚀 Como usar

### No Google Colab
Abra `notebook_colab/aula24_conexao_pi.ipynb` pelo **GitHub** no Colab. Ele cria um
mini-repositório de exemplo, encontra os candidatos a GPU e gera o plano de ação.

### Localmente (modo de referência)
```bash
cd aulas/bloco4/aula24/scripts
python mapear_conexoes_pi.py /caminho/do/PI   # lista candidatos a GPU
python plano_acao_pi.py visao                  # plano por domínio
```

---

## 🔑 Conceitos-chave

- **Análise de repositório** — encontrar loops, `np.dot` e modelos em CPU.
- **Integração de scripts** — levar monitor, alertas e dashboards para o PI.
- **Plano de ação por domínio** — visão, NLP ou séries temporais.
- **W&B no PI** — rastrear experimentos integrados à UC.
- **Arquitetura de referência** — estrutura de pastas e pipeline de execução.
- **Transfer learning no PI** — aproveitar modelos pré-treinados.

---

## 📌 Entregas finais da UC

1. **Repositório do projeto GPU** com README, `requirements.txt` e histórico de runs no W&B.
2. **Dashboard final** em PNG commitado no repositório (`logs/dashboards/`).
3. **Monitor integrado** ao `train.py` com log CSV de pelo menos 1 treinamento completo.
4. **Documento de 1 página:** "3 conexões entre GPU/UC e o nosso PI".
5. **Avaliação formativa** respondida individualmente.
