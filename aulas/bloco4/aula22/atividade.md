# 📝 Atividade: Aula 22 — Automação e Monitoramento

## 🎯 Situação

O modelo agora treina por horas ou dias. Ninguém fica olhando o terminal — é preciso
**monitorar automaticamente** e ser avisado se algo sair do normal.

---

## 🚀 Roteiro

1. Inicie o treino e pegue o PID dele.
2. Rode o monitor junto (em outro terminal):
   ```bash
   cd aulas/bloco4/aula22/scripts
   ./monitor_treinamento.sh $PID_DO_TREINO 10
   ```
3. Confira o CSV gerado em `logs/monitor/`.
4. Baixe o limite de temperatura (ex.: 60) e veja o alerta disparar.

> 💡 No Windows/GPU AMD, use como referência o laboratório da Aula 17.

---

## 💬 Discussão em grupo (10 min)

1. O monitor encerrou sozinho quando o treino acabou?
2. Que limite de temperatura faz sentido para a sua GPU?
3. O CSV mostra alguma anomalia (pico de temperatura, VRAM crescendo)?

---

## 📚 Trilha de pesquisa (alternativa sem código)

Documente o **monitoramento como requisito**: quais métricas importam, custo/energia estimado e
quais ferramentas seriam usadas — sem precisar executar o monitor.


## 📌 Tarefa de casa (para a Aula 23)

1. Rodar um treino completo com o monitor e salvar o CSV.
2. Testar o alerta de temperatura.
3. Preparar o **pitch** do projeto.
