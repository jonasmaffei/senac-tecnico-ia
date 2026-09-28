# Tutorial: Interface Gráfica para IAs Locais com Docker e Open WebUI

Executar modelos via terminal é essencial para automação, mas a experiência de uso diário exige uma interface visual (front-end). Neste tutorial, vamos subir o **Open WebUI**, um front-end robusto e de código aberto que imita a interface do ChatGPT e se conecta nativamente ao Ollama.

Usaremos o **Docker** para isolar a aplicação e garantir que ela rode sem poluir o sistema operacional.

---

## 1. Pré-requisitos

1. **Ollama instalado e rodando:** Você deve ter concluído o tutorial anterior e o serviço do Ollama deve estar ativo (teste acessando `http://localhost:11434` no navegador; deve aparecer a mensagem "Ollama is running").
2. **Docker Desktop:** Instalado e rodando no Windows. 

---

## 2. Subindo o Front-end via Docker (Comando Único)

Abra o **PowerShell** e execute o comando abaixo. Ele fará o download da imagem oficial e iniciará o contêiner:

```powershell
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

### Dissecando o comando (Visão de Engenharia):
* `-d`: Roda o contêiner em segundo plano (*detached*), liberando seu terminal.
* `-p 3000:8080`: Mapeia a porta 8080 (interna do contêiner) para a porta 3000 do seu Windows.
* `--add-host=host.docker.internal:host-gateway`: **Muito importante!** Isso permite que o contêiner "enxergue" a máquina local. Sem isso, o Open WebUI isolado no Docker não conseguiria achar o Ollama rodando no host.
* `-v open-webui:/app/backend/data`: Cria um volume persistente. Se você deletar o contêiner, seu histórico de chats não será perdido.
* `--restart always`: Se você reiniciar o PC, o Docker sobe essa interface automaticamente.

---

## 3. Acessando a Interface

1. Abra o seu navegador e acesse: `http://localhost:3000`
2. Você verá uma tela de login. Como é a primeira vez, clique em **Sign Up** (Cadastrar-se).
   * *Nota de Segurança:* Este cadastro é **100% local**. Os dados ficam salvos apenas no volume do Docker na sua máquina. O primeiro usuário criado se torna o Administrador do sistema.
3. Faça o login.

---

## 4. Conectando e Usando o Modelo

1. No topo da tela principal do Open WebUI, há um seletor de modelos.
2. Clique nele e você verá o `qwen2.5:0.5b` (ou qualquer outro modelo que você tenha baixado via terminal com o Ollama).
3. Selecione o modelo e digite sua mensagem no chat.

Pronto! Você agora tem um clone privado do ChatGPT rodando totalmente na sua infraestrutura local.

---

## Bônus: Infraestrutura como Código (Docker Compose)

Como boa prática de infraestrutura (Infra as Code), é melhor ter isso documentado em um arquivo do que rodar comandos soltos. 

Crie um arquivo chamado `docker-compose.yml` e cole o código abaixo:

```yaml
version: '3.8'

services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    restart: always
    ports:
      - "3000:8080"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui_data:/app/backend/data

volumes:
  open-webui_data:
```

Para subir essa infraestrutura, abra o PowerShell na mesma pasta do arquivo e digite:
```powershell
docker compose up -d
```
Isso faz exatamente a mesma coisa que o comando gigante anterior, mas agora sua arquitetura está documentada e versionável!