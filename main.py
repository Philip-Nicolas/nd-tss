import random, numpy, math, matplotlib.pyplot as plt


# Adapted from https://ericphanson.com/blog/2016/the-traveling-salesman-and-10-lines-of-python/

def solve_tsp(pts):
    validate_tsp_input(pts)
    n = len(pts)
    tour = list(range(0, n))

    for temp in numpy.logspace(0, 5, num=100000)[::-1]:
        # Create a new tour by randomly swapping 2 points in the previous tour
        [i, j] = sorted(random.sample(range(n), 2));
        new_tour = tour.copy()
        new_tour[j] = tour[i]
        new_tour[i] = tour[j]

        old_distance = sum([dist(pts[tour[(k + 1) % n]], pts[tour[k % n]]) for k in [j, j - 1, i, i - 1]])
        new_distance = sum([dist(pts[new_tour[(k + 1) % n]], pts[new_tour[k % n]]) for k in [j, j - 1, i, i - 1]])

        if math.exp((old_distance - new_distance) / temp) > random.random():
            tour = new_tour.copy()

    return tour


def validate_tsp_input(pts):
    n = len(pts)
    assert n > 1

    d = len(pts[0])
    for i in range(n):
        assert d == len(pts[i])


def dist(p1, p2):
    return math.sqrt(sum([(p1[e] - p2[e]) ** 2 for e in range(len(p1))]))


cities = [random.sample(range(100), 2) for x in range(15)]
cities_tour = solve_tsp(cities)

plt.plot([cities[cities_tour[i % 15]][0] for i in range(16)], [cities[cities_tour[i % 15]][1] for i in range(16)],
         'xb-')
plt.show()
