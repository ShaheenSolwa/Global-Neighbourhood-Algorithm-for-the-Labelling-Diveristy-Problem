import random, operator

"""
1. set modulation order M, number of swaps k and Hypershpere Radius R
"""
M = 64
K = 6
R = 1

"""
2. population size, number of iterations t
"""
m = 50
t = 10000

#AddedPop = []

def initial_population(mapper1, popSize):
    pop = []
    for i in range(popSize):
        m1 = mapper1.copy()
        random.shuffle(m1)
        pop.append(m1)
    return list(tuple(pop))

def mappoints(map, mapper):
    mapped = {}
    for i in range(len(mapper)):
        for j in map.keys():
            if j == mapper[i]:
                #print(mapper[i], map.get(i))
                mapped[j] = map.get(i)
    return mapped

def fitness(list1, list2, map):
    list3 = []
    list1, list2 = mappoints(map, list1), mappoints(map, list2)
    #list1 = mappoints(map, list1)
    for i in range(len(list1)):
        for j in range(len(list2)):
            if i != j:
                fit = abs(list1[i]-list1[j]) * abs(list2[i]-list2[j])
                list3.append(fit)
    #print("length of fit calcs: " + str(len(list3)))
    return round(min(list3),4)

def rank_fitness(gray, population, map):
    rFit = {}
    for i in range(len(population)):
        rFit[i] = fitness(gray, population[i], map)
    return sorted(rFit.items(), key=operator.itemgetter(1), reverse=True)

def neighbours(parent, point, map):
    neighbours = []
    points = mappoints(map, parent)
    x = points[point]
    for i in range(len(points)):
        y = points[i]
        dist = abs(x - y)
        if dist <= R-0.5:
            neighbours.append(i)
    return neighbours

def crossover(parent1, parent2, map):
    p1 = list(parent1)
    p2 = list(parent2)
    for i in range(K):
        ind = random.randint(0, M-1)
        n1 = neighbours(p1, ind, map)
        n2 = neighbours(p2, ind, map)

        ind2 = random.randint(0, M-1)
        while ind2 in n1 or ind2 in n2:
            ind2 = random.randint(0, M-1)

        p1[ind], p1[ind2] = p1[ind2], p1[ind]
        p2[ind], p2[ind2] = p2[ind2], p2[ind]
    return p1, p2

def crossoverPopulation(population, map):
    crossed = []
    for i in range(len(population)):
        for j in range(len(population)):
            crossed.append(crossover(list(population[i]), list(population[j]), map))
    return crossed


def mutation(child, rate):
    if random.random() < rate:
        i = random.randint(0, len(child)-1)
        j = random.randint(0, len(child)-1)

        child[i], child[j] = child[j], child[i]
    return child

def mutatePopulation(children, rate):
    mutated = []
    for i in range(len(children)):
        for j in range(len(children[i])):
            mutated.append(mutation(children[i][j], rate))
    return mutated

def generate_local_neighbourhood(optimal, rate):
    neighbours = []
    for i in range(int(m)):
        new = mutation(optimal, rate)
        neighbours.append(new)
    return neighbours

def generate_search_space_solutions(mapper1, population, map, rate):
    x = crossoverPopulation(population, map)
    y = mutatePopulation(x, rate)
    ssSols = []
    rank = rank_fitness(mapper1, y, map)
    for i in range(int(m)):
        ssSols.append(y[rank[i][0]])
    return ssSols

def join(search, local, optimal, kay):
    new = []
    for i in search:
        new.append(i)
    for i in local:
        new.append(i)
    for i in kay:
      new.append(i)
    new.append(optimal)
    return new


def find_best_Generated_Solution(mapper1, joint, map):
    rank = rank_fitness(mapper1, joint, map)
    print(rank[0])
    return joint[rank[0][0]]

def Keeping_best_chromosomes(mapper1, population, map):
    rank = rank_fitness(mapper1, population, map)
    best = rank[0][1]
    keep = []
    for i in range(len(population)):
        if fitness(mapper1, population[i], map) == best:
            keep.append(list(population[i]).copy())
            #if len(keep) == len(list(population))/2: break
    return keep

