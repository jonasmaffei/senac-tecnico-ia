# 📖 Guia Passo a Passo: Como Abrir e Rodar o Notebook da Aula 12 no Google Colab

> **Para quem é este guia?**  
> Para os alunos realizarem a aula prática no Google Colab mesmo sem conhecimento prévio de programação ou ferramentas de TI.

---

## 🚀 Opção 1: Abrir Direto via GitHub (Mais Rápido e Recomendado)

1. Acesse o site do [Google Colab](https://colab.research.google.com/).
2. Faça login com a sua conta Google (Gmail).
3. Na janela pop-up que abrir, selecione a aba **GitHub**.
4. No campo de busca, cole a URL do repositório da turma:
   ```text
   https://github.com/jonasmaffei/senac-tecnico-ia
   ```
5. O Colab irá listar os arquivos do repositório. Clique em:
   `aulas/aula12/aula12_pratica_colab.ipynb`
6. Pronto! O notebook abrirá na sua tela.

---

## 💻 Opção 2: Fazer Download do Arquivo e Subir no Colab (Upload)

Se você já baixou o repositório ou o arquivo `.ipynb` para o seu computador:

1. Acesse o site do [Google Colab](https://colab.research.google.com/).
2. Na janela inicial, clique na aba **Fazer upload** (ou **Upload**).
3. Clique em **Escolher arquivo** e selecione o arquivo `aula12_pratica_colab.ipynb` no seu computador.
4. Aguarde o carregamento e o notebook abrirá automaticamente.

---

## ⚙️ PASSO CRÍTICO: Ativar a GPU no Google Colab

Por padrão, o Google Colab roda usando apenas o processador tradicional (**CPU**). Como nosso foco é testar a aceleração para IA, você **deve ativar a GPU** antes de rodar os exercícios:

1. No menu superior do Colab, clique em **Ambiente de execução** (ou *Runtime*).
2. Clique na opção **Alterar tipo de ambiente de execução** (ou *Change runtime type*).
3. Na janela que abrir, localize a opção **Acelerador de hardware** (ou *Hardware accelerator*).
4. Mude de **None/CPU** para **T4 GPU** (ou GPU disponível gratuitamente).
5. Clique no botão **Salvar** (ou *Save*).
6. No canto superior direito, verifique se aparece um ícone verde mostrando **RAM / GPU**.

---

## 🟢 Como Executar os Blocos da Aula

* Cada bloco cinza com código possui um botão de **Play ▶️** no lado esquerdo superior do bloco.
* Para rodar uma etapa, basta passar o mouse por cima do bloco de código e clicar no botão **Play ▶️**.
* Você também pode usar o atalho do teclado: selecione o bloco e pressione **`Ctrl + Enter`** (ou `Cmd + Enter` no Mac).
* **Campos Interativos (Formulários):** Alguns blocos possuem **sliders (barras deslizantes)** e **caixas de texto**. Altere os valores na interface e clique no botão de **Play ▶️** novamente para ver o resultado mudar!
