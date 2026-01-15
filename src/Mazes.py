from World import Wall, Completion
from Agent import AgentRandom, AgentFollower, LeftAgent, AgentEvolver

def load_maze(world, maze_id):

    world.reset()

    # MAZE 1
    if maze_id == 1:

        world.place_completion(5, 1)

        walls = [
            (0, 1), (0, 3), (0, 5), (0, 6), (2, 1), (2, 2),
            (2, 3), (2, 4), (2, 5), (3, 0), (4, 0), (4, 1),
            (4, 2), (4, 3), (4, 5), (5, 0), (5, 2), (5, 4),
            (5, 5), (6, 0)
        ]

        for x, y in walls:
            world.place_wall(x, y)

        world.place(AgentRandom(0, 4))
        world.place(AgentFollower(0, 2))
        world.place(LeftAgent(0, 0))

        world.compute_distance_map()

    #MAZE 2
    if maze_id == 4:
        world.place_completion(5, 1)

        walls = [
            (0,1),(0,3),(0,5),(0,6),(2,1),(2,2),
            (2, 3),(2,4),(2,5),(3,0),(4,0),(4,1),
            (4, 2),(4,3),(4,5),(5,0),(5,2),(5,4),
            (5, 5),(6, 0)
        ]
        for x,y in walls:
            world.place_wall(x,y)

        world.compute_distance_map()

