import random
import nqueen

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

    for var, values in enumerate(lookup):
        if var not in assigned_var:
            if len(values) == min_cnt:
                min_var_list.append(var)
            elif len(values) < min_cnt:
                min_var_list = [var]

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
    same_cnt_list = []

    for val in lookup[var]:
        if visited[var][val] == 1:
            continue
        elim_idx = find_elimination(lookup, var, val)
        cnt = len(elim_idx)

        if cnt == min_cnt:
            same_cnt_list.append((val, elim_idx))
        elif cnt < min_cnt:
            min_cnt = cnt
            same_cnt_list = [(val, elim_idx)]

    return random.choice(same_cnt_list)
    
def backtracking(N):
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

        # backtrack when no possible values or there were values but all visited
        if len(lookup[var]) == 0 or all([visited[var][val] for val in lookup[var]]):
            back = True

            canceled_var = assigned_var.pop()
            canceled_val = assigned_val.pop()
            visited[var] = [0]*N
            var = canceled_var
            elim_idx = elimination_trace.pop()
            restore_value(lookup, elim_idx)

            #print("back to var = {} val = {}".format(canceled_var, canceled_val))
            if canceled_var == start_var and all(visited[start_var]):
                print("FAIL")
                return step, None
            else:
                continue

        val, elim_idx = select_value(lookup, assigned_var, var, visited)
        visited[var][val] = 1

        assigned_var.append(var)
        assigned_val.append(val)
        elimination_trace.append(elim_idx)
        eliminate_value(lookup, elim_idx)

        #print("select var = {} val = {}".format(var, val))
    
    assert(len(assigned_var) == N)

    result = [0]*N
    for var, val in list(zip(assigned_var, assigned_val)):
        result[var] = val
    return step, result

def print_lookup(lookup):
    print("lookup:")
    for var, val in enumerate(lookup):
        print("var:", var, " val:",val)

def test(N, times):
    total_step = 0
    for i in range(times):
        step, _ = backtracking(N)
        total_step += step
    return total_step/times

if __name__ == "__main__":
    """
    N = int(input("How big is your puzzle? : "))
    step, coord = backtracking(N)
    print("step:", step)
    result = nqueen.State(N, coord)
    result.print_board()
    """
    print(test(10, 20))
