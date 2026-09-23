# 🧠 Aula 03 — Estrutura de Memória em GPUs

**Objetivo:** interpretar a **hierarquia de memória** nas GPUs e identificar como ela impacta
o desempenho de aplicações de IA, permitindo otimizações eficazes no uso de **registradores**,
**memória compartilhada** e **memória global**.

---

## 🎯 Situação de aprendizagem

O modelo de IA da startup está com um **gargalo de desempenho** durante o treinamento: a GPU
fica ocupada apenas **40% do tempo**, mesmo com dados disponíveis. A suspeita da equipe é de
**uso ineficiente da memória da GPU**. Você precisa diagnosticar o problema — entender como a
memória é organizada na GPU — e propor melhorias concretas para aumentar a utilização do
hardware.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula03.html`](apresentacao_aula03.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** com explicação + **5 exercícios** |
| [`laboratorio_windows/`](laboratorio_windows/README.md) | **Experimentos com hardware real** (`iniciar.bat`) |
| [`atividade.md`](atividade.md) | Atividade guiada (monitoramento) + discussão em grupo |

### Estrutura da aula

```
aula03/
  apresentacao_aula03.html
  README.md
  notebook_colab/aula03_memoria_gpu.ipynb
  laboratorio_windows/          # 1_benchmark_ram_vram.py, 2_hierarquia_memoria.py, 3_monitor_memoria.py, lib_backend.py
  atividade.md
```

---

## 🚀 Como rodar

### No Google Colab (notebook + 5 exercícios)

1. Abra `notebook_colab/aula03_memoria_gpu.ipynb` pelo **GitHub** no Colab
   (`https://github.com/jonasmaffei/senac-tecnico-ia`).
2. *Runtime ➔ Change runtime type ➔ **T4 GPU*** ➔ *Save*.
3. Rode as células na ordem.

> 💡 **Sem GPU?** O notebook detecta e entra em **modo simulado** — a aula roda do começo ao
> fim e ainda mostra a hierarquia pela própria RAM da CPU.

### No Windows do laboratório (hardware real)

Dê **duplo clique** em [`laboratorio_windows/iniciar.bat`](laboratorio_windows/iniciar.bat):

```
[1] 1_benchmark_ram_vram.py  - RAM (CPU) vs. VRAM (GPU) + custo do PCIe
[2] 2_hierarquia_memoria.py  - a piramide de latencia na pratica
[3] 3_monitor_memoria.py     - diagnostico de memoria (nvidia-smi/RAM)
[0] Sair
```

> O mesmo código roda nos dois ambientes: ele detecta o backend em tempo de execução.
> Detalhes em [`laboratorio_windows/README.md`](laboratorio_windows/README.md).

---

## 🔑 Conceitos-chave

### A hierarquia de memória da GPU

| Nível | Latência | Tamanho | Escopo |
| :--- | :--- | :--- | :--- |
| **Registradores** | ~1 ciclo | ~256 KB / SM | por thread |
| **Shared (SRAM)** | ~1–5 ciclos | ~48–164 KB / bloco | por bloco |
| **Cache L1 / L2** | ~20–50 ciclos | L1 ~128 KB, L2 ~6 MB | automático |
| **VRAM Global** | ~400–800 ciclos | 8–80 GB | toda a GPU |
| **RAM do host** | milhares de ciclos | 16–512 GB | CPU (via PCIe) |

> **Regra 90/10:** ~90% do tempo de processamento em IA é gasto **esperando memória**, não
> calculando.

### RAM vs. VRAM

| Característica | RAM (DDR5) | VRAM (HBM3 / GDDR6) |
| :--- | :--- | :--- |
| Largura de banda | ~80 GB/s | ~3.35 TB/s (HBM3) |
| Capacidade típica | 16–512 GB | 4–80 GB |
| Controlador | CPU | GPU |
| Transferência CPU↔GPU | Via **PCIe** (~32 GB/s) | Interna na GPU (muito rápido) |

### O gargalo do PCIe

O PCIe 4.0 x16 oferece ~**32 GB/s** — cerca de **100× mais lento** que a largura de banda
interna da VRAM. Por isso, **copiar** dados da RAM para a GPU pode custar mais que o próprio
cálculo. **Minimize o tráfego PCIe:** mantenha os batches na VRAM e só traga o resultado no
final.

---

## 🧪 Atividade guiada (monitoramento)

No Colab/Linux é possível **medir** antes de otimizar:

```bash
watch -n 1 nvidia-smi                                        # painel ao vivo
nvidia-smi --query-gpu=memory.used,memory.total --format=csv # memória
nvidia-smi --query-compute-apps=pid,used_memory --format=csv # por processo
```

No **Windows/AMD**, use `python scripts/monitor_memoria.py` para ver a RAM do host e o exemplo
do painel. Detalhes e exercícios em [`atividade.md`](atividade.md).

---

## 💬 Discussão em grupo

Retomando a situação da startup (**GPU a 40%**), em grupos de 3–4:

1. Se a GPU está ociosa 60% do tempo, qual é a causa mais provável? (Dica: PCIe.)
2. Qual memória priorizar numa multiplicação de matrizes 4096×4096?
3. Um LLM de 70B parâmetros precisa de ~140 GB em FP32. Como resolver a VRAM insuficiente?
4. Quando faz sentido usar memória compartilhada vs. apenas a global?

---

## 📌 Tarefa de casa (opcional)

Pesquise **quantização de modelos** (FP32 → FP16 → INT8) e explique como ela reduz o uso de
VRAM sem comprometer muito a acurácia:

- Quantos parâmetros cabem em **16 GB** de VRAM em **FP16** vs. **FP32**?
- O que é *mixed precision training* (`torch.cuda.amp`)?
- Qual o impacto na acurácia de modelos quantizados?

---

## 🔗 Relação com o curso

- **Aula 2** mostrou **como** CPU e GPU processam (SIMD/MIMD, RISC/CISC). Esta aula revela o
  **verdadeiro vilão** de performance: entregar dados pela rodovia **PCIe/VRAM**, e não a
  falta de cálculo no SIMD.
- **Próxima (Aula 4):** *Processos e Threads* — quem despacha os lotes do sistema operacional
  para o barramento sem travar o processador enquanto a GPU espera dados.
