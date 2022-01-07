import random, numpy, math, matplotlib.pyplot as plt


def validate_tsp_input(pts):
    """ Validates list of points passed as input to solve_tsp.
        Ensures:
            - There are at least 2 points
            - All points have the same dimension
            - Dimension of the points is at least 1

        Returns a tuple containing the list of points, the number of points, and the dimension of the points.
    """
    n = len(pts)
    assert n >= 2

    d = len(pts[0])
    assert d >= 1
    for i in range(n):
        assert d == len(pts[i])

    return pts, n, d


def validate_and_solve_tsp(input_points):
    return solve_tsp(*validate_tsp_input(input_points))


def solve_tsp(pts, n, d):
    # Adapted from https://ericphanson.com/blog/2016/the-traveling-salesman-and-10-lines-of-python/
    tour = list(range(0, n))

    for temp in numpy.logspace(0, 5, num=100000)[::-1]:
        # Create a new tour by randomly swapping 2 points in the previous tour
        [i, j] = sorted(random.sample(range(n), 2))
        new_tour = tour.copy()
        new_tour[j] = tour[i]
        new_tour[i] = tour[j]

        old_distance = sum([dist(pts, d, tour[(k + 1) % n], tour[k % n]) for k in [j, j - 1, i, i - 1]])
        new_distance = sum([dist(pts, d, new_tour[(k + 1) % n], new_tour[k % n]) for k in [j, j - 1, i, i - 1]])

        if math.exp((old_distance - new_distance) / temp) > random.random():
            tour = new_tour.copy()

    return tour


def dist(pts, d, i_1, i_2):
    return math.sqrt(sum([(pts[i_1][e] - pts[i_2][e]) ** 2 for e in range(d)]))


cities = [random.sample(range(100), 2) for x in range(15)]
cities_tour = validate_and_solve_tsp(cities)

plt.plot([cities[cities_tour[i % 15]][0] for i in range(16)], [cities[cities_tour[i % 15]][1] for i in range(16)],
         'xb-')
plt.show()
