import random

def make_puzzle(N):
    coord = list(range(N))
    for i in range(N):
        coord[i] = random.randint(0,N-1)
    return coord
    s = State(N, coord)
    return s

def count_attack_total(coord):
    N = len(coord)
    result = 0
    for n in range(N-1):
        result += count_attack_ranged(coord, n, n+1, N-1, N)
    return result

def test_flag(i, u, r, d, l, go_flag):
    if go_flag[0] == 1 and i > u:
        go_flag[0] = 0
    if go_flag[1] == 1 and i > r:
        go_flag[1] = 0
    if go_flag[2] == 1 and i > d:
        go_flag[2] = 0
    if go_flag[3] == 1 and i > l:
        go_flag[3] = 0
    
def count_attack_ranged(x, n, l, r, N):
    go_flag = [1]*4
    m = x[n]

    result = 0
    for i in range(1, max(m, r-n, N-1-m, n-l)+1):
        test_flag(i, m, r-n, N-1-m, n-l, go_flag)
        if go_flag[0] and go_flag[1] and x[n+i] == m-i:
            result += 1
        if go_flag[1] and x[n+i] == m:
            result += 1
        if go_flag[1] and go_flag[2] and x[n+i] == m+i:
            result += 1
        if go_flag[2] and go_flag[3] and x[n-i] == m+i:
            result += 1
        if go_flag[3] and x[n-i] == m:
            result += 1
        if go_flag[3] and go_flag[0] and x[n-i] == m-i:
            result += 1
    return result
