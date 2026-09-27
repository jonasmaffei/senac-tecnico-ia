# 🐙 Guia Completo de Git e GitHub — Do Básico ao Primeiro Projeto

Este guia cobre o tutorial **passo a passo do básico ao avançado no Git e GitHub**: desde a configuração inicial no terminal shell, a organização de pastas no seu computador, até a criação de repositórios na interface gráfica (UI) do GitHub e o envio do seu primeiro projeto.

---

## 🗂️ Organização das Pastas no Seu Computador

Para manter seus trabalhos organizados, adotamos o seguinte padrão de pastas dentro da sua pasta **Documentos**:

```text
Documentos/
├── projetos/      # Para seus rascunhos, experimentos e arquivos de teste locais
└── repositorios/  # Para onde você faz o 'git clone' dos seus repositórios do GitHub
```

- **`Documentos/projetos`**: Onde você cria e desenvolve seus scripts ou protótipos locais iniciais.
- **`Documentos/repositorios`**: Onde você clona seus repositórios oficiais vinculados ao GitHub.

---

## 📋 Pré-requisitos

| Item | Descrição / Onde Obter |
| :--- | :--- |
| **Conta no GitHub** | Cadastre-se gratuitamente em [github.com](https://github.com) |
| **Git for Windows** (inclui o **Git Bash**) | Baixe e instale via [git-scm.com/download/win](https://git-scm.com/download/win) |
| **Visual Studio Code** | Editor de código recomendado em [code.visualstudio.com](https://code.visualstudio.com) |

Para confirmar se o Git está instalado, abra o **Git Bash** e digite:
```bash
git --version
```

---

## ⚙️ 1. Configuração de Usuário e E-mail via Shell

Antes de realizar commits, você precisa configurar sua identidade global no Git. Abra o **Git Bash** e execute:

```bash
# Configurar seu nome completo
git config --global user.name "Seu Nome Completo"

# Configurar seu e-mail (use o mesmo e-mail cadastrado no GitHub)
git config --global user.email "seu.email@exemplo.com"
```

Para verificar se a configuração foi gravada com sucesso:
```bash
git config --list
```

---

## 🌐 2. Criar o Repositório na UI do GitHub

1. Acesse **[github.com](https://github.com)** e faça login.
2. No canto superior direito, clique no ícone **`+`** e selecione **New repository** (Novo repositório).
3. Preencha as informações:
   - **Repository name:** `meu-primeiro-projeto` (ou o nome da sua aplicação).
   - **Description:** *(Opcional)* Breve descrição do projeto.
   - **Visibilidade:** Escolha **Public** (Público) ou **Private** (Privado).
   - **Add a README file:** Marque esta opção para criar o repositório já com o arquivo de apresentação inicial.
4. Clique no botão verde **Create repository** (Criar repositório).

---

## 📥 3. Clonar o Repositório na pasta `Documentos/repositorios`

Com o repositório criado na UI do GitHub, vamos cloná-lo para a pasta **`repositorios`** na sua máquina.

1. No GitHub, clique no botão verde **Code** e copie a URL em **HTTPS** (ex.: `https://github.com/seu-usuario/meu-primeiro-projeto.git`).
2. Abra o **Git Bash** e navegue até a pasta de repositórios:

```bash
# 1. Garantir que as pastas existam
mkdir -p ~/Documentos/projetos
mkdir -p ~/Documentos/repositorios

# 2. Entrar na pasta repositorios
cd ~/Documentos/repositorios

# 3. Clonar o repositório criado na UI do GitHub
git clone https://github.com/seu-usuario/meu-primeiro-projeto.git

# 4. Entrar na pasta do projeto clonado
cd meu-primeiro-projeto
```

3. Abra a pasta no VS Code:
```bash
code .
```

---

## 🚀 4. Criar e Enviar o Primeiro Projeto (`add`, `commit`, `push`)

Agora você pode copiar seus códigos desenvolvidos na pasta `projetos` para a pasta do repositório clonado em `repositorios/meu-primeiro-projeto`, ou criar novos arquivos diretamente no VS Code.

### O Ciclo de Envio das 3 Etapas:

```
 [ Arquivos Editados ] ───( git add . )───> [ Área de Staging ] ───( git commit )───> [ Histórico Local ] ───( git push )───> [ GitHub (Nuvem) ]
```

#### Passo 4.1: Verificar alterações
No terminal do Git Bash (dentro da pasta do projeto):
```bash
git status
```

#### Passo 4.2: Adicionar arquivos para envio (`add`)
```bash
git add .
```

#### Passo 4.3: Gravar a alteração no histórico local (`commit`)
```bash
git commit -m "feat: primeiro envio do meu projeto"
```

#### Passo 4.4: Enviar para a nuvem no GitHub (`push`)
```bash
git push origin main
```

---

## 🔄 5. Atualizar Repositórios Existentes (`pull`)

Quando o professor atualizar o repositório do curso ou um colega enviar alterações, navegue até a pasta do projeto em `Documentos/repositorios` e execute:

```bash
cd ~/Documentos/repositorios/senac-tecnico-ia
git pull
```

---

## 🔧 Solução de Problemas Comuns

| Problema | Causa Provável | Solução |
| :--- | :--- | :--- |
| `fatal: not a git repository` | Você rodou o comando fora da pasta do projeto. | Use `cd ~/Documentos/repositorios/nome-do-projeto` antes de rodar comandos git. |
| `Please tell me who you are` | Nome/e-mail não configurados no shell. | Execute os comandos `git config --global user.name` e `user.email`. |
| `Permission denied (publickey)` | Falta de autenticação HTTPS/SSH. | Use a URL em HTTPS e informe um **Personal Access Token** se solicitado. |
| `code .` não abre o VS Code | VS Code não está no PATH do sistema. | Abra o VS Code manualmente e vá em **Arquivo ➔ Abrir Pasta...**. |

---

## 📌 Resumo Visual dos Comandos

```bash
# Configuração inicial (só 1 vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Entrar na pasta de repositórios e clonar
cd ~/Documentos/repositorios
git clone <URL_DO_GITHUB>
cd <NOME_DO_PROJETO>

# Enviar alterações (dia a dia)
git status
git add .
git commit -m "mensagem explicativa"
git push origin main
```
