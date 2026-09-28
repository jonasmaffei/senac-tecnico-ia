# Atividade Guiada: Aula 3 — Estrutura de Memória em GPUs

## Parte 1 — Atividade guiada: medir antes de otimizar

O objetivo é **diagnosticar** o gargalo de memória com números, antes de propor qualquer
otimização. Rode no **Colab** (ou no terminal do laboratório) e registre os resultados.

### Passo 1 — Painel da GPU em tempo real

```bash
# Painel contínuo (atualiza a cada 1 segundo)
watch -n 1 nvidia-smi

# Só o essencial, em CSV (útil para registrar num arquivo)
nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu \
           --format=csv,noheader
```

Observação: com a GPU **ociosa** (utilização baixa), a VRAM usada costuma estar muito abaixo
do total. Anote os dois números.

### Passo 2 — Quem está usando a VRAM

```bash
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv
```

### Passo 3 — A hierarquia na prática (script)

No **Windows/AMD** ou no Colab:

```bash
python scripts/hierarquia_memoria.py     # banda: cache vs. RAM
python scripts/benchmark_ram_vram.py     # RAM vs. VRAM + custo do PCIe
```

### Exercício de fixação

1. Na sua medição, qual foi a **diferença de tempo** entre calcular na RAM e na VRAM?
2. Quanto tempo levou a **transferência RAM→VRAM** em comparação com o cálculo?
3. Se a GPU está ociosa 60% do tempo, o gargalo está no **cálculo** ou na **memória**?
   Justifique com os números que você obteve.

> 💡 A lição: copiar dados pelo **PCIe** (~32 GB/s) pode custar mais que o próprio cálculo.
> A primeira otimização é **reduzir as transferências**.

---

## Parte 2 — Discussão em grupo (3 a 4 pessoas)

Retomando a situação da startup — **GPU ocupada apenas 40% do tempo**:

1. Se a GPU está ociosa 60% do tempo durante o treinamento, qual é a causa mais provável?
   (Dica: pense no PCIe e na transferência CPU→GPU.)
2. Qual tipo de memória (**registradores**, **compartilhada**, **global**) deve ser
   priorizado para uma multiplicação de matrizes **4096×4096**?
3. Um **LLM de 70 bilhões de parâmetros** precisa de ~**140 GB em FP32**. Como você vai
   resolver o problema de **VRAM insuficiente**?
4. Quando faz sentido usar **memória compartilhada** vs. apenas **memória global** numa GPU?

---

## Parte 3 — Pesquisa (tarefa de casa, opcional)

Pesquise sobre **quantização de modelos** (FP32 → FP16 → INT8) e explique como ela reduz o
uso de VRAM sem comprometer muito a acurácia. Registre:

- Quantos parâmetros cabem em **16 GB** de VRAM em **FP16** vs. **FP32**?
- O que é *mixed precision training* (`torch.cuda.amp`)?
- Qual o **impacto na acurácia** de modelos quantizados?
