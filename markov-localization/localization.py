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

        self.__position = np.random.choice(np.argwhere(map == 0))

    def sense(self):
        r, c = self.__position
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
        r, c = self.__position

        if direction == Direction.U:
            if self.__is_free_cell(r + 1, c):
                self.__position = (r + 1, c)
        elif direction == Direction.D:
            if self.__is_free_cell(r - 1, c):
                self.__position = (r - 1, c)
        elif direction == Direction.L:
            if self.__is_free_cell(r, c - 1):
                self.__position = (r, c - 1)
        elif direction == Direction.R:
            if self.__is_free_cell(r, c + 1):
                self.__position = (r, c + 1)
        else:
            raise ValueError(f"Invalid {direction = }.")

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
