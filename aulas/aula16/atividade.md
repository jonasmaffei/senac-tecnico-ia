# 📝 Atividade: Aula 16 — GitHub para Iniciantes, Agentes de Código, Contexto e AGENTS.md

---

## 🐙 Parte 1 — Tutorial Completo de GitHub para Iniciantes

O **GitHub** é a plataforma onde desenvolvedores armazenam, versionam e compartilham seus projetos de código. Quando trabalhamos com **agentes de IA** (`agy`, Claude Code, Cursor), o GitHub atua como a **rede de segurança central**: ele registra cada alteração feita pelo agente e permite voltar atrás se a IA errar.

---

### Passo 1 — Entendendo Git vs. GitHub

- **Git:** É a ferramenta instalada no seu computador que guarda o histórico de alterações dos arquivos (como uma máquina do tempo do projeto).
- **GitHub:** É o serviço na nuvem (o "Google Drive dos programadores") onde você salva seus repositórios Git para colaborar com outras pessoas ou acessar de qualquer lugar.

---

### Passo 2 — Criar uma conta no GitHub

1. Acesse **[github.com](https://github.com)**.
2. Clique em **Sign up** (Cadastrar-se).
3. Informe seu e-mail, crie uma senha forte e escolha um nome de usuário (*username*).
4. Complete a verificação e confirme a conta pelo link enviado ao seu e-mail.

---

### Passo 3 — Configurar sua identidade local no Git

Abra o **Git Bash** (no Windows) ou o terminal do VS Code e configure seu nome e e-mail (use o mesmo e-mail cadastrado no GitHub):

```bash
git config --global user.name "Seu Nome Completo"
git config --global user.email "seu.email@exemplo.com"
```

Para confirmar as configurações:
```bash
git config --list
```

---

### Passo 4 — Criar um repositório no GitHub

1. No GitHub, clique no ícone **`+`** no canto superior direito e selecione **New repository** (Novo repositório).
2. Nomeie o repositório (ex.: `meu-primeiro-projeto-ia`).
3. Escolha **Public** (Público) ou **Private** (Privado).
4. Marque a opção **Add a README file** (Adicionar um arquivo README).
5. Clique no botão verde **Create repository** (Criar repositório).

---

### Passo 5 — Clonar e o Ciclo Básico de Trabalho (`add`, `commit`, `push`)

#### 1. Clonar (Baixar para a sua máquina)
Copie a URL HTTPS do seu repositório no botão **Code** do GitHub e rode no Git Bash:
```bash
cd Documentos
git clone https://github.com/seu-usuario/meu-primeiro-projeto-ia.git
cd meu-primeiro-projeto-ia
```

#### 2. Criar ou editar arquivos
Abra a pasta no VS Code (`code .`) e crie um arquivo simples (ex.: `mensagem.txt`).

#### 3. O ciclo das 3 etapas do Git:
```
 [ Arquivos Modificados ]  ──( git add )──>  [ Ária de Staging ]  ──( git commit )──>  [ Repositório Local ]  ──( git push )──>  [ GitHub ]
```

- **Verificar o estado atual:**
  ```bash
  git status
  ```
- **Preparar os arquivos (`add`):**
  ```bash
  git add .
  ```
- **Gravar a alteração no histórico (`commit`):**
  ```bash
  git commit -m "feat: cria arquivo inicial de mensagem"
  ```
- **Enviar para a nuvem no GitHub (`push`):**
  ```bash
  git push origin main
  ```

---

### Passo 6 — Branches e Pull Requests (Trabalho Seguro em Equipe)

- **Branch (Ramificação):** Uma linha de desenvolvimento paralela onde você ou a IA podem testar alterações sem afetar o código principal (`main`).
  ```bash
  git checkout -b minha-nova-feature
  ```
- **Pull Request (PR):** Uma proposta de alteração enviada no GitHub para revisar o código antes de fundi-lo (*merge*) com o código principal.

---

### Passo 7 — Por que o GitHub é essencial ao trabalhar com Agentes de IA?

1. **Rastreabilidade total:** Você sabe exatamente quais linhas de código a IA alterou em cada *commit*.
2. **Rollback de emergência:** Se o agente fizer alterações indesejadas (*vibe coding* descontrolado), você recupera o código anterior com `git reset` ou restaurando o commit anterior.
3. **Auditoria:** Permite revisar os diffs propostos pela IA antes de aprovar e juntar ao projeto final.

---

## 🧠 Parte 2 — O que é Contexto no Desenvolvimento com IA?

### O que é Contexto e Janela de Contexto (*Context Window*)?

Quando você conversa com um modelo de linguagem ou agente de código, o **contexto** é a quantidade de informação que o modelo consegue "lembrar" e processar em uma única interação.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        JANELA DE CONTEXTO (TOKENS)                     │
│ ┌──────────────────────┬──────────────────────┬──────────────────────┐ │
│ │ Prompt do Usuário    │ Arquivos do Projeto  │ Histórico e Output   │ │
│ │ (Sua instrução)      │ (Lidos pelas Tools)  │ (Respostas e Diffs)  │ │
│ └──────────────────────┴──────────────────────┴──────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

- **O que entra no contexto?**
  - O prompt enviado por você.
  - As regras do projeto (`AGENTS.md`).
  - O histórico das mensagens trocadas na sessão.
  - O conteúdo dos arquivos lidos pelo agente através de ferramentas (*tools*).
  - O resultado da execução de comandos no terminal.

- **Por que gerenciar o contexto importa?**
  1. **Limite de Tokens:** Se o contexto estoura o limite da janela, o agente começa a esquecer trechos anteriores ou falhar.
  2. **Degradação de Qualidade (*Context Rot*):** Quanto mais informações irrelevantes ou repetidas estiverem na memória do agente, maior a chance de ele se distrair e cometer erros.

- **Boas Práticas de Gerenciamento de Contexto:**
  - **Especifique arquivos:** Indique os arquivos exatos com `@arquivo` ou forneça os caminhos completos.
  - **Inicie sessões limpas:** Se o agente estiver confuso após muitas tentativas, resete a conversa ou use comandos como `/rewind`.
  - **Mantenha arquivos de contexto centralizados:** Em vez de repetir instruções a cada mensagem, crie um arquivo estático [`AGENTS.md`](#parte-3--o-que-é-agentsmd-e-como-funciona).

---

## 📄 Parte 3 — O que é `AGENTS.md` e Como Funciona?

O [`AGENTS.md`](../laboratorio_monitoramento/AGENTS.md) é um padrão adotado por projetos modernos para servir como **memória persistente do repositório para agentes de IA**.

### Por que usar um `AGENTS.md`?

Sem o `AGENTS.md`, você precisa repetir para a IA em todo prompt: *"Use Python 3, use o framework Flask, formate o código em UTF-8 e comente cada função"*.

Com o `AGENTS.md` na raiz do projeto:
- O agente lê o arquivo **automaticamente** assim que é iniciado na pasta.
- O agente respeita a arquitetura, convenções e comandos definidos pelo projeto.
- Funciona com diversas ferramentas agênticas (Antigravity CLI `agy`, Claude Code, Cursor, GitHub Copilot CLI).

### Estrutura Recomendada de um `AGENTS.md`

```markdown
# AGENTS.md — Contexto do Repositório

## 📌 Sobre o Projeto
Descrição sucinta do objetivo do software e tecnologias aceitas.

## 🗂️ Estrutura Relevante
Árvore de diretórios e onde cada componente deve residir.

## ✅ Regras e Convenções
- Padrões de código e formatação.
- Tratamento de erros exigido.
- Requisitos de idioma e documentação.

## 🧪 Como Executar e Testar
Comandos exatos para rodar o ambiente, testes e validação.
```

---

## 🛠️ Parte 4 — Prática Guiada: Agente (`agy`) + `AGENTS.md` + Programa de Monitoramento Web em Python

Nesta prática, você usará a **Antigravity CLI** (`agy`) para ler o arquivo [`AGENTS.md`](../laboratorio_monitoramento/AGENTS.md) e construir um programa completo de **monitoramento de hardware em Python** acessível pelo navegador Web.

---

### Passo 1 — Entrar na pasta do laboratório

No seu terminal (Git Bash / PowerShell), navegue até a pasta do laboratório:

```bash
cd aulas/aula16/laboratorio_monitoramento
```

Verifique se o arquivo `AGENTS.md` está na pasta:
```bash
ls -l AGENTS.md
```

---

### Passo 2 — Iniciar a Antigravity CLI (`agy`)

Execute a CLI no terminal:
```bash
agy
```

> 💡 **Nota:** Se ainda não instalou o `agy`, instale via PowerShell com:
> `irm https://antigravity.google/cli/install.ps1 | iex`

---

### Passo 3 — Enviar o comando baseado no `AGENTS.md`

No prompt do agente, digite:

```
Leia o arquivo AGENTS.md desta pasta. Com base nele, crie o aplicativo de monitoramento web em Python com Flask e psutil, gerando os arquivos app.py, coletor.py, templates/index.html, static/style.css, static/script.js, requirements.txt e iniciar.bat. Em seguida, execute a validação.
```

---

### Passo 4 — Observar o Loop Agêntico e Revisar com `/diff`

1. Observe o agente executando o loop: **Observar → Planejar → Agir → Verificar**.
2. Antes de aceitar ou encerrar, digite no agente:
   ```
   /diff
   ```
3. Verifique se o código gerado segue as regras descritas no `AGENTS.md` (dashboard Dark Mode, atualização a cada 2s, estatísticas de CPU, RAM e Disco).

---

### Passo 5 — Testar a Aplicação Web no Navegador

Saia da CLI (`Ctrl + C` ou `exit`) e execute o script de inicialização no terminal:

```bash
./iniciar.bat
```

Ou manualmente com Python:
```bash
python -m venv .venv
source .venv/Scripts/activate  # no Git Bash
pip install -r requirements.txt
python app.py
```

Abra o seu navegador em **`http://localhost:5000`** e observe o painel de monitoramento dinâmico em tempo real!

---

### Passo 6 — Gravar o Progresso no Git e Enviar para o GitHub

Após testar o programa de monitoramento, salve suas alterações no Git:

```bash
git status
git add .
git commit -m "feat: cria sistema de monitoramento web em python via agy e AGENTS.md"
git push origin main
```

---

## 💬 Parte 5 — Discussão em Grupo (3 a 4 pessoas)

1. Como o arquivo `AGENTS.md` evitou que você tivesse que escrever um prompt gigantesco com todas as instruções de código?
2. De que forma o **GitHub** ajudaria sua equipe se o agente de IA gerasse uma alteração com bug que quebrasse a aplicação de monitoramento?
3. O que acontece com o comportamento do agente quando o contexto contém arquivos irrelevantes ou informação em excesso?

---

## 📌 Parte 6 — Tarefa de Casa (Fixação)

1. **Personalizar o `AGENTS.md`:** Adicione uma nova regra ao `AGENTS.md` do seu projeto de monitoramento (ex.: *"Adicionar alerta sonoro ou visual quando o uso de CPU ultrapassar 90%"*).
2. **Executar o agente novamente:** Abra o `agy` e peça para ele atualizar a aplicação com base no `AGENTS.md` modificado.
3. **Enviar para o GitHub:** Faça o `commit` e `push` da atualização para o seu repositório no GitHub.
