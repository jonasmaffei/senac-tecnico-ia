# 📋 Orientação do Projeto Integrador — Tecnologia e Infraestrutura para IA

> **Curso:** Técnico em Inteligência Artificial — Senac  
> **Público-alvo:** Profissionais de diversas áreas (Negócios, Saúde, Design, Educação, Comunicação, etc.)  
> **Objetivo:** Aplicar os conceitos de arquitetura de hardware (CPU vs GPU), modelos de processamento e memória (SIMD, RAM e VRAM), redes de comunicação (TCP/IP) e sistemas operacionais Linux para planejar e demonstrar a infraestrutura necessária para rodar ou treinar um modelo de Inteligência Artificial voltado a um caso de uso real.

---

## 💡 Sobre a Abordagem do Projeto

Este trabalho avalia a sua **capacidade de análise técnica de infraestrutura e tomada de decisão**. Você não precisa desenvolver códigos complexos do zero! 

Você atuará na **especificação técnica e validação prática da infraestrutura de IA**:
1. Mapear as exigências de processamento e memória do problema no seu setor de atuação.
2. Definir a arquitetura ideal (hardware, redes/comunicação e sistema operacional).
3. Validar a execução da infraestrutura em ambiente de testes no Google Colab.

---

## 🚀 Ideias e Exemplos de Temas por Área de Atuação

> Use uma destas sugestões caso precise de inspiração para o seu projeto!

* 💼 **Gestão & Negócios:** "Estudo de Custo e Viabilidade para Otimização de Atendimento com LLMs em GPU Nuvem vs Servidor Local."
* 🏥 **Saúde & Bem-Estar:** "Infraestrutura Local com Linux para Sumarização de Prontuários com Privacidade Garantida (sem envio para nuvem via TCP/IP público)."
* 🎨 **Design & Mídia:** "Processamento Paralelo de Imagens em Lote com PyTorch: Comparativo de Tempo CPU vs GPU em Campanhas de Marketing."
* 📚 **Educação & RH:** "Criando um Tutor Interativo / Assistente de Dúvidas sobre Apostilas e Normas Internas com Modelos Open-Source Leves no Colab."
* ⚖️ **Jurídico / Compliance:** "Análise Local e Extração de Entidades em Contratos com Modelos Quantizados para Garantia de Privacidade de Dados."

---

## 🎯 Estrutura da Entrega

O projeto pode ser desenvolvido individualmente ou em dupla e é dividido em 3 pilares alinhados aos elementos da competência:

### 1. Especificação de Hardware e Processamento
* **Modelo de Processamento (CPU vs GPU):** O problema exige processamento massivo paralelo (SIMD/GPU) ou sequencial complexo (CPU)?
* **Hierarquia de Memória:** Qual o consumo estimado de RAM e VRAM? Há risco de gargalo na transferência via barramento PCIe?
* **Arquitetura de GPU:** O modelo utilizará CUDA (NVIDIA) ou ROCm (AMD)? Qual a estratégia para evitar estouro de memória (VRAM Out Of Memory)?

### 2. Infraestrutura de Redes, Linux e Armazenamento
* **Comunicação de Dados e Redes (TCP/IP):** Como os dados chegam à infraestrutura? Qual a relevância da latência, largura de banda e endereçamento de rede para essa aplicação?
* **Ambiente de Operação (Linux):** Como o ambiente de execução será configurado (gerenciamento de processos, permissões, contêineres Docker ou rotinas agendadas via `cron`)?
* **Segurança e Privacidade:** A infraestrutura rodará em nuvem pública ou em servidor local privado para proteger os dados?

### 3. Validação Prática em Ambiente Colab
* Executar um teste prático no Google Colab (utilizando o notebook da Aula 12 ou Aula 13 como base ou adaptado).
* Registrar o tempo de execução (CPU vs GPU) e a ocupação da VRAM (`nvidia-smi`).
* Demonstrar o resultado da saída do modelo ou pipeline de processamento.

---

## 📦 Formato da Entrega

1. **Documento/Relatório Técnico (PDF ou Slides):** Contendo as análises dos pilares 1 e 2 (máximo 5 a 8 slides ou páginas).
2. **Link do Notebook no Google Colab:** Com a execução e os gráficos/métricas coletadas no pilar 3 (com permissão de leitura/execução).

---

## 📊 Rubrica de Avaliação (Alinhada à Ementa)

| Critério | Peso | O que será avaliado? |
| :--- | :---: | :--- |
| **Análise de Hardware & Memória** | 35% | Uso correto dos conceitos de Von Neumann, CPU vs GPU, SIMD, RAM/VRAM e barramentos. |
| **Arquitetura de Redes & Linux** | 35% | Justificativa adequada sobre TCP/IP, segurança, permissões e gerenciamento de processos no Linux. |
| **Validação Prática (Colab)** | 20% | Sucesso na execução dos testes e coleta de métricas de desempenho (tempo/VRAM). |
| **Clareza & Defesa Técnica** | 10% | Coerência na apresentação da proposta e justificativa da solução alinhada ao setor do aluno. |
