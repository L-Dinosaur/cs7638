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

P_init = matrix()
P_init.identity(3)

COLD_START = 10
X_BUFFER = 0.1
Y_BUFFER = 0.1
JUMP_BUFFER = 0.3

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
        self.cold_start = COLD_START
        self.x_buffer = self.x_bounds[1] * X_BUFFER
        self.y_buffer = self.y_bounds[1] * Y_BUFFER
        self.asteroid_ridden = None

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

    def find_jumpable_asteroids(self, agent_data):
        res = {}
        if agent_data['ridden_asteroid'] is None:
            starting_pos = self.agent_pos_start
        else:
            starting_pos = (self.asteroid_states[agent_data['ridden_asteroid']][0][0], self.asteroid_states[agent_data['ridden_asteroid']][1][0])
        for i, state in self.asteroid_states.items():
            if i == agent_data['ridden_asteroid']:
                continue
            coordinate = (state[0][0], state[1][0])
            if euc_distance(starting_pos, coordinate) < agent_data['jump_distance'] * (1 - JUMP_BUFFER):
                res[i] = coordinate
        return res

    def _near_y_bound(self, location):
        return location[1] < self.y_buffer

    def _near_x_bound_left(self, location):
        return location[0] < self.x_buffer

    def _near_x_bound_right(self, location):
        return (self.x_bounds[1] - location[0]) < self.x_buffer


    def _jump_back_x(self, available_asteroid_pos):
        dist_tracker = -1 * math.inf
        target = None
        for i, coordinate in available_asteroid_pos.items():
            dist = math.sqrt(coordinate[0]**2 + (coordinate[0] - self.x_bounds[1])**2)
            if math.sqrt(coordinate[0]**2 + (coordinate[0] - self.x_bounds[1])**2) > dist_tracker:
                target = i
                dist_tracker = dist
        return target

    @staticmethod
    def _jump_back_y(available_asteroid_pos):
        dist_tracker = -1 * math.inf
        target = None
        for i, coordinate in available_asteroid_pos.items():
            if coordinate[1] > dist_tracker:
                target = i
                dist_tracker = coordinate[1]
        return target

    def _find_better_asteroid(self, available_asteroid_pos):
        available_asteroids = available_asteroid_pos.keys()
        positions = {}
        velocities = {}
        accelerations = {}
        for i in available_asteroids:
            state = self.asteroid_states[i]
            positions[i] = state[1][0]
            velocities[i] = state[3][0]
            accelerations[i] = state[5][0]

        ranking_pos = rank_dict_vals(positions)
        ranking_vel = rank_dict_vals(velocities)
        ranking_acc = rank_dict_vals(accelerations)

        ranking = {k: v for k, v in zip(ranking_pos.keys(), elem_addition(elem_addition(ranking_pos.values(), ranking_vel.values()), ranking_acc.values()))}

        ranking_holder = math.inf
        target = None
        for k, v in ranking.items():
            if v < ranking_holder:
                target = k
                ranking_holder = v

        return target

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

        # Wait till KF calibrate
        if self.cold_start > 0:
            self.cold_start -= 1
            return None, None

        # Find available asteroids to jump to
        available_asteroids = self.find_jumpable_asteroids(agent_data)
        if not available_asteroids:
            return None, None

        if agent_data['ridden_asteroid'] is None:
            target = self._find_better_asteroid(available_asteroids)
            return target, asteroid_pos_predictions[target]
        else:
            current_state = self.asteroid_states[agent_data['ridden_asteroid']]
            current_pos = (current_state[0][0], current_state[1][0])
            # 1. if near bottom boundary
            if self._near_y_bound(current_pos) and self.asteroid_states[agent_data['ridden_asteroid']][3][0] < 0:
                target = self._jump_back_y(available_asteroids)
                return target, asteroid_pos_predictions[target]

            # 2. if near side boundaries
            if (self._near_x_bound_left(current_pos) and (self.asteroid_states[agent_data['ridden_asteroid']][2][0] < 0))\
                    or (self._near_x_bound_right(current_pos) and (self.asteroid_states[agent_data['ridden_asteroid']][2][0] > 0)):
                target = self._jump_back_x(available_asteroids)
                return target, asteroid_pos_predictions[target]

            # 3. if not near boundaries
            available_asteroids.update({agent_data['ridden_asteroid']: asteroid_pos_predictions[agent_data['ridden_asteroid']]})
            target = self._find_better_asteroid(available_asteroids)
            if target == agent_data['ridden_asteroid']:
                return None, None
            else:
                return target, asteroid_pos_predictions[target]


def who_am_i():
    # Please specify your GT login ID in the whoami variable (ex: jsmith326).
    whoami = 'test'
    return whoami

if __name__ == '__main__':

    # Test my utility functions

    # Test rank_dict
    dict_1 = {'a': 3, 'b': 5, 'e': 27, 'z': 9, 'xx': 7}
    print(rank_dict_vals(dict_1))