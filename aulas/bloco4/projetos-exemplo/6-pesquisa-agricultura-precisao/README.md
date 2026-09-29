# 🚁 Projeto de Pesquisa 6 — Agricultura de Precisão com Drones: Borda vs Nuvem

> **Natureza:** pesquisa aplicada (**sem código obrigatório**). Estilo do
> [`projeto-integrador/`](../../../projeto-integrador/README.md).
> **Área:** Agricultura. **Etapas:** aulas 20 a 24.

---

## 🎯 Problema proposto

Produtores rurais usam drones para fotografar lavouras e detectar pragas, mas o volume de
imagens é grande e a conectividade no campo é limitada. A pergunta central é: **o
processamento deve acontecer na borda (a bordo do drone / gateway) ou na nuvem com GPU**,
considerando latência, energia e custo?

---

## 🗂️ Roteiro de pesquisa (as 5 etapas)

### 1. Contexto e problema (A20)
- Volume de imagens por voo e urgência da detecção.
- Conectividade rural limitada e custo de banda.
- Fontes: estudos de agricultura de precisão + documentação de hardware de borda.

### 2. Processamento e arquitetura (A20)
- Borda: GPU/NPU embarcada (Jetson) — baixa latência, RISC/CISC e energia.
- Nuvem: GPU de data center — mais capacidade, mas exige rede.
- Modelo candidato: YOLO/EfficientNet leve para detecção.

### 3. Memória e comunicação (A20)
- Comparar requisitos de VRAM na borda vs na nuvem.
- Envio de imagens: `rsync`/`scp` vs compressão; UDP para telemetria.
- Gargalo provável: rede rural e armazenamento no drone.

### 4. Aceleração e portabilidade (A21)
- Quantização e modelos leves para caber na borda.
- CUDA (Jetson) vs Vulkan/OpenCL para hardware diverso.
- Trade-offs: latência, energia, custo e autonomia.

### 5. Medição e decisão final (A23)
- Medir: latência por imagem, consumo (W), custo por hectare.
- **Recomendação** borda × nuvem (ou híbrido) com justificativa.
- Riscos e limitações (clima, autonomia de bateria).

---

## 📊 Resultados esperados (referência)

| Aspecto | Borda (drone) | Nuvem (GPU) |
| :--- | :--- | :--- |
| Latência | baixa | depende da rede |
| Capacidade | limitada | alta |
| Custo de banda | baixo | alto |

---

## 🎤 Apresentação (A23)

Pitch: problema → arquitetura borda/nuvem → resultados → decisão e conexão com o PI.

## 🔗 Conexão com o PI (A24)

- Processamento de imagens de campo acelerado por GPU no PI.
- Telemetria e monitoramento (Bloco 3) aplicados ao pipeline agrícola.

> ℹ️ **Não é obrigatório codar.** O foco é comparar arquiteturas e justificar a escolha.
