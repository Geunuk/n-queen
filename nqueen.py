import random

class State():
    def __init__(self, N, coord, step=0):
        self.N = N
        self.coord = coord
        self.value = State.count_kill_total(self.coord, self.N)
        #self.value = -self.kill_cnt
        self.step = step
        self.summary = None
    
    def print_result(self):
        for feature, value in self.summary.items():
            print(feature, " : ", value)

    def print_board(self):
        y = [[] for i in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                if self.coord[i] == j:
                    y[j].append(i)

        print(" "+"-"*(2*self.N+1)+" ")
        for i in range(self.N):
            line = list("X"*self.N)
            for j in y[i]:
                line[j] = "Q"
            line.insert(0, "|")
            line.append("|")
            print(' '.join(line))
        print(" "+"-"*(2*self.N+1)+" ")
        
    @staticmethod
    def count_kill_total(coord, N):
        result = 0
        for n in range(N-1):
            result += State.count_kill_ranged(coord, n, n+1, N-1, N)
        return result

    @staticmethod    
    def test_flag(i, u, r, d, l, go_flag):
        if go_flag[0] == 1 and i > u:
            go_flag[0] = 0
        if go_flag[1] == 1 and i > r:
            go_flag[1] = 0
        if go_flag[2] == 1 and i > d:
            go_flag[2] = 0
        if go_flag[3] == 1 and i > l:
            go_flag[3] = 0
        
    @staticmethod
    def count_kill_ranged(x, n, l, r, N):
        go_flag = [1]*4
        m = x[n]

        result = 0
        for i in range(1, max(m, r-n, N-1-m, n-l)+1):
            State.test_flag(i, m, r-n, N-1-m, n-l, go_flag)
            if go_flag[0] and go_flag[1] and x[n+i] == m-i:
                result += 1
                #print((i, n+i,m-i))
            if go_flag[1] and x[n+i] == m:
                result += 1
                #print((i, n+i,m))
            if go_flag[1] and go_flag[2] and x[n+i] == m+i:
                result += 1
                #print((i, n+i,m+i))
            if go_flag[2] and go_flag[3] and x[n-i] == m+i:
                result += 1
                #print((i, n-i,m+i))
            if go_flag[3] and x[n-i] == m:
                result += 1
                #print((i, n-i,m))
            if go_flag[3] and go_flag[0] and x[n-i] == m-i:
                result += 1
                #print((i, n-i,m-i))
        return result

    @staticmethod
    def count_kill_solo(x, n, N):
        return State.count_kill_ranged(x, n, 0, N-1, N)

def make_puzzle(N):
    coord = list(range(N))
    for i in range(N):
        coord[i] = random.randint(0,N-1)
    s = State(N, coord)

    return s

if __name__ == "__main__":
    """
    N = int(input("How big is your puzzle? : "))
    s = make_puzzle(N)
    s =State(N,[3,0,2,3])
    s.print_board()
    print(s.kill_cnt)
    #print(State.count_kill_solo(s.coord, 0, N))
    #print(State.count_kill_solo(s.coord, 1, N))
    #print(State.count_kill_solo(s.coord, 2, N))
    print(State.count_kill_solo(s.coord, 3, N))
    """
    print_board([2,1,3,0])
