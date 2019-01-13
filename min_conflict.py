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

def min_conflict(N, return_dict):
    ran_init_cnt = 0
    total_step = 0

    result = None
    while result == None:
        ran_init_cnt += 1
        queens, k, initial_step = initial_search(N)   # Number of Leftover queens
        result, final_step = final_search(queens, N, k)
    
        total_step += initial_step + final_step

    s = nqueen.State(N, result)
    s.summary = {"Random initialize": ran_init_cnt, "Total step": total_step}
    return_dict["min"] = s
    return s

def initial_search(N):
    queens = list(range(0, N))
    j = 0
    step = 0

    for t in range(0, int(3.08*N)):
        step += 1
        m = random.randint(j+1, N-1)    # Random integer i from t+1 <= i <= N-1
        swap(queens, j, m)
        if partial_collisions(queens, j) == 0:
            j += 1
        else:
            swap(queens, j, m)

        if j == N-1:
            break
    
    return queens, N-j+1, step

def final_search(queens, N, k):
    if N < 200:
        step = 0
        for t1 in range(N-k+1, N):
            if total_collisions(queens, t1) > 0:
                for t2 in range(N):
                    if t2 == t1:
                        continue

                    step += 1
                    swap(queens, t1, t2)
                    if total_collisions(queens, t1) > 0 or total_collisions(queens, t2) > 0:
                        swap(queens, t1, t2)
                    else:
                        break
    else:
        step = 0
        for t1 in range(N-k+1, N):
            if step >= 7000:
                break
            if total_collisions(queens, t1) > 0:
                flag = True
                while flag and step <= 7000:
                    t2 = random.randint(0, N-1)
                    while t1 == t2:
                        t2 = random.randint(0, N-1)
                           
                    step += 1

                    swap(queens, t1, t2)
                    if total_collisions(queens, t1) > 0 or total_collisions(queens, t2) > 0:
                        swap(queens, t1, t2)
                        flag = True
                    else:
                        flag = False
  
    if all([total_collisions(queens, i) == 0 for i in range(N)]):
        return queens, step
    else:
        return None, step

if __name__ == "__main__":
    import sys
    N = int(sys.argv[1])
    s = min_conflict(N, {})
    s.print_board()
    s.print_summary()
