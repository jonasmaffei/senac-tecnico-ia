# 📋 Orientação do Projeto Integrador — Introdução a Arquitetura de Computadores

> **Curso:** Técnico em Inteligência Artificial — Senac  
> **Unidade Curricular (UC):** Introdução a Arquitetura de Computadores  
> **Natureza do trabalho:** Pesquisa aplicada com análise crítica. **Não é obrigatório programar.**  
> **Objetivo:** Investigar um problema real e propor a solução de Inteligência Artificial necessária para viabilizá-lo, articulando os conhecimentos de toda a Unidade Curricular (UC).

---

## 🎯 O que é o Projeto Integrador?

O Projeto Integrador é o trabalho que **amarra todo o conteúdo da UC em uma única entrega**. Em vez de estudar cada assunto isoladamente, você escolhe um problema real do seu setor, pesquisa sobre ele e demonstra que compreende:

- **Qual solução de IA resolve o problema** (modelo, abordagem e dados necessários);
- **Onde o processamento acontece** (arquitetura e modelos de execução);
- **Onde os dados vivem e circulam** (memória, redes e sistemas operacionais);
- **Como o código é acelerado** (CUDA, tiling, OpenCL e ROCm);
- **Como se mede e se decide** (benchmarks, custo, energia e escolha de fornecedor).

A pergunta central que o seu trabalho deve responder é:

> **“Como solucionar com IA um problema proposto?”**

Não existe resposta única: existem **decisões justificadas**. O valor do projeto está no raciocínio, na pesquisa de fontes confiáveis e na capacidade de conectar os conceitos da UC a um problema concreto.

---

## 🧩 Conteúdo da UC que o Projeto Deve Integrar

Use esta lista como roteiro. O projeto não precisa ter uma seção para cada item, mas deve **mobilizar a maioria dos conceitos** ao longo do texto.

| Bloco | Aula | Conceitos que devem aparecer no projeto |
| :--- | :---: | :--- |
| **1 — Fundamentos** | 1 | Von Neumann vs. Harvard, CPU (poucos núcleos, sequencial) vs. GPU (paralelismo massivo) |
| | 2 | Modelos SIMD, MIMD, RISC vs. CISC e o balanço energético das arquiteturas |
| | 3 | Hierarquia de memória (registradores → SRAM → cache → VRAM), latência e gargalo do barramento PCIe |
| | 4 | Processos, threads, GIL do Python, `multiprocessing` e hierarquia CUDA (Warp/Bloco/Grade) |
| | 5 | IPv4/IPv6, TCP vs. UDP, SSH, `scp` e `rsync` para grandes datasets |
| | 6 | Linux (`/proc`, `/sys`, `/dev`), `tmux`/`screen`, `cron`, `systemd` e monitoramento de GPU |
| **2 — Programação e Heterogeneidade** | 7 | Kernels CUDA, índices (`blockIdx`, `threadIdx`), `cuda.synchronize()` |
| | 8 | Tiling, memória compartilhada, coalescing, `cuda.event`, Nsight Systems e nvprof |
| | 9 | OpenCL, PyOpenCL, JIT, portabilidade multi-vendor e seus trade-offs |
| | 10 | ROCm, HIP, `rocminfo`, Docker com GPUs AMD e o problema do *vendor lock-in* |
| | 11 | Treinamento de modelos (ResNet), throughput, VRAM, Mixed Precision (FP16), W&B e TCO |
| | 12 | Latência RAM ↔ VRAM, prototipagem no Colab e validação prática |
| | 13 | Python puro vs. NumPy vs. CUDA Numba vs. CuPy, limiar de compensação da GPU e curva de speedup |

---

## 💡 Como Escolher o Tema

Um bom tema de Projeto Integrador tem três características:

1. **É um problema real** do seu setor (ou de um setor que você queira estudar).
2. **Envolve dados em volume relevante** (imagens, textos, áudio, sensores, prontuários, contratos, etc.).
3. **Permite comparar alternativas de arquitetura** (nuvem vs. local, CPU vs. GPU, NVIDIA vs. AMD, centralizado vs. distribuído).

Você **não precisa implementar** o modelo. O foco é a **solução proposta**, a **arquitetura que a sustenta** e a **justificativa das escolhas**.

---

## 🚀 Banco de Temas por Área de Atuação

> Escolha um tema da sua área (ou proponha outro). Os títulos são pontos de partida; você pode adaptá-los.

