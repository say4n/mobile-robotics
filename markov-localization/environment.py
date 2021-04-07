import numpy as np
from enum import Enum

class State(Enum):
    FREE = 0                # Cell is free.
    OCCUPIED = 1            # Cell is a wall.

class Stage(Enum):
    PREDICTION = 100        # Prediction/action stage.
    PERCEPTION = 101        # Perception/measurement/correction stage.

class Direction(Enum):
    U = 200                 # Up action.
    D = 201                 # Down action.
    L = 202                 # Left action.
    R = 203                 # Right action.

class Environment:
    def __init__(self, map):
        n_rows = len(map)
        n_cols = len(map[0])

        self.map = [[None for _ in range(n_cols)] for _ in range(n_rows)]

        for r in range(n_rows):
            for c in range(n_cols):
                self.map[r][c] = State.FREE if map[r][c] == 0 else State.OCCUPIED

        self.map = np.array(self.map)

        self.n_rows = n_rows
        self.n_cols = n_cols

        self.free_cells = np.argwhere(self.map == State.FREE)
        self.__position = self.free_cells[np.random.choice(np.arange(len(self.free_cells)))]

    def get_n_rows(self):
        return self.n_rows

    def get_n_cols(self):
        return self.n_cols

    def sense(self, position = None):
        r, c = self.__position if position is None else position
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

    def get_possible_locations_given_observation(self, observation):
        slots = []
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                if self.sense((r, c)) == observation:
                    slots.append((r, c))

        return slots

    def __repr__(self):
        to_print = ""

        pos_r, pos_c = self.__position

        for r in range(self.n_rows):
            for c in range(self.n_cols):
                to_print += "|"
                if pos_r == r and pos_c == c:
                    to_print += "x"
                elif self.map[r][c] == State.FREE:
                    to_print += " "
                else:
                    to_print += "#"

            to_print += "|\n"

        return to_print


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
    print(env)
