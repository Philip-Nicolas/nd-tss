import random, numpy, math, copy, matplotlib.pyplot as plt


# Adapted from https://ericphanson.com/blog/2016/the-traveling-salesman-and-10-lines-of-python/

def solve_tsp(pts):
    validate_tsp_input(pts)
    n = len(pts)
    tour = list(range(0, n))

    for temp in numpy.logspace(0, 5, num=100000)[::-1]:
        [i, j] = sorted(random.sample(range(n), 2))
        new_tour = tour[:i] + tour[j:j + 1] + tour[i + 1:j] + tour[i:i + 1] + tour[j + 1:]

        old_distance = sum(
            [math.sqrt(sum([(pts[tour[(k + 1) % n]][d] - pts[tour[k % n]][d]) ** 2 for d in [0, 1]])) for k in
             [j, j - 1, i, i - 1]])
        new_distance = sum(
            [math.sqrt(sum([(pts[new_tour[(k + 1) % n]][d] - pts[new_tour[k % n]][d]) ** 2 for d in [0, 1]])) for
             k in [j, j - 1, i, i - 1]])

        if math.exp((old_distance - new_distance) / temp) > random.random():
            tour = copy.copy(new_tour)

    return tour


def validate_tsp_input(pts):
    n = len(pts)
    assert n > 1

    d = len(pts[0])
    for i in range(n):
        assert d == len(pts[i])


cities = [random.sample(range(100), 2) for x in range(15)]
cities_tour = solve_tsp(cities)

plt.plot([cities[cities_tour[i % 15]][0] for i in range(16)], [cities[cities_tour[i % 15]][1] for i in range(16)],
         'xb-')
plt.show()
