# 📝 Atividade Prática: Aula 19 — Otimização de Processamento e Uso de Energia em GPUs

---

## 🎯 Situação de Aprendizagem

O data center da instituição recebeu uma notificação de custo energético: o cluster GPU
consome **40% mais energia** do que o projetado. A auditoria revelou que as GPUs operam
no **TDP máximo** mesmo durante fases de baixa carga do treinamento. O time precisa
implementar um sistema automático de gerenciamento de potência: medir o consumo real,
calibrar **Power Limits** por fase de treinamento e criar alertas térmicos — tudo via
scripts Bash e Python com `nvidia-smi` e `nvidia-ml-py`.

---

## 🗂️ Roteiro de Execução

Você pode realizar esta atividade no **Google Colab** ou localmente no **Windows Host**.

| Ambiente | Onde abrir | Como executar |
| :--- | :--- | :--- |
| **Google Colab** | [`notebook_colab/aula19_energia_gpu.ipynb`](notebook_colab/aula19_energia_gpu.ipynb) | Execute as células em sequência |
| **Windows Host** | [`laboratorio_windows/iniciar.bat`](laboratorio_windows/iniciar.bat) | Dê duplo clique no `iniciar.bat` |

---

## 🚀 Parte 1 — Monitoramento térmico e energético

1. Execute o coletor por ~15 segundos:
   - No Colab: `!python3 monitor_thermal.py 2 8 gpu_ex1.csv`
   - No Windows: **opção 1** do menu `iniciar.bat`.
2. Abra o CSV e verifique as colunas `temp_c`, `power_w`, `power_limit_w` e `clock_sm_mhz`.
3. Compare a **potência instantânea** com o **limite** configurado da GPU.

---

## 📊 Parte 2 — Power Limit e eficiência (imgs/J)

1. Analise a tabela de trade-off: a cada redução de PL, quanto cai o throughput e
   quanto cai o consumo?
2. No Windows, rode a **opção 3** (`3_benchmark_energia.py`) e observe o gráfico
   `reports/benchmark_energia.png`.
3. Identifique em qual **% do TDP** a eficiência (imgs/J) é máxima.
4. Compare com a heurística vista em aula: o ponto ótimo costuma ficar em **~75% do TDP**.

---

## 🌡️ Parte 3 — Alertas térmicos automáticos

1. Rode a **opção 2** (`2_alerta_termico.py`) e observe os registros em
   `reports/alertas_termicos.log`.
2. Ajuste os limiares (ex.: 70/80 °C) e verifique quantos alertas são gerados.
3. Em servidor Linux, configure o `alerta_termico.sh` no `cron`:
   ```
   sudo crontab -e
   */2 * * * * /opt/scripts/alerta_termico.sh
   ```
4. Explique: por que o script **age** (reduz o PL), e não apenas notifica?

---

## 🎛️ Parte 4 — Controle programático com nvidia-ml-py

1. Rode a **opção 4** (`4_controle_pl.py`) e observe a faixa de Power Limit suportada.
2. Em GPU NVIDIA real, compare ler os dados via `nvidia-smi` (texto) e via NVML
   (Python). Quais são as vantagens do NVML em automações?
3. Proponha um **algoritmo de ajuste dinâmico**: PL alto nas épocas iniciais (maior
   perda) e PL reduzido no refinamento final. Quais riscos existem?

---

## 💬 Parte 5 — Discussão em Grupo (10 min)

Em grupos de 3 a 4 alunos, discutam com base no cenário do data center:

1. Reduzir o Power Limit em 20% sacrifica ~8% de throughput mas economiza ~20% de
   energia. Em um projeto com **deadline em 2 dias**, qual decisão você tomaria? E em
   um projeto de **3 meses**?
2. A eficiência máxima ocorreu com PL a 75% do TDP, assumindo treinamento contínuo. Em
   **inferência (produção)**, o perfil de carga muda — o PL ótimo seria o mesmo?
3. O nvidia-ml-py permite ajustar o PL dinamicamente por época. Proponha um algoritmo
   que aumente o PL nas épocas de maior perda e reduza nas épocas finais de refinamento.
4. Um servidor headless (sem X11) não suporta `nvidia-settings`. Quais alternativas
   existem para ajustar clocks além do Power Limit? Pesquise `nvidia-smi --lock-gpu-clocks`.

---

## 📌 Parte 6 — Tarefa de Casa

Implementar e analisar o benchmark energético completo:

1. Execute o `benchmark_energetico.sh` (ou `3_benchmark_energia.py`) com pelo menos
   4 Power Limits diferentes.
2. Plote um gráfico (matplotlib) de **throughput × eficiência** para cada PL e identifique
   o ponto ótimo.
3. Configure o `alerta_termico.sh` no `crontab` e observe seu comportamento por
   30 minutos de treinamento.
4. **Bônus:** use `nvidia-ml-py` para ajustar o PL automaticamente a cada época, com base
   na temperatura atual da GPU.
