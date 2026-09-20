######################################################################
# This file copyright the Georgia Institute of Technology
#
# Permission is given to students to use or modify this file (only)
# to work on their assignments.
#
# You may NOT publish this file or make it available to others not in
# the course.
#
######################################################################

# If you see different scores locally and on Gradescope, this may be because:
# - you forgot that the test cases for each are different (e.g., if your
#   solution is not robust enough, you may pass Test Case 4 locally but still
#   fail Test Case 4 on Gradescope, or vice-versa);
# - you are uploading a different file than the one you are executing locally
#   (i.e., if this local ID doesn't match the ID on Gradescope, this indicates
#   that you uploaded a different file), in which case you should use the
#   OUTPUT_UNIQUE_FILE_ID to determine if this is the case; and/or
# - you modified one of the other files in the project in a way that causes your
#   local results to differ (since those changes don't carry over to
#   Gradescope), in which case you should download a fresh copy of all the
#   project files.
from rait import matrix
import math
# constant F, H, and R for the six variable state system
F = matrix([[1, 0, 1, 0, 0.5, 0],
            [0, 1, 0, 1, 0, 0.5],
            [0, 0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]])

H = matrix([[1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0]])

rx = 0.045
ry = 0.075

R = matrix([[rx**2, 0],
            [0, ry**2]])

P_init = matrix([[1, 0, 0],
                 [0, 2, 0],
                 [0, 0, 4]])

COLD_START = 10
X_BUFFER = 0.2
Y_BUFFER = 0.2
JUMP_BUFFER = 0.4

OUTPUT_UNIQUE_FILE_ID = False
if OUTPUT_UNIQUE_FILE_ID:
    import hashlib, pathlib
    file_hash = hashlib.md5(pathlib.Path(__file__).read_bytes()).hexdigest()
    print(f'Unique file ID: {file_hash}')


def euc_distance(point_1, point_2):
    return math.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)

def rank_dict_vals(d):
    ranked_v = []
    ranked_k = []
    res = {}
    for k, v in d.items():
        if not ranked_v:
            ranked_v.append(v)
            ranked_k.append(k)
            continue
        idx = 0
        while idx < len(ranked_v):
            if v < ranked_v[idx]:
                idx += 1
            else:
                break
        ranked_v.insert(idx, v)
        ranked_k.insert(idx, k)
    for i, k in enumerate(ranked_k):
        res[k] = i
    return res

def elem_addition(a, b):
    if len(a) != len(b):
        raise ValueError('A and B must have same length')
    return [ax + bx for ax, bx in zip(a, b)]

class Asteroid:
    def __init__(self, state):
        self.x_pos = state[0]
        self.y_pos = state[1]
        self.x_vel = state[2]
        self.y_vel = state[3]

class AsteroidScorer:
    def __init__(self, agent_asteroid, x_bound):
        self.x_pos = agent_asteroid.x_pos
        self.y_pos = agent_asteroid.y_pos
        self.x_vel = agent_asteroid.x_vel
        self.y_vel = agent_asteroid.y_vel
        self.x_bound = x_bound
        self.A = max(x_bound / 2 - self.x_pos, 0)
        self.B = max(x_bound / 2 - self.x_pos, 0)**2
        self.C = max(self.x_pos - x_bound / 2, 0)
        self.D = max(self.x_pos - x_bound / 2, 0)**2
        self.E = 1
        self.F = 1

    def score(self, asteroid):
        return (self.A * asteroid.x_pos
                + self.B * asteroid.x_vel
                + self.C * (self.x_bound - asteroid.x_pos)
                - self.D * asteroid.x_vel
                + self.E * asteroid.y_pos
                + self.F * asteroid.y_vel)

class AsteroidSelector:
    def __init__(self, asteroid_states, scorer):
        self.available_asteroids = {i: Asteroid(state.transpose()[0]) for i, state in asteroid_states.items()}
        self.scorer = scorer
        self.best_score = -1 * math.inf
        self.best_asteroid_id = None

    def select(self):
        for i, asteroid in self.available_asteroids.items():
            score = self.scorer.score(asteroid)
            if score > self.best_score:
                self.best_score = score
                self.best_asteroid_id = i
        return self.best_asteroid_id


