# ðŸ“ Atividade: Aula 16 â€” GitHub para Iniciantes, Agentes de CÃ³digo, Contexto e AGENTS.md

---

## ðŸ™ Parte 1 â€” Tutorial Completo de GitHub para Iniciantes

O **GitHub** Ã© a plataforma onde desenvolvedores armazenam, versionam e compartilham seus projetos de cÃ³digo. Quando trabalhamos com **agentes de IA** (`agy`, Claude Code, Cursor), o GitHub atua como a **rede de seguranÃ§a central**: ele registra cada alteraÃ§Ã£o feita pelo agente e permite voltar atrÃ¡s se a IA errar.

---

### Passo 1 â€” Entendendo Git vs. GitHub

- **Git:** Ã‰ a ferramenta instalada no seu computador que guarda o histÃ³rico de alteraÃ§Ãµes dos arquivos (como uma mÃ¡quina do tempo do projeto).
- **GitHub:** Ã‰ o serviÃ§o na nuvem (o "Google Drive dos programadores") onde vocÃª salva seus repositÃ³rios Git para colaborar com outras pessoas ou acessar de qualquer lugar.

---

### Passo 2 â€” Criar uma conta no GitHub

1. Acesse **[github.com](https://github.com)**.
2. Clique em **Sign up** (Cadastrar-se).
3. Informe seu e-mail, crie uma senha forte e escolha um nome de usuÃ¡rio (*username*).
4. Complete a verificaÃ§Ã£o e confirme a conta pelo link enviado ao seu e-mail.

---

### Passo 3 â€” Configurar sua identidade local no Git

Abra o **Git Bash** (no Windows) ou o terminal do VS Code e configure seu nome e e-mail (use o mesmo e-mail cadastrado no GitHub):

```bash
git config --global user.name "Seu Nome Completo"
git config --global user.email "seu.email@exemplo.com"
```

Para confirmar as configuraÃ§Ãµes:
```bash
git config --list
```

---

### Passo 4 â€” Criar um repositÃ³rio no GitHub

1. No GitHub, clique no Ã­cone **`+`** no canto superior direito e selecione **New repository** (Novo repositÃ³rio).
2. Nomeie o repositÃ³rio (ex.: `meu-primeiro-projeto-ia`).
3. Escolha **Public** (PÃºblico) ou **Private** (Privado).
4. Marque a opÃ§Ã£o **Add a README file** (Adicionar um arquivo README).
5. Clique no botÃ£o verde **Create repository** (Criar repositÃ³rio).

---

### Passo 5 â€” Clonar e o Ciclo BÃ¡sico de Trabalho (`add`, `commit`, `push`)

#### 1. Clonar (Baixar para a sua mÃ¡quina)
Copie a URL HTTPS do seu repositÃ³rio no botÃ£o **Code** do GitHub e rode no Git Bash:
```bash
cd Documentos
git clone https://github.com/seu-usuario/meu-primeiro-projeto-ia.git
cd meu-primeiro-projeto-ia
```

#### 2. Criar ou editar arquivos
Abra a pasta no VS Code (`code .`) e crie um arquivo simples (ex.: `mensagem.txt`).

#### 3. O ciclo das 3 etapas do Git:
```
 [ Arquivos Modificados ]  â”€â”€( git add )â”€â”€>  [ Ãria de Staging ]  â”€â”€( git commit )â”€â”€>  [ RepositÃ³rio Local ]  â”€â”€( git push )â”€â”€>  [ GitHub ]
```

- **Verificar o estado atual:**
  ```bash
  git status
  ```
- **Preparar os arquivos (`add`):**
  ```bash
  git add .
  ```
- **Gravar a alteraÃ§Ã£o no histÃ³rico (`commit`):**
  ```bash
  git commit -m "feat: cria arquivo inicial de mensagem"
  ```
- **Enviar para a nuvem no GitHub (`push`):**
  ```bash
  git push origin main
  ```

---

### Passo 6 â€” Branches e Pull Requests (Trabalho Seguro em Equipe)

- **Branch (RamificaÃ§Ã£o):** Uma linha de desenvolvimento paralela onde vocÃª ou a IA podem testar alteraÃ§Ãµes sem afetar o cÃ³digo principal (`main`).
  ```bash
  git checkout -b minha-nova-feature
  ```
- **Pull Request (PR):** Uma proposta de alteraÃ§Ã£o enviada no GitHub para revisar o cÃ³digo antes de fundi-lo (*merge*) com o cÃ³digo principal.

---

### Passo 7 â€” Por que o GitHub Ã© essencial ao trabalhar com Agentes de IA?

1. **Rastreabilidade total:** VocÃª sabe exatamente quais linhas de cÃ³digo a IA alterou em cada *commit*.
2. **Rollback de emergÃªncia:** Se o agente fizer alteraÃ§Ãµes indesejadas (*vibe coding* descontrolado), vocÃª recupera o cÃ³digo anterior com `git reset` ou restaurando o commit anterior.
3. **Auditoria:** Permite revisar os diffs propostos pela IA antes de aprovar e juntar ao projeto final.

---

## ðŸ§  Parte 2 â€” O que Ã© Contexto no Desenvolvimento com IA?

### O que Ã© Contexto e Janela de Contexto (*Context Window*)?

Quando vocÃª conversa com um modelo de linguagem ou agente de cÃ³digo, o **contexto** Ã© a quantidade de informaÃ§Ã£o que o modelo consegue "lembrar" e processar em uma Ãºnica interaÃ§Ã£o.

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                        JANELA DE CONTEXTO (TOKENS)                     â”‚
â”‚ â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ Prompt do UsuÃ¡rio    â”‚ Arquivos do Projeto  â”‚ HistÃ³rico e Output   â”‚ â”‚
â”‚ â”‚ (Sua instruÃ§Ã£o)      â”‚ (Lidos pelas Tools)  â”‚ (Respostas e Diffs)  â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

- **O que entra no contexto?**
  - O prompt enviado por vocÃª.
  - As regras do projeto (`AGENTS.md`).
  - O histÃ³rico das mensagens trocadas na sessÃ£o.
  - O conteÃºdo dos arquivos lidos pelo agente atravÃ©s de ferramentas (*tools*).
  - O resultado da execuÃ§Ã£o de comandos no terminal.

- **Por que gerenciar o contexto importa?**
  1. **Limite de Tokens:** Se o contexto estoura o limite da janela, o agente comeÃ§a a esquecer trechos anteriores ou falhar.
  2. **DegradaÃ§Ã£o de Qualidade (*Context Rot*):** Quanto mais informaÃ§Ãµes irrelevantes ou repetidas estiverem na memÃ³ria do agente, maior a chance de ele se distrair e cometer erros.

- **Boas PrÃ¡ticas de Gerenciamento de Contexto:**
  - **Especifique arquivos:** Indique os arquivos exatos com `@arquivo` ou forneÃ§a os caminhos completos.
  - **Inicie sessÃµes limpas:** Se o agente estiver confuso apÃ³s muitas tentativas, resete a conversa ou use comandos como `/rewind`.
  - **Mantenha arquivos de contexto centralizados:** Em vez de repetir instruÃ§Ãµes a cada mensagem, crie um arquivo estÃ¡tico [`AGENTS.md`](#parte-3--o-que-Ã©-agentsmd-e-como-funciona).

---

## ðŸ“„ Parte 3 â€” O que Ã© `AGENTS.md` e Como Funciona?

O [`AGENTS.md`](laboratorio_monitoramento/AGENTS.md) Ã© um padrÃ£o adotado por projetos modernos para servir como **memÃ³ria persistente do repositÃ³rio para agentes de IA**.

### Por que usar um `AGENTS.md`?

Sem o `AGENTS.md`, vocÃª precisa repetir para a IA em todo prompt: *"Use Python 3, use o framework Flask, formate o cÃ³digo em UTF-8 e comente cada funÃ§Ã£o"*.

Com o `AGENTS.md` na raiz do projeto:
- O agente lÃª o arquivo **automaticamente** assim que Ã© iniciado na pasta.
- O agente respeita a arquitetura, convenÃ§Ãµes e comandos definidos pelo projeto.
- Funciona com diversas ferramentas agÃªnticas (Antigravity CLI `agy`, Claude Code, Cursor, GitHub Copilot CLI).

### Estrutura Recomendada de um `AGENTS.md`

```markdown
# AGENTS.md â€” Contexto do RepositÃ³rio

## ðŸ“Œ Sobre o Projeto
DescriÃ§Ã£o sucinta do objetivo do software e tecnologias aceitas.

## ðŸ—‚ï¸ Estrutura Relevante
Ãrvore de diretÃ³rios e onde cada componente deve residir.

## âœ… Regras e ConvenÃ§Ãµes
- PadrÃµes de cÃ³digo e formataÃ§Ã£o.
- Tratamento de erros exigido.
- Requisitos de idioma e documentaÃ§Ã£o.

## ðŸ§ª Como Executar e Testar
Comandos exatos para rodar o ambiente, testes e validaÃ§Ã£o.
```

---

## ðŸ› ï¸ Parte 4 â€” PrÃ¡tica Guiada: Agente (`agy`) + `AGENTS.md` + Programa de Monitoramento Web em Python

Nesta prÃ¡tica, vocÃª usarÃ¡ a **Antigravity CLI** (`agy`) para ler o arquivo [`AGENTS.md`](laboratorio_monitoramento/AGENTS.md) e construir um programa completo de **monitoramento de hardware em Python** acessÃ­vel pelo navegador Web.

---

### Passo 1 â€” Entrar na pasta do laboratÃ³rio

No seu terminal (Git Bash / PowerShell), navegue atÃ© a pasta do laboratÃ³rio:

```bash
cd aulas/bloco3/aula16/laboratorio_monitoramento
```

Verifique se o arquivo `AGENTS.md` estÃ¡ na pasta:
```bash
ls -l AGENTS.md
```

---

### Passo 2 â€” Iniciar a Antigravity CLI (`agy`)

Execute a CLI no terminal:
```bash
agy
```

> ðŸ’¡ **Nota:** Se ainda nÃ£o instalou o `agy`, instale via PowerShell com:
> `irm https://antigravity.google/cli/install.ps1 | iex`

---

### Passo 3 â€” Enviar o comando baseado no `AGENTS.md`

No prompt do agente, digite:

```
Leia o arquivo AGENTS.md desta pasta. Com base nele, crie o aplicativo de monitoramento web em Python com Flask e psutil, gerando os arquivos app.py, coletor.py, templates/index.html, static/style.css, static/script.js, requirements.txt e iniciar.bat. Em seguida, execute a validaÃ§Ã£o.
```

---

### Passo 4 â€” Observar o Loop AgÃªntico e Revisar com `/diff`

1. Observe o agente executando o loop: **Observar â†’ Planejar â†’ Agir â†’ Verificar**.
2. Antes de aceitar ou encerrar, digite no agente:
   ```
   /diff
   ```
3. Verifique se o cÃ³digo gerado segue as regras descritas no `AGENTS.md` (dashboard Dark Mode, atualizaÃ§Ã£o a cada 2s, estatÃ­sticas de CPU, RAM e Disco).

---

### Passo 5 â€” Testar a AplicaÃ§Ã£o Web no Navegador

Saia da CLI (`Ctrl + C` ou `exit`) e execute o script de inicializaÃ§Ã£o no terminal:

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

Abra o seu navegador em **`http://localhost:5000`** e observe o painel de monitoramento dinÃ¢mico em tempo real!

---

### Passo 6 â€” Gravar o Progresso no Git e Enviar para o GitHub

ApÃ³s testar o programa de monitoramento, salve suas alteraÃ§Ãµes no Git:

```bash
git status
git add .
git commit -m "feat: cria sistema de monitoramento web em python via agy e AGENTS.md"
git push origin main
```

---

## ðŸ’¬ Parte 5 â€” DiscussÃ£o em Grupo (3 a 4 pessoas)

1. Como o arquivo `AGENTS.md` evitou que vocÃª tivesse que escrever um prompt gigantesco com todas as instruÃ§Ãµes de cÃ³digo?
2. De que forma o **GitHub** ajudaria sua equipe se o agente de IA gerasse uma alteraÃ§Ã£o com bug que quebrasse a aplicaÃ§Ã£o de monitoramento?
3. O que acontece com o comportamento do agente quando o contexto contÃ©m arquivos irrelevantes ou informaÃ§Ã£o em excesso?

---

## ðŸ“Œ Parte 6 â€” Tarefa de Casa (FixaÃ§Ã£o)

1. **Personalizar o `AGENTS.md`:** Adicione uma nova regra ao `AGENTS.md` do seu projeto de monitoramento (ex.: *"Adicionar alerta sonoro ou visual quando o uso de CPU ultrapassar 90%"*).
2. **Executar o agente novamente:** Abra o `agy` e peÃ§a para ele atualizar a aplicaÃ§Ã£o com base no `AGENTS.md` modificado.
3. **Enviar para o GitHub:** FaÃ§a o `commit` e `push` da atualizaÃ§Ã£o para o seu repositÃ³rio no GitHub.
