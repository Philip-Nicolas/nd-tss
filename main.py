import random, numpy, math, matplotlib.pyplot as plt


def validate_tsp_input(points):
    """ Validates list of points passed as input to solve_tsp.
        Ensures:
            - There are at least 2 points
            - All points have the same dimension
            - Dimension of the points is at least 1

        Returns a tuple containing the list of points, the number of points, and the dimension of the points.
    """
    n = len(points)
    assert n >= 2

    d = len(points[0])
    assert d >= 1
    for i in range(n):
        assert d == len(points[i])

    return points, n, d


def validate_and_solve_tsp(input_points):
    return solve_tsp(*validate_tsp_input(input_points))


def solve_tsp(points, n, d):
    # Adapted from https://ericphanson.com/blog/2016/the-traveling-salesman-and-10-lines-of-python/
    tour = list(range(0, n))

    for temp in numpy.logspace(0, 5, num=100000)[::-1]:
        # Create a new tour by randomly swapping 2 points in the previous tour
        [i, j] = sorted(random.sample(range(n), 2))
        new_tour = tour.copy()
        new_tour[j] = tour[i]
        new_tour[i] = tour[j]

        old_distance = sum([dist(points, d, tour[(k + 1) % n], tour[k % n]) for k in [j, j - 1, i, i - 1]])
        new_distance = sum([dist(points, d, new_tour[(k + 1) % n], new_tour[k % n]) for k in [j, j - 1, i, i - 1]])

        if math.exp((old_distance - new_distance) / temp) > random.random():
            tour = new_tour.copy()

    return tour


def dist(points, d, i_1, i_2):
    return math.sqrt(sum([(points[i_1][e] - points[i_2][e]) ** 2 for e in range(d)]))


def plot(points, n, d):
    assert 1 <= d <= 3

    plt.plot(*[get_components(points, n, e) for e in range(d)], 'xb-')
    plt.show()


def get_components(points, n, e):
    return [points[i][e] for i in range(n)]


cities = [random.sample(range(100), 2) for x in range(15)]
cities_tour = validate_and_solve_tsp(cities)

plot([cities[cities_tour[i % 15]] for i in range(16)], 15, 2)