class Spaceship():
    """A class representing the Environment within which the spaceship will run,
     and containing the methods that will act on the spaceship."""

    def __init__(self, bounds, xy_start):
        """Initialize the Spaceship."""
        self.x_bounds = bounds['x']
        self.y_bounds = bounds['y']
        self.agent_pos_start = xy_start
        self.asteroid_states = None
        self.asteroid_uncertainty = None
        self.asteroid_life = {}
        self.coordinate = self.agent_pos_start
        self.ridden_asteroid_id = 0
        self.jump_distance = None

    def _init_single_asteroid(self, coordinate):
        state = matrix([[coordinate[0], coordinate[1], 0, 0, 0, 0]]).transpose()
        uncertainty = P_init.expand(6, 6, [0, 2, 4], [0, 2, 4]).scalar_mul(self.x_bounds[1]) + P_init.expand(6, 6, [1, 3, 5], [1, 3, 5]).scalar_mul(self.y_bounds[1])
        return state, uncertainty

    def _init_asteroids(self, asteroid_observations):
        # initialize X and P for the k asteroids to be estimated
        # TODO: enhance initialization strategy: potentially directly use first observation?
        self.asteroid_states = {}
        self.asteroid_uncertainty = {}
        for i, coordinate in asteroid_observations.items():
            self.asteroid_states[i], self.asteroid_uncertainty[i] = self._init_single_asteroid(coordinate)

    def predict_from_observations(self, asteroid_observations):
        """Observe asteroid locations and predict their positions at time t+1.
        Parameters
        ----------
        self = a reference to the current object, the Spaceship
        asteroid_observations = A dictionary in which the keys represent asteroid IDs
        and the values are a tuple of noisy x-coordinate observations,
        and noisy y-coordinate observations taken at time t.
        asteroid_observations format:
        ```
        `{1: (x-measurement, y-measurement),
          2: (x-measurement, y-measurement)...
          100: (x-measurement, y-measurement),
          }`
        ```

        Returns
        -------
        The output of the `predict_from_observations` function should be a dictionary of tuples
        of estimated asteroid locations one timestep into the future
        (i.e. the inputs are for measurements taken at time t, and you return where the asteroids will be at time t+1).

        A dictionary of tuples containing i: (x, y), where i, x, and y are:
        i = the asteroid's ID
        x = the estimated x-coordinate of asteroid i's position for time t+1
        y = the estimated y-coordinate of asteroid i's position for time t+1
        Return format:
        `{1: (x-coordinate, y-coordinate),
          2: (x-coordinate, y-coordinate)...
          100: (x-coordinate, y-coordinate)
          }`
        """
        # To view the visualization with the default pdf output (incorrect) uncomment the line below
        # return asteroid_observations

        # FOR STUDENT
        if self.asteroid_states is None:
            self._init_asteroids(asteroid_observations)

        # to address new asteroids getting added
        new_asteroids = asteroid_observations.keys() - self.asteroid_states.keys()
        if new_asteroids:
            for i in new_asteroids:
                new_state, new_uncertainty = self._init_single_asteroid(asteroid_observations[i])
                self.asteroid_states[i] = new_state
                self.asteroid_uncertainty[i] = new_uncertainty

        removed_asteroids = self.asteroid_states.keys() - asteroid_observations.keys()
        if removed_asteroids:
            for i in removed_asteroids:
                self.asteroid_states.pop(i)

        I = matrix()
        I.identity(6)
        # Measurement step
        for i, ob in asteroid_observations.items():
            x = self.asteroid_states[i]
            P = self.asteroid_uncertainty[i]
            z = matrix([[ob[0], ob[1]]]).transpose()
            y = z - H * x
            S = H * P * H.transpose() + R
            K = P * H.transpose() * S.inverse()
            self.asteroid_states[i] = x + K * y
            self.asteroid_uncertainty[i] = (I - K * H) * P

        # Prediction step
        for i in asteroid_observations.keys():
            self.asteroid_states[i] = F * self.asteroid_states[i]
            self.asteroid_uncertainty[i] = F * self.asteroid_uncertainty[i] * F.transpose()

        return {i: (self.asteroid_states[i][0][0], self.asteroid_states[i][1][0]) for i in asteroid_observations.keys()}

    def _find_jumpable_asteroids(self):
        res = {}
        for i, state in self.asteroid_states.items():
            # If it's the asteroid I'm on:
            if i == self.ridden_asteroid_id:
                continue
            # If it's too new
            if self.asteroid_life[i] <= COLD_START:
                continue
            coordinate = (state[0][0], state[1][0])
            if euc_distance(self.coordinate, coordinate) < self.jump_distance * (1 - JUMP_BUFFER):
                res[i] = state
        return res

    def _filter_initial_asteroid(self, asteroid_states):
        pop_list = []
        res = asteroid_states.copy()
        for i, state in asteroid_states.items():
            if state[1][0] < self.jump_distance * JUMP_BUFFER:
                pop_list.append(i)
                continue
            if state[3][0] < 0:
                pop_list.append(i)
                continue
        for i in pop_list:
            res.pop(i)
        return res

    def _select_asteroid(self, asteroid_states):
        if not self.ridden_asteroid_id: # if starting position
            scorer = AsteroidScorer(Asteroid([self.coordinate[0], self.coordinate[1], 0, 0]), self.x_bounds[1])
        else:
            scorer = AsteroidScorer(Asteroid(self.asteroid_states[self.ridden_asteroid_id].transpose()[0]), self.x_bounds[1])
        selector = AsteroidSelector(asteroid_states, scorer)
        return selector.select()

    def _no_jump(self):
        # If at end zone and y velocity positive, don't jump
        if not self.ridden_asteroid_id:
            return False
        y_pos = self.asteroid_states[self.ridden_asteroid_id][1][0]
        y_vel = self.asteroid_states[self.ridden_asteroid_id][3][0]
        x_pos = self.asteroid_states[self.ridden_asteroid_id][0][0]
        if (y_pos > self.y_bounds[1] * (1-JUMP_BUFFER)) and (y_vel > 0) and (x_pos > self.x_bounds[1] * X_BUFFER) and (x_pos < self.x_bounds[1] * (1-X_BUFFER)):
            return True
        else:
            return False

    def jump(self, asteroid_observations, agent_data):
        """ Return the id of the asteroid the spaceship should jump/hop onto in the next timestep
        ----------
        self = a reference to the current object, the Spaceship
        asteroid_observations: Same as predict_from_observations method
        agent_data: a dictionary containing agent related data:
        'jump_distance' - a float representing agent jumping distance,
        'ridden_asteroid' - an int representing the ID of the ridden asteroid if available, None otherwise.
        Note: 'agent_pos_start' - A tuple representing the (x, y) position of the agent at t=0 is available in the constructor.

        agent_data format:
        {'ridden_asteroid': None,
         'jump_distance': agent.jump_distance,
         }
        Returns
        -------
        You are to return two items.
        1: idx, this represents the ID of the asteroid on which to jump if a jump should be performed in the next timestep.
        Return None if you do not intend to jump on an asteroid in the next timestep
        2. Return the estimated positions of the asteroids (i.e. the output of 'predict_from_observations method)
        IFF you intend to have them plotted in the visualization. Otherwise return None
        -----
        an example return
        idx to hop onto in the next timestep: 3,
        estimated_results = {1: (x-coordinate, y-coordinate),
          2: (x-coordinate, y-coordinate)}

        return 3, estimated_return

        """
        # FOR STUDENT
        # Predict
        asteroid_pos_predictions = self.predict_from_observations(asteroid_observations)

        # Update self info
        if agent_data['ridden_asteroid'] is not None:
            self.ridden_asteroid_id = agent_data['ridden_asteroid']
            self.coordinate = asteroid_pos_predictions[self.ridden_asteroid_id]
        if self.jump_distance is None:
            self.jump_distance = agent_data['jump_distance']

        # Update asteroid life
        for i, coordinate in asteroid_observations.items():
            if i in self.asteroid_life:
                self.asteroid_life[i] += 1
            else:
                self.asteroid_life[i] = 1

        pop_list = []
        for i, count in self.asteroid_life.items():
            if i not in asteroid_observations:
                pop_list.append(i)
        for i in pop_list:
            self.asteroid_life.pop(i)

        # If at end zone: don't choose
        if self._no_jump():
            return None, asteroid_observations

        # Find available asteroids to jump to
        available_asteroid_states = self._find_jumpable_asteroids()
        if not available_asteroid_states:
            return None, asteroid_pos_predictions

        # Extra filter for initial jump
        if agent_data['ridden_asteroid'] is None:
            available_asteroid_states = self._filter_initial_asteroid(available_asteroid_states)
            if not available_asteroid_states:
                return None, asteroid_pos_predictions
        else:
            available_asteroid_states.update({self.ridden_asteroid_id: self.asteroid_states[self.ridden_asteroid_id]})

        target = self._select_asteroid(available_asteroid_states)
        if target == self.ridden_asteroid_id:
            target = None

        return target, asteroid_pos_predictions


def who_am_i():
    # Please specify your GT login ID in the whoami variable (ex: jsmith326).
    whoami = 'test'
    return whoami

if __name__ == '__main__':

    # Test my utility functions

    # Test rank_dict
    dict_1 = {'a': 3, 'b': 5, 'e': 27, 'z': 9, 'xx': 7}
    print(rank_dict_vals(dict_1))