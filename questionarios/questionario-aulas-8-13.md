# Questionário de Revisão — Aulas 8 a 13
## Introdução a Arquitetura de Computadores

> **Status:** 📤 Para entrega.
>
> **Entrega:** Envie as respostas por e-mail para **`03049691093@senacrs.edu.br`**.  
> **Assunto do e-mail:** `Questionario aulas 8 a 13`
>
> **Instruções:** Responda às questões abaixo de forma fundamentada, conectando os conceitos de processamento heterogêneo e otimização vistos no Bloco 2.

---

### Aula 8 — Manipulação de Memória em CUDA e Tiling
> **Situação:** Seu kernel CUDA está lento e suspeita-se de má gestão de memória compartilhada. Você deve implementar duas versões do kernel (memória global e memória compartilhada), medir com `cuda.event` e analisar com NVIDIA Nsight Systems / nvprof.

1. Qual é a vantagem de carregar os dados em blocos (**Tiling**) para a memória compartilhada antes de calcular? Qual o papel do `cuda.syncthreads()` nesse fluxo?
2. Por que medir kernels com **`cuda.event`** é mais preciso do que usar `time.time()`, e como o *warm-up* influencia a medição?
3. O que o **NVIDIA Nsight Systems** / **nvprof** permite identificar em um kernel? Cite um gargalo comum, como acessos **não coalescidos** à memória global.

### Aula 9 — Alternativas ao CUDA: OpenCL
> **Situação:** Sua empresa quer usar GPUs de diferentes fabricantes (Intel, AMD, NVIDIA) sem depender do CUDA. OpenCL é uma solução multiplataforma.

4. O que torna o **OpenCL** uma alternativa multiplataforma ao CUDA, e como o **PyOpenCL** permite escrever kernels portáveis?
5. O que é a compilação **JIT** (*Just-In-Time*) do OpenCL e qual é o impacto prático dela no primeiro uso do kernel?
6. Compare **OpenCL** e **CUDA** em termos de sintaxe, portabilidade e desempenho. Por que o CUDA ainda domina no ecossistema de IA?

### Aula 10 — Introdução ao ROCm e GPUs AMD
> **Situação:** A equipe adquiriu GPUs AMD para reduzir custos e você deve adaptar os modelos de IA para rodar no ROCm.

7. O que são o **ROCm** e a camada **HIP**, e como o HIP permite portar código escrito para CUDA para GPUs AMD?
8. Qual é o papel do **`rocminfo`** na verificação de compatibilidade e do **Docker** (`rocm/pytorch`) na execução de modelos PyTorch em AMD?
9. Quais são as vantagens e os riscos do ROCm em relação ao CUDA, considerando custo, maturidade do ecossistema e ***vendor lock-in***?

### Aula 11 — Aplicação de Modelos de IA em GPUs NVIDIA e AMD
> **Situação:** Você precisa treinar o mesmo modelo (ex.: ResNet-18) em GPUs NVIDIA e AMD e comparar desempenho, custo e facilidade de uso.

10. Quais métricas devem ser registradas para comparar os dois ambientes (**throughput**, uso de VRAM, tempo por época, energia) e o que cada uma revela?
11. O que é **Mixed Precision (FP16)** e por que essa técnica aumenta o throughput e reduz o consumo de memória durante o treinamento?
12. Quais *trade-offs* (custo do hardware, facilidade de uso, maturidade do ecossistema e dependência de fabricante) devem entrar no relatório técnico ao recomendar NVIDIA ou AMD?

### Aula 12 — Implementação de um Modelo Paralelo Simples
> **Situação:** Você deve demonstrar o poder do paralelismo da GPU com um exemplo didático: multiplicação de vetores.

13. Descreva como implementar a operação vetorial em **CPU (Python puro/NumPy)** e em **GPU (CUDA com Numba)**. Por que a GPU só compensa para valores grandes de $N$?
14. Como gerar o gráfico de **speedup** com Matplotlib e interpretar o ponto em que a curva cruza a linha de **1.0x** (ponto de equilíbrio)?
15. No mini-relatório, como explicar o **overhead de transferência via PCIe** e a necessidade de **warm-up** para justificar o desempenho observado?

### Aula 13 — Síntese: Modelo Paralelo na Prática
> **Situação:** Você comparou quatro implementações (Python puro, NumPy, CUDA Numba e CuPy) de soma vetorial e produto escalar, gerando curvas de speedup e um mini-relatório.

16. Quais são as diferenças de desempenho entre **Python puro, NumPy, CUDA Numba e CuPy**? Em que cenário cada abordagem é mais indicada?
17. Explique como o **produto escalar** é calculado na GPU usando **redução em árvore** (*Tree Reduction*) em memória compartilhada e por que se usa `cuda.atomic.add` ao final.
18. Com base na **curva de speedup**, o que representa o *limiar de compensação* da GPU e quais conclusões um mini-relatório técnico deve apresentar?
