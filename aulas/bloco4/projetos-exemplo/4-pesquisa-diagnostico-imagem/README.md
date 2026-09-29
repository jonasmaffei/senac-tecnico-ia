# 🏥 Projeto de Pesquisa 4 — Diagnóstico por Imagem em GPU: CUDA vs ROCm

> **Natureza:** pesquisa aplicada (**sem código obrigatório**). Estilo do
> [`projeto-integrador/`](../../../projeto-integrador/README.md).
> **Área:** Saúde. **Etapas:** aulas 20 a 24.

---

## 🎯 Problema proposto

Um hospital de médio porte recebe, por dia, centenas de exames de imagem (raios-X, tomografias).
O diagnóstico assistido por IA reduziria o tempo de fila, mas exige **processamento pesado**.
A pergunta central é: **qual arquitetura de GPU adotar — CUDA (NVIDIA) ou ROCm (AMD)** — para
processar esses exames em lote, considerando desempenho, custo, energia e soberania dos dados?

---

## 🗂️ Roteiro de pesquisa (as 5 etapas)

### 1. Contexto e problema (A20)
- Volume de exames/dia e impacto do diagnóstico tardio.
- Por que a carga é paralela (milhares de imagens → inferência em lote).
- Fontes: papers de radiologia + documentação NVIDIA/AMD.

### 2. Processamento e arquitetura (A20)
- Workload predominantemente **SIMD**: a mesma inferência aplicada a milhares de imagens.
- Comparar: servidor local com GPU vs nuvem vs Colab Pro.
- Modelo candidato: ResNet/EfficientNet pré-treinado (transfer learning).

### 3. Memória e comunicação (A20)
- Estimar **VRAM** por exame e o risco de OOM ao processar lotes grandes.
- Gargalo provável: carregamento das imagens (disco/rede) e o barramento PCIe.
- Dados sensíveis (LGPD): onde podem trafegar; `rsync` para datasets grandes.

### 4. Aceleração e portabilidade (A21)
- CUDA: ecossistema maduro, mais bibliotecas.
- ROCm/HIP: alternativa viável para evitar *vendor lock-in*.
- Trade-offs: desempenho, maturidade, custo e dependência de fabricante.

### 5. Medição e decisão final (A23)
- Como medir: throughput (imagens/s), VRAM de pico, tempo por lote e energia (imgs/J).
- **Recomendação** de arquitetura com argumentos técnicos e financeiros.
- Riscos e limitações.

---

## 📊 Resultados esperados (referência)

| Aspecto | Alternativa A | Alternativa B |
| :--- | :--- | :--- |
| Ecossistema | CUDA (maduro) | ROCm (em evolução) |
| Custo | maior | menor |
| Portabilidade | baixa | maior |

---

## 🎤 Apresentação (A23)

Pitch: problema → arquitetura proposta → demonstração (opcional) → resultados →
decisão e conexão com o PI.

## 🔗 Conexão com o PI (A24)

- Inferência de imagens de exames acelerada por GPU no PI de saúde.
- Monitoramento de GPU (Bloco 3) integrado ao pipeline hospitalar.

> ℹ️ **Não é obrigatório codar.** Se quiser, complemente com os projetos de código do Bloco 4.
