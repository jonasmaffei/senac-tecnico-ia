# 🖥️ Laboratório Windows Host: Energia e Térmica de GPU (Aula 19)

Este laboratório permite **medir temperatura/potência**, gerar **alertas térmicos**,
estimar a **eficiência por Power Limit** e demonstrar o **controle programático** da
GPU — tudo no host Windows, sem Docker ou Linux.

> ⚠️ No laboratório a GPU é **AMD**: o Windows não expõe temperatura/potência pelo
> `nvidia-smi`. Por isso o laboratório detecta o backend e, quando não há sensor,
> usa o **modo simulado** com valores plausíveis. Em servidor **Linux + NVIDIA**, os
> mesmos scripts leem os sensores reais.

---

## 🗂️ Estrutura da pasta

```
laboratorio_windows/
├── iniciar.bat               # Menu interativo (cria .venv e roda os scripts)
├── requirements.txt          # matplotlib + nvidia-ml-py
├── lib_energia.py            # Detecção de backend + modelo de consumo/eficiência
├── 1_monitor_thermal.py      # Coleta temp/potência/clock em reports/gpu_thermal.csv
├── 2_alerta_termico.py       # Analisa o CSV e grava alertas em reports/
├── 3_benchmark_energia.py    # Trade-off throughput x eficiência (gráfico PNG)
├── 4_controle_pl.py          # Demonstra o ajuste de Power Limit via NVML
└── README.md                 # Este guia
```

---

## 🚀 Como executar

1. Dê **duplo clique** em `iniciar.bat`. Ele cria o `.venv`, instala as dependências e
   exibe o menu.
2. Escolha uma das opções:

| Opção | Script | O que faz |
| :---: | :--- | :--- |
| **1** | `1_monitor_thermal.py` | Coleta 6 amostras (a cada 2 s) e grava o histórico em `reports/gpu_thermal.csv` |
| **2** | `2_alerta_termico.py` | Lê o CSV e registra AVISO (≥80 °C) / CRÍTICO (≥88 °C) |
| **3** | `3_benchmark_energia.py` | Estima eficiência por PL e salva `reports/benchmark_energia.png` |
| **4** | `4_controle_pl.py` | Mostra a faixa de PL suportada e demonstra o ajuste |

---

## 🔧 Backend de leitura (detecção automática)

| Backend | Quando | O que é lido |
| :--- | :--- | :--- |
| `nvidia` | Existe `nvidia-smi` | Temp/potência/clock **reais** |
| `amd` | Windows com GPU AMD/Intel | Nome e uso (%) **reais**; temp/potência **estimados** |
| `simulado` | Sem GPU acessível | Valores sintéticos plausíveis |

Forçar um backend (útil em aula):
```bat
set GPU19_BACKEND=simulado
python 1_monitor_thermal.py 1 5
```

---

## 📊 Saídas geradas (`reports/`)

- `gpu_thermal.csv` — histórico incremental das amostras;
- `alertas_termicos.log` — avisos e alertas críticos;
- `benchmark_energia.png` — gráfico throughput × eficiência.

---

## 💡 Conceitos praticados

- **TDP × TGP** e **thermal throttling**;
- **Power Limit** e o ponto ótimo de eficiência (~75% do TDP);
- **Eficiência (imgs/J)** = throughput ÷ potência média;
- **Alertas com ação**: ao cruzar o limite crítico, reduzir o PL automaticamente.
