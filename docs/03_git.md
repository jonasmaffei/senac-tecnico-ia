# 🐙 Guia Básico de Git — Clonar e Atualizar (somente leitura)

Este guia cobre o **essencial do Git** para acompanhar o repositório do curso: **baixar o
projeto uma vez** (clonar) e **atualizá-lo** sempre que o professor publicar novidades
(`pull`). O repositório é de **somente leitura** para os alunos — você **não** envia arquivos,
apenas baixa e atualiza.

> 💡 **O que é Git?** É um sistema que guarda o **histórico** de um projeto. Em vez de baixar
> arquivos soltos (e perder as atualizações), você **clona** o repositório uma vez e depois só
> executa **`git pull`** para ficar com a versão mais recente.

**Ferramentas usadas na aula:**

| Ferramenta | Para quê |
| :--- | :--- |
| **Git Bash** | Terminal onde você roda os comandos `git` (vem com o Git for Windows) |
| **VS Code** | Editor para abrir e ler os arquivos do projeto (tem terminal integrado) |

---

## 📋 Pré-requisitos

| Item | Onde obter |
| :--- | :--- |
| **Git for Windows** (inclui o **Git Bash**) | [git-scm.com/download/win](https://git-scm.com/download/win) |
| **Visual Studio Code** | [code.visualstudio.com](https://code.visualstudio.com) |

Verifique se o Git está instalado — abra o **Git Bash** e digite:

```bash
git --version
```

Se aparecer algo como `git version 2.x.x`, está pronto.

---

## 📥 1. Clonar o repositório (só na primeira vez)

Clonar é **baixar uma cópia completa** do projeto para a sua máquina, já com o histórico e o
vínculo com o repositório remoto. Faça isso **uma vez**; depois, use apenas `pull`.

Abra o **Git Bash** e rode:

```bash
# Entre na pasta onde quer guardar o projeto (ex.: Documentos/repos)
cd Documentos/repos

# Clone o repositório do curso
git clone https://github.com/jonasmaffei/senac-tecnico-ia

# Entre na pasta criada
cd senac-tecnico-ia
```

### Abrir no VS Code

Ainda no Git Bash, dentro da pasta do projeto:

```bash
code .
```

> 💡 O `code .` abre a **pasta atual** no VS Code. Se o comando não funcionar, abra o VS Code
> manualmente e use **Arquivo ➔ Abrir Pasta…** e selecione a pasta `senac-tecnico-ia`.
>
> **De onde vem a URL?** No GitHub, clique no botão verde **Code** e copie o endereço em
> **HTTPS**.

---

## 🔄 2. Atualizar o repositório (`pull`) — o comando do dia a dia

Sempre que o professor **publicar novidades** (novas aulas, correções), atualize a sua cópia
com **um único comando**. Rode **dentro da pasta do projeto**:

```bash
git pull
```

Pronto — sua pasta fica igual à do professor.

> ⚠️ **Importante:** o `pull` deve ser rodado **dentro da pasta do projeto**
> (`senac-tecnico-ia`), não na pasta de cima. Para conferir onde você está: `pwd`.

### Rotina recomendada — toda aula

Abra o **Git Bash**, entre no projeto e atualize:

```bash
cd Documentos/repos/senac-tecnico-ia   # entra no projeto
git pull                               # baixa as novidades
```

> 💡 **No VS Code:** você pode usar o **terminal integrado** (*Terminal ➔ Novo Terminal*, ou
> `Ctrl + '`). Ele já abre na pasta do projeto — basta digitar `git pull`.

---

## 🔍 3. Ver o que mudou (`status` e `log`)

Alguns comandos de leitura ajudam a entender o estado do projeto:

```bash
git status              # mostra o que mudou na sua cópia
git log --oneline -5    # mostra os 5 últimos commits (histórico resumido)
git branch              # mostra em qual "linha" (branch) você está (normalmente main)
```

Exemplo de saída do `git status` logo após um `pull`:

```
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

`working tree clean` significa que sua cópia está **igual à do repositório** — nada pendente.

> 💡 Como o repositório é **somente leitura**, o esperado é você **nunca modificar** os arquivos
> originais. Se quiser testar algo, faça uma **cópia** do arquivo (ex.: `aula05_redes_COPIA.ipynb`).

---

## 🗂️ 4. Fluxo completo (resumo visual)

```
Primeira vez:   git clone <URL>   ->  cd senac-tecnico-ia  ->  code .
Toda aula:      git pull          ->  pronto para usar
```

---

## 🔧 Solução de problemas

| Problema | Causa provável | Solução |
| :--- | :--- | :--- |
| `not a git repository` | Você rodou o comando fora da pasta do projeto | `cd senac-tecnico-ia` e tente de novo |
| `git: command not found` | Git não instalado / fora do PATH | Instale o [Git for Windows](https://git-scm.com/download/win) e reabra o **Git Bash** |
| `code .` não funciona | VS Code não está no PATH | Abra o VS Code e use **Arquivo ➔ Abrir Pasta…** |
| `pull` reclama de arquivos alterados | Você editou um arquivo original | Desfaça a alteração (`git checkout -- .`) ou salve sua versão com outro nome; peça orientação ao professor |
| Pediu **usuário e senha** | Autenticação do GitHub | Como é só leitura, normalmente não pede; se pedir, use um **Personal Access Token** no lugar da senha |
| Clonou na pasta errada | `cd` antes do `clone` | Apague a pasta criada e clone novamente no lugar certo |

> 💡 **Dica:** rode `git status` sempre que estiver em dúvida — ele diz exatamente o que está
> acontecendo e sugere o próximo comando.

---

## 🔗 Relação com o curso

- O repositório é a **fonte da verdade** das aulas: rode `git pull` **antes de cada aula** para
  garantir que está com a versão mais recente.
- As aulas com **laboratório Windows** rodam no **Git Bash** a partir da sua cópia clonada; os
  **notebooks** podem ser abertos no **Colab** direto pelo GitHub.
- Tutoriais complementares: [WSL](06_tutorial-instalacao-wsl.md) e
  [Docker no WSL](07_tutorial-instalacao-docker-wsl.md).
