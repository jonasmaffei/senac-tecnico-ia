# Questionário de Revisão — Aulas 14 a 19
## Introdução a Arquitetura de Computadores

> **Status:** 📤 Para entrega.
>
> **Entrega:** Envie as respostas por e-mail para **`03049691093@senacrs.edu.br`**.
> **Assunto do e-mail:** `Questionario aulas 14 a 19`
>
> **Instruções:** Responda às questões abaixo de forma fundamentada, conectando os conceitos de
> **operação e automação de GPUs** vistos no Bloco 3.

---

### Aula 14 — Automação de GPUs com Bash
> **Situação:** O servidor de treinamento da empresa ficou travado de madrugada — a GPU passou de
> 95 °C e o job falhou silenciosamente. Ninguém percebeu até o dia seguinte. Você deve montar um
> monitoramento automático **24h/7d** que colete métricas da GPU, gere alertas e publique um
> relatório.

1. O que a opção `nvidia-smi --query-gpu` permite extrair, e por que a flag
   `--format=csv,noheader,nounits` é ideal para alimentar um script de coleta?
2. Qual é o papel de cada script: um que **coleta** métricas para CSV (`monitor_gpu.sh`) e
   outro que **alerta** quando um limite é ultrapassado (`alerta_gpu.sh`)?
3. Compare `cron` e `systemd timers` como agendadores: cite uma vantagem de cada um e uma
   situação em que você escolheria o `systemd timer`.

### Aula 15 — Gestão de Processos e Carga de Trabalho
> **Situação:** O laboratório tem **1 GPU** e **4 alunos** treinando ao mesmo tempo. Sem
> controle, os jobs competem pela VRAM, geram **CUDA OOM** e corrompem resultados. Você deve
> garantir uso justo da GPU sem Slurm nem Kubernetes.

4. O que é uma **race condition** nesse cenário, e por que ela pode causar `CUDA Out of Memory`
   e resultados incorretos?
5. Explique como o `flock` (ou o **lock por diretório** no Windows) garante **exclusão mútua**,
   e o que as flags `-n` (*non-blocking*) e `-w` (*timeout*) mudam no comportamento.
6. Como funciona a **fila por prioridade** baseada em tickets (`prioridade_timestamp_nome`), e
   por que é necessário o **aging** para evitar *starvation* de jobs de baixa prioridade?

### Aula 16 — Agentes de Código, Contexto e `AGENTS.md`
> **Situação:** Para acelerar o time, a empresa adotou um **agente de código** no terminal. É
> preciso usá-lo com segurança, mantendo o controle de qualidade e o histórico no Git.

7. O que é o **harness** de um agente de código e qual é o papel da **janela de contexto**
   (e do "contexto demais") no desempenho do agente?
8. O que é o arquivo **`AGENTS.md`** e por que centralizar as regras do projeto nele é melhor
   do que repetir instruções a cada prompt?
9. Por que o **GitHub** funciona como "rede de segurança" ao trabalhar com agentes de IA que
   editam arquivos automaticamente? Relacione com os comandos `diff`, `commit` e `push`.

### Aula 17 — Automação de GPUs com Python
> **Situação:** Parte da equipe usa **Windows** e **Colab**, onde não há `cron` nem `gnuplot`.
> É preciso o **mesmo monitoramento** da Aula 14, mas em Python e portátil.

10. Como o Python pode consultar as métricas da GPU (por exemplo, via `subprocess`) e por que
    isso é útil em ambientes sem servidor Linux?
11. O que substitui o `cron` e o `gnuplot` na versão Python (agendamento e visualização)?
12. Quais são as vantagens e as limitações de reimplementar em Python o pipeline que a Aula 14
    fazia em Bash?

### Aula 18 — Concorrência: Lock e Fila em Python
> **Situação:** No laboratório Windows não existe `flock`. Você precisa reproduzir a exclusão
> mútua e a fila por prioridade **sem** os recursos do Linux.

13. Por que criar uma pasta com `os.mkdir` funciona como um **lock atômico**, e como o código
    sabe que a GPU está ocupada quando a pasta já existe?
14. No experimento de 4 jobs concorrentes, por que a **fila** (ticket por prioridade) é
    necessária além do lock? O que aconteceria sem ela?
15. Como o **lock** e a **fila** se combinam para garantir que os jobs executem um por vez, na
    ordem certa, sem OOM?

### Aula 19 — Energia: TDP, Power Limit e Eficiência
> **Situação:** A auditoria apontou que o cluster consome **40% mais energia** que o projetado:
> as GPUs operam no TDP máximo mesmo em fases de baixa carga. Você deve medir, limitar e
> monitorar o consumo.

16. O que são **TDP/TGP** e **thermal throttling**, e por que uma GPU quente pode gastar mais
    energia **e** entregar menos desempenho?
17. O que é o **Power Limit** (`nvidia-smi -pl`) e por que reduzir o PL em ~20–30% costuma
    custar pouco throughput? O que é a métrica de **eficiência (imgs/J)** e onde costuma estar
    o ponto ótimo?
18. Como um **alerta térmico com ação** (agendado no `cron`) pode, ao cruzar o limite crítico,
    reduzir automaticamente o Power Limit e restaurá-lo quando a temperatura normaliza?
