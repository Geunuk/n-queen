import numpy as np

from nqueen import State, make_puzzle

def mutate(individual):
    N = len(individual)
    i, j = np.random.randint(N,size=2)
    if i != j:
        individual[i], individual[j] = individual[j], individual[i]
        return individual
    else:
        return []

def crossover(mother, father):
    N = len(mother)
    cutting_point = np.random.randint(N)
    offspring1 = np.concatenate((mother[:cutting_point+1], father[cutting_point+1:]))
    offspring2 = np.concatenate((father[:cutting_point+1], mother[cutting_point+1:]))
    return offspring1, offspring2

def EA(puzzle_size, pop_size, mutation_prob, max_gen):
    # initialize population
    population = []
    fitnesses = []
    gen_cnt = 0

    print("Gen", gen_cnt)
    for i in range(pop_size):
        individual = np.random.permutation(puzzle_size) 
        fitness = State.count_attack_total(individual, puzzle_size)
        if fitness == 0:
            State(puzzle_size, individual).print_board()
            return
        else:
            population.append(individual)
            fitnesses.append(fitness)
    
    while gen_cnt <= max_gen:
        gen_cnt += 1
        print("Gen", gen_cnt)
        
        # mutate
        for mutated_idx in np.random.randint(pop_size, size=int(mutation_prob*pop_size)):
            mutated_individual = mutate(population[mutated_idx])
            if mutated_individual != []:
                fitness = State.count_attack_total(mutated_individual, puzzle_size)
                if fitness == 0:
                    State(puzzle_size, mutated_individual).print_board()
                    return
                else:
                    population.append(mutated_individual)
                    fitnesses.append(fitness)
    
        new_idx = np.argsort(fitnesses)[:pop_size]
        
        population = [population[i] for i in new_idx]
        fitnesses = [fitnesses[i] for i in new_idx]
        
if __name__ == "__main__":
    EA(13, 1000, 0.8, 10000)
