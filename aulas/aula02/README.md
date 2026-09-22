# 🧮 Aula 02 — Modelos de Processamento: SIMD, MIMD, RISC e CISC

**Objetivo:** reconhecer modelos de processamento paralelo (**SIMD** e **MIMD**) e
instrucionais (**RISC** e **CISC**) e aplicá-los na escolha de hardware para **IA
embarcada**.

---

## 🎯 Situação de aprendizagem

Sua equipe avalia placas de desenvolvimento — **Raspberry Pi** (ARM/RISC) vs.
**NVIDIA Jetson** (ARM + GPU) — para um projeto de **visão computacional embarcada** que
precisa identificar objetos **em tempo real** numa câmera industrial. Antes de comprar,
é preciso entender como cada arquitetura afeta **desempenho** e **consumo de energia**.

---

## 🗂️ Conteúdo

| Arquivo | O que é |
| :--- | :--- |
| [`apresentacao_aula02.html`](apresentacao_aula02.html) | Slides teóricos (abra no navegador, navegue com ← →) |
| [`aula02_modelos_processamento.ipynb`](aula02_modelos_processamento.ipynb) | Notebook do **Google Colab** (SIMD, RISC/CISC e estudo de imagem) |
| [`atividade.md`](atividade.md) | Atividade guiada (QEMU/emulação) + discussão em grupo |
| `scripts/` | Scripts comentados que rodam no **Colab** e no **Windows com GPU AMD** |

### Scripts

| Script | O que faz |
| :--- | :--- |
| [`lib_backend.py`](scripts/lib_backend.py) | Detecta o backend (CuPy → PyTorch CUDA → DirectML → NumPy) |
| [`benchmark_simd.py`](scripts/benchmark_simd.py) | Sequencial vs. SIMD (NumPy) + GPU, se houver |
| [`estudo_imagem.py`](scripts/estudo_imagem.py) | Imagem 1080p: loop por pixel vs. vetorizado (SIMD + MIMD) |
| [`arquitetura_instrucoes.py`](scripts/arquitetura_instrucoes.py) | Identifica RISC/CISC e lista os recursos SIMD da CPU |

---

## 🚀 Como rodar

### No Google Colab (recomendado)

1. Abra `aula02_modelos_processamento.ipynb` pelo **GitHub** no Colab
   (`https://github.com/jonasmaffei/senac-tecnico-ia`).
2. *Runtime ➔ Change runtime type ➔ **T4 GPU*** ➔ *Save*.
3. Rode as células na ordem.

> 💡 **Sem GPU?** O notebook detecta e cai para **NumPy (SIMD na CPU)** — a comparação
> sequencial vs. vetorizado funciona igual.

### No Windows do laboratório (GPU AMD)

```bat
cd aulas\aula02\scripts
python benchmark_simd.py
python estudo_imagem.py
python arquitetura_instrucoes.py
```

> O mesmo código roda nos dois ambientes: ele detecta o backend em tempo de execução.
> Requer apenas **NumPy** (`pip install numpy`); CuPy/PyTorch são opcionais.

---

## 🔑 Conceitos-chave

### Taxonomia de Flynn

| Modelo | Instruções | Dados | Exemplo |
| :--- | :--- | :--- | :--- |
| **SISD** | 1 | 1 | CPU clássica sequencial |
| **SIMD** | 1 | Múltiplos | GPU, AVX/SSE, NumPy |
| **MISD** | Múltiplas | 1 | Raro (pipelines especializados) |
| **MIMD** | Múltiplas | Múltiplos | CPU multi-core, clusters |

- **SIMD** — uma instrução aplicada a **muitos dados** de uma vez (vetores, imagens, matrizes).
- **MIMD** — várias instruções sobre vários dados; cada núcleo faz uma tarefa diferente.

### RISC vs. CISC

| | RISC | CISC |
| :--- | :--- | :--- |
| Instruções | Simples, **tamanho fixo** | Complexas, **tamanho variável** |
| Pipeline | Eficiente e previsível | Mais complexo |
| Energia | Menor consumo | Maior consumo |
| Exemplos | **ARM** (Raspberry Pi, smartphones, Apple Silicon) | **x86/x64** (Intel, AMD) |
| Onde brilha | Embarcados, mobile | Desktops, servidores |

> 🍏 **Curiosidade:** os chips **Apple Silicon (M1/M2/M3)** são RISC (ARM) e superam
> muitos x86 em **performance por watt**.

### GPU = SIMD + MIMD
Dentro de um **warp** (32 threads) a instrução é a mesma → **SIMD**. Vários **blocos/SMs**
processam pedaços diferentes ao mesmo tempo → **MIMD**.

---

## 🧪 Atividade guiada (QEMU / emulação)

No Colab/Linux é possível **ver** a arquitetura:

```bash
cat /proc/cpuinfo | grep "model name" | head -1   # x86 (CISC) vs. ARM (RISC)
objdump -d /bin/ls | head -30                     # RISC=tamanho fixo; CISC=variável
```

O **QEMU** emula outra arquitetura (ex.: ARM) num PC x86 — útil para comparar o formato
das instruções. Detalhes e exercícios em [`atividade.md`](atividade.md).

---

## 💬 Discussão em grupo

1. **Raspberry Pi** (ARM/RISC) ou **NVIDIA Jetson** (ARM + GPU) para visão computacional em tempo real?
2. Em que situações o **CISC (x86)** ainda vence o RISC (ARM)?
3. Um smartphone usa GPU para games. Por que ela também serve para **reconhecimento facial**?
4. Se SIMD acelera tanto, por que não colocamos SIMD em **tudo**?

---

## 📌 Tarefa de casa (opcional)

Compare **NVIDIA Jetson Nano** × **Raspberry Pi 4** para o projeto de visão computacional
embarcada: núcleos de CPU/GPU, suporte a SIMD/CUDA, consumo em watts, preço e
disponibilidade.

---

## 🔗 Relação com o curso

- **Aula 1** trouxe Von Neumann/Harvard e CPU vs. GPU; esta aula explica **como** cada um
  processa (paralelismo e conjunto de instruções).
- **Próxima (Aula 3):** *Estrutura de Memória em GPUs* — onde os dados ficam e por que o
  barramento é o próximo gargalo.
