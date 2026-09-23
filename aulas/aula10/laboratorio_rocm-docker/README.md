# Laboratório: ROCm + PyTorch via Docker (GPUs AMD)

Este laboratório roda o benchmark portável (`rocm_pytorch_benchmark.py`) dentro da **imagem
oficial da AMD** `rocm/pytorch`, que já traz ROCm, PyTorch compilado com HIP e todas as
dependências prontas. É a forma **recomendada** de usar ROCm: sem instalar drivers complexos no
host.

> **Diferença em relação aos labs irmãos:** aqui usamos uma imagem **pronta da AMD** (ROCm de
> verdade). Os labs [`../verificar-gpu-container/`](../verificar-gpu-container/README.md) e
> [`../stressar-gpu-container/`](../stressar-gpu-container/README.md) usam Vulkan/D3D12 no WSL 2,
> para a máquina de laboratório com Windows/AMD.

---

## Pré-requisitos

- **Servidor Linux** com GPUs **AMD compatíveis com ROCm** (Instinct MI300X/MI250, Radeon
  RX 7900 XTX, etc.).
- **Docker** instalado e o usuário nos grupos `video` e `render`:
  ```bash
  sudo usermod -aG video,render $USER   # depois faça logout/login
  ```
- Drivers AMD (`amdgpu`) e ROCm instalados no host.

---

## Passo a passo (comando direto)

```bash
# 1) Baixar a imagem oficial PyTorch + ROCm
docker pull rocm/pytorch:rocm6.2_ubuntu22.04_py3.10_pytorch_release_2.3.0

# 2) Rodar o benchmark dentro do container, com acesso às GPUs AMD
docker run --rm -it \
  --device=/dev/kfd \
  --device=/dev/dri \
  --group-add=video \
  --group-add=render \
  --ipc=host --shm-size 8G \
  -v "$(pwd)/../laboratorio_windows":/workspace \
  rocm/pytorch:rocm6.2_ubuntu22.04_py3.10_pytorch_release_2.3.0 \
  python3 /workspace/rocm_pytorch_benchmark.py
```

## Passo a passo (com Docker Compose)

```bash
docker compose up --build
```

---

## Monitoramento no host (segundo terminal)

```bash
watch -n 1 rocm-smi --showuse --showmeminfo vram --showtemp --showpower
```

---

## Tabela de arquivos

| Arquivo | Papel |
| :--- | :--- |
| `Dockerfile` | Parte da imagem `rocm/pytorch` e copia o benchmark para `/workspace`. |
| `docker-compose.yml` | Descreve o serviço com os dispositivos `/dev/kfd` e `/dev/dri`. |
| `../laboratorio_windows/1_rocm_pytorch_benchmark.py` | Script executado (diagnóstico + matmul + treino). |

---

## O que observar

- `torch.cuda.is_available()` retorna **True** mesmo em GPU AMD — o ROCm emula a API CUDA.
- `torch.version.hip` mostra a versão do HIP (ex.: `6.2.0`).
- O **mesmo código Python** roda em NVIDIA (CUDA) e AMD (ROCm), sem alterações.

---

## Solução de problemas

| Sintoma | Causa provável | Ação |
| :--- | :--- | :--- |
| `permission denied` em `/dev/kfd` | usuário fora dos grupos | `sudo usermod -aG video,render $USER` + relogin |
| `torch.cuda.is_available()` = False | dispositivo não repassado | confira `--device=/dev/kfd --device=/dev/dri` |
| `HSA error` / crash | driver ROCm incompatível | alinhe a versão do host com a da imagem |
| treino lento / OOM | `shm` pequeno | use `--shm-size 8G` e `--ipc=host` |

---

## Relação com a aula

- Prova a **portabilidade** prometida pelo HIP: pipeline CUDA roda em AMD sem reescrever código.
- Demonstra **containers** como forma de isolar o ambiente ROCm e evitar conflitos de driver.
- Prepara a análise de **TCO** e *vendor lock-in* discutida na aula.
