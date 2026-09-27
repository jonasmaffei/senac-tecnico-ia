# 🤖 Aula 16 — Agentes de Código, GitHub, Contexto, AGENTS.md e Monitoramento Web

**Objetivo:** reconhecer os componentes de um **agente de código** (harness, contexto, skills, RAG, `AGENTS.md`), aplicar o **GitHub** como controle de versão e rede de segurança, e utilizar a **Google Antigravity CLI** (`agy`) para criar uma aplicação de monitoramento web em Python guiada por um arquivo `AGENTS.md`.

---

## 🎯 Situação de Aprendizagem

A startup precisa **acelerar o time de desenvolvimento** mantendo controle de qualidade. Você vai usar um **agente de código no terminal** para criar uma **aplicação de monitoramento de sistema em Python acessível via web**, guiando o agente através de um arquivo de diretrizes (`AGENTS.md`) e salvando o progresso de forma segura no **GitHub**.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula16.html`](apresentacao_aula16.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`atividade.md`](atividade.md) | Tutorial completo de GitHub, guia de Contexto e `AGENTS.md` + Roteiro prático da CLI (`agy`) |
| [`laboratorio_monitoramento/`](laboratorio_monitoramento/) | Laboratório prático com `AGENTS.md` para construção do monitor web em Python |

### Estrutura da aula

```
aula16/
  apresentacao_aula16.html
  README.md
  atividade.md
  laboratorio_monitoramento/
    AGENTS.md
    README.md
```

---

## 🚀 Como Usar

### 1. Assistir à apresentação
Abra [`apresentacao_aula16.html`](apresentacao_aula16.html) com duplo clique no navegador e navegue com `←` / `→`.

### 2. Seguir o roteiro prático
Abra [`atividade.md`](atividade.md) para:
1. Aprender e praticar os comandos básicos de **GitHub** (`clone`, `add`, `commit`, `push`).
2. Entender como a **Janela de Contexto** afeta o desempenho do agente de IA.
3. Entender a estrutura e importância do arquivo **`AGENTS.md`**.
4. Usar a **Antigravity CLI** (`agy`) dentro de `laboratorio_monitoramento/` para construir a aplicação de monitoramento web em Python.

---

## 🔑 Conceitos-chave

- **GitHub para Iniciantes** — repositório remoto, versionamento e rede de segurança contra erros de geração de código.
- **Harness** — a “armação” que faz o modelo **agir**: loop agêntico, ferramentas, contexto e permissões.
- **Contexto & Janela de Contexto** — o volume de dados (prompts, arquivos, histórico) processado pela IA a cada turno.
- **AGENTS.md** — arquivo de memória persistente na raiz do repositório que orienta agentes de IA sobre regras, estrutura e testes.
- **Skills** — pastas de **instruções reutilizáveis** (`.agents/skills/<nome>/SKILL.md`).
- **RAG** — **buscar** o conhecimento certo e **injetar** no contexto antes de responder.
- **Vibe coding** — gerar código por linguagem natural; rápido para prototipar, **arriscado sem verificação humana e Git**.

---

## 💬 Discussão em Grupo

Em grupos de 3–4:

1. Como o arquivo `AGENTS.md` ajuda a padronizar o trabalho de múltiplos agentes ou desenvolvedores no mesmo projeto?
2. Por que o versionamento com **GitHub** é indispensável para evitar desastres em sessões de *vibe coding*?
3. Qual é o impacto do excesso de contexto na qualidade do código gerado por uma IA?

---

## 🔗 Relação com o Curso

- Conecta os blocos de **Automação** e **Versionamento**: integra a prática de Git em [`docs/03_git.md`](../../docs/03_git.md) com o uso de agentes no terminal.
- Mostra como automatizar a criação de scripts de telemetria em Python (vistos na Aula 14) utilizando **instruções declarativas** via `AGENTS.md`.

---

## 🔧 Recursos de Apoio

- Documentação da **Antigravity**: CLI, [Agent Skills](https://antigravity.google/docs/skills) e [Best Practices](https://antigravity.google/docs/cli/best-practices).
- Padrão aberto de **Agent Skills**: <https://agentskills.io/home>.
- `AGENTS.md` do repositório do curso — exemplo real de arquivo de regras para agentes.
