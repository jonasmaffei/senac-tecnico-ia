# Atividade: Aula 9 — Alternativas ao CUDA: OpenCL

## Parte 1 — Atividade guiada (experimente e observe)

Rode no **Colab** ou no Windows do laboratório:

```bash
python scripts/listar_dispositivos.py     # quais plataformas/dispositivos existem?
python scripts/primeiro_kernel.py         # kernel OpenCL: soma de vetores
python scripts/benchmark_work_groups.py   # CPU vs. GPU e o efeito do work-group
```

Registre: nome do dispositivo, número de compute units, tempo do kernel OpenCL e o speedup vs.
NumPy. Qual `local_size` foi mais rápido no seu hardware?

---

## Parte 2 — Questões conceituais

1. **O Preço da Flexibilidade (JIT):** o OpenCL compila o código no primeiro uso
   (*Just-In-Time*). Num serviço de áudio que precisa processar o primeiro lote sem travar,
   qual é o impacto prático dessa compilação inicial? Como mitigá-lo?
2. **O Mito do "Roda em Tudo":** a Apple depreciou o OpenCL em favor do Metal. Como essa
   movimentação de mercado desafia a premissa de que o OpenCL resolve 100% dos cenários
   multi-hardware?
3. **Visibilidade de Memória:** o OpenCL exige a criação explícita de buffers (`cl.Buffer`). Em
   termos de clareza de engenharia, por que forçar o desenvolvedor a declarar o tráfego de
   dados ajuda a mapear gargalos?
4. **O Dilema do Prazo (MVP):** se o cliente exige entrega em curto prazo (2 semanas) mas o
   hardware de destino é heterogêneo (AMD/Intel), o uso de OpenCL acelera ou retarda o
   *time-to-market* da startup? Justifique.

---

## Parte 3 — Discussão em grupo (3 a 4 pessoas)

No cenário do cliente com GPUs AMD e Intel:

1. Se o cliente tem GPUs AMD e a startup tem NVIDIA, como você estruturaria o projeto para
   manter o **mesmo código-base** funcionando nas duas plataformas?
2. O kernel OpenCL compila em tempo de execução. Quais são as implicações para um sistema de
   produção que processa **áudio em tempo real**?
3. O PyTorch **não suporta OpenCL** diretamente — usa CUDA ou ROCm. Como isso afeta a decisão
   de usar OpenCL para **treinar** modelos de IA?
4. Compare: quando vale a pena usar **OpenCL vs. CUDA**? Cite **3 cenários** onde OpenCL seria
   a melhor escolha.

---

## Parte 4 — Pesquisa (tarefa de casa, opcional)

Porte o kernel de **multiplicação de matrizes com tiling** da Aula 8 (memória compartilhada)
para OpenCL usando memória `__local`:

- Reescreva o kernel CUDA de tiling em **OpenCL C**;
- Use `__local float tile_A[TILE][TILE]` para a memória local;
- Compare os tempos: **CUDA (numba) vs. OpenCL (pyopencl)** para N = 256, 512, 1024;
- Identifique diferenças de desempenho e explique as causas num README.

> **Dica:** o `barrier(CLK_LOCAL_MEM_FENCE)` é o equivalente OpenCL do `cuda.syncthreads()`.
> Assim como no CUDA, são necessárias **duas** barreiras por iteração do tile.
