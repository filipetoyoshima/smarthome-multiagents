# Modelando Agentes

Agentes inteligentes (autonomia, cooperação, aprendizado): Agente de sensores(reativos), de saída elétrica (reativos), de ar-condicionado(reativos), lâmpada (reativos), Luminosidade(proativo), presença (proativa e reativa).

## Descrição

1. Agente de sensor de temperatura 

* Estado: Valor de temperatura varia ao logo do dia entre -50 a 50 C. Modifica situação do agente ar-condicionado.
* Comportamento: Varia temperatura sozinho (mocar clima ao longo do dia numa região média); Não aceita e não precisa ser modificado abruptamente por outro agente,
                               Aceita consultas/solicitação do estado, aceita mudanças de estado por outros agentes (ar-condicionado).

2. Agente de saída elétrica

* Estado: Valor da corrente elétrica. Modifica situação de todos os sensores(envia sinal avisando que não tem energia).
* Comportamento: Corrente varia conforme região em que se encontra <Usar dados "mocados" reais>

3. Agente de Ar-Condicionado 

* Estado: Pode estar ligado, desligado e com problema.
* Comportamento: Se receber mensagem da temperatura, muda estado para ligado/desligado. Caso apresente problema (2 anos de uso/mais) manda msg ao usuário para que ele leve o equipamento no técnico.

4. Agente lâmpada:

* Estado: Pode estar ligada, desligada ou queimada.
* Comportamento: Se oscilação de energia é muito alta, lâmpada tem brilho menor. Se pessoa pessoa envia sinal de que entrou no cômodo, lâmpada acende. Se pessoa envia sinal sonoro desligar, ela desliga. Após as 18h se iluminação for baixa liga a luz de fora automaticamente.

5. Agente luminosidade

* Estado: Contabilização de iluminação no ambiente
* Comportamento: Varia ao longo do dia (valores mocados) e envia valores pras lâmpadas após as 18h e para as cortinas da sala.

6. Agente presença

* Estado: Capta a presença de alguém no cômodo em que se encontra
* Comportamento: Detecta presença e envia sinal pros agentes lâmpada e ar-condicionado para que cu

7. Agente de sensor de proximidade

* Estado: Detecta proximidade de pessoa da porta, podendo ter ou não alguém presente.
* Comportamento: Ao detectar presença de alguém, envia sinal para a porta <VER SE FAZ A PORTA FICAR CONSULTANDO SENSOR DE PROXIMIDADE>

- Kitnet automatizada: 1 quarto, 1 sala, 1 cozinha, 1 banheiro, 1 portão, 2 portas.

## Funções do sistema

1. Ao entrar num ambiente escuro, a luz acende.
2. Quando temperatura estiver acima de 20 graus, o ar-condicionado liga em 17 graus.
3. Presença aciona abertura do portão pelo celular, portão destranca.
4. Em casos de grande luminosidade, as cortinas fecham.
5. Ao usuário se aproximar de uma porta, a porta se abre.
