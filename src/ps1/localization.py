p = [0.2, 0.2, 0.2, 0.2, 0.2]
world = ['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'red']
motions = [1, 1]
pHit = 0.6
pMiss = 0.2
pExact = 0.8
pOver = 0.1
pUnder = 0.1
def sense(p, Z):
    update = [pHit if Z == world[i] else pMiss for i in range(len(world))]
    q = [a*b for a, b in zip(update, p)]
    q_sum = sum(q)
    return [x / q_sum for x in q]

# def multi_sense(p, Me, Mo):
#
#     q = sense(p, Me[0])
#
#     if len(Me) > 1:
#         for m in Me[1:]:
#             q = move_inexact_2(q, 1)
#             q = sense(q, m)
#
#     return q

def move(p, U):
    return [p[(i-U) % len(p)] for i in range(len(p))]

def move_inexact(p, U):
    q = []
    for i in range(len(p)):
        s = p[(i - U) % len(p)] * pExact + p[(i - U + 1) % len(p)] * pUnder + p[(i - U - 1) % len(p)] * pOver
        q.append(s)
    return q

def move_inexact_2(p, U):
    under = [pUnder * m for m in move(p, U-1)]
    over = [pOver * m for m in move(p, U+1)]
    exact = [pExact * m for m in move(p, U)]
    return [u + o + e for u, o, e in zip(under, over, exact)]


if __name__ == '__main__':
    for i in range(2):
        p = sense(p, measurements[i])
        p = move_inexact_2(p, motions[i])
    print(p)