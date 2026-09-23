# Laboratório: verificar acesso à GPU no container (Windows / AMD)

Este laboratório **verifica** se o container consegue enxergar a GPU AMD do host Windows via
`/dev/dxg` (GPU-PV no WSL 2). É o passo de diagnóstico **antes** de estressar ou rodar cargas
de IA.

---

## Pré-requisitos

- **Windows 10/11** com **WSL 2** habilitado e GPU **AMD** com driver atualizado.
- **Docker Desktop** instalado e usando o backend **WSL 2**.

---

## Passo a passo

```bash
# 1) Clone o repositório (uma vez)
mkdir repos && cd repos
git clone https://github.com/jonasmaffei/senac-tecnico-ia
# depois, para atualizar:  git pull

# 2) Entre na pasta do laboratório
cd aulas/aula10/laboratorio_verificar-gpu

# 3) Construa a imagem
docker build . -t verificar-gpu-container

# 4) Execute, repassando o dispositivo da GPU
docker run --rm --device=/dev/dxg verificar-gpu-container
```

Saída esperada (quando o acesso funciona):

```
=== TESTE DE GPU NO CONTAINER ===
Dispositivo /dev/dxg:
GPU-PV disponível dentro do container!
✓ /dev/dxg encontrado
```

---

## Tabela de arquivos

| Arquivo | Papel |
| :--- | :--- |
| `Dockerfile` | Base Ubuntu com Python; copia o teste e executa. |
| `teste_gpu.py` | Verifica a existência de `/dev/dxg` (a GPU exposta ao WSL). |

---

## Laboratórios irmãos

| Laboratório | O que faz |
| :--- | :--- |
| [`../laboratorio_stressar-gpu/`](../laboratorio_stressar-gpu/README.md) | Mantém a GPU ocupada via Vulkan/D3D12 para observar no Gerenciador de Tarefas. |
| [`../laboratorio_rocm-docker/`](../laboratorio_rocm-docker/README.md) | Versão **industrial**: ROCm + PyTorch via Docker em GPUs AMD. |

---

## Relação com a aula

- Confirma que o **container acessa a GPU** — pré-requisito para qualquer carga de IA conteinerizada.
- Introduz o conceito de repassar dispositivos (`--device=`) que reaparece no laboratório ROCm
  (`--device=/dev/kfd --device=/dev/dri`).
