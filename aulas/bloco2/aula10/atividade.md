# Atividade: Aula 10 — Introdução ao ROCm e GPUs AMD

## Parte 1 — Atividade guiada (verifique e meça)

Rode no **Colab**, no Windows do laboratório ou dentro do container ROCm
(`laboratorio_rocm-docker/`):

```bash
python scripts/lib_rocm.py                    # qual backend está ativo?
python scripts/diagnostico_portabilidade.py   # equivalências CUDA x ROCm
python scripts/rocm_pytorch_benchmark.py      # matmul + treino sintético
```

Registre: backend detectado, nome da GPU, VRAM, tempo do matmul e throughput de treino.

> **No servidor AMD (Docker ROCm):** rode dentro do container
> `rocm/pytorch`. Verifique também, no host, `rocm-smi --showuse --showmeminfo vram`.

---

## Parte 2 — Questões conceituais

1. **A Promessa do "Zero Código":** o engenheiro sênior afirmou que o PyTorch em CUDA roda no
   ROCm/AMD sem mudar nenhuma linha em Python. Por que ter uma camada de compatibilidade
   (**HIP**) que emula o CUDA facilita a vida de uma empresa que quer trocar de fabricante?
2. **Dependência de Fabricante (*Vendor Lock-in*):** se uma empresa depende exclusivamente de
   tecnologias proprietárias da NVIDIA (CUDA, cuDNN), qual é o risco estratégico e financeiro
   ao negociar preços de infraestrutura em nuvem no futuro?
3. **Praticidade com Docker:** instalar drivers de GPU diretamente no SO pode gerar conflitos.
   De que forma contêineres pré-configurados (`rocm/pytorch`) ajudam profissionais a testar
   novas tecnologias sem complicação?
4. **Decisão de Investimento (Custo vs. Treinamento):** GPUs AMD (MI300X) chegam a ser 40% mais
   baratas. Além do preço da placa, que outros fatores devem ser considerados antes de migrar
   toda a equipe para um novo ecossistema?

---

## Parte 3 — Discussão em grupo (3 a 4 pessoas)

No cenário das GPUs AMD na startup:

1. Se o PyTorch roda código CUDA em GPUs AMD via ROCm sem modificação, por que o **CUDA ainda
   é tão dominante** em IA? Quais barreiras ainda existem?
2. A empresa tem modelos treinados com NVIDIA + cuDNN. Ao migrar para AMD + MIOpen, os
   resultados (loss, acurácia) serão **numericamente idênticos**? Por quê?
3. Docker facilita o uso do ROCm, mas adiciona overhead. Em que cenários de produção Docker
   seria **problemático** para workloads de IA?
4. Compare os custos: NVIDIA H100 (US$30.000) vs. AMD MI300X (US$20.000). Além do preço, quais
   outros fatores técnicos e operacionais influenciam a escolha?

---

## Parte 4 — Pesquisa (tarefa de casa, opcional)

Compare o treinamento da **ResNet-50** em CUDA (Google Colab) vs. ROCm (Docker local ou AMD
Cloud) e produza um relatório técnico:

- Meça: **tempo por epoch**, **throughput** (imgs/s), **uso de VRAM** e **consumo de energia
  (W)**;
- Use `torch.profiler` para gerar um *trace* de execução nos dois ambientes;
- Documente as diferenças de setup (CUDA vs. Docker ROCm) em um README;
- Calcule o **TCO** (Total Cost of Ownership) para 1 ano de treinamento em cada plataforma.

> **Dica:** compare também o **tempo de setup** — um dos grandes argumentos a favor do uso de
> containers prontos é justamente reduzir o tempo gasto configurando drivers e dependências.
