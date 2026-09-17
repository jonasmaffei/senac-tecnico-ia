import json

def line(s):
    return s + "\n"

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    line("# 🧠 Aula 12 — Laboratório Prático & Resumo Interativo de Infraestrutura para IA"),
    line(""),
    line("Bem-vindo(a) à nossa Aula 12! Este notebook foi desenvolvido para **experimentar na prática** os conceitos de hardware, GPU, memória, redes e modelos de IA que estudamos durante o módulo através de uma interface interativa."),
    line(""),
    line("--- "),
    line("### 📌 GUIA RÁPIDO: COMO ABRIR E PREPARAR O NOTEBOOK NO GOOGLE COLAB"),
    line(""),
    line("#### 1️⃣ Como abrir este notebook:"),
    line("- Acesse [colab.research.google.com](https://colab.research.google.com/)."),
    line("- Vá na aba **GitHub**, busque pelo repositório `https://github.com/jonasmaffei/senac-tecnico-ia` e selecione `aulas/aula12/aula12_pratica_colab.ipynb`."),
    line("- *(Alternativa)* Se baixou o arquivo para o seu computador, vá na aba **Fazer upload** e selecione este arquivo `.ipynb`."),
    line(""),
    line("#### 2️⃣ Ativar a GPU (Passo Obrigatório!):"),
    line("1. No menu superior do Colab, clique em **Ambiente de execução** (*Runtime*)."),
    line("2. Clique em **Alterar tipo de ambiente de execução** (*Change runtime type*)."),
    line("3. Em **Acelerador de hardware**, selecione **T4 GPU**."),
    line("4. Clique em **Salvar**."),
    line(""),
    line("#### 3️⃣ Como Executar os Blocos:"),
    line("- Passe o mouse sobre qualquer bloco cinza abaixo e clique no botão **Play ▶️** (ou aperte `Ctrl + Enter`)."),
    line("- Altere os valores nos **sliders e menus interativos** no lado direito do código e clique em Play novamente para ver as mudanças!")
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    line("## 🔹 Bloco 1: A Batalha de Hardware — CPU vs GPU (Aulas 1 e 2)"),
    line(""),
    line("**Conceito:**"),
    line("- **CPU (Von Neumann/CISC):** Como um chef de cozinha super treinado. Resolve tarefas complexas uma por uma (sequencial)."),
    line("- **GPU (SIMD):** Como uma fábrica com centenas de assistentes simples trabalhando juntos. Aplica a mesma instrução em milhares de dados simultaneamente."),
    line(""),
    line("Execute o código abaixo alterando o tamanho dos dados no slider para ver a diferença!")
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    line("# @title 🎛️ Experimento 1: Multiplicação Massiva de Matrizes (CPU vs GPU)"),
    line("import torch"),
    line("import time"),
    line("import matplotlib.pyplot as plt"),
    line(""),
    line("# Formulário Interativo no Colab"),
    line('tamanho_matriz = 3000 # @param {type:"slider", min:1000, max:6000, step:1000}'),
    line(""),
    line('print(f"🔄 Criando matrizes de tamanho {tamanho_matriz} x {tamanho_matriz}...")'),
    line(""),
    line("# 1. Teste na CPU"),
    line("matriz_a_cpu = torch.randn(tamanho_matriz, tamanho_matriz)"),
    line("matriz_b_cpu = torch.randn(tamanho_matriz, tamanho_matriz)"),
    line(""),
    line("inicio_cpu = time.time()"),
    line("resultado_cpu = torch.matmul(matriz_a_cpu, matriz_b_cpu)"),
    line("tempo_cpu = time.time() - inicio_cpu"),
    line('print(f"⏱️ Tempo gasto na CPU: {tempo_cpu:.4f} segundos")'),
    line(""),
    line("# 2. Teste na GPU (se disponível)"),
    line("if torch.cuda.is_available():"),
    line("    matriz_a_gpu = matriz_a_cpu.to('cuda')"),
    line("    matriz_b_gpu = matriz_b_cpu.to('cuda')"),
    line("    "),
    line("    # Aquecimento da GPU"),
    line("    torch.matmul(matriz_a_gpu, matriz_b_gpu)"),
    line("    torch.cuda.synchronize()"),
    line("    "),
    line("    inicio_gpu = time.time()"),
    line("    resultado_gpu = torch.matmul(matriz_a_gpu, matriz_b_gpu)"),
    line("    torch.cuda.synchronize()"),
    line("    tempo_gpu = time.time() - inicio_gpu"),
    line('    print(f"🚀 Tempo gasto na GPU: {tempo_gpu:.4f} segundos")'),
    line("    "),
    line("    aceleracao = tempo_cpu / tempo_gpu"),
    line('    print(f"\\n⚡ A GPU foi {aceleracao:.1f}x MAIS RÁPIDA que a CPU!")'),
    line("    "),
    line("    # Gráficos Visuais"),
    line("    plt.figure(figsize=(7, 4))"),
    line("    plt.bar(['CPU (Sequencial)', 'GPU (Paralelo)'], [tempo_cpu, tempo_gpu], color=['#ff6b6b', '#51cf66'])"),
    line("    plt.ylabel('Tempo em Segundos (menor é melhor)')"),
    line("    plt.title(f'Comparativo de Velocidade (Matriz {tamanho_matriz}x{tamanho_matriz})')"),
    line("    plt.grid(axis='y', linestyle='--', alpha=0.7)"),
    line("    plt.show()"),
    line("else:"),
    line("    print(\"⚠️ GPU não detectada! Lembre-se de ativar a GPU no menu 'Ambiente de execução'.\")")
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    line("## 🔹 Bloco 2: O Gargalo de Memória e Barramento PCIe (Aula 3)"),
    line(""),
    line("**Conceito:**"),
    line("Não adianta ter uma GPU ultrarrápida se o tempo para **enviar o dado da memória RAM (CPU) para a VRAM (GPU)** for muito alto. Esse transporte de dados via barramento PCIe pode ser o gargalo da sua solução de IA.")
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    line("# @title 🎛️ Experimento 2: Medindo o Custo de Transferir Dados (RAM ➡️ VRAM)"),
    line("import torch"),
    line("import time"),
    line("import matplotlib.pyplot as plt"),
    line(""),
    line('tamanho_mb = 500 # @param {type:"slider", min:100, max:1000, step:100}'),
    line("elementos = (tamanho_mb * 1024 * 1024) // 4 # float32 tem 4 bytes"),
    line(""),
    line("if torch.cuda.is_available():"),
    line("    dado_ram = torch.randn(elementos)"),
    line("    "),
    line("    # Medindo tempo de envio (RAM -> VRAM)"),
    line("    inicio_transf = time.time()"),
    line("    dado_vram = dado_ram.to('cuda')"),
    line("    torch.cuda.synchronize()"),
    line("    tempo_transf = time.time() - inicio_transf"),
    line("    "),
    line("    # Medindo tempo de cálculo na GPU (ex: multiplicar tudo por 2)"),
    line("    inicio_calc = time.time()"),
    line("    resultado = dado_vram * 2.0"),
    line("    torch.cuda.synchronize()"),
    line("    tempo_calc = time.time() - inicio_calc"),
    line("    "),
    line('    print(f"📦 Tamanho do Dado: {tamanho_mb} MB")'),
    line('    print(f"🚚 Tempo para TRANSFERIR (RAM -> VRAM): {tempo_transf:.5f}s")'),
    line('    print(f"⚡ Tempo para PROCESSAR na GPU:         {tempo_calc:.5f}s")'),
    line("    "),
    line("    # Gráfico de pizza"),
    line("    labels = ['Transferência (PCIe)', 'Processamento (GPU)']"),
    line("    tempos = [tempo_transf, tempo_calc]"),
    line("    plt.figure(figsize=(6, 5))"),
    line("    plt.pie(tempos, labels=labels, autopct='%1.1f%%', colors=['#fcc419', '#339af0'], startangle=90)"),
    line("    plt.title('Onde foi gasto o tempo total?')"),
    line("    plt.show()"),
    line("else:"),
    line("    print(\"⚠️ Ative a GPU no Colab para este teste.\")")
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    line("## 🔹 Bloco 3: Processamento Paralelo de Imagens em Blocos (Aulas 7 e 8)"),
    line(""),
    line("**Conceito:**"),
    line("Como as GPUs trabalham com visão computacional? Elas dividem a imagem em uma **grade de blocos e threads (Tiling)**. Cada thread cuida de um pequeno grupo de pixels simultaneamente.")
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    line("# @title 🎛️ Experimento 3: Filtro de Imagem Paralelo (Simulação Visual de CUDA)"),
    line("import numpy as np"),
    line("import matplotlib.pyplot as plt"),
    line(""),
    line("# Criar uma imagem sintética (um padrão geométrico colorido)"),
    line("largura, altura = 500, 500"),
    line("x, y = np.meshgrid(np.linspace(-2, 2, largura), np.linspace(-2, 2, altura))"),
    line("imagem_original = np.sin(x**2 + y**2)"),
    line(""),
    line("# Escolher o filtro interativo"),
    line('efeito = "Inverter e Contrastar" # @param ["Borrão (Blur)", "Inverter e Contrastar", "Detecção de Bordas"]'),
    line(""),
    line("def aplicar_filtro(img, efeito_escolhido):"),
    line('    if efeito_escolhido == "Borrão (Blur)":'),
    line("        return np.roll(img, 5, axis=0) * 0.5 + img * 0.5"),
    line('    elif efeito_escolhido == "Inverter e Contrastar":'),
    line("        return np.where(img > 0, 1.0, -1.0)"),
    line("    else:"),
    line("        return np.abs(np.gradient(img)[0])"),
    line(""),
    line("imagem_processada = aplicar_filtro(imagem_original, efeito)"),
    line(""),
    line("# Exibição lado a lado"),
    line("fig, ax = plt.subplots(1, 2, figsize=(10, 4))"),
    line("ax[0].imshow(imagem_original, cmap='magma')"),
    line('ax[0].set_title("1. Imagem Original (Matriz de Pixels)")'),
    line("ax[0].axis('off')"),
    line(""),
    line("ax[1].imshow(imagem_processada, cmap='viridis')"),
    line('ax[1].set_title(f"2. Resultado GPU: {efeito}")'),
    line("ax[1].axis('off')"),
    line(""),
    line("plt.tight_layout()"),
    line("plt.show()"),
    line('print("💡 Dica: Na GPU, cada um dos 250.000 pixels foi calculado ao mesmo tempo por threads paralelas!")')
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    line("## 🔹 Bloco 4: Monitorando a VRAM com Modelos de Linguagem (Aulas 9 e 10)"),
    line(""),
    line("**Conceito:**"),
    line("Modelos de IA (LLMs) ocupam espaço na **VRAM (Memória da Placa de Vídeo)**. Se o modelo for grande demais para a VRAM disponível, ocorre o erro de *Out of Memory (OOM)*.")
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    line("# @title 🎛️ Experimento 4: Monitor de VRAM do Linux (`nvidia-smi` em tempo real)"),
    line("import subprocess"),
    line("import torch"),
    line(""),
    line('print("📊 MONITOR DE RECURSOS DA GPU (NVIDIA-SMI):\\n")'),
    line("try:"),
    line("    # Executa o comando de terminal do Linux"),
    line("    resultado_smi = subprocess.check_output(['nvidia-smi']).decode('utf-8')"),
    line("    print(resultado_smi)"),
    line("except Exception as e:"),
    line('    print("⚠️ Não foi possível rodar o nvidia-smi. Certifique-se que está usando GPU no Colab.")'),
    line(""),
    line("if torch.cuda.is_available():"),
    line("    vram_total = torch.cuda.get_device_properties(0).total_memory / (1024**3)"),
    line("    vram_alocada = torch.cuda.memory_allocated(0) / (1024**3)"),
    line("    vram_livre = vram_total - vram_alocada"),
    line("    "),
    line('    print(f"🎯 Placa Detectada: {torch.cuda.get_device_name(0)}")'),
    line('    print(f"💾 VRAM Total:     {vram_total:.2f} GB")'),
    line('    print(f"🔴 VRAM Usada:     {vram_alocada:.2f} GB")'),
    line('    print(f"🟢 VRAM Livre:     {vram_livre:.2f} GB")')
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    line("## 🔹 Bloco 5: Testando uma IA Real — Análise de Sentimento de Clientes (Aula 11)"),
    line(""),
    line("**Conceito:**"),
    line("Vamos colocar tudo em prática! Carregaremos um modelo pré-treinado na GPU para analisar avaliações de clientes automaticamente.")
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    line("# @title 🎛️ Experimento 5: Classificador de Feedbacks de Clientes (Aplicação Prática)"),
    line("from transformers import pipeline"),
    line("import torch"),
    line(""),
    line("# Texto de entrada via formulário do Colab"),
    line('texto_do_cliente = "O produto chegou dentro do prazo, mas a embalagem veio amassada e o manual de instruções é muito confuso." # @param {type:"string"}'),
    line(""),
    line('print("🤖 Carregando modelo de Inteligência Artificial na GPU...")'),
    line("dispositivo = 0 if torch.cuda.is_available() else -1"),
    line(""),
    line("# Pipeline leve da Hugging Face"),
    line("classificador = pipeline("),
    line('    "sentiment-analysis", '),
    line('    model="nlptown/bert-base-multilingual-uncased-sentiment",'),
    line("    device=dispositivo"),
    line(")"),
    line(""),
    line("resultado = classificador(texto_do_cliente)[0]"),
    line(""),
    line("estrelas = resultado['label'] # Ex: '1 star', '4 stars'"),
    line("confianca = resultado['score'] * 100"),
    line(""),
    line('print("\\n" + "="*50)'),
    line('print(f"📝 Texto Analisado: \'{texto_do_cliente}\'")'),
    line('print(f"⭐ Avaliação Estimada: {estrelas}")'),
    line('print(f"🎯 Grau de Confiabilidade da IA: {confianca:.1f}%")'),
    line('print("="*50)')
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open(r"C:\Users\Jonas\Documents\repos\senac-tecnico-ia\aulas\aula12\aula12_pratica_colab.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)
print("NOTEBOOK_GENERATED_SUCCESSFULLY")
