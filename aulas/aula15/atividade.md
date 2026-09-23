# Atividade: Aula 15 — Gestão de Processos e Carga de Trabalho

## Parte 1 — Atividade guiada: a fila de GPU na prática

No **laboratório Windows** (`laboratorio_windows/`), rode o experimento principal:

```bash
cd aulas/aula15/laboratorio_windows
chmod +x *.sh
./teste_fila.sh          # lança 4 jobs e mostra a fila serializando por prioridade
```

Em outro terminal Git Bash, monitore em tempo real:

```bash
./monitor_gpu_proc.sh
```

Registre: a **ordem** em que os jobs executaram e se ela correspondeu à prioridade.

---

## Parte 2 — Discussão em grupo (3 a 4 pessoas)

No cenário de **1 GPU e 4 alunos**:

1. Por que dois jobs na mesma GPU podem causar **CUDA OOM** e **corromper resultados**?
2. Como a **fila por prioridade** garante uso justo? O que é *starvation*?
3. Qual a diferença entre **`flock`** (laboratório) e **systemd** (produção)?
4. Além da GPU, que outros recursos (disco, memória, rede) também precisam de controle de
   concorrência num servidor de IA?

---

## Parte 3 — Pesquisa (tarefa de casa)

1. Execute o `teste_fila.sh` com 4 jobs e observe a ordem por prioridade.
2. Adicione um **5º job de prioridade 1 após 30 s** e verifique se ele "passa à frente" dos de
   prioridade 2 e 3.
3. Integre o monitor (`monitor_gpu_proc.sh`) ao pipeline de monitoramento da Aula 14.
4. **Bônus:** implemente **aging** — jobs aguardando mais de 10 minutos sobem de prioridade
   automaticamente.

> **Dica:** a fila usa o padrão `prioridade_timestamp_nome`. Como o `sort` é lexicográfico,
> `1_...` (alta) vem antes de `2_...` (média) antes de `3_...` (baixa); o *timestamp* garante
> FIFO dentro da mesma prioridade.
