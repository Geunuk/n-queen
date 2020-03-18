import random
import math

import matplotlib.pyplot as plt

from puzzle_util import make_puzzle, count_attack_total

def random_successor(coord):
    N = len(coord)
    i = random.randint(0, N-1)
    cur_val = coord[i]

    successor_coord = coord[:]
    candidate = list(range(N))
    candidate.pop(cur_val)
    successor_coord[i] = random.choice(candidate)
    
    return successor_coord

def probability(delta, avg_delta, time, max_time):
    #avg_delta = -1
    #a = (avg_delta*max_time)/math.log(0.00001)
    #return math.e**(delta*time/a)
    a = (max_time)/math.log(0.001)
    return math.e**(time/a)

def print_plot(e_trace, time_trace, attack_trace, max_time):
        plt.subplot(211)
        plt.plot(time_trace, e_trace,'r--')
        plt.axis([1,max_time,0,100])
        plt.title('Probability')
        plt.xlabel('Time')
        plt.ylabel('Probability')

        plt.subplot(212)
        plt.plot(list(range(1, max_time+1)), attack_trace,'b--')
        plt.axis([1,max_time,0,N*(N-1)//2])
        plt.title('Kill Count')
        plt.xlabel('Time')
        plt.ylabel('Kill Count')

        plt.show()

def simulated_annealing(max_time_step, print_mode, return_dict):
    coord = make_puzzle(N)
    time_steps = 0
    delta_cnt = 0
    avg_delta = 0

    e_trace = []
    time_trace = []
    attack_trace = []

    while True:
        time_steps += 1
        value = count_attack_total(coord)
        attack_trace.append(value)

        if time == max_time:
            print("time:", time, "attack:", value)
            if print_mode:
                print_plot(e_trace, time_trace, attack_trace, max_time)
            return s

        successor_coord = random_successor(coord)
        successor_value = count_attack_total(successor_coord)
        delta = successor_value - value

        if delta >= 0:
            coord = successor_coord
        else:
            delta_cnt += 1
            avg_delta = (avg_delta*(delta_cnt-1)+ delta)/delta_cnt
            #print(avg_delta)
            p = probability(delta, avg_delta, time_steps, max_time_step)
            e = math.floor(p*100)

            time_trace.append(time_steps)
            e_trace.append(e)

            r = random.randint(0,100)
            if r <= e:
                s = successor_coord
            else:
                pass

def tester(times, max_time_step):
    cnt = 0
    success = 0
    for i in range(times):
        cnt += 1
        s = make_puzzle()
        result = simulated_anneal(s, max_time_step, False)
        #print(result.attack_cnt)
        if result.attack_cnt == 0:
            success += 1
    success_rate = success*100/cnt
    print("[{}] times:\nMax time = {}\tSuccess rate = {}".format(
          times,max_time,success_rate))

if __name__ == "__main__":
    import sys
    N = int(sys.argv[1])

    result = simulated_annealing(2000, True, {})
