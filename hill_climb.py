import math
from nqueen import State, make_puzzle

def find_local_min(s):
    step = 0
    N = s.N
    base_val = s.value
    base_coord = s.coord[:]

    while True:
        min_val = base_val
        min_coord = base_coord[:]
        for i in range(s.N):
            for j in range(s.N):
                tmp_coord = base_coord[:]
                tmp_coord[i] = j
                tmp_val = State.count_attack_total(tmp_coord, N)
                if min_val > tmp_val:
                    min_val = tmp_val
                    min_coord = tmp_coord[:]
                    step += 1
                      
        if base_val != min_val:
            base_val = min_val
            base_coord = min_coord[:]
        else:
            return State(N, min_coord, step)

def hill_climb(N, result_dict):
    total_step = 0

    s = make_puzzle(N)
    ran_cnt = 1
    if s.value == 0:
        s.summary = {"Total step": s.step, "Random initialize": ran_cnt}
        return s

    for i in range(math.factorial(N)):
        local_min = find_local_min(s)
        total_step += local_min.step
        if local_min.value == 0:
            local_min.summary = {"Total step": total_step, "Random initialize": ran_cnt}
            result_dict["hill"] = local_min
            return local_min

        s = make_puzzle(s.N)
        ran_cnt += 1
    else:
        result_dict["hill"] = None
        return None

if __name__ == "__main__":
    import sys
    N = int(sys.argv[1])
    s = hill_climb(N, {})
    s.print_board()
    s.print_summary()
