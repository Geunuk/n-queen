import math

from puzzle_util import make_puzzle, count_attack_total

def find_local_min(coord):
    step = 0
    N = len(coord)
    base_val = count_attack_total(coord)
    base_coord = coord[:]

    while True:
        min_val = base_val
        min_coord = base_coord[:]
        for i in range(N):
            for j in range(N):
                tmp_coord = base_coord[:]
                tmp_coord[i] = j
                tmp_val = count_attack_total(tmp_coord)
                if min_val > tmp_val:
                    min_val = tmp_val
                    min_coord = tmp_coord[:]
                    step += 1
                      
        if base_val != min_val:
            base_val = min_val
            base_coord = min_coord[:]
        else:
            return min_coord, min_val, step

def hill_climb(N, return_dict):
    total_step = 0

    coord = make_puzzle(N)
    ran_cnt = 1
    if count_attack_total(coord) == 0:
        summary = {"Total step": 0, "Random initialize": ran_cnt}
        return_dict["hill"] = (coord, summary)
        return coord, summary

    for i in range(math.factorial(N)):
        local_min_coord, local_min_val, step = find_local_min(coord)
        total_step += step
        if local_min_val == 0:
            summary = {"Total step": total_step, "Random initialize": ran_cnt}
            return_dict["hill"] = (local_min_coord, summary)
            return local_min_coord, summary

        coord = make_puzzle(N)
        ran_cnt += 1
    else:
        summary = {"Result": "Fail", "Total step": total_step, "Random initialize": ran_cnt}
        return_dict["hill"] = (None, summary)
        return None, summary

if __name__ == "__main__":
    import sys
    from print_util import print_board, print_summary
    
    N = int(sys.argv[1])
    coord, summary = hill_climb(N, {})
    print_board(coord)
    print_summary(summary)
