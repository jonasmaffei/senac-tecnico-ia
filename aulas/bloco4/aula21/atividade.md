# 📝 Atividade: Aula 21 — Implementação do Modelo

## 🎯 Situação

O plano está pronto e o baseline medido. Agora é implementar o modelo com **aceleração GPU real**.

---

## 🚀 Roteiro

1. Rode o exemplo para ver o pipeline com AMP:
   ```bash
   cd aulas/bloco4/aula21/scripts
   python treino_otimizado.py
   ```
2. No seu `train.py`, adicione:
   - `autocast` + `GradScaler` (mixed precision);
   - `DataLoader` com `num_workers` e `pin_memory`;
   - `zero_grad(set_to_none=True)`.
3. Meça o **throughput (imgs/s)** com e sem AMP.
4. Se o batch não couber na VRAM, use **gradient accumulation**.

---

## 💬 Discussão em grupo (10 min)

1. Qual foi o ganho de velocidade com AMP na sua GPU?
2. O modelo cabe na VRAM com o batch planejado?
3. Comparado ao baseline, quantas épocas faltam para superá-lo?

---

## 📚 Trilha de pesquisa (alternativa sem código)

Em vez de treinar, **levante evidências**: compare alternativas (CUDA vs ROCm), cite papers e
documentações oficiais. O entregável é a **análise fundamentada**, não o código.


## 📌 Tarefa de casa (para a Aula 22)

1. Treinar pelo menos **10 épocas** com AMP e logging.
2. Comparar o throughput com e sem AMP e registrar no README.
