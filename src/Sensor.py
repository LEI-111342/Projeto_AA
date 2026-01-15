class Sensor:
    # Direções: N, NE, E, SE, S, SW, W, NW
    DIRS = [(-1,0), (-1,1), (0,1), (1,1),
            (1,0), (1,-1), (0,-1), (-1,-1)]

    @staticmethod
    def sense(world, agent):
        sensors = []

        for dx, dy in Sensor.DIRS:
            x = agent.x + dx
            y = agent.y + dy

            if not (0 <= x < world.rows and 0 <= y < world.cols):
                sensors.append(1)
            elif world.grid[x][y] == "|":
                sensors.append(1)
            elif world.grid[x][y] == "*":
                sensors.append(2)
            else:
                sensors.append(0)

        # Quadrante do farol
        gx, gy = world.completion.x, world.completion.y
        dx = gx - agent.x
        dy = gy - agent.y

        quad_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        quad_y = 0 if dy == 0 else (1 if dy > 0 else -1)

        quadrant_map = {
            (-1,-1): 0, (-1,0): 1, (-1,1): 2,
            (0,-1): 3,  (0,0): 4,  (0,1): 5,
            (1,-1): 6,  (1,0): 7,  (1,1): 8
        }

        sensors.append(quadrant_map[(quad_x, quad_y)])

        return tuple(sensors)