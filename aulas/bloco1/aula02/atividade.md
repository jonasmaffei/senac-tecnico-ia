# Atividade Guiada: Aula 2 — Modelos de Processamento (SIMD, MIMD, RISC, CISC)

## Parte 1 — Atividade guiada: QEMU e emulação de arquiteturas

O objetivo é **visualizar** a diferença entre RISC e CISC inspecionando a arquitetura da
máquina. Rode no **Colab/Linux** (ou no terminal do laboratório, se disponível).

### Passo 1 — Identificar a arquitetura da CPU

```bash
# x86 (CISC): "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz"
# ARM (RISC): "ARMv7 Processor rev 3 (v7l)"
cat /proc/cpuinfo | grep "model name" | head -1
```

### Passo 2 — Ver o tamanho das instruções

```bash
# Em RISC as instruções têm tamanho fixo; em CISC, variável.
objdump -d /bin/ls | head -30
```

### Passo 3 — Emular ARM com QEMU (opcional, via Docker)

```bash
# Executa um binário ARM num PC x86 para comparar o formato das instruções
docker run --rm --privileged multiarch/qemu-user-static --reset
```

### Exercício de fixação

1. Quantas instruções são necessárias para uma **soma simples** em RISC vs. CISC?
2. O tamanho das instruções é **fixo** ou **variável** em cada arquitetura?
3. Qual arquitetura tem o **pipeline mais previsível**? Por quê?

> No **Windows/AMD**, use `python scripts/arquitetura_instrucoes.py` para identificar o
> tipo (RISC/CISC) e listar os recursos SIMD da CPU (AVX2, SSE4…).

---

## Parte 2 — Discussão em grupo (3 a 4 pessoas)

1. **Raspberry Pi (ARM/RISC) ou NVIDIA Jetson (ARM + GPU):** qual escolher para visão
   computacional em tempo real? Por quê?
2. Em que situações o **CISC (x86)** ainda vence o **RISC (ARM)** em desempenho?
3. Um smartphone usa GPU para games. Por que ela também é útil para
   **reconhecimento facial**?
4. Se o **SIMD** acelera tanto o processamento, por que não colocamos instruções SIMD
   em **tudo**?

---

## Parte 3 — Pesquisa (tarefa de casa, opcional)

Compare o **NVIDIA Jetson Nano** com o **Raspberry Pi 4** para o projeto de visão
computacional embarcada da situação de aprendizagem. Registre:

- Número de núcleos de **CPU** e de **GPU**
- Suporte a **SIMD/CUDA**
- **Consumo energético** (Watts)
- **Preço** e disponibilidade
