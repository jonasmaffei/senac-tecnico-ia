# 📝 Atividade Prática: Aula 20 — Definição do Projeto Final

---

## 🎯 Situação de Aprendizagem

A empresa organizou um **hackathon interno de 4 semanas**: cada time deve desenvolver
uma solução de IA acelerada por GPU para um problema real. Os times têm acesso a um
servidor com **2× RTX 4090** e ao **Google Colab Pro**. O desafio desta aula é estruturar
o projeto do zero: escolher o domínio, identificar o problema, selecionar o dataset e
planejar a arquitetura — integrando as técnicas de monitoramento e automação aprendidas
nas aulas anteriores.

---

## 🗂️ Roteiro de Execução

Você pode realizar esta atividade no **Google Colab** ou localmente nos **scripts**.

| Ambiente | Onde abrir | Como executar |
| :--- | :--- | :--- |
| **Google Colab** | [`notebook_colab/aula20_definicao_projeto.ipynb`](notebook_colab/aula20_definicao_projeto.ipynb) | Execute as células em sequência |
| **Local (referência)** | [`scripts/`](scripts) | `python arquitetura_projeto.py` e `python checklist_projeto.py` |

---

## 🚀 Parte 1 — Escolher o domínio e o problema

1. Em grupo, escolham o domínio: **visão computacional**, **PNL** ou **séries temporais**.
2. Definam um **problema real** com impacto mensurável (ex.: detecção de doenças em plantas).
3. No notebook, ajustem `MEU_DOMINIO` e criem o `ConfigProjeto` do time.

---

## 📊 Parte 2 — Dataset e viabilidade de VRAM

1. Explorem o dataset sugerido no Hugging Face (ou outro da mesma família).
2. Estimem a **VRAM** necessária com `estimar_vram` para `batch_size` de 16 e 64.
3. Verifiquem se o projeto **cabe** na RTX 4090, na T4 e na V100 do Colab Pro.

---

## 🏗️ Parte 3 — Estrutura do repositório

1. Criem a árvore de pastas: `config/`, `data/`, `models/`, `training/`, `scripts/`,
   `notebooks/` e `checkpoints/`.
2. Adicionem ao `.gitignore`: `checkpoints/` e `data/raw/`.
3. Escrevam um **README** com objetivo, dataset e instruções de reprodução.

---

## ⚙️ Parte 4 — Integração com a automação (Blocos 1–3)

1. Copiem para o `scripts/` do projeto: o monitor de GPU (Aula 14), a fila de jobs
   (Aula 15) e o script de Power Limit (Aula 19).
2. Deixem planejado **como** o monitor rodará junto do `train.py`.

---

## 💬 Parte 5 — Discussão em Grupo (10 min)

Em grupos de 3 a 4 alunos, cada time apresenta o plano (2 min) e recebe feedback:

1. Qual problema vocês escolheram? Por que é relevante e como a GPU acelera a solução?
2. O dataset tem desafios de qualidade (desbalanceamento, ruído, gaps)? Como tratá-los?
3. Qual será o **baseline mais simples** para comparar com o modelo profundo?
4. Em 4 semanas, quantas épocas vocês estimam treinar? Quanta VRAM o modelo usa?

---

## 📌 Parte 6 — Tarefa de Casa (para a Aula 21)

1. Completar o **checklist de prontidão** (`checklist_projeto.py`) com 100% dos itens.
2. Criar o **repositório GitHub** com a estrutura definida e compartilhar o link.
3. Testar que o dataset carrega corretamente no Colab e medir o tempo de carregamento.
4. Implementar o **baseline mais simples** e medir a métrica principal — será o ponto de
   comparação do modelo profundo.
