colors=[['R', 'G', 'G', 'R', 'R'],
        ['R', 'R', 'G', 'R', 'R'],
        ['R', 'R', 'G', 'G', 'R'],
        ['R', 'R', 'R', 'R', 'R']]

measurements=['G', 'G', 'G', 'G', 'G']

motions=[[0, 0],[0, 1],[1, 0],[1, 0],[0, 1]]
sensor_right=0.7
p_move=0.8
expected_output =  [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
                    [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
                    [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
                    [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]

sensor_wrong = 1 - sensor_right
p_stuck = 1 - p_move

def sense(q, Z):
    # Calculate posterior for each grid cell
    for i in range(len(q)):
        for j in range(len(q[i])):
            if Z == colors[i][j]:
                # color match
                q[i][j] *= sensor_right
            else:
                q[i][j] *= sensor_wrong
    # Normalize
    norm = 1 / sum([sum(q[i]) for i in range(len(q))])
    for i in range(len(q)):
        for j in range(len(q[i])):
            q[i][j] *= norm
    return q


def move(q, M):
    # Calculate posterior for each grid cell
    q_new = []
    for i in range(len(q)):
        q_new.append([])
        for j in range(len(q[i])):
            # if it moved successfully + if it failed to move
            q_new[i].append(q[(i - M[0]) % len(q)][(j - M[1]) % len(q[i])] * p_move + q[i][j] * p_stuck)
    return q_new

if __name__ == '__main__':
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for _col in range(len(colors[0]))] for _row in range(len(colors))]
    p = move(p, [0, 0])
    p = sense(p, 'G')
    p = move(p, [0, 1])
    p = sense(p, 'G')
    print(p)