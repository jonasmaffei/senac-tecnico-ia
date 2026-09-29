# 🌱 Projeto de Pesquisa 5 — Green AI: Eficiência Energética em Data Centers

> **Natureza:** pesquisa aplicada (**sem código obrigatório**). Estilo do
> [`projeto-integrador/`](../../../projeto-integrador/README.md).
> **Área:** Energia/Sustentabilidade. **Etapas:** aulas 20 a 24.

---

## 🎯 Problema proposto

O data center de uma instituição recebeu um alerta: o cluster GPU consome **40% mais energia**
que o projetado, pois as GPUs operam no TDP máximo mesmo em fases de baixa carga. A pergunta
central é: **como reduzir o consumo energético sem sacrificar o tempo de treino**, e qual o
**ponto ótimo de eficiência** (imgs/J) para a operação?

---

## 🗂️ Roteiro de pesquisa (as 5 etapas)

### 1. Contexto e problema (A20)
- Custo energético de um cluster GPU (nó de 8 GPUs pode passar de 6 kW).
- Impacto ambiental e financeiro; metas de sustentabilidade.
- Fontes: *Green AI* (ACL 2020), relatórios da NVIDIA/AMD.

### 2. Processamento e arquitetura (A20)
- Energia vs. throughput: trade-off entre velocidade e consumo.
- **Power Limit** (`nvidia-smi -pl`) e **thermal throttling**.
- Eficiência (imgs/J) como métrica de decisão.

### 3. Memória e comunicação (A20)
- Relação entre VRAM, batch size e energia gasta por experimento.
- Gargalos que forçam a GPU a ficar ociosa (desperdício de energia).
- Monitoramento contínuo: temperatura, potência e utilização.

### 4. Aceleração e portabilidade (A21)
- Mixed precision (fp16) reduz tempo e energia por época.
- Comparar o custo energético de CUDA vs ROCm.
- Papel do `nvidia-ml-py`/NVML no ajuste dinâmico de potência.

### 5. Medição e decisão final (A23)
- Medir: kWh por treino, imgs/J, temperatura média.
- Estimar a **economia** ao fixar o Power Limit em ~70–75% do TDP.
- **Recomendação** de política de energia + riscos.

---

## 📊 Resultados esperados (referência)

| Política | Consumo | Throughput | Eficiência |
| :--- | :--- | :--- | :--- |
| TDP máximo | 100% | 100% | menor |
| ~75% do TDP | ~75% | ~90% | **ótima** |

---

## 🎤 Apresentação (A23)

Pitch: problema → estratégia de energia → resultados → economia e conexão com o PI.

## 🔗 Conexão com o PI (A24)

- Monitoramento de energia (Bloco 3, Aula 19) aplicado ao PI.
- Calibração de Power Limit para treinos longos do PI.

> ℹ️ **Não é obrigatório codar.** O foco é a decisão fundamentada sobre energia.
