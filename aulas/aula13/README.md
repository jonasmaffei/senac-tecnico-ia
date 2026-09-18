# 📖 Guia Passo a Passo: Como Abrir e Rodar o Notebook da Aula 13 no Google Colab

---

## 🚀 Opção 1: Abrir Direto via GitHub (Mais Rápido e Recomendado)

1. Acesse o site do [Google Colab](https://colab.research.google.com/).
2. Faça login com a sua conta Google (Gmail).
3. Na janela pop-up que abrir, selecione a aba **GitHub**.
4. No campo de busca, cole a URL do repositório da turma:
   ```text
   https://github.com/jonasmaffei/senac-tecnico-ia
   ```
5. O Colab irá listar os arquivos do repositório. Clique em:
   `aulas/aula13/aula13_implementacao_modelo_paralelo.ipynb`
6. Pronto! O notebook abrirá na sua tela.

---

## 💻 Opção 2: Fazer Download do Arquivo e Subir no Colab (Upload)

Se você já baixou o repositório ou o arquivo `.ipynb` para o seu computador:

1. Acesse o site do [Google Colab](https://colab.research.google.com/).
2. Na janela inicial, clique na aba **Fazer upload** (ou **Upload**).
3. Clique em **Escolher arquivo** e selecione o arquivo `aula13_implementacao_modelo_paralelo.ipynb` no seu computador.
4. Aguarde o carregamento e o notebook abrirá automaticamente.

---

## ⚙️ PASSO CRÍTICO: Ativar a GPU no Google Colab

Por padrão, o Google Colab roda usando apenas o processador tradicional (**CPU**). Como nosso foco é testar a aceleração paralela em GPU (CUDA Numba e CuPy), você **deve ativar a GPU** antes de rodar as medições:

1. No menu superior do Colab, clique em **Ambiente de execução** (ou *Runtime*).
2. Clique na opção **Alterar tipo de ambiente de execução** (ou *Change runtime type*).
3. Na janela que abrir, localize a opção **Acelerador de hardware** (ou *Hardware accelerator*).
4. Mude de **None/CPU** para **T4 GPU** (ou GPU disponível gratuitamente).
5. Clique no botão **Salvar** (ou *Save*).
6. No canto superior direito, verifique se aparece um ícone verde mostrando **RAM / GPU**.

---

## 🟢 Conteúdo do Notebook da Aula 13

No notebook `aula13_implementacao_modelo_paralelo.ipynb`, você encontrará:
1. **Introdução Teórica & Modelo SIMT vs SIMD**
2. **Versão 1 — CPU Python Puro** (Soma vetorial e Produto escalar)
3. **Versão 2 — CPU com NumPy** (Vetorização e BLAS otimizado)
4. **Versão 3 — GPU com CUDA Numba** (Kernels customizados com redução em Shared Memory)
5. **Versão 4 — GPU com CuPy** (NumPy acelerado na GPU)
6. **Benchmark Completo e Coleta de Métricas** (Varredura de $N \in [10K, 100K, 1M, 10M, 100M]$)
7. **Visualização Gráfica Interativa** (Tempos absolutos e Speedup com Matplotlib)
8. **Tarefa Final do Bloco 2 & Seção Extra (`np.linalg.norm` vs `cp.linalg.norm`)**
9. **Mini-Relatório Técnico e Conclusão**
10. **Lista de 20 Exercícios Práticos e Teóricos** (Exercícios 1 a 10 conceituais e 11 a 20 mão na massa em Python/CUDA/CuPy)
