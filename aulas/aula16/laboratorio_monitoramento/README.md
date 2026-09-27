# 🖥️ Laboratório: Monitoramento Web em Python com Agente de IA

Este laboratório é um exercício prático da **Aula 16** para demonstrar como um **agente de código** (`agy`) utiliza o arquivo [`AGENTS.md`](AGENTS.md) como **contexto** para construir uma aplicação completa de monitoramento do sistema em Python acessível via navegador.

---

## 🎯 Objetivo

Usar a **Antigravity CLI** (`agy`) dentro desta pasta para ler o [`AGENTS.md`](AGENTS.md) e implementar a aplicação de monitoramento web.

---

## 🗂️ Conteúdo da Pasta

```
laboratorio_monitoramento/
├── AGENTS.md        # Arquivo de diretrizes, regras e requisitos do projeto para o agente
└── README.md        # Este guia de uso
```

---

## 🚀 Passo a Passo da Prática

### 1. Abrir o terminal no Git Bash / PowerShell nesta pasta
```bash
cd aulas/aula16/laboratorio_monitoramento
```

### 2. Iniciar a Antigravity CLI
```bash
agy
```

### 3. Fazer o pedido ao agente
Digite no prompt do `agy`:
```
Leia o arquivo AGENTS.md desta pasta e crie a aplicação de monitoramento web em Python conforme a estrutura e regras descritas.
Em seguida, crie os arquivos de código (app.py, coletor.py, templates/index.html, static/style.css, static/script.js, requirements.txt e iniciar.bat) e teste a aplicação.
```

### 4. Revisar as alterações do agente
Antes de aceitar ou rodar, use o comando `/diff` no agente para entender o que ele gerou.

### 5. Executar a aplicação
No Windows, rode:
```bash
./iniciar.bat
```
Ou manualmente no terminal:
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python app.py
```

Abra no navegador em `http://localhost:5000` e veja o dashboard dinâmico em funcionamento!
