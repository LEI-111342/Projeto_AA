from collections import deque


class Wall:
    def __init__(self, x, y):
        # Inicializa uma parede na posição (x, y)
        self.x = x
        self.y = y
        self.name = "|"


class Completion:
    def __init__(self, x, y):
        # Inicializa o farol na posição (x, y)
        self.x = x
        self.y = y
        self.name = "*"


class World:
    rows = 7
    cols = 7

    def __init__(self):
        # Cria um grid vazio e inicializa lista de agentes e completion
        self.grid = [['.' for _ in range(World.cols)] for _ in range(World.rows)]
        self.agents = []
        self.completion = None
        self.distance_map = None

    def reset(self):
        # Reseta o mundo para um grid vazio e limpa agentes/completion
        self.grid = [['.' for _ in range(World.cols)] for _ in range(World.rows)]
        self.agents = []
        self.completion = None
        self.distance_map = None

    def place(self, obj):
        # Coloca um objeto (agente ou completion) no grid
        if self.grid[obj.x][obj.y] == '.':
            self.grid[obj.x][obj.y] = obj.name
            from Agent import AgentBase
            if isinstance(obj, AgentBase):
                self.agents.append(obj)
            elif isinstance(obj, Completion):
                self.completion = obj
    def place_wall(self, x, y):
        # Coloca uma parede na posição (x, y)
        self.grid[x][y] = "|"

    def place_completion(self, x, y):
        # Coloca o farol na posição (x, y)
        self.completion = Completion(x, y)
        self.grid[x][y] = "*"

    def is_valid_move(self, x, y):
        # Verifica se a posição (x, y) é válida para mover
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return self.grid[x][y] != "|"
        return False

    def move_agent_to(self, agent, x, y):
        # Move o agente para a posição
        if (agent.x, agent.y) != (self.completion.x, self.completion.y):
            self.grid[agent.x][agent.y] = "."

        agent.x = x
        agent.y = y

        # Escreve o agente no grid se não estiver na completion
        if (x, y) != (self.completion.x, self.completion.y):
            self.grid[x][y] = agent.name

    def compute_distance_map(self):
        # Calcula a distância mínima de cada célula até a completion usando BFS
        if not self.completion:
            return

        self.distance_map = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        q = deque()
        cx, cy = self.completion.x, self.completion.y
        self.distance_map[cx][cy] = 0
        q.append((cx, cy))

        while q:
            x, y = q.popleft()
            dist = self.distance_map[x][y]

            # Explora vizinhos: cima, baixo, esquerda, direita
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx = x + dx
                ny = y + dy

                if 0 <= nx < self.rows and 0 <= ny < self.cols:
                    if self.grid[nx][ny] == "|":
                        continue
                    if self.distance_map[nx][ny] is None:
                        # Atualiza distância e adiciona à file
                        self.distance_map[nx][ny] = dist + 1
                        q.append((nx, ny))
