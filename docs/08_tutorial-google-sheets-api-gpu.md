# 📊 Tutorial Completo: Google Sheets API & Service Account para Telemetria de GPU

> **Objetivo:** Configurar a integração remota sem intervenção humana para enviar métricas de GPU salvas em CSV diretamente para uma planilha do Google Sheets via Service Account (*Conta de Serviço*).

---

## 🎯 Por que usar uma Service Account (*Conta de Serviço*)?

Em servidores de produção ou clusters de treinamento de IA, a coleta e o envio de métricas acontecem de maneira autônoma em segundo plano (via `cron`, `systemd` ou scripts em loop). Não há tela nem navegador para um usuário clicar em "Fazer login com o Google".

A **Service Account (SA)** funciona como um "robô" autorizado no Google Cloud que possui uma chave privada em formato JSON (`service_account.json`). O script utiliza essa chave para se autenticar diretamente na API do Google Sheets sem precisar de navegação web.

---

## 📋 Pré-requisitos

- Uma conta de e-mail do Google (Gmail ou Google Workspace).
- Python 3 instalado com as bibliotecas:
  ```bash
  pip install google-auth google-api-python-client
  ```

---

## 🚀 Passo a Passo de Configuração

### Passo 1 — Criar um Projeto no Google Cloud Console

1. Acesse **[console.cloud.google.com](https://console.cloud.google.com)**.
2. Faça login com sua conta Google.
3. No topo da tela, clique no seletor de projetos e escolha **Novo Projeto**.
4. Defina o nome do projeto (ex.: `Monitoramento-GPU`) e clique em **Criar**.
5. Certifique-se de selecionar o projeto recém-criado na barra superior.

---

### Passo 2 — Ativar a Google Sheets API

1. Abra o menu lateral (`≡`) e vá em **APIs e Serviços ➔ Biblioteca**.
2. Na barra de busca, digite `Google Sheets API`.
3. Selecione o card **Google Sheets API** e clique no botão **Ativar**.

---

### Passo 3 — Criar a Conta de Serviço (Service Account)

1. No menu lateral, acesse **APIs e Serviços ➔ Credenciais**.
2. Clique em **+ Criar Credenciais** (no topo) e escolha **Conta de serviço**.
3. Preencha os campos:
   - **Nome da conta de serviço:** `bot-gpu-monitor`
   - **Descrição:** `Bot de telemetria autônoma de GPUs`
4. Clique em **Criar e Continuar** e depois em **Concluir**.

---

### Passo 4 — Baixar a Chave JSON (`service_account.json`)

1. Na lista de **Contas de serviço**, localize a conta criada. O e-mail será semelhante a:  
   `bot-gpu-monitor@monitoramento-gpu-123456.iam.gserviceaccount.com`
2. Clique no e-mail da conta de serviço e acesse a aba **Chaves**.
3. Clique em **Adicionar chave ➔ Criar nova chave**.
4. Escolha o tipo **JSON** e confirme em **Criar**.
5. O arquivo `.json` será baixado no seu computador.
6. Renomeie o arquivo para **`service_account.json`** e coloque-o na pasta do seu projeto de monitoramento.

> ⚠️ **REGRA DE SEGURANÇA:** O arquivo `service_account.json` contém credenciais privadas. Nunca envie este arquivo para repositórios públicos no GitHub! Adicione `service_account.json` ao seu `.gitignore`.

---

### Passo 5 — Criar a Planilha e Conceder Permissão

1. Acesse **[sheets.google.com](https://sheets.google.com)** e crie uma **Nova Planilha**.
2. Dê um nome à planilha (ex.: `Dashboard de GPUs`).
3. Renomeie a aba inferior para **`GPU_Logs`**.
4. Clique no botão **Compartilhar** (canto superior direito).
5. Cole o e-mail da Conta de Serviço (ex.: `bot-gpu-monitor@monitoramento-gpu-123456.iam.gserviceaccount.com`).
6. Mantenha a permissão como **Editor**, desmarque "Notificar pessoas" e clique em **Compartilhar**.

---

### Passo 6 — Obter o ID da Planilha (`SHEETS_ID`)

A URL da sua planilha no navegador segue o formato:
```text
https://docs.google.com/spreadsheets/d/ 1a2b3c4d5e6f7g8h9i0j-XYZ /edit#gid=0
```

Copie o código alfanumérico contido entre `/d/` e `/edit`. Este código é o seu **`SHEETS_ID`**.

---

## 💻 Executando a Integração no Código

Com o arquivo `gpu_log.csv` gerado e o `service_account.json` salvo, execute a publicação definindo as variáveis de ambiente:

### No Windows (PowerShell):
```powershell
$env:SHEETS_ID="SEU_ID_DA_PLANILHA_AQUI"
$env:GOOGLE_CREDS="service_account.json"
python 4_enviar_sheets.py
```

### No Linux / Git Bash:
```bash
export SHEETS_ID="SEU_ID_DA_PLANILHA_AQUI"
export GOOGLE_CREDS="service_account.json"
python3 4_enviar_sheets.py
```

---

## 🔧 Solução de Problemas Comuns

| Erro / Comportamento | Causa Provável | Solução |
| :--- | :--- | :--- |
| `403 Forbidden` / `The caller does not have permission` | A planilha não foi compartilhada com o e-mail da Service Account. | Abra a planilha no Sheets ➔ Compartilhar ➔ Adicionar e-mail da SA como Editor. |
| `404 Not Found` | O `SHEETS_ID` informado na variável de ambiente está incorreto. | Verifique a URL da planilha e copie o ID entre `/d/` e `/edit`. |
| `Unable to parse range` | A aba da planilha não se chama `GPU_Logs`. | Renomeie a aba inferior da planilha no Google Sheets para `GPU_Logs`. |
| `FileNotFoundError: service_account.json` | O arquivo de chave não está no diretório correto. | Mova o arquivo JSON para a mesma pasta de onde o script Python é executado. |
