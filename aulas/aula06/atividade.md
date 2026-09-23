# Atividade Guiada: Aula 6 — Sistemas Operacionais Linux e GPU

## Parte 1 — Atividade guiada: inspecionar o servidor

Você acabou de receber acesso ao servidor de GPUs. Faça o checklist inicial.

### Passo 1 — Onde estão as GPUs?

```bash
ls /dev/                 # nvidia* aparece?
ls /dev/nvidia*          # dispositivos NVIDIA
ls /sys/class/drm/       # GPUs (DRM)
lspci | grep -iE 'vga|3d|display|nvidia|amd|radeon'
```

### Passo 2 — Os drivers respondem?

```bash
nvidia-smi -L                                   # NVIDIA
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader

rocminfo || rocm-smi --showmeminfo vram         # AMD (ROCm)
```

Se aparecer **"couldn't communicate with the NVIDIA driver"**, o driver não está OK:

```bash
sudo apt install nvidia-driver-535 nvidia-utils-535
sudo reboot
nvidia-smi
```

### Passo 3 — Ler os pseudo-arquivos

```bash
cat /proc/cpuinfo | grep "model name" | head -1
cat /proc/meminfo | head -5
cat /proc/uptime
```

### Passo 4 — Rodar o script de status

```bash
bash scripts/gpu_status.sh
LIMITE_TEMP=75 bash scripts/gpu_status.sh    # muda o limite do alerta
```

### Exercício de fixação

1. Quantas GPUs o servidor tem? Qual a versão do driver?
2. Qual é a **temperatura** e a **utilização** de cada GPU agora?
3. Por que `/proc` e `/sys` **não ocupam espaço em disco**?
4. Se o `nvidia-smi` falha, o que você verifica primeiro?

---

## Parte 2 — Atividade guiada: automação com cron e systemd

### Passo 1 — Agendar com cron

```bash
crontab -e
```

Adicione uma linha para monitorar a GPU a cada 5 minutos (veja
`scripts/cron_exemplos.sh`):

```cron
*/5 * * * * /home/usuario/scripts/gpu_status.sh >> /var/log/gpu_monitor.log 2>&1
```

Confira com `crontab -l` e acompanhe o log com `tail -f /var/log/gpu_monitor.log`.

### Passo 2 — Serviço contínuo com systemd

```bash
sudo cp scripts/gpu-monitor.service /etc/systemd/system/gpu-monitor.service
sudo systemctl daemon-reload
sudo systemctl enable gpu-monitor
sudo systemctl start  gpu-monitor
sudo systemctl status gpu-monitor
```

### Passo 3 — Manter o treino vivo após o logout

```bash
tmux new -s treino          # abre uma sessão chamada 'treino'
# dentro dela: python treinar.py
# Ctrl+B, depois D  -> desanexa e deixa rodando
tmux attach -t treino       # volta à sessão depois
```

Alternativas: `screen -S treino` e `nohup python treinar.py &`.

### Exercício de fixação

1. Qual a diferença entre **cron** (periódico) e **systemd** (contínuo)?
2. Como o **tmux** evita perder 12h de treino quando o SSH cai?
3. O que `Restart=always` faz no serviço systemd?

---

## Parte 3 — Discussão em grupo (3 a 4 pessoas)

No cenário do servidor da startup:

1. O treinamento estava rodando há 12h quando você desconectou o SSH acidentalmente. Como
   teria evitado isso? Quais ferramentas usaria?
2. Dois cientistas de dados querem usar as **mesmas 4 GPUs** do servidor ao mesmo tempo. Como
   gerenciar o acesso e os recursos com ferramentas Linux?
3. O script `gpu_status.sh` mostra **85°C** numa GPU. Quais os próximos passos? Como
   automatizar um alerta por e-mail?
4. Por que `/proc` e `/sys` são chamados de "sistemas de arquivos virtuais"? O que isso
   significa para o monitoramento de GPUs?

---

## Parte 4 — Pesquisa (tarefa de casa, opcional)

Expanda o `scripts/gpu_status.sh` para incluir:

- Envio de **e-mail automático** quando a temperatura &gt; 80°C (usando `mail` ou `curl` +
  webhook);
- **Log estruturado em CSV** com timestamp, temperatura e utilização;
- **Relatório** da utilização média das últimas 24h;
- **Agendamento via cron** a cada 5 minutos.
