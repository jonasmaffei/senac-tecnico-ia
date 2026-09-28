# Tutorial Completo: Executando Inteligência Artificial Local com Ollama (Windows / PowerShell)

O **Ollama** é uma ferramenta de código aberto que simplifica drasticamente a execução de Grandes Modelos de Linguagem (LLMs) localmente. Ele empacota os pesos do modelo, as configurações e o motor de inferência em um único ambiente, permitindo que você rode IAs avançadas sem depender da nuvem, garantindo privacidade total e custo zero de execução.

Este tutorial guiará você desde a instalação via linha de comando no Windows até o consumo do modelo via API.

---

## 1. Pré-requisitos
* Sistema Operacional Windows 10 ou 11.
* Acesso à internet para o download inicial da ferramenta e do modelo.
* Terminal **PowerShell** aberto com privilégios de Administrador.

---

## 2. Instalação via PowerShell

Abra o menu Iniciar, digite `PowerShell`, clique com o botão direito e selecione **"Executar como Administrador"**. Em seguida, execute o comando oficial de instalação:

```powershell
irm [https://ollama.com/install.ps1](https://ollama.com/install.ps1) | iex
```

### O que este comando faz?
* `irm` (Invoke-RestMethod): Faz o download do script de instalação oficial diretamente dos servidores do Ollama.
* `|` (Pipe): Pega o resultado do download e passa para o próximo comando.
* `iex` (Invoke-Expression): Executa o script baixado automaticamente, configurando os arquivos binários e criando o serviço do Ollama em segundo plano (background).

---

## 3. Validação do Serviço

Após a conclusão, precisamos garantir que o serviço foi iniciado corretamente. No mesmo terminal, digite:

```powershell
ollama --version
```

*Se a instalação foi bem-sucedida, você verá a versão atual do Ollama (ex: `ollama version is 0.3.x`).*

---

## 4. O Primeiro Contato: Baixando um Modelo "Peso-Pena"

Os modelos de IA variam muito em tamanho (de gigabytes a centenas de gigabytes). Para testes locais rápidos em máquinas com menos memória RAM, usaremos o **Qwen 2.5 (0.5B)**. Ele possui "apenas" 500 milhões de parâmetros, exigindo menos de 1 GB de RAM, e o download é de aproximadamente 350 MB.

Execute o comando abaixo para baixar o modelo e entrar no modo interativo:

```powershell
ollama run qwen2.5:0.5b
```

### 4.1. Conversando com a IA (Modo Interativo)
Assim que o download terminar, o prompt mudará para `>>>`, indicando que o modelo está carregado na memória e pronto para responder. 

Faça um teste enviando um prompt:
```text
>>> Qual é a diferença entre CPU e GPU de forma simples?
```

Para encerrar a sessão e liberar a memória RAM, digite `/exit` e pressione Enter, ou use o atalho `Ctrl + D`.

---

## 5. Modo de Execução Rápida (Non-Interactive)

Para automações ou scripts, você não quer abrir um chat, mas apenas enviar uma instrução e receber a resposta direta no terminal. Basta passar o texto entre aspas após o nome do modelo:

```powershell
ollama run qwen2.5:0.5b "Escreva um script simples em Python que imprima 'Olá, Mundo'."
```

O Ollama vai carregar o modelo em segundo plano, gerar a resposta, imprimi-la no terminal e liberar o prompt.

---

## 6. Testando a API REST Local (Modo Engenheiro)

Quando o Ollama está instalado, ele sobe automaticamente um servidor local na porta `11434`. Isso significa que você pode integrar o Ollama em suas próprias aplicações (Python, Node.js, C#, etc.).

Para testar a API diretamente no PowerShell usando o comando nativo `Invoke-RestMethod`:

```powershell
$body = @{
    model  = "qwen2.5:0.5b"
    prompt = "Resuma o que é a linguagem Markdown em uma frase."
    stream = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $body -ContentType "application/json" | Select-Object -ExpandProperty response
```

Isso simula o que uma aplicação web ou um script faria ao "conversar" com o seu LLM local.


---
> **Dica de Infraestrutura:** Se o modelo estiver rodando lentamente, verifique se há outros programas consumindo muita memória. O Ollama tentará usar a GPU se houver drivers compatíveis instalados, caso contrário, fará o processamento direto na CPU.