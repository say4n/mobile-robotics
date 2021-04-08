from copy import deepcopy
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

    print(f"Initial {belief = }")

    actions = [
        [Stage.PERCEPTION],
        [Stage.PREDICTION, Direction.L],
        [Stage.PERCEPTION],
        [Stage.PREDICTION, Direction.U],
        [Stage.PERCEPTION],
        [Stage.PREDICTION, Direction.R],
        [Stage.PERCEPTION],
        [Stage.PREDICTION, Direction.R],
        [Stage.PERCEPTION]
    ]

    for action in actions:
        if action[0] == Stage.PERCEPTION:
            # See phase.
            obs = env.sense()
            possible_locs = env.get_possible_locations_given_observation(obs)

            # Computer posterior probabilities.
            posteriors = np.zeros(len(possible_locs))
            for i, (r, c) in enumerate(possible_locs):
                # Assuming perfect sensing.
                posteriors[i] = 1 * belief[r][c]

            # Normalize probabilities.
            # breakpoint()
            posteriors = posteriors / np.sum(posteriors)

            # Update beliefs.
            belief = np.zeros(belief.shape)
            for i, (r, c) in enumerate(possible_locs):
                belief[r][c] = posteriors[i]
        else:
            # Act phase.
            direction = action[1]
            env.act(direction)

            # Keep a copy of previous beliefs.
            belief_copy = deepcopy(belief)

            # Re-initialize beliefs.
            belief = np.zeros(belief.shape)

            # Update beliefs.
            non_zero_probability_cells = np.argwhere(belief_copy > 0)
            for r, c in non_zero_probability_cells:
                next_r, next_c = env.get_next_state(direction, (r, c))
                # Assuming single possible movement here.
                # Else, needs to be divided by number of possible next states.
                belief[next_r][next_c] += belief_copy[r][c]

        # print(f"Action `{action = }` executed.\n{belief = }")
        # print(env)

    print(f"Final {belief = }")
