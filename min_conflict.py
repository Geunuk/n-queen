import random
from nqueen import State, make_puzzle
MAX_TRY = 100000

def choose_variable(s):
    variables = []

    if choose_variable.loop_cnt != 0:
        for var in range(s.N):
            if State.count_kill_solo(s.coord, var, s.N) == 0:
                variables.append(var)
                if len(variables) == 0:
                    choose_variable.loop_cnt = 10000


    else:
        for var in range(s.N):
            if State.count_kill_solo(s.coord, var, s.N) != 0:
                variables.append(var)

    if choose_variable.variables == variables:
        choose_variable.loop_cnt += 1
    else:
        choose_variable.loop_cnt = 0

    if len(variables) == 0:
        variables = list(range(s.N))
    choose_variable.variables = variables
    return random.choice(variables)

def choose_value(s, var):
    min_val_list = []
    min_coord = s.coord[:]
    min_kill_cnt = State.count_kill_solo(min_coord, var, s.N)

    values = list(range(s.N))
    values.pop(values.index(s.coord[var]))

    for val in values:
        tmp_coord = s.coord[:]
        tmp_coord[var] = val
        tmp_kill_cnt = State.count_kill_solo(tmp_coord, var, s.N)

        if tmp_kill_cnt == min_kill_cnt:
            min_val_list.append(val)
        elif tmp_kill_cnt < min_kill_cnt:
            min_kill_cnt = tmp_kill_cnt
            min_val_list = [val]

    if len(min_val_list) == 0:
        return s.coord[var]
    else:
        return random.choice(min_val_list)

def min_conflict(N):
    s = make_puzzle(N)

    choose_variable.loop_cnt = 0
    choose_variable.variables = []

    for i in range(MAX_TRY):
        print("kill_cnt:", s.kill_cnt)
        if choose_variable.loop_cnt >= 3:
            print("!loop")
            new_s = make_puzzle(N)
            new_s.step = s.step
            s = new_s
            choose_variable.loop_cnt = 0

        if s.kill_cnt == 0:
            #print("step:", s.step)
            #s.print_board()
            return s.step, s
  

        var = choose_variable(s)
        val = choose_value(s, var)

        print("var:", var, " val:", val)
        #print()
        new_coord = s.coord[:]
        new_coord[var] = val

        s = State(N, new_coord, s.step+1)

    else:
        print("Failed")
        s.print_board()
        return s.step, None

if __name__ == "__main__":
    N = int(input("How big is your puzzle? : "))
    step, s = min_conflict(N)
    print("step:", step)
    s.print_board()
