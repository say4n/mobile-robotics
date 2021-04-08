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
    print(env)

    free_cells = env.get_free_cells()

    belief = np.zeros((env.get_n_rows(), env.get_n_cols()))
    for cell in free_cells:
        r, c = cell
        belief[r, c] = 1/len(free_cells)

    print(f"Initial {belief = }.")

    actions = [
        [Stage.PERCEPTION],
        [Stage.PREDICTION, Direction.L],
        [Stage.PERCEPTION],
        [Stage.PREDICTION, Direction.U],
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
            posteriors = posteriors / np.sum(posteriors)

            # Update beliefs.
            belief = np.zeros(belief.shape)
            for i, (r, c) in enumerate(possible_locs):
                belief[r][c] = posteriors[i]
        else:
            # Act phase.
            a = action[1]

        print(f"Action `{action = }` executed.\n{belief = }")
