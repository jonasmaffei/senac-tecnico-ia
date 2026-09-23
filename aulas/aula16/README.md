# 🤖 Aula 16 — Agentes de Código: Harness, RAG, Skills e Vibe Coding

**Objetivo:** reconhecer os componentes de um **agente de código** (harness, contexto, skills,
RAG) e aplicar a **Google Antigravity CLI** (`agy`) numa prática, com postura crítica sobre
**vibe coding**.

---

## 🎯 Situação de aprendizagem

A startup precisa **acelerar o time de desenvolvimento**. Você vai usar um **agente de código no
terminal** para criar algo real — e precisa entender **o que ele é**, **o que ele sabe** e
**o que ele pode fazer** antes de confiar no resultado.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula16.html`](apresentacao_aula16.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`atividade.md`](atividade.md) | Roteiro prático da CLI (`agy`) + discussão + tarefa de casa |

### Estrutura da aula

```
aula16/
  apresentacao_aula16.html
  README.md
  atividade.md
```

---

## 🚀 Como usar

### 1. Assistir à apresentação

Abra [`apresentacao_aula16.html`](apresentacao_aula16.html) com duplo clique no navegador e
navegue com `←` / `→`.

### 2. Praticar com a CLI

Siga o roteiro em [`atividade.md`](atividade.md). Você vai instalar a **Antigravity CLI**,
abrir um projeto e pedir ao agente uma tarefa simples — **revisando cada mudança** com `/diff`.

---

## 🔑 Conceitos-chave

- **Harness** — a “armação” que faz o modelo **agir**: loop, ferramentas, contexto e permissões.
- **Agente** — persegue um objetivo em passos: **observar → planejar → agir → verificar**.
- **Ferramentas (tools)** — ler/editar arquivos, rodar comandos, buscar no código/web.
- **Skills** — pastas de **instruções reutilizáveis** (`.agents/skills/<nome>/SKILL.md`).
- **RAG** — **buscar** o conhecimento certo e **injetar** no contexto antes de responder.
- **Vibe coding** — gerar código por linguagem natural; rápido para prototipar, **arriscado sem
  verificação**.

> **Regra de ouro:** o agente **acelera**, mas **você responde** pelo resultado. Sem
> verificação (testes, build, leitura do diff), não vale.

---

## 💬 Discussão em grupo

Em grupos de 3–4:

1. Onde o **harness** termina e a **responsabilidade do engenheiro** começa?
2. Quando o **RAG** resolve mais que “decorar” os dados no modelo? Exemplo do seu setor.
3. O que uma boa **skill** deveria conter para o agente acertar de primeira?
4. **Vibe coding** sem testes é aceitável num projeto real?

---

## 📌 Tarefa de casa (opcional)

- Escreva **uma skill** (pasta + `SKILL.md`) para uma tarefa sua.
- Explique, num parágrafo, como um **RAG** ajudaria no seu projeto.
- Liste **2 riscos** do vibe coding e como mitigá-los.

---

## 🔗 Relação com o curso

- **Bloco 3 (Automação)** tratou de operar GPU com Bash (`cron`, filas, monitoramento). Esta aula
  sobe um nível: **automatizar o próprio trabalho de desenvolvimento** com agentes.
- Conecta com toda a trilha: o agente **lê o repositório** (o mesmo que você versiona com Git em
  [`docs/03_git.md`](../../docs/03_git.md)) e **busca contexto** (RAG) para trabalhar.

---

## 🔧 Recursos de apoio

- Documentação da **Antigravity**: CLI, [Agent Skills](https://antigravity.google/docs/skills) e
  [Best Practices](https://antigravity.google/docs/cli/best-practices).
- Padrão aberto de **Agent Skills**: <https://agentskills.io/home>.
- `AGENTS.md` do repositório do curso — exemplo real de arquivo de regras para agentes.
