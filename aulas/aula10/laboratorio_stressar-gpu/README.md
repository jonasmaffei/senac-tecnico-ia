# Laboratório: estressar a GPU via container (Windows / AMD)

Este laboratório sobe um container Linux que **acessa a GPU AMD do Windows** através do
backend **Vulkan → D3D12 (Dozen)** no **WSL 2**, e mantém a GPU ocupada para você observar o
uso no **Gerenciador de Tarefas** do Windows.

É a versão prática do monitoramento/estresse do servidor de GPUs, adaptada à máquina do
laboratório (AMD/Windows), sem precisar de uma instalação ROCm nativa.

---

## Pré-requisitos

- **Windows 10/11** com **WSL 2** habilitado e uma GPU **AMD** com driver atualizado.
- **Docker Desktop** instalado e configurado para usar o backend **WSL 2**.
- A GPU exposta ao WSL (`/dev/dxg`). Confirme no laboratório irmão:
  [`../laboratorio_verificar-gpu/`](../laboratorio_verificar-gpu/README.md).
- Versão **industrial** com ROCm de verdade: [`../laboratorio_rocm-docker/`](../laboratorio_rocm-docker/README.md).

---

## Passo a passo

```bash
cd aulas/aula10/laboratorio_stressar-gpu

# 1) Construir a imagem (instala Vulkan + bindings Python)
docker build . -t stressar-gpu-container

# 2) Executar (com acesso ao dispositivo /dev/dxg)
docker run --rm --device=/dev/dxg stressar-gpu-container
```

Durante a execução:

1. Abra o **Gerenciador de Tarefas** do Windows → aba **Desempenho** → **GPU**.
2. Observe a **utilização da GPU** e a **memória dedicada**.
3. No terminal, pressione `Ctrl+C` para encerrar.

---

## Tabela de arquivos

| Arquivo | Papel |
| :--- | :--- |
| `Dockerfile` | Instala `vulkan-tools`, `mesa-vulkan-drivers` e os bindings Python (`vulkan`, `numpy`). |
| `teste_gpu.py` | Descobre a GPU via Vulkan, cria a fila de compute e a mantém ocupada em loop. |

---

## Como o acesso à GPU funciona (visão de engenharia)

- No WSL 2, a GPU aparece como `/dev/dxg` (GPU-PV). O container recebe esse dispositivo com
  `--device=/dev/dxg`.
- As variáveis de ambiente do `Dockerfile` apontam para o **ICD Dozen** (Vulkan sobre D3D12),
  permitindo falar com a GPU AMD do host.
- O `MESA_D3D12_DEFAULT_ADAPTER_NAME` força o uso da placa dedicada.

---

## Relação com a aula

- Mostra, na prática, **como um container acessa a GPU** — o mesmo princípio do laboratório
  ROCm (`--device=/dev/kfd --device=/dev/dri` na versão Linux/AMD).
- Serve de base para **observar utilização/temperatura** durante cargas de IA.
- Complementa [`../laboratorio_verificar-gpu/`](../laboratorio_verificar-gpu/README.md), que
  apenas **verifica** o acesso (sem estressar).
