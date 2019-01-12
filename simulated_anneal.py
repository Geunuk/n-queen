import random
import math
import matplotlib.pyplot as plt
from nqueen import State, make_puzzle

def random_successor(s):
    i = random.randint(0,N-1)
    cur_val = s.coord[i]

    successor_coord = s.coord[:]
    candidate = list(range(N))
    candidate.pop(cur_val)
    successor_coord[i] = random.choice(candidate)
    successor = State(s.N, successor_coord)

    return successor

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

def simulated_annealing(s, max_time, print_mode=True):
    time = 0
    delta_cnt = 0
    avg_delta = 0

    e_trace = []
    time_trace = []
    attack_trace = []

    while True:
        time += 1
        attack_trace.append(s.attack_cnt)

        if time == max_time:
            print("time:", time, "attack:", s.attack_cnt)
            if print_mode:
                print_plot(e_trace, time_trace, attack_trace, max_time)
            return x

        successor = random_successor(s)
        delta = successor.value - s.value

        if delta >= 0:
            s = successor
        else:
            delta_cnt += 1
            avg_delta = (avg_delta*(delta_cnt-1)+ delta)/delta_cnt
            #print(avg_delta)
            p = probability(delta, avg_delta, time, max_time)
            e = math.floor(p*100)

            time_trace.append(time)
            e_trace.append(e)

            r = random.randint(0,100)
            if r <= e:
                x = successor
            else:
                pass

def tester(times, max_time):
    cnt = 0
    success = 0
    for i in range(times):
        cnt += 1
        s = make_puzzle()
        result = simulated_anneal(s, max_time, False)
        #print(result.attack_cnt)
        if result.attack_cnt == 0:
            success += 1
    success_rate = success*100/cnt
    print("[{}] times:\nMax time = {}\tSuccess rate = {}".format(
          times,max_time,success_rate))

if __name__ == "__main__":
    N = int(input("How big is your puzzle? : "))
    s = make_puzzle(N)
    ressult = simulated_annealing(s, 200)
