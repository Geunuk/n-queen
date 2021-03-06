import random

def eliminate_value(lookup, pos):
    for var, val in pos:
        lookup[var].remove(val)
           
def restore_value(lookup, pos):
    for var, val in pos:
        lookup[var].add(val)

def find_elimination(lookup, var, val):
    def test_flag(i, u, r, d, l, go_flag):
        if go_flag[0] == 1 and i > u:
            go_flag[0] = 0
        if go_flag[1] == 1 and i > r:
            go_flag[1] = 0
        if go_flag[2] == 1 and i > d:
            go_flag[2] = 0
        if go_flag[3] == 1 and i > l:
            go_flag[3] = 0
 
    N = len(lookup)
    go_flag = [1]*4
    result = set([(var,val)])

    for i in range(1, max(val, N-1-var, N-1-val, var)+1):
        test_flag(i, val, N-1-var, N-1-val, var, go_flag)

        if go_flag[0] and go_flag[1] and (val-i in lookup[var+i]):
            result.add((var+i,val-i))
        if go_flag[1] and (val in lookup[var+i]):
            result.add((var+i,val))
        if go_flag[1] and go_flag[2] and (val+i in lookup[var+i]):
            result.add((var+i,val+i))
        if go_flag[2] and go_flag[3] and (val+i in lookup[var-i]):
            result.add((var-i,val+i))
        if go_flag[3] and (val in lookup[var-i]):
            result.add((var-i,val))
        if go_flag[3] and go_flag[0] and (val-i in lookup[var-i]):
            result.add((var-i,val-i))

    return result

def select_variable(lookup, assigned_var):
    N = len(lookup)
    min_var_list = []
    min_cnt = N

    # Find variables that have min number of values
    for var, values in enumerate(lookup):
        if var not in assigned_var:
            if min_cnt == len(values):
                min_var_list.append(var)
            elif min_cnt > len(values):
                min_cnt = len(values)
                min_var_list = [var]
                
    # Choose variable from min_var_list
    mid = (N-1)/2
    for i in range(len(min_var_list)-1):
        d1 = min_var_list[i]-mid
        d2 = min_var_list[i+1]-mid

        if d1*d2 <= 0:
            if abs(d1) <= abs(d2):
                return min_var_list[i]
            else:
                return min_var_list[i+1]

    if min_var_list[-1] < mid:
        return min_var_list[-1]
    elif mid < min_var_list[0]:
        return min_var_list[0]
    else:
        print("ERROR: fun select_variable")
        sys.exit(-1)

def select_value(lookup, assigned_var, var, visited):
    min_cnt = (len(lookup))**2
    min_cnt_list = []

    for val in lookup[var]:
        if visited[var][val] == 1:
            continue
        elim_idx = find_elimination(lookup, var, val)
        cnt = len(elim_idx)

        if min_cnt == cnt:
            min_cnt_list.append((val, elim_idx))
        elif min_cnt > cnt:
            min_cnt = cnt
            min_cnt_list = [(val, elim_idx)]

    return random.choice(min_cnt_list)
    
def backtracking(N, return_dict):
    lookup = [set(range(N)) for _ in range(N)]
    visited = [[0]*N for _ in range(N)]
    assigned_var = []
    assigned_val = []
    elimination_trace = []

    start_var = 0
    step = 0
    back = False

    while len(assigned_var) != N:
        if not back:
            var = select_variable(lookup, assigned_var)
        else:
            back = False

        step += 1
        if step == 1:
            start_var = var

        # backtrack when no possible values or values exist but all visited
        if len(lookup[var]) == 0 or all([visited[var][val] for val in lookup[var]]):
            back = True

            canceled_var = assigned_var.pop()
            canceled_val = assigned_val.pop()
            visited[var] = [0]*N
            var = canceled_var
            elim_idx = elimination_trace.pop()
            restore_value(lookup, elim_idx)

            if canceled_var == start_var and all(visited[start_var]):
                return None
            else:
                continue

        val, elim_idx = select_value(lookup, assigned_var, var, visited)
        visited[var][val] = 1

        assigned_var.append(var)
        assigned_val.append(val)
        elimination_trace.append(elim_idx)
        eliminate_value(lookup, elim_idx)
    
    assert(len(assigned_var) == N)

    result = [0]*N
    for var, val in list(zip(assigned_var, assigned_val)):
        result[var] = val

    summary = {"Step" : step}
    return_dict["back"] = (result, summary)
    
    return result, summary
    
def print_lookup(lookup):
    print("lookup:")
    for var, val in enumerate(lookup):
        print("var:", var, " val:",val)

def test(N, times):
    total_step = 0
    for i in range(times):
        _, summary = backtracking(N, {})
        total_step += summary['Step']
    return total_step/times

if __name__ == "__main__":
    import sys
    from print_util import print_board, print_summary

    N = int(sys.argv[1])
    coord, summary = backtracking(N, {})
    print_board(coord)
    print_summary(summary)
