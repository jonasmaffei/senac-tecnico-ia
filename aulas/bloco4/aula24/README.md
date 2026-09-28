# 🔗 Aula 24 — Conexão com o Projeto Integrador

**Objetivo:** conectar os aprendizados da UC ao **Projeto Integrador** — identificar onde a
GPU acelera o PI e propor um plano de ação.

> 🧭 **Bloco 4 — Projeto Final.** Última aula da UC.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula24.html`](apresentacao_aula24.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`scripts/mapear_conexoes_pi.py`](scripts/mapear_conexoes_pi.py) | Encontra candidatos a GPU no repositório do PI + plano por domínio |
| [`atividade.md`](atividade.md) | Roteiro e entregas finais |

---

## 🚀 Como usar

```bash
cd aulas/bloco4/aula24/scripts
python mapear_conexoes_pi.py /caminho/do/pi
```

> ℹ️ O **PI é uma pesquisa** e não exige código — a GPU entra como complemento opcional.

---

## 🔑 Conceitos-chave

- **Mapear conexões** — achar loops, `np.dot` e modelos em CPU.
- **Plano por domínio** — visão, PNL ou séries temporais.
- **W&B no PI** — rastrear experimentos integrados.

---

## 🔀 Outra trilha: pesquisa (sem código)

A conexão com o PI vale para as **duas trilhas**: aponte onde a aceleração por GPU ajudaria o
Projeto Integrador e justifique com base na sua pesquisa ou no seu experimento.


## 📌 Entregas finais da UC

**Trilha de código:**
1. Repositório do projeto com README e `requirements.txt`.
2. Relatório final (PNG) no repositório.
3. Monitoramento com log CSV de um treino completo.
4. Documento com **3 conexões** GPU ↔ PI.

**Trilha de pesquisa (sem código):**
1. Trabalho de pesquisa (relatório ou slides) com problema, alternativas e recomendação.
2. Referências bibliográficas e declaração de uso de IA.
3. Documento com **3 conexões** GPU ↔ PI.
