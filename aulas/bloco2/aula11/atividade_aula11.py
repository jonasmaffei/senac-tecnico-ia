# atividade_aula11.py
"""
Aula 11: Treinamento e Benchmark Comparativo (NVIDIA vs AMD)
Script Didático e Passo a Passo para o Curso Técnico de IA

Instruções para o aluno:
1. Execute este script no Google Colab ou no terminal do WSL.
2. Observe os resultados impressos na tela.
3. Compare o tempo e a velocidade no modo Padrão vs Otimizado (FP16).
"""

import torch
import torch.nn as nn
import time

def verificar_ambiente():
    """Identifica se o computador/nuvem possui placa de vídeo disponível."""
    print("=" * 60)
    print("  VERIFICANDO O HARDWARE DO COMPUTADOR")
    print("=" * 60)
    
    if torch.cuda.is_available():
        nome_gpu = torch.cuda.get_device_name(0)
        vram_total = torch.cuda.get_device_properties(0).total_memory // (1024 ** 3)
        print(f" STATUS : [OK] Placa de vídeo (GPU) detectada com sucesso!")
        print(f" NOME   : {nome_gpu}")
        print(f" MEMÓRIA: ~{vram_total} GB de VRAM")
        
        # Identifica se é NVIDIA (CUDA) ou AMD (ROCm via HIP)
        backend = "AMD ROCm (via HIP)" if hasattr(torch.version, "hip") and torch.version.hip else "NVIDIA CUDA"
        print(f" SISTEMA: {backend}")
        dispositivo = "cuda"
    else:
        print(" STATUS : [ATENCAO] Nenhuma GPU detectada. Executando no processador (CPU).")
        dispositivo = "cpu"
        
    print("=" * 60)
    return dispositivo

def criar_modelo_ia(dispositivo):
    """Cria uma rede neural simples de visão computacional."""
    modelo = nn.Sequential(
        # Camada 1: Extração de características da imagem
        nn.Conv2d(3, 32, kernel_size=3, padding=1),
        nn.BatchNorm2d(32),
        nn.ReLU(),
        
        # Camada 2: Redução de tamanho
        nn.AdaptiveAvgPool2d((1, 1)),
        nn.Flatten(),
        
        # Camada 3: Classificação final em 10 categorias
        nn.Linear(32, 10)
    ).to(dispositivo)
    return modelo

def executar_treinamento(dispositivo, usar_fp16=False):
    """Executa a simulação do treinamento e mede a velocidade."""
    nome_modo = "Otimizado com Mixed Precision (FP16)" if usar_fp16 else "Padrão de Alta Precisão (FP32)"
    print(f"\n--> Testando modo: {nome_modo}")
    print("-" * 60)
    
    modelo = criar_modelo_ia(dispositivo)
    otimizador = torch.optim.SGD(modelo.parameters(), lr=0.01)
    criterio = nn.CrossEntropyLoss()
    scaler = torch.amp.GradScaler('cuda') if (usar_fp16 and dispositivo == "cuda") else None

    lotes_totais = 40
    tamanho_lote = 64
    
    t_inicio = time.time()
    
    for lote in range(1, lotes_totais + 1):
        # Gera lote de imagens fictícias (simulação)
        imagens = torch.randn(tamanho_lote, 3, 224, 224, device=dispositivo)
        etiquetas = torch.randint(0, 10, (tamanho_lote,), device=dispositivo)

        otimizador.zero_grad()

        if usar_fp16 and dispositivo == "cuda":
            # Modo otimizado: reduz uso de memória na GPU
            with torch.amp.autocast('cuda'):
                saida = modelo(imagens)
                perda = criterio(saida, etiquetas)
            scaler.scale(perda).backward()
            scaler.step(otimizador)
            scaler.update()
        else:
            # Modo padrão
            saida = modelo(imagens)
            perda = criterio(saida, etiquetas)
            perda.backward()
            otimizador.step()

        if lote % 10 == 0:
            print(f"  --> Processado lote {lote}/{lotes_totais}...")

    # Sincroniza o tempo se estiver na GPU
    if dispositivo == "cuda":
        torch.cuda.synchronize()
        
    tempo_total = time.time() - t_inicio
    total_imagens = lotes_totais * tamanho_lote
    velocidade = total_imagens / tempo_total
    
    print("-" * 60)
    print(f" RESULTADOS DO MODO: {nome_modo}")
    print(f" Tempo Total Gasto         : {tempo_total:.2f} segundos")
    print(f" Velocidade (Throughput)    : {velocidade:.1f} imagens/segundo")
    print("=" * 60)
    
    return velocidade

if __name__ == "__main__":
    dispositivo = verificar_ambiente()
    
    print("\nIniciando testes comparativos de desempenho...\n")
    vel_fp32 = executar_treinamento(dispositivo, usar_fp16=False)
    vel_fp16 = executar_treinamento(dispositivo, usar_fp16=True)
    
    speedup = vel_fp16 / vel_fp32 if vel_fp32 > 0 else 1.0
    
    print("\n" + "=" * 20 + " RESUMO FINAL " + "=" * 20)
    print(f" Modo Padrão (FP32)    : {vel_fp32:.1f} imagens/segundo")
    print(f" Modo Otimizado (FP16) : {vel_fp16:.1f} imagens/segundo")
    print(f" Ganho de Desempenho   : {speedup:.2f}x mais rápido no modo otimizado!")
    print("=" * 60)
