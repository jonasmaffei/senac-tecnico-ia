# 📋 Guia e Roteiro do Projeto Final — Infraestrutura e Tecnologia para IA

> **Curso:** Técnico em Inteligência Artificial — Senac  
> **Público-alvo:** Profissionais de diversas áreas (Negócios, Saúde, Design, Educação, Comunicação, etc.)  
> **Objetivo:** Aplicar os conceitos de infraestrutura de hardware, redes, Linux e modelos de IA estudados no módulo para propor uma solução real na sua área de atuação.

---

## 💡 Sobre o Projeto

Você não precisa desenvolver códigos complexos do zero! O objetivo deste projeto é que você atue como **Especialista/Consultor em Infraestrutura de IA**: identificando uma oportunidade no seu setor, avaliando as necessidades técnicas de hardware/rede, executando um teste prático no Google Colab e justificando a melhor decisão de implementação.

---

## 🎯 Estrutura do Projeto Final

O trabalho pode ser entregue em dupla ou individualmente e deve conter 3 partes principais:

### Parte 1: Definição do Problema do Mundo Real (Sua Área)
Escolha um problema real do seu setor de atuação que possa ser resolvido ou otimizado com IA.
* **Exemplo Negócios/Marketing:** Analisar centenas de avaliações de clientes para identificar insatisfação em tempo real.
* **Exemplo Saúde:** Transcrever e resumir consultas médicas ou analisar relatórios sem enviar dados sensíveis para servidores externos.
* **Exemplo Design/Comunicação:** Processar e aplicar filtros/classificação em lotes de milhares de imagens de catálogo.
* **Exemplo Educação/RH:** Criar um assistente local para responder dúvidas sobre apostilas e normas internas da empresa.

### Parte 2: Proposta e Justificativa de Infraestrutura (Teoria)
Responda às seguintes perguntas sobre a solução proposta:
1. **CPU vs GPU:** O processamento precisa de GPU? Por quê? (Paralelismo SIMD, volume de dados, etc.)
2. **Memória (RAM e VRAM):** Qual é a estimativa de memória necessária para rodar a solução?
3. **Nuvem vs Local (Privacidade e Custo):** A solução deve rodar na nuvem (Google Colab/AWS) ou em servidor local (Linux/Ollama)? Por quê? (Considere segurança de dados TCP/IP, largura de banda e custo).
4. **Sistema Operacional e Automação:** Como a solução seria mantida no ar? (ex: scripts Linux, tarefas agendadas via `cron`, contêineres Docker).

### Parte 3: Demonstração Prática (Google Colab)
Execute um teste simples no Google Colab (utilizando o notebook da Aula 12 ou um notebook personalizado com Hugging Face / Ollama / PyTorch) e inclua os resultados no seu relatório:
* Captura de tela ou dados do tempo de processamento (CPU vs GPU).
* Monitoramento de consumo de VRAM / Memória.
* Exemplo do resultado final gerado pela IA.

---

## 📦 O que Entregar?

Você deve enviar no formulário da turma:
1. **Relatório em PDF ou Slides de Apresentação** (máximo 5 a 8 slides) cobrindo as Partes 1 e 2.
2. **Link do Notebook Google Colab** (com permissão de leitura/execução) referente à Parte 3.

---

## 📊 Rubrica de Avaliação

| Critério | Peso | O que será avaliado? |
| :--- | :---: | :--- |
| **Clareza do Problema** | 20% | Aplicação prática bem alinhada ao setor do aluno. |
| **Justificativa de Infraestrutura** | 40% | Uso correto dos conceitos do módulo (GPU, VRAM, RAM, Linux, Redes/Privacidade). |
| **Execução no Colab** | 30% | Teste prático executado com sucesso e evidenciado no relatório. |
| **Apresentação e Organização** | 10% | Organização do documento/slides e clareza na explicação. |

---

## 🚀 Ideias de Temas por Área de Atuação

> Use uma destas sugestões caso precise de inspiração!

* 💼 **Gestão & Negócios:** "Estudo de Custo e Viabilidade para Otimização de Atendimento com LLMs em GPU Nuvem vs Servidor Local."
* 🏥 **Saúde & Bem-Estar:** "Infraestrutura Local com Linux para Sumarização de Prontuários com Privacidade Garantida (sem envio para nuvem)."
* 🎨 **Design & Mídia:** "Processamento Paralelo de Imagens em Lote com PyTorch: Comparativo de Tempo CPU vs GPU em Campanhas de Marketing."
* 📚 **Educação:** "Criando um Tutor Interativo de Estudos com Modelos Open-Source Leves em Colab."
