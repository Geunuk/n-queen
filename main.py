import argparse
import sys

from hill_climb import hill_climb 
from backtracking import backtracking
from min_conflict import min_conflict

fun_dic = {"min":min_conflict, "back":backtracking, "hill":hill_climb}

def handle_args():
    state, fun = None, None

    parser = argparse.ArgumentParser()
    parser.add_argument('alg' ,metavar='alg',type=str, help="choose algorithm between 'min', 'back','hill' and 'simul'")
    parser.add_argument('N', metavar='N', type=int, help='row and column size of the chess board')
    parser.add_argument('-p', '--print', action='store_true', help="print chess board of result")
   

    args = parser.parse_args()

    alg_name = args.alg
    if alg_name == "simul":
        parser.error("'simul' is under development. Choose other algorithm.")
    if alg_name in fun_dic.keys():
        fun = fun_dic[alg_name]
    return args, fun, args.N
"""
def run(init_state, fun):
    print("Init :")
    State.print_state(init_state.index)
    print()

    time, route = fun(init_state)
    print("Changed :")
    State.print_state(init_state.answer)
    print()

    print("Time    :", time)
    print("Length  :", len(route))
    print("Route   :")
    print()

    print("   |  0  1  2  3  4  5  6  7  8  9 ")
    print("-----------------------------------")
    for i, r in enumerate(route):
        if i%10 == 0:
            print('{:2} | '.format(i), end=' ')
        print(r, end='  ')

        if i%10 == 9:
            print()
    print()

def compare(init_state):
    print("Init       :")
    State.print_state(init_state.index)
    print()

    time_list = []
    length_list = []

    for fun in fun_dic.values():
        time, route = fun(init_state)
        time_list.append(str(time))
        length_list.append(str(len(route)))

    fun_list = ["{:^5}".format(x) for x in fun_dic.keys()]
    time_list = ["{:^5}".format(x) for x in time_list]
    length_list = ["{:^5}".format(x) for x in length_list]

    print("Comparison :")
    print()
    print("       | " + '  '.join(fun_list))
    print("-"*35)
    print("Time   | " + '  '.join(time_list))
    print("Length | " + '  '.join(length_list))
"""

def main():
    args, fun, N = handle_args()

    result = fun(N)
    if result != None:
        result.print_board()
        result.print_summary()
    else:
        print("FAIL")

if __name__ == "__main__":
    main()
