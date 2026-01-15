# Evolver.py

import random
from Agent import AgentEvolver


# ---------------------------------------------------------
# Distância de Jaccard entre dois comportamentos
# Agora comportamento = conjunto de posições visitadas
# ---------------------------------------------------------
def jaccard_distance(set1, set2):
    if not set1 and not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return 1.0 - (intersection / union)


# ---------------------------------------------------------
# Novelty score: média das k menores distâncias
# ---------------------------------------------------------
def compute_novelty(current_behavior, archive, k=5):
    if not archive:
        return 1.0

    distances = [
        jaccard_distance(current_behavior, past)
        for past in archive
    ]
    distances.sort()

    k = min(k, len(distances))
    return sum(distances[:k]) / k


# ---------------------------------------------------------
# Classe Evolver
# ---------------------------------------------------------
class Evolver:
    def __init__(
        self,
        world_template,
        population_size,
        num_generations,
        mutation_rate,
        tournament_size,
        novelty_weight,
        archive_add,
        num_steps
    ):
        self.world_template = world_template
        self.POP = population_size
        self.NGEN = num_generations
        self.MUT = mutation_rate
        self.TOUR = tournament_size
        self.novelty_weight = novelty_weight
        self.N_ARCHIVE_ADD = archive_add
        self.num_steps = num_steps

        # posição inicial (todos começam aqui)
        if world_template.agents:
            self.start_x = world_template.agents[0].x
            self.start_y = world_template.agents[0].y
        else:
            self.start_x = 0
            self.start_y = 0

        # população inicial (SEM genome_length)
        self.population = [
            AgentEvolver(self.start_x, self.start_y)
            for _ in range(self.POP)
        ]

        self.archive = []
        self.avg_fitness_history = []
        self.best_paths = []

    # -----------------------------------------------------
    # Seleção por torneio (fitness combinada)
    # -----------------------------------------------------
    def select_parent(self):
        tournament = random.sample(self.population, self.TOUR)
        tournament.sort(key=lambda a: a.combined_fitness, reverse=True)
        return tournament[0]

    # -----------------------------------------------------
    # Avaliação da população
    # -----------------------------------------------------
    def evaluate_population(self):
        total = 0.0

        for agent in self.population:
            world = agent.run_simulation(
                self.world_template,
                max_steps=self.num_steps
            )

            obj = agent.calculate_objective_fitness(world)
            nov = compute_novelty(agent.behavior, self.archive)

            agent.objective_score = obj
            agent.novelty_score = nov
            agent.combined_fitness = obj + (nov * self.novelty_weight)

            total += agent.combined_fitness

        return total / len(self.population)

    # -----------------------------------------------------
    # Atualização do arquivo de novelty
    # -----------------------------------------------------
    def update_archive(self):
        self.population.sort(
            key=lambda a: compute_novelty(a.behavior, self.archive),
            reverse=True
        )

        for i in range(min(self.N_ARCHIVE_ADD, len(self.population))):
            self.archive.append(set(self.population[i].behavior))

    # -----------------------------------------------------
    # Criação da nova geração
    # -----------------------------------------------------
    def create_new_generation(self):
        self.population.sort(
            key=lambda a: a.combined_fitness,
            reverse=True
        )

        # elitismo (10%)
        elite_size = max(1, self.POP // 10)
        new_population = [
            self.population[i].clone()
            for i in range(elite_size)
        ]

        # resto por crossover + mutação
        while len(new_population) < self.POP:
            p1 = self.select_parent()
            p2 = self.select_parent()

            c1, c2 = AgentEvolver.crossover(p1, p2)
            c1.mutate(self.MUT)
            c2.mutate(self.MUT)

            new_population.append(c1)
            if len(new_population) < self.POP:
                new_population.append(c2)

        self.population = new_population

    # -----------------------------------------------------
    # Loop principal da evolução
    # -----------------------------------------------------
    def run(self):
        print("Starting evolution...")

        for gen in range(self.NGEN):
            avg = self.evaluate_population()
            self.avg_fitness_history.append(avg)

            best = max(
                self.population,
                key=lambda a: a.combined_fitness
            )
            self.best_paths.append(best.path)

            print(
                f"Gen {gen+1}/{self.NGEN} | "
                f"Avg: {avg:.2f} | "
                f"Best: {best.combined_fitness:.2f} "
                f"(obj={best.objective_score:.2f}, "
                f"nov={best.novelty_score:.2f})"
            )

            self.update_archive()

            if gen < self.NGEN - 1:
                self.create_new_generation()

        # avaliação final
        self.evaluate_population()
        self.population.sort(
            key=lambda a: a.combined_fitness,
            reverse=True
        )

        print("Evolution finished.")
        return self.population[0]
