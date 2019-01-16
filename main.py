import argparse
import sys
import time
import multiprocessing

from hill_climb import hill_climb 
from backtracking import backtracking
from min_conflict import min_conflict

fun_dic = {"min":min_conflict, "back":backtracking, "hill":hill_climb}

def handle_args():
    state, fun = None, None

    parser = argparse.ArgumentParser()
    parser.add_argument('alg' ,metavar='alg',type=str, help="Coose algorithm between 'min', 'back','hill' and 'simul'")
    parser.add_argument('N', metavar='N', type=int, help='row and column size of the chess board')
    parser.add_argument('-s', '--short', action='store_true', help="short version. turn off chess board printingt")
   
    args = parser.parse_args()

    alg_name = args.alg
    if alg_name == "simul":
        parser.error("'simul' is under development. Choose other algorithm.")
    if alg_name in fun_dic.keys():
        fun = fun_dic[alg_name]
    else:
        parser.error("Coose algorithm between 'min', 'back','hill' and 'simul'")
    return args, fun, args.N

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def print_waiting_msg(jobs):
    spinner = spinning_cursor()
    print("Calculating...... ", end='')
    while any([p.is_alive() for p in jobs]):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
    print("\n")

def main():
    args, fun, N = handle_args()

    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    p = multiprocessing.Process(target=fun, args=(N,return_dict))
    p.start()
    print_waiting_msg([p])

    result = return_dict.values()[0]

    if result == None:
        print("FAIL")
        return
    elif not args.short:
        result.print_board()
    result.print_summary()

if __name__ == "__main__":
    main()
