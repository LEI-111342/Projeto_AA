import random
from World import *

class AgentBase:
    def __init__(self, x, y, name="A", max_moves=50):
        # Inicializa a posição, nome e número máximo de movimentos
        self.x = x
        self.y = y
        self.name = name
        self.moves_left = max_moves
        self.max_moves = max_moves


    def has_moves(self):
        # Verifica se o agente ainda tem movimentos restantes
        return self.moves_left > 0

    def __repr__(self):
        # Representação do agente como seu nome
        return f"{self.name}"


# ---------------------------------------------------------
# RANDOM AGENT - move-se de forma aleatoria
# ---------------------------------------------------------
class AgentRandom(AgentBase):
    def __init__(self, x, y, name="R"):
        super().__init__(x, y, name)

    def act(self, world):
        # Executa um movimento aleatório válido no mundo
        if not self.has_moves():
            return

        directions = [(-1,0),(1,0),(0,-1),(0,1)]  # cima, baixo, esquerda, direita
        random.shuffle(directions)  # embaralha para escolher aleatoriamente

        for dx, dy in directions:
            nx = self.x + dx
            ny = self.y + dy

            if world.is_valid_move(nx, ny):
                world.move_agent_to(self, nx, ny)
                self.moves_left -= 1
                return


# ---------------------------------------------------------
# FOLLOWER AGENT - usa distance_map
# ---------------------------------------------------------
class AgentFollower(AgentBase):
    def __init__(self, x, y, name="F"):
        super().__init__(x, y, name)

    def act(self, world):
        # Move em direção à completion seguindo o distance_map
        if not self.has_moves():
            return

        dm = world.distance_map
        if dm is None:
            return

        best_val = dm[self.x][self.y]
        best_pos = None

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx = self.x + dx
            ny = self.y + dy
            if 0 <= nx < world.rows and 0 <= ny < world.cols:
                if world.is_valid_move(nx, ny):
                    val = dm[nx][ny]
                    if val is not None and val < best_val:
                        best_val = val
                        best_pos = (nx, ny)

        if best_pos:
            world.move_agent_to(self, best_pos[0], best_pos[1])
            self.moves_left -= 1


# ---------------------------------------------------------
# LEFT-HAND RULE AGENT
# ---------------------------------------------------------
class LeftAgent(AgentBase):
    def __init__(self, x, y, name="L"):
        super().__init__(x, y, name)
        # 0=UP, 1=RIGHT, 2=DOWN, 3=LEFT
        self.dir_index = 0
        self.directions = [(-1,0),(0,1),(1,0),(0,-1)]

    def act(self, world):
        if not self.has_moves():
            return

        # PARA se já chegou ao objetivo
        if (self.x, self.y) == (world.completion.x, world.completion.y):
            return

        left = (self.dir_index - 1) % 4
        forward = self.dir_index
        right = (self.dir_index + 1) % 4
        back = (self.dir_index + 2) % 4

        for d in [left, forward, right, back]:
            dx, dy = self.directions[d]
            nx, ny = self.x + dx, self.y + dy

            if world.is_valid_move(nx, ny):
                self.dir_index = d
                world.move_agent_to(self, nx, ny)
                self.moves_left -= 1
                return


# ---------------------------------------------------------
# EVOLUTIONARY AGENT - aprende o labirinto
# ---------------------------------------------------------
from Sensor import Sensor
import random

class AgentEvolver(AgentBase):
    def __init__(self, x, y, genotype=None, genome_size=300, name="E"):
        super().__init__(x, y, name, max_moves=1000)

        self.start_x = x
        self.start_y = y

        if genotype is None:
            self.genotype = {}
            for _ in range(genome_size):
                key = tuple(random.randint(0,2) for _ in range(8)) + (random.randint(0,8),)
                self.genotype[key] = random.randint(0,3)
        else:
            self.genotype = genotype.copy()

        self.behavior = set()
        self.path = []

        self.objective_score = 0
        self.novelty_score = 0
        self.combined_fitness = 0

    def clone(self):
        return AgentEvolver(self.start_x, self.start_y, self.genotype)

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.moves_left = 1000
        self.behavior = set()
        self.path = []

    def act(self, world):
        if not self.has_moves():
            return

        sensors = Sensor.sense(world, self)

        if sensors not in self.genotype:
            self.genotype[sensors] = random.randint(0, 3)

        preferred_move = self.genotype[sensors]

        # tenta ação preferida primeiro
        moves = [preferred_move] + [m for m in range(4) if m != preferred_move]

        for move in moves:
            dx, dy = [(-1, 0), (0, 1), (1, 0), (0, -1)][move]
            nx, ny = self.x + dx, self.y + dy

            if world.is_valid_move(nx, ny):
                world.move_agent_to(self, nx, ny)
                break  # executa só um movimento

        self.behavior.add((self.x, self.y))
        self.path.append((self.x, self.y))
        self.moves_left -= 1

    def run_simulation(self, world_template, max_steps):
        import copy
        self.reset()

        world = copy.deepcopy(world_template)
        world.agents = [self]
        world.grid[self.x][self.y] = self.name

        for _ in range(max_steps):
            self.act(world)
            if (self.x, self.y) == (world.completion.x, world.completion.y):
                break

        return world

    def calculate_objective_fitness(self, world):
        last_x, last_y = self.x, self.y

        dx = abs(last_x - world.completion.x)
        dy = abs(last_y - world.completion.y)
        dist = dx + dy

        # recompensa base por proximidade
        score = 20 / (1 + dist)

        # recompensa por completar
        if (last_x, last_y) == (world.completion.x, world.completion.y):
            score += 200

        # penalização por revisitar posições
        revisits = len(self.path) - len(self.behavior)
        score -= 0.1 * (revisits ** 2)

        # penalização leve por caminho longo
        score -= 0.01 * len(self.path)

        return score

    @staticmethod
    def crossover(p1, p2):
        child_genotype = {}
        for k in p1.genotype:
            child_genotype[k] = p1.genotype[k] if random.random() < 0.5 else p2.genotype.get(k, random.randint(0,3))
        return AgentEvolver(p1.start_x, p1.start_y, child_genotype), \
               AgentEvolver(p1.start_x, p1.start_y, child_genotype)

    def mutate(self, rate):
        for k in list(self.genotype.keys()):
            if random.random() < rate:
                self.genotype[k] = random.randint(0,3)