def nextGeneration(gray, population, popSize, map):
    newPop = []
    rank = rank_fitness(gray, population, map)
    for i in range(popSize):
        newPop.append(population[rank[i][0]])
    return newPop

map = {
0:complex(0.3646,0),1:complex(0.2273,0.2851),2:complex(-0.0811,0.3555),3:complex(-0.3285,0.1582),
4:complex(-0.3285,-0.1582),5:complex(-0.0811,-0.3555),6:complex(0.2273,-0.2851),7:complex(0.6611,0),
8:complex(0.5854,0.3072),9:complex(0.3756,0.5441),10:complex(0.0797,0.6563),11:complex(-0.2344,0.6182),
12:complex(-0.4948,0.4384),13:complex(-0.6419,0.1583),14:complex(-0.6419,-0.1583),15:complex(-0.4949,-0.4383),
16:complex(-0.2346,-0.6181),17:complex(0.0795,-0.6563),18:complex(0.3754,-0.5442),19:complex(0.5853,-0.3074),
20:complex(0.9612,0),21:complex(0.3128,0.1074),22:complex(0.261,0.2031),23:complex(0.1809,0.2769),
24:complex(0.08117,0.3206),25:complex(-0.0273,0.3296),26:complex(-0.1329,0.3028),27:complex(-0.224,0.2433),
28:complex(-0.2908,0.1574),29:complex(-0.3262,0.05441),30:complex(-0.3262,-0.05441),31:complex(-0.2908,-0.1574),
32:complex(-0.2248,-0.2425),33:complex(-0.1353,-0.3018),34:complex(-0.0273,-0.3296),35:complex(0.0812,-0.3206),
36:complex(0.181,-0.2768),37:complex(0.2604,-0.2038),38:complex(0.3128,-0.1073),39:complex(1.2623,0),
40:complex(1.2223,0.3139),41:complex(1.1062,0.6081),42:complex(0.9202,0.864),43:complex(0.6765,1.0657),
44:complex(0.3902,1.2005),45:complex(0.0795,1.2598),46:complex(-0.2363,1.24),47:complex(-0.5372,1.1423),
48:complex(-0.8044,0.9728),49:complex(-1.021,0.742),50:complex(-1.1735,0.465),51:complex(-1.2523,0.1586),
52:complex(-1.2524,-0.1578),53:complex(-1.1738,-0.4642),54:complex(-1.0215,-0.7415),55:complex(-0.805,-0.9723),
56:complex(-0.538,-1.1419),57:complex(-0.2371,-1.2398),58:complex(0.0786,-1.2599),59:complex(0.3894,-1.2007),
60:complex(0.6758,-1.0662),61:complex(0.9197,-0.8647),62:complex(1.1058,-0.6088),63:complex(1.2224,-0.3147),
}


a = initial_population([x for x in range(64)], m)
b = rank_fitness([x for x in range(64)], a, map)[0][0]
optimal = [60, 46, 45, 51, 49, 44, 43, 30, 56, 48, 35, 38, 57, 22, 16, 2, 41, 0, 39, 9, 15, 21, 55, 18, 27, 20, 33, 47, 61, 40, 29, 63, 17, 12, 62, 50, 58, 7, 11, 10, 13, 36, 31, 26, 8, 59, 1, 19, 6, 32, 3, 53, 54, 5, 24, 4, 37, 42, 14, 23, 34, 28, 52, 25]
print("best initial solution: ", optimal, fitness([x for x in range(64)], optimal, map))
i = 0
best = optimal

while i < t:
    k = Keeping_best_chromosomes([x for x in range(64)], a, map)
    c = generate_local_neighbourhood(list(best), 0.05)
    d = generate_search_space_solutions([x for x in range(64)], a, map, 0.05)
    e = join(c,d,list(best), k)
    f = find_best_Generated_Solution([x for x in range(64)], e, map)
    if fitness([x for x in range(64)], f, map) > fitness([x for x in range(64)], list(best), map):
        best = f
        print("Best generated solution: ", list(best), fitness([x for x in range(64)], list(best), map))
    else:
        print("Best solution is still: ", best, fitness([x for x in range(64)], best, map))
    a = nextGeneration([x for x in range(64)], e, m, map)
    i = i + 1
