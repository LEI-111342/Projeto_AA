# Projeto_AA README

# Créditos
### Pedro Correia 111342 
### José Gil
### Ambos estudantes do Instituto Universitário de Lisboa aka ISCTE

# Descrição 
Este projeto tem como função fazer um agente aprender usando a novelty e fitness. Este agente vai aprender a andar num 
labirinto à procura da melhor solução. Também é possível correr agentes fixos sem inteligência.

# Importante antes de correr o programa

## Como alterar o número de passos maximos dos agentes
Para se alterar o número de passos maximos dos agentes nao inteligentes basta alterar o valor da variável max_moves no 
AgentBase. No agente inteligente é a variável num_Steps que se encontra na segunda célula do modulo Graphs.ipynb

## Como adicionar novo agente no labirinto 
Para se adicionar um novo agente é preciso criar uma classe para ele no módulo Agent.py e depois no módulo Mazes.py 
fazer world.place(Nome_do_Agente(x, y)), onde (x, y) são as coordenadas iniciais.

## Como adicionar um novo labirinto 
Para se adicionar um novo labirinto é só seguir a estrutura de como os outros labirintos são criados, é apenas importante 
lembrar de dar um maze_id unico para todos eles. Depois é mudar o número do maze_id no fim do módulo Simulator.py para 
correr os agentes não inteligentes ou na segunda celula do módulo Graphs.ipynb para correr o agente inteligente

## Como acelerar/abrandar os agentes na interface 
No início do módulo Simulator existe uma variavel chamada FPS, quanto maior o número mais rapido os agentes mexem-se e 
vice-versa, note que esta mudança é apenas visual e não afeta o comportamento de nenhum agente.

## Mudei o codigo mas o Graphs.ipynb continua a utilizar o codigo antigo
Não sei se este problema é geral, mas no pycharm, o programa usado para criar este codigo, para as alterações fora desse 
modulo registarem é necessário clicar no botão Restart_kernel dentro do mesmo

# Como correr o codigo já existente
Para correr os agentes não inteligentes basta dar run no módulo Simulator.py, para corre o agente inteligente é necessário
ir ao módulo Graphs.ipynb e correr primeiro a primeira célula do mesmo, só depois se pode correr a segunda celula,
esta, sim, metendo o agente a aprender
