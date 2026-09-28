# 🖥️ Laboratório Windows Host: Automação de GPU (Aula 17)

Este laboratório permite executar e testar os scripts de **coleta de métricas, alertas, geração de dashboards e envio para Google Sheets** diretamente no sistema hospedeiro Windows (sem necessidade de Linux ou Docker).

---

## 🗂️ Estrutura da Pasta

```
laboratorio_windows/
├── iniciar.bat             # Menu interativo (cria .venv e roda os scripts)
├── requirements.txt        # Dependências Python (matplotlib, psutil, google-api-python-client)
├── 1_monitor_gpu.py        # Coleta telemetria do hardware local e salva em reports/gpu_log.csv
├── 2_alerta_gpu.py         # Analisa métricas e gera alertas em reports/alertas.log
├── 3_gerar_graficos.py     # Cria o dashboard visual em reports/gpu_dashboard.png
├── 4_enviar_sheets.py      # Envia os dados para a API do Google Sheets (modo simulação/real)
└── README.md               # Este guia
```

---

## 🚀 Como Executar

### 1. Duplo clique no `iniciar.bat`
Ao executar o `iniciar.bat`, o script cria automaticamente o ambiente virtual `.venv`, instala as bibliotecas necessárias e exibe um menu com as opções de 1 a 5.

### 2. Opções do Menu

- **Opção 1 (Coleta):** Coleta métricas a cada 3 segundos durante 30 segundos. Se a máquina possuir GPU NVIDIA, o `nvidia-smi` será utilizado; caso contrário, o script consulta métricas do Windows Host (CPU/RAM/GPU AMD/Intel) com fallback seguro.
- **Opção 2 (Alertas):** Analisa o arquivo `reports/gpu_log.csv` e dispara avisos se a temperatura for $\ge 75^\circ\text{C}$ ou o uso for $\ge 90\%$.
- **Opção 3 (Dashboard):** Renderiza o gráfico de 4 painéis em `reports/gpu_dashboard.png`.
- **Opção 4 (Google Sheets):** Tenta enviar os dados via API do Google Sheets. Se a variável `SHEETS_ID` não estiver definida, executa em modo simulação.

---

## 📊 Arquivos Gerados (`reports/`)

- `reports/gpu_log.csv`: Histórico de telemetria coletado.
- `reports/alertas.log`: Registro de alertas de ultrapassagem de limiar.
- `reports/gpu_dashboard.png`: Gráfico gerado contendo Temperatura, Utilização, Memória e Potência.
