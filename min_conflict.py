import random

import nqueen

def swap(queens, m, n):
    tmp = queens[m]
    queens[m] = queens[n]
    queens[n] = tmp

def partial_collisions(queens, i):
    N = len(queens)
    neg_collisions = [0]*(N+i-1)
    pos_collisions = [0]*(N+i-1)

    for t in range(i):
        queen_t = queens[t]
        neg_collisions[t+queen_t] += 1  # 0 < = neg collision index <= 2(N-1)
        # Add N-1 for bias correction
        pos_collisions[t-queen_t+N-1] += 1 # -(N-1) <= pos collision index <= N-1

    result = 0
    for x in neg_collisions + pos_collisions:
        if x != 0:
            result += x-1
    return result

def total_collisions(queens, i):
    N = len(queens)
    neg_invariant = i + queens[i]
    pos_invariant = i - queens[i]

    # Count negative collision
    if neg_invariant <= N-1:
        start_idx = 0
        end_idx = neg_invariant
    else:
        start_idx = neg_invariant-(N-1)
        end_idx = N-1

    neg_collisions = 0
    for i in range(start_idx, end_idx+1):
        if i + queens[i] == neg_invariant:
            neg_collisions += 1
    if neg_collisions != 0:
        neg_collisions -= 1

    # Count positive collision
    if pos_invariant <= 0:
        start_idx = 0
        end_idx = pos_invariant + N-1
    else:
        start_idx = pos_invariant
        end_idx = N-1

    pos_collisions = 0
    for i in range(start_idx, end_idx+1):
        if i - queens[i] == pos_invariant:
            pos_collisions += 1
    if pos_collisions != 0:
        pos_collisions -= 1

    return neg_collisions + pos_collisions

def min_conflict(N):
    result = None
    i = 0
    while result == None:
        i += 1
        print("iter :", i)
        queens, k = initial_search(N)   # Number of Leftover queens
        print("k :", k) 
        result = final_search(queens, N, k)
        print(result)

    s = nqueen.State(N, result)
    s.summary = {"Random initialize": i}
    return s

def initial_search(N):
    print("initial search")
    queens = list(range(0, N))
    j = 0
    print(queens)
    for t in range(0, int(3.08*N)):
        m = random.randint(j+1, N-1)    # Random integer i from t+1 <= i <= N-1
        print("t", t,"m",m)
        swap(queens, j, m)
        if partial_collisions(queens, j) == 0:
            print("queens :", queens, " t :", t, " m : ", m, " j : ", j)
            j += 1
        else:
            swap(queens, j, m)

        if j == N-1:
            break
    
    return queens, N-j+1

def final_search(queens, N, k):
    print("final search")
    for t1 in range(N-k+1, N):
        print("t1 : ", t1)
        if total_collisions(queens, t1) > 0:
            flag = True
            while flag:
                t2 = random.randint(0, N-1)
                while t1 == t2:
                    t2 = random.randint(0, N-1)

                swap(queens, t1, t2)
                if total_collisions(queens, t1) > 0 or total_collisions(queens, t2) > 0:
                    swap(queens, t1, t2)
                    flag = False
                else:
                    flag = True
    if all([total_collisions(queens, i) == 0 for i in range(N)]):
        return queens
    else:
        return None
if __name__ == "__main__":
    min_conflict(30)
