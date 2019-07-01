# SIMULADOR DE AUTOMAÇÃO RESIDENCIAL 

Este repositório contém todo o código necessário para simular a automação residencial de uma kitnet, com os seguintes cômodos:

- 1 quarto, com 1 ar-condicionado, 1 porta e 1 lâmpada;
- 1 cozinha, com 1 lâmpada;
- 1 sala, com 1 ar-condicionado, 1 porta e 1 lâmpada;
- 1 banheiro, com 1 porta e 1 lâmpada;

A partir disso, através da navegação do mouse em diferentes cômodos da casa, o sistema permite as seguintes funções: 

1. Ao entrar em um cômodo, a lâmpada acende;
2. Ao sair de um cômodo, a lâmpada apaga;
3. Ao entrar em um cômodo com ar-condicionado, quando a temperatura estiver acima de 25 graus, o ar-condicionado liga;
4. Quando a temperatura estiver abaixo de 20 graus, os ar-condicionados desligam (mesmo detectando presença nos cômodos);
5. Ao sair de um cômodo com ar-condicionado, o mesmo é desligado;
6. Ao se aproximar de uma porta, a porta se abre;

**Maiores descrições da implementação podem ser vista na [wiki](https://github.com/filipetoyoshima/smarthome-multiagents/wiki)**

## Como rodar a aplicação

Para visualizar a simulação é preciso ter instaladas as seguintes dependências na sua máquina: 

* Python 3: sudo apt-get install python3.6
* Osbrain: pip3 install osbrain
* TkInter: sudo apt-get install python3-tk

Assim, basta executar a interface gráfica : python3 src/graphic_user_interface/kitnet_gui.py