### 💼 Gestão, Negócios e Finanças
1. Arquitetura para um chatbot de atendimento com LLMs: nuvem pública vs. servidor local — análise de custo e latência.
2. Detecção de fraudes em transações em tempo real: processamento em CPU vs. GPU e impacto do TCP vs. UDP na captura de eventos.
3. Previsão de demanda e estoque com redes neurais: dimensionamento de VRAM e estratégia de batches.
4. Análise de risco de crédito com modelos tabulares: quando a CPU ainda é suficiente e por quê.
5. Sistema de recomendação para e-commerce: pipeline de treino diário em GPU agendado via `cron`/`systemd`.

### 🏥 Saúde e Bem-Estar
6. Sumarização local de prontuários com privacidade garantida: por que não enviar dados sensíveis para a nuvem pública.
7. Diagnóstico por imagem (raios-X, ressonância) em GPU: comparativo CUDA vs. ROCm para um hospital de médio porte.
8. Triagem de exames em lote com Tiling e memória compartilhada: reduzindo o tempo de processamento.
9. Telemedicina e telemetria de sinais vitais: por que UDP é mais adequado que TCP nesse cenário.
10. Monitoramento de pacientes com modelos de borda (edge): RISC vs. CISC e consumo de energia.

### 🎨 Design, Mídia e Comunicação
11. Processamento paralelo de imagens em lote para uma agência de marketing: CPU vs. GPU.
12. Geração e edição de vídeo com IA: gargalo de armazenamento, PCIe e VRAM em projetos longos.
13. Transcrição e legendagem automática de podcasts: pipeline com CPU (pré-processamento) e GPU (inferência).
14. Restauração de acervos fotográficos antigos: análise de memória e custo de manter um servidor dedicado.
15. Moderação de conteúdo em redes sociais: throughput, latência e escalabilidade horizontal.

### 📚 Educação, RH e Treinamento
16. Tutor inteligente para apostilas e normas internas com modelos abertos rodando localmente.
17. Correção automática de redações: arquitetura, privacidade dos alunos e custo por correção.
18. Análise de clima organizacional a partir de pesquisas abertas: NLP em GPU vs. CPU.
19. Plataforma de aprendizagem adaptativa: dados de interação, redes e transferência entre servidores.
20. Gamificação com visão computacional em salas de aula: processamento de borda e energia.

### ⚖️ Jurídico, Compliance e Segurança
21. Análise local de contratos com extração de entidades: modelos quantizados e soberania de dados.
22. Monitoramento de conformidade com LGPD: onde os dados podem trafegar e como protegê-los via SSH e subredes.
23. Investigação forense digital com grandes volumes de documentos: `rsync`, armazenamento e GPU.
24. Detecção de anomalias em logs de segurança: streaming via UDP e processamento em tempo real.
25. Reconhecimento facial ético e regulado: implicações de energia, viés e escolha de hardware.

### 🏭 Indústria, Agricultura e Logística
26. Inspeção de qualidade em linha de produção com visão computacional: latência de borda e NVIDIA vs. AMD.
27. Agricultura de precisão com drones: processamento de imagens de borda vs. nuvem.
28. Manutenção preditiva com sensores IoT: MQTT/UDP, volume de dados e capacidade de processamento.
29. Otimização de rotas de entrega com GPU: benchmark e curva de speedup aplicada.
30. Gêmeos digitais (digital twins) de fábricas: SIMD, memória e simulação em larga escala.

### 🌱 Meio Ambiente, Energia e Cidades
31. Previsão meteorológica com dados massivos: FFT, GPU e custo energético.
32. Monitoramento de desmatamento por satélite: transferência de datasets gigantes e `rsync`.
33. Eficiência energética em data centers de IA: Green AI e impacto da memória global.
34. Mobilidade urbana inteligente: processamento de vídeo de câmeras e latência de rede.
35. Detecção de vazamentos em redes de água: modelos leves em borda e CPU.

### 🔬 Ciência, Games e Tecnologia
36. Simulação científica com CUDA: matrizes, tiling e comparação com OpenCL.
37. Treinamento de agentes de jogos com aprendizado por reforço: ciclos de GPU e throughput.
38. Análise de partículas em laboratório: portabilidade ROCm/AMD vs. CUDA/NVIDIA.
39. Renderização 3D com traçado de raios: paralelismo massivo e papel dos Warps.
40. Pesquisa acadêmica reproduzível: como montar um ambiente Linux estável para experimentos longos.

---

## 🗂️ Roteiro de Pesquisa Sugerido

O trabalho pode ser escrito como um **relatório de pesquisa**. Estruture a investigação em cinco etapas:

