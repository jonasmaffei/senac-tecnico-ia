# Questionário de Revisão — Aulas 1 a 7
## Introdução a Arquitetura de Computadores


> **Instruções:** Utilize o resumo consolidado das aulas como guia de consulta, focando na aplicação prática e na visão de negócios.

---

### BLOCO 1: FUNDAMENTOS

#### Aula 1: Quem Faz o Quê? (CPU vs. GPU)
1. Qual é a principal diferença funcional, apresentada na analogia da aula, entre a CPU (o cérebro central) e a GPU (a placa de vídeo)?
2. Por que as CPUs tradicionais não conseguem atender sozinhas à demanda pesada de processamento exigida pelo treinamento de modelos modernos de Inteligência Artificial?
3. Na visão de infraestrutura de uma empresa, o que define a escolha entre utilizar o poder de uma CPU ou de uma GPU para uma determinada tarefa computacional?

#### Aula 2: Como Eles Trabalham? (Organização do Trabalho)
4. Explique como funciona o modelo SIMD (Sincronia Total) utilizado pelas GPUs, comparando-o com a dinâmica de uma equipe de trabalho.
5. Qual é a principal vantagem da arquitetura de processamento RISC (com instruções simples e padronizadas) em comparação à CISC na fabricação de dispositivos modernos?
6. Como a escolha entre arquiteturas voltadas para eficiência energética (como em dispositivos móveis) impacta o desenvolvimento de soluções em tecnologia?

#### Aula 3: A Logística e a Memória (Por que a IA fica lenta?)
7. O que é o "gargalo da rodovia" mencionado ao discutir a transferência de dados entre a memória RAM e a VRAM da placa de vídeo?
8. Descreva a diferença prática entre os registradores (na mão do operário) e a Memória Global/VRAM dentro da hierarquia de memória da GPU.
9. Por que a lentidão na busca de informações em camadas de memória distantes pode prejudicar a performance geral de um algoritmo de Inteligência Artificial?

#### Aula 4: Como a Máquina Divide o Trabalho (Processos vs. Threads)
10. Qual é a principal diferença de segurança e custo operacional entre abrir um novo "Processo" e alocar novas "Threads" em um sistema computacional?
11. O que é o GIL (Global Interpreter Lock) na linguagem Python e de que maneira ele restringe o aproveitamento de múltiplos núcleos em processamentos pesados por threads?
12. O que ocorre com o desempenho de uma GPU quando o fluxo de processamento paralelizável sofre com a chamada "Divergência" (excesso de desvios condicionais do tipo "se/senão")?

#### Aula 5: A Logística e a Comunicação da I.A. (Redes e Transferência)
13. Explique por que a escassez de endereços no padrão IPv4 gerou a necessidade urgente de migração para o IPv6 no ecossistema de grandes data centers.
14. Qual é o critério técnico e de negócio que define quando uma aplicação deve optar pelo protocolo de transporte TCP em detrimento do UDP?
15. Ao transferir um volume massivo de dados (como centenas de gigabytes) para um servidor em nuvem, por que a utilização da ferramenta `rsync` é financeiramente e operacionalmente superior ao uso de ferramentas tradicionais como o `scp`?

#### Aula 6: Sistemas Operacionais Linux e Gerenciamento de GPU
16. Qual é a função dos diretórios virtuais `/proc` e `/sys` no sistema operacional Linux para a administração de servidores de infraestrutura?
17. Por que ferramentas como `screen`, `tmux` ou `nohup` são consideradas essenciais para profissionais que gerenciam treinamentos longos de I.A. em servidores remotos via SSH?
18. Qual é a utilidade prática do agendador de tarefas `cron` combinado com o `systemd` na rotina de manutenção de um ambiente produtivo de GPUs?

---

### BLOCO 2: PROGRAMAÇÃO

#### Aula 7: Introdução ao Modelo CUDA
19. O que é um *kernel* dentro da plataforma de computação paralela CUDA desenvolvida pela NVIDIA?
20. Como a hierarquia CUDA organiza o problema computacional utilizando Grades (Grids), Blocos (Blocks) e Threads individuais controladas por índices?
21. Por que a etapa de sincronização (`cuda.synchronize()`) é obrigatória antes de transferir de volta os dados processados na VRAM para a memória da CPU?
