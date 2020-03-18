import numpy as np

from print_util import print_board, print_summary
from puzzle_util import count_attack_total

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
    summary = {"Puzzle size": puzzle_size, "Population": pop_size, "Mutation prob": mutation_prob, "Max gen": max_gen}
    
    #print("Gen", gen_cnt)
    for i in range(pop_size):
        individual = np.random.permutation(puzzle_size) 
        fitness = count_attack_total(individual)
        if fitness == 0:
            summary["Gen"] = gen_cnt
            print_board(individual)
            print_summary(summary)
            return
        else:
            population.append(individual)
            fitnesses.append(fitness)
    
    while gen_cnt <= max_gen:
        gen_cnt += 1
        #print("Gen", gen_cnt)
        
        # mutate
        for mutated_idx in np.random.randint(pop_size, size=int(mutation_prob*pop_size)):
            mutated_individual = mutate(population[mutated_idx])
            if mutated_individual != []:
                fitness = count_attack_total(mutated_individual)
                if fitness == 0:
                    summary["Gen"] = gen_cnt
                    print_board(mutated_individual)
                    print_summary(summary)
                    return
                else:
                    population.append(mutated_individual)
                    fitnesses.append(fitness)
    
        new_idx = np.argsort(fitnesses)[:pop_size]
        
        population = [population[i] for i in new_idx]
        fitnesses = [fitnesses[i] for i in new_idx]
    
    summary["Result"] = "Over max gens"
    print_summary(summary)
        
if __name__ == "__main__":
    EA(15, 1000, 0.8, 10)