### 1. Contexto e Problema
- Descreva o cenário escolhido e o problema de IA que ele envolve.
- Explique **por que** a demanda computacional é relevante (volume de dados, frequência de execução, número de usuários).
- Apresente as **fontes de pesquisa** consultadas (artigos, documentações, estudos de caso, reportagens técnicas).

### 2. Processamento e Arquitetura
- O workload é predominantemente **sequencial (CPU)** ou **paralelo massivo (GPU/SIMD)**? Justifique.
- Que **modelo de execução** é mais adequado (SIMD, MIMD) e qual o papel do RISC/CISC na escolha do ambiente?
- Discuta o impacto da escolha no **consumo de energia** e no custo.

### 3. Memória e Comunicação
- Estime as necessidades de **RAM e VRAM** e o risco de *Out Of Memory*.
- Explique onde está o provável **gargalo** (barramento PCIe, disco, latência de rede, etc.).
- Descreva como os dados **chegam** à arquitetura da solução (TCP para integridade, UDP para telemetria, `scp`/`rsync` para datasets).
- Explique como o ambiente **Linux** seria configurado e monitorado (`tmux`/`screen`, `cron`/`systemd`, `/proc`, `/sys`, `nvidia-smi`).

### 4. Aceleração e Portabilidade
- Discuta as estratégias de aceleração relevantes: **kernels CUDA, tiling, memória compartilhada, coalescing**.
- Avalie as alternativas de **portabilidade**: OpenCL e ROCm/HIP frente ao CUDA.
- Analise os *trade-offs*: **desempenho, ecossistema, maturidade, custo e dependência de fabricante** (*vendor lock-in*).

### 5. Medição e Decisão Final
- Proponha como **medir** os resultados: throughput, uso de VRAM, tempo por época, energia e custo.
- Descreva o **limiar de compensação da GPU**: em que ponto a aceleração passa a valer a pena?
- Apresente sua **recomendação final** de arquitetura, com argumentos técnicos, financeiros e estratégicos.
- Aponte **riscos, limitações** e alternativas caso o cenário mude.

> **Dica:** Um bom projeto cita números e fontes. Sempre que afirmar “a GPU é mais rápida” ou “a AMD é mais barata”, traga um dado ou um estudo que sustente a afirmação.

---

## 📦 Formato da Entrega

O projeto pode ser desenvolvido **individualmente ou em dupla** e entregue em um dos formatos abaixo:

1. **Relatório de pesquisa (PDF ou Word):** 6 a 10 páginas, seguindo o roteiro sugerido.
2. **Apresentação de slides (PDF ou PowerPoint):** 8 a 15 slides, com tempo de defesa curta.
3. **Vídeo-podcast/aula (opcional, combinado com o professor):** 5 a 10 minutos apresentando o cenário e a recomendação.

Em todos os formatos, inclua:
- Identificação do tema e do setor;
- O roteiro de pesquisa desenvolvido;
- **Referências bibliográficas** (links, artigos, documentações oficiais);
- **Declaração de uso de IA** (se e como utilizou ferramentas de IA na elaboração).

> **Importante:** O uso de código/notebooks é **opcional**. Se você quiser complementar a pesquisa com uma demonstração prática, pode usar como base os notebooks das Aulas 12 e 13 — mas isso **não é obrigatório**.

---

## 🗓️ Entregas Parciais (Acompanhamento)

As datas e o formato de acompanhamento serão definidos pelo professor. Como sugestão de processo:

1. **Definição do tema** — escolha do cenário e problema.
2. **Roteiro de pesquisa** — fontes iniciais e estrutura do trabalho.
3. **Versão preliminar** — desenvolvimento dos pilares técnicos.
4. **Entrega final e apresentação** — recomendação fundamentada.

---

## ✅ Boas Práticas de Pesquisa

- Prefira **fontes primárias**: documentações oficiais (NVIDIA, AMD, Khronos), artigos e estudos de caso.
- **Compare evidências conflitantes** em vez de apenas reproduzir o senso comum.
- Separe **fato** (dado mensurável) de **opinião** (interpretação).
- Explique os conceitos da UC **com suas palavras**, aplicando-os ao seu cenário.
- Seja honesto sobre **incertezas e limitações** do seu estudo.

---

> **Mensagem final:** O melhor profissional de IA não é apenas quem conhece os modelos, mas quem entende a **arquitetura** que os sustenta e toma decisões capazes de alinhar **desempenho, custo, energia e soberania de dados**. Este projeto é a oportunidade de praticar exatamente isso.
