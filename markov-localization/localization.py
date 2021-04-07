import numpy as np
from environment import State, Stage, Direction, Environment


if __name__ == "__main__":
    map = [
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    ]

    env = Environment(map)
    free_cells = env.get_free_cells()

    belief = np.zeros((env.get_n_rows(), env.get_n_cols()))
    for cell in free_cells:
        r, c = cell
        belief[r, c] = 1/len(free_cells)

    print(belief)

    actions = [
        [Stage.PERCEPTION],
        [Stage.PREDICTION, Direction.L],
        [Stage.PERCEPTION],
        [Stage.PREDICTION, Direction.U],
        [Stage.PERCEPTION],
        [Stage.PREDICTION, Direction.R],
        [Stage.PERCEPTION]
    ]