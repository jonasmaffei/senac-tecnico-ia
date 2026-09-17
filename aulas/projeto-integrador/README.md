# 📋 Orientação do Projeto Integrador — Tecnologia e Infraestrutura para IA

## 🎯 Objetivo da Unidade Curricular
Aplicar os conhecimentos de **Arquitetura de Computadores (CPU vs GPU)**, **Modelos de Processamento e Memória (SIMD, RAM e VRAM)**, **Redes de Comunicação (TCP/IP e Subredes)** e **Sistemas Operacionais Linux** para planejar e demonstrar a infraestrutura necessária para rodar ou treinar um modelo de Inteligência Artificial voltado a um caso de uso real.

---

## 💡 Sobre a Abordagem do Projeto

Este trabalho avalia a **capacidade de análise técnica de infraestrutura e tomada de decisão**. 

Você atuará na **especificação técnica e validação prática da infraestrutura de IA**:
1. Mapear as exigências de processamento e memória do problema.
2. Definir a arquitetura ideal (hardware, redes/comunicação e sistema operacional).
3. Validar a execução da infraestrutura em ambiente de testes no Google Colab.

---

## 🎯 Estrutura da Entrega

O projeto pode ser desenvolvido individualmente ou em dupla e é dividido em 3 pilares alinhados aos elementos da competência:

### 1. Especificação de Hardware e Processamento
* **Modelo de Processamento (CPU vs GPU):** O problema exige processamento massivo paralelo (SIMD/GPU) ou sequencial complexo (CPU)?
* **Hierarquia de Memória:** Qual o consumo estimado de RAM e VRAM? Há risco de gargalo na transferência via barramento PCIe?
* **Arquitetura de GPU:** O modelo utilizará CUDA (NVIDIA) ou ROCm (AMD)? Qual a estratégia para evitar estouro de memória (VRAM Out Of Memory)?

### 2. Infraestrutura de Redes, Linux e Armazenamento
* **Comunicação de Dados e Redes (TCP/IP):** Como os dados chegam à infraestrutura? Qual a relevância da latência, largura de banda e endereçamento de rede para essa aplicação?
* **Ambiente de Operação (Linux):** Como o ambiente de execução será configurado (gerenciamento de processos, permissões, contêineres Docker ou rotinas agendadas)?
* **Segurança e Privacidade:** A infraestrutura rodará em nuvem pública ou em servidor local privado para proteger os dados?

### 3. Validação Prática em Ambiente Colab
* Executar um teste prático no Google Colab (utilizando o notebook da Aula 12 como base ou adaptado).
* Registrar o tempo de execução (CPU vs GPU) e a ocupação da VRAM (`nvidia-smi`).
* Demonstrar o resultado da saída do modelo ou pipeline de processamento.

---

## 📦 Formato da Entrega

1. **Documento/Relatório Técnico (PDF ou Slides):** Contendo as análises dos pilares 1 e 2.
2. **Link do Notebook no Google Colab:** Com a execução e os gráficos/métricas coletadas no pilar 3.

---

## 📊 Rubrica de Avaliação (Alinhada à Ementa)

| Critério | Peso | O que será avaliado? |
| :--- | :---: | :--- |
| **Análise de Hardware & Memória** | 35% | Uso correto dos conceitos de Von Neumann, CPU vs GPU, SIMD, RAM/VRAM e barramentos. |
| **Arquitetura de Redes & Linux** | 35% | Justificativa adequada sobre TCP/IP, segurança, permissões e gerenciamento de processos no Linux. |
| **Validação Prática (Colab)** | 20% | Sucesso na execução dos testes e coleta de métricas de desempenho (tempo/VRAM). |
| **Clareza & Defesa Técnica** | 10% | Coerência na apresentação da proposta e justificativa da solução. |
