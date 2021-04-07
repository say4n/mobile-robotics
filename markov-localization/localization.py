import numpy as np
from enum import Enum

class Direction(Enum):
    U = 0               # Up action.
    D = 1               # Down action.
    L = 2               # Left action.
    R = 3               # Right action.

class Stage(Enum):
    PREDICTION = 100    # Prediction/action stage.
    PERCEPTION = 101    # Perception/measurement/correction stage.

class State(Enum):
    FREE = 200          # Cell is free.
    OCCUPIED = 201      # Cell is a wall.

class Environment:
    def __init__(self, map):
        self.map = map

        self.n_rows = len(map)
        self.n_cols = len(map[0])

        self.position = np.random.choice(np.argwhere(map == 0))

    def sense(self):
        r, c = self.position
        obs = [None, None, None, None]  # Up, down, left, right.

        # Up.
        if self.__is_free_cell((r - 1, c)):
            obs[0] = State.FREE
        else:
            obs[0] = State.OCCUPIED

        # Down.
        if self.__is_free_cell((r + 1, c)):
            obs[0] = State.FREE
        else:
            obs[0] = State.OCCUPIED

        # Left.
        if self.__is_free_cell((r, c - 1)):
            obs[0] = State.FREE
        else:
            obs[0] = State.OCCUPIED

        # Right.
        if self.__is_free_cell((r, c + 1)):
            obs[0] = State.FREE
        else:
            obs[0] = State.OCCUPIED

        return obs

    def act(self, direction):
        pass

    def __is_free_cell(self, position):
        r, c = position
        if 0 <= r < self.n_rows and 0 <= c < self.n_cols:
            return self.map[r][c] == State.FREE
        else:
            # Invalid position.
            return State.OCCUPIED

    def __repr__(self):
        return self.map


if __name__ == "__main__":
    map = []
