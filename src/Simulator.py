import pygame
import sys
import time

from World import World
from Mazes import load_maze

CELL_SIZE = 40
FPS = 10

def draw_world(screen, world):
    COLOR_EMPTY = (255,255,255)
    COLOR_WALL = (60,60,60)
    COLOR_GRID = (180,180,180)
    COLOR_AGENT = (0,152,255)
    COLOR_GOAL = (255,255,0)

    screen.fill((255,255,255))

    # Fonte para as letras dos agentes
    font = pygame.font.SysFont("Arial", 22, bold=True)

    for i in range(world.rows):
        for j in range(world.cols):
            cell_rect = (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cell = world.grid[i][j]


            if cell == "|":
                color = COLOR_WALL
            elif cell == "*":
                color = COLOR_GOAL
            else:
                color = COLOR_EMPTY

            pygame.draw.rect(screen, color, cell_rect)


            for agent in world.agents:
                if agent.x == i and agent.y == j:
                    # fundo azul
                    pygame.draw.rect(screen, COLOR_AGENT, cell_rect)

                    # letra do agente
                    letter = agent.name

                    text_surface = font.render(letter, True, (255,255,255))
                    text_rect = text_surface.get_rect(center=(
                        j * CELL_SIZE + CELL_SIZE//2,
                        i * CELL_SIZE + CELL_SIZE//2
                    ))
                    screen.blit(text_surface, text_rect)


            if cell == "*":
                text_surface = font.render("*", True, (0,0,0))
                text_rect = text_surface.get_rect(center=(
                    j * CELL_SIZE + CELL_SIZE//2,
                    i * CELL_SIZE + CELL_SIZE//2
                ))
                screen.blit(text_surface, text_rect)


    for j in range(world.cols + 1):
        pygame.draw.line(screen, COLOR_GRID,
                         (j * CELL_SIZE, 0),
                         (j * CELL_SIZE, world.rows * CELL_SIZE))

    for i in range(world.rows + 1):
        pygame.draw.line(screen, COLOR_GRID,
                         (0, i * CELL_SIZE),
                         (world.cols * CELL_SIZE, i * CELL_SIZE))

    pygame.display.flip()


# ---------------------------------------------------------
def run_maze(world):
    pygame.init()
    screen = pygame.display.set_mode((world.cols * CELL_SIZE,
                                      world.rows * CELL_SIZE))
    pygame.display.set_caption("Maze Simulation")

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for agent in world.agents:
            agent.act(world)

        draw_world(screen, world)

        all_done = all(a.moves_left == 0 or
                       (a.x,a.y)==(world.completion.x,world.completion.y)
                       for a in world.agents)

        if all_done:
            time.sleep(1)

            print("\nResultados da Simulação")
            for agent in world.agents:

                usados = agent.max_moves - agent.moves_left

                chegou = (agent.x, agent.y) == (world.completion.x, world.completion.y)

                print(f"Agente {agent.name}:")
                print(f"  Passos usados: {usados}")
                print(f"  Chegou ao final? {'SIM' if chegou else 'NÃO'}")

            running = False

    pygame.quit()


def main():
    world = World()

    maze_id = 1
    print(f"\n=== Maze {maze_id} ===")
    load_maze(world, maze_id)
    run_maze(world)

    print("Todos os mazes concluídos!")


if __name__ == "__main__":
    main()
