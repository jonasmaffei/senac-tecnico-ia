# Atividade: Aula 16 — Agentes de Código, Harness, RAG, Skills e Vibe Coding

## Parte 1 — Prática guiada: Antigravity CLI (`agy`)

Vamos colocar um **agente de código** para trabalhar dentro de um projeto real e observar, na
prática, os conceitos da aula.

> ⚠️ **Antes de começar:** um agente de código pode **ler e escrever arquivos** e **executar
> comandos**. Trabalhe numa **pasta de teste** (nunca num projeto importante) e **revise cada
> mudança** antes de aceitar.

### Passo 1 — Instalar a CLI

No **PowerShell** (Windows):

```powershell
irm https://antigravity.google/cli/install.ps1 | iex
```

Confirme que o binário `agy` foi instalado:

```powershell
agy --version
```

### Passo 2 — Criar uma pasta de teste e abrir o agente

```powershell
mkdir agente-teste
cd agente-teste
agy
```

Na primeira execução, a TUI faz um setup rápido (tema, modo de renderização e **confiança no
workspace**). Confirme que você confia na pasta (ela está vazia).

### Passo 3 — Primeira tarefa

No prompt do agente, peça algo simples e **verificável**:

```
Crie um script Python que imprima os números de 1 a 5.
Depois execute o script para confirmar que funciona.
```

Observe as fases do **loop agêntico**:

1. **Observar** — ele lê a pasta (vazia).
2. **Planejar** — ele propõe o que vai fazer.
3. **Agir** — ele cria o arquivo e roda o comando.
4. **Verificar** — ele confere a saída.

### Passo 4 — Revisar com `/diff`

Antes de aceitar qualquer mudança, veja o que o agente alterou:

```
/diff
```

> 💡 Essa é a etapa de **verificação humana**. Sem ela, você está fazendo *vibe coding* no escuro.

### Passo 5 — Explorar os comandos

| Comando | O que faz |
| :--- | :--- |
| `/agents` | Painel de **subagentes** (tarefas em paralelo) |
| `/skills` | Lista as **skills** disponíveis |
| `/diff` | Revisa as mudanças propostas |
| `/permissions` | Ajusta o nível de autonomia do agente |
| `/rewind` | Volta a um ponto anterior da conversa |

---

## Parte 2 — Discussão em grupo (3 a 4 pessoas)

1. Onde o **harness** termina e a **responsabilidade do engenheiro** começa? Quem responde por um
   bug gerado pelo agente?
2. Em que situações o **RAG** resolve mais que “decorar” os dados no modelo? Dê um exemplo do
   seu setor.
3. Uma **skill** bem escrita é como um manual. O que ela deveria conter para o agente acertar de
   primeira?
4. **Vibe coding** sem testes é aceitável num projeto real? Como convencer um colega a mudar de
   prática?

---

## Parte 3 — Pesquisa (tarefa de casa)

1. **Escreva uma skill** (pasta + `SKILL.md`) para uma tarefa sua e explique quando o agente
   deveria usá-la.
2. Explique, num parágrafo, como um **RAG** ajudaria no seu projeto (o que buscaria, onde).
3. Liste **2 riscos** do vibe coding e como mitigá-los.

> **Dica:** a `description` da skill é o que o agente lê para decidir usá-la. Escreva-a na
> **terceira pessoa**, com as palavras que você usaria ao pedir a tarefa.
