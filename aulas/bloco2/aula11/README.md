# Aula 11: Aplicação de Modelos de IA (NVIDIA vs AMD) — Guia Prático Nivelado

---

## 🎯 Objetivo da Aula (Sem Complicação!)

Nesta aula, você vai atuar como um **consultor de tecnologia**. O seu objetivo é rodar o treinamento de um modelo de inteligência artificial (ResNet) e comparar como duas marcas de placas de vídeo (**NVIDIA** e **AMD**) se comportam.

Você não precisa ser um programador experiente para esta aula! O código já está pronto. Sua missão é **executar, observar os números (métricas) e responder às perguntas de pesquisa**.

---

## 📊 O que significam os números que vamos medir?

Imagine que treinar um modelo de IA é como fazer entregas de mercadorias:

| Métrica | O que significa na prática? | Analogia simples |
| :--- | :--- | :--- |
| **Throughput (imgs/s)** | Quantas imagens o computador consegue processar por segundo. **(Quanto maior, melhor!)** | Velocidade de pacotes entregues por minuto. |
| **VRAM Usada (MB)** | Quanta memória da placa de vídeo está sendo ocupada durante o treino. | O espaço ocupado no porta-malas do veículo. |
| **Tempo por Época (s)** | Quanto tempo leva para o modelo ler todo o conjunto de dados uma vez. | O tempo de uma viagem completa de ida e volta. |
| **Mixed Precision (FP16)** | Técnica que reduz o tamanho dos números usados nos cálculos para gastar menos memória. | Dobrar as caixas dentro do caminhão para caber o dobro de carga. |

---

## 💻 1. Executando o Script Prático no Google Colab ou WSL

Abra o arquivo `atividade_aula11.py` ou cole o código no seu **Google Colab**. 

### O Código Explicado Passo a Passo:

```python
import torch
import torch.nn as nn
import time

# Passo 2: Descobrir automaticamente qual placa de vídeo está no computador
def checar_placa():
    if torch.cuda.is_available():
        nome_gpu = torch.cuda.get_device_name(0)
        print(f"✅ Placa de Vídeo Detectada: {nome_gpu}")
        return "cuda"
    else:
        print("⚠️ Nenhuma GPU detectada. Usando a CPU.")
        return "cpu"

dispositivo = checar_placa()

# Passo 3: O Modelo (Mantive o original)
modelo = nn.Sequential(
    nn.Conv2d(3, 32, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.AdaptiveAvgPool2d((1, 1)),
    nn.Flatten(),
    nn.Linear(32, 10)
).to(dispositivo)

# Passo 4: Função para treinar o modelo e medir a velocidade
def simular_treinamento(usar_mixed_precision=False):
    modo = "Otimizado (FP16)" if usar_mixed_precision else "Padrão (FP32)"
    print(f"\n🚀 Iniciando treino no modo: {modo}")
    
    otimizador = torch.optim.SGD(modelo.parameters(), lr=0.01)
    criterio = nn.CrossEntropyLoss()
    
    # Sintaxe do PyTorch (Agnóstica de hardware)
    scaler = torch.amp.GradScaler('cuda') if usar_mixed_precision else None

    # WARM-UP (Aquecimento)
    # A GPU sempre é mais lenta na 1ª iteração porque precisa compilar os kernels.
    # Rodamos um lote invisível antes de ligar o cronômetro.
    img_warmup = torch.randn(64, 3, 224, 224, device=dispositivo)
    lbl_warmup = torch.randint(0, 10, (64,), device=dispositivo)
    modelo(img_warmup)
    
    # Sincroniza a placa de vídeo antes de iniciar o relógio!
    if dispositivo == "cuda": torch.cuda.synchronize()
    t0 = time.time()
    
    for lote in range(50):
        imagens = torch.randn(64, 3, 224, 224, device=dispositivo)
        etiquetas = torch.randint(0, 10, (64,), device=dispositivo)

        otimizador.zero_grad()

        if usar_mixed_precision:
            # Sintaxe do autocast
            with torch.amp.autocast('cuda'):
                saida = modelo(imagens)
                perda = criterio(saida, etiquetas)
            scaler.scale(perda).backward()
            scaler.step(otimizador)
            scaler.update()
        else:
            saida = modelo(imagens)
            perda = criterio(saida, etiquetas)
            perda.backward()
            otimizador.step()

    # Sincroniza a GPU para garantir que ela terminou o trabalho
    if dispositivo == "cuda": torch.cuda.synchronize()
    tempo_total = time.time() - t0
    
    imagens_processadas = 50 * 64
    velocidade = imagens_processadas / tempo_total
    
    print(f"⏱️ Tempo Total: {tempo_total:.2f} segundos")
    print(f"⚡ Velocidade (Throughput): {velocidade:.1f} imagens por segundo")

# Executa as duas simulações
simular_treinamento(usar_mixed_precision=False)
simular_treinamento(usar_mixed_precision=True)
```

---

## 🔍 2. Atividade de Pesquisa e Análise de Negócios

Em duplas ou trios, pesquisem na internet e respondam às perguntas a seguir para ajudar na decisão de compra de uma empresa fictícia de tecnologia:

### 📄 Cenário da Empresa:
> A startup **"IA Entregas"** precisa contratar servidores de placa de vídeo na nuvem para treinar seus modelos pelos próximos 3 anos. O diretor financeiro quer saber se deve escolher placas **NVIDIA** ou **AMD**.

### 📋 Roteiro de Pesquisa:

1. **Pesquisa de Custo na Nuvem:**
   * Pesquise o valor por hora de aluguel de uma GPU **NVIDIA T4** (ou A10G) no Google Cloud ou AWS.
   * Pesquise sobre o preço de placas **AMD Instinct (como a MI300X)** ou placas AMD na nuvem.
   * *Qual das marcas costuma ter um preço de aluguel por hora mais baixo?*

2. **Facilidade de Uso vs Economia:**
   * A NVIDIA usa o ecossistema **CUDA** (muito popular e fácil de instalar). A AMD usa o **ROCm**.
   * Se uma empresa tem uma equipe técnica habituada ao ecossistema NVIDIA, qual seria o desafio operacional de mudar para AMD? O valor mais baixo da AMD compensa a necessidade de adaptação da equipe?

3. **Análise dos Resultados do Código:**
   * Ao rodar o código acima no modo **Otimizado (FP16)**, o que aconteceu com a velocidade de processamento (imagens por segundo)? 
   * Por que usar técnicas de otimização é importante antes de gastar dinheiro comprando mais placas de vídeo?

---

## 📝 Tarefa de Casa (Relatório Simples em Word/PDF)

Escreva um texto curto de 1 a 2 páginas respondendo à pergunta:
> *"Se você fosse o gerente de tecnologia, qual marca de placa de vídeo recomendaria comprar para a sua empresa hoje e por quê?"*

**Dica:** Considere a facilidade de uso, o preço do hardware e os resultados observados na prática!
