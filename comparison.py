from hill_climb import hill_climb
from min_conflict import min_conflict
from backtracking import backtracking

def comparison(N, fun, times):
    total_step = 0
    for i in range(times):
        result = fun(N)
        total_step += result[0]
    return total_step/times

if __name__ == "__main__":
    with open('comparison.dat', 'wb') as f:
        ...

    N_list = [10]
    times = 20
    fun_list = [hill_climb, backtracking, min_conflict]
    for N in N_list:
        print("N:", N)
        for fun in fun_list:
            avg_step = comparison(N, fun, times)
            print("{}: {} steps".format(fun.__name__, avg_step))
