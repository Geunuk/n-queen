def print_summary(summary_dict):
    for attr, value in summary_dict.items():
        print(attr, " : ", value)

def print_board(coord):
    if coord == None:
        print("Caannot print 'None' coordiante")
        return

    N = len(coord)
    y = [[] for i in range(N)]
    for i in range(N):
        for j in range(N):
            if coord[i] == j:
                y[j].append(i)

    print(" "+"-"*(2*N+1)+" ")
    for i in range(N):
        line = list("X"*N)
        for j in y[i]:
            line[j] = "Q"
        line.insert(0, "|")
        line.append("|")
        print(' '.join(line))
    print(" "+"-"*(2*N+1)+" ")
