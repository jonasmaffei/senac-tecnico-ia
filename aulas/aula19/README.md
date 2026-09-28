# 🌱 Aula 19 — Otimização de Processamento e Uso de Energia em GPUs

**Objetivo:** aplicar técnicas de gerenciamento **térmico e energético** em GPUs —
monitorar temperatura e potência em tempo real, configurar **Power Limits** via
`nvidia-smi`, controlar a GPU programaticamente com **nvidia-ml-py** e implementar
**alertas automáticos** que equilibram desempenho e sustentabilidade em projetos de IA.

Esta aula **fecha o Bloco 3** integrando os três pilares:

```
Aula 17 (automação/telemetria) + Aula 18 (gestão de processos) = Aula 19 (energia)
```

---

## 🎯 Situação de aprendizagem

O data center da instituição recebeu uma notificação de custo energético: o cluster
GPU consome **40% mais energia** do que o projetado. Uma auditoria revelou que as GPUs
operam no **TDP máximo** mesmo durante fases de baixa carga do treinamento. O time
precisa implementar um sistema automático de gerenciamento de potência: medir o consumo
real, calibrar **Power Limits** por fase e criar alertas térmicos.

---

## 🗂️ Conteúdo

| Item | O que é |
| :--- | :--- |
| [`apresentacao_aula19.html`](apresentacao_aula19.html) | Slides **só conceito** (abra no navegador, navegue com ← →) |
| [`notebook_colab/`](notebook_colab) | Notebook do **Google Colab** com explicação + **5 exercícios** |
| [`laboratorio_windows/`](laboratorio_windows/README.md) | **Experimentos no host Windows** (detecta backend e usa modo simulado sem NVIDIA) |
| [`scripts_linux/`](scripts_linux) | Scripts para **servidor Linux + NVIDIA** (monitorar, definir PL, benchmark, alerta) |
| [`atividade.md`](atividade.md) | Atividade prática, discussão e tarefa de casa |

### Estrutura da aula

```
aula19/
  apresentacao_aula19.html
  README.md
  notebook_colab/aula19_energia_gpu.ipynb
  laboratorio_windows/          # lib_energia.py + 1_monitorar, 2_alerta, 3_benchmark, 4_controle_pl
  scripts_linux/                # monitor_thermal.sh, set_power_limit.sh, benchmark_energetico.sh, alerta_termico.sh
  atividade.md
```

---

## 🚀 Como rodar

### No Google Colab (notebook + 5 exercícios)

Abra `notebook_colab/aula19_energia_gpu.ipynb` pelo **GitHub** no Colab. Sem GPU
NVIDIA, o notebook detecta o ambiente e entra em **modo simulado** — todos os conceitos
(coleta, benchmark de eficiência, controle de PL e lock) continuam funcionando.

### No laboratório (Windows Host)

```bat
cd aulas\aula19\laboratorio_windows
iniciar.bat
```

O menu cria o `.venv`, instala as dependências e executa:

1. **Monitorar** temperatura/potência/clock → `reports/gpu_thermal.csv`
2. **Alertas térmicos** (≥80 °C aviso / ≥88 °C crítico) → `reports/alertas_termicos.log`
3. **Benchmark de eficiência** por Power Limit → `reports/benchmark_energia.png`
4. **Controle do Power Limit** (demonstra NVML / faixa suportada)

> 💡 No laboratório a GPU é **AMD** e o Windows não expõe temp/potência pelo
> `nvidia-smi`; o laboratório lê o **uso real** da GPU e estima o resto, ou usa o
> **modo simulado** (`set GPU19_BACKEND=simulado`). Em servidor **Linux + NVIDIA**, os
> scripts em `scripts_linux/` leem os sensores de verdade.

### Em servidor Linux (produção)

```bash
cd aulas/aula19/scripts_linux
chmod +x *.sh
./monitor_thermal.sh 5 60          # coleta temp/potência por 60 s
sudo ./set_power_limit.sh 200      # define PL=200W em todas as GPUs
./benchmark_energetico.sh 250 200 150 100
sudo crontab -e                    # */2 * * * * /opt/scripts/alerta_termico.sh
```

---

## 🔑 Conceitos-chave

- **TDP / TGP** — potência de dissipação projetada × potência total da placa.
- **Power Limit (`-pl`)** — teto configurável; reduzir 20–30% sacrifica ~5–10% de throughput.
- **Thermal Throttling** — queda automática de clock acima de ~83–87 °C.
- **nvidia-ml-py (NVML)** — leitura/controle programático sem parsing de shell.
- **Eficiência (imgs/J)** — throughput ÷ potência média; ponto ótimo em ~75% do TDP.
- **Alertas com ação** — ao cruzar o limite crítico, reduzir o PL automaticamente.

---

## 📌 Tarefa de casa

1. Execute o benchmark energético com pelo menos **4 Power Limits** diferentes.
2. Plote (Matplotlib) **throughput × eficiência** para cada PL e identifique o ponto ótimo.
3. Configure o **alerta térmico** no `cron` e observe o comportamento por 30 minutos.
4. **Bônus:** use `nvidia-ml-py` para ajustar o PL a cada época, com base na temperatura.

---

## 🛠️ Tecnologias e recursos

- [nvidia-smi — Power Management](https://developer.nvidia.com/nvidia-system-management-interface)
- [nvidia-ml-py (PyPI)](https://pypi.org/project/nvidia-ml-py/)
- [NVML Reference](https://docs.nvidia.com/deploy/nvml-api/index.html)
- [Green AI — Paper ACL 2020](https://arxiv.org/abs/1907.10597)
