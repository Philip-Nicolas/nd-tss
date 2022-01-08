import math
import time

import matplotlib.pyplot as plt
import numpy
import random


# region Solver

def validate_tsp_input(input_points):
    """ Validates list of points passed as input to solve_tsp.
        Ensures:
            - There are at least 2 points
            - All points have the same dimension
            - Dimension of the points is at least 1

        Returns a tuple containing the list of points, the number of points, and the dimension of the points.
    """
    n = len(input_points)
    assert n >= 2

    d = len(input_points[0])
    assert d >= 1
    for i in range(n):
        assert d == len(input_points[i])

    return input_points, n, d


def solve_tsp(points, n, d, compare_loops=False):
    # Adapted from https://ericphanson.com/blog/2016/the-traveling-salesman-and-10-lines-of-python/
    tour = list(range(0, n))

    best_dist = get_loop_dist(get_tour_order(points, n, tour), n, d)
    best_tour = tour.copy()

    for temp in numpy.logspace(-2, 4, num=100000)[::-1]:
        # Create a new tour by randomly swapping 2 points in the previous tour
        [i, j] = sorted(random.sample(range(n), 2))
        new_tour = tour.copy()
        new_tour[j] = tour[i]
        new_tour[i] = tour[j]

        old_distance = sum([dist(points, d, tour[(k + 1) % n], tour[k % n]) for k in [j, j - 1, i, i - 1]])
        new_distance = sum([dist(points, d, new_tour[(k + 1) % n], new_tour[k % n]) for k in [j, j - 1, i, i - 1]])

        if math.exp((old_distance - new_distance) / temp) > random.random():
            tour = new_tour.copy()
            if not compare_loops or best_dist > get_loop_dist(get_tour_order(points, n, tour), n, d):
                best_tour = tour.copy()

    ordered_points = get_tour_order(points, n, best_tour)
    loop_dist = get_loop_dist(ordered_points, n, d)

    return ordered_points, loop_dist


# endregion

# region Presentation

def plot(ordered_points, n, d):
    assert 1 <= d <= 3

    components = [get_components(*get_loop(ordered_points, n), e=e) for e in range(d)]

    if d == 3:
        axes = plt.axes(projection="3d")
        x, y, z = components

        # Set 3D axis bounds
        axes.set_xlim3d(min(x), max(x))
        axes.set_ylim3d(min(y), max(y))
        axes.set_zlim3d(min(z), max(z))

        # Set 3D aspect ratio
        axes.set_box_aspect([ub - lb for lb, ub in (getattr(axes, f'get_{a}lim')() for a in 'xyz')])

        # plot points and connecting lines
        axes.plot3D(x, y, z, 'blue')
        axes.scatter3D(x, y, z, 'blue', depthshade=True)
    else:
        plt.plot(*components, 'xb-')

    plt.title("Distance: " + str(get_loop_dist(ordered_points, n, d)))
    plt.show()


def present_tsp_input_summary(n, d):
    print("\nSolving", d, "dimension TSP with", n, "points.")


def present_tsp_solution(ordered_points, loop_dist, n, d):
    if d <= 3:
        plot(ordered_points, n, d)
    print("Distance:", loop_dist)
    print("Path:", ordered_points)


def validate_solve_present_tsp(input_points):
    # validate & parse input points
    points, n, d = validate_tsp_input(input_points)
    present_tsp_input_summary(n, d)

    # solve tsp
    ordered_points, loop_dist = solve_tsp(points, n, d)

    # display solution
    present_tsp_solution(ordered_points, loop_dist, n, d)


# endregion

# region Utilities

def dist(points, d, i_1, i_2):
    return math.sqrt(sum([(points[i_1][e] - points[i_2][e]) ** 2 for e in range(d)]))


def get_loop_dist(ordered_points, n, d):
    return round(sum(dist(ordered_points, d, i, (i + 1) % n) for i in range(n)), 2)


def get_components(points, n, e):
    return [points[i][e] for i in range(n)]


def get_tour_order(points, n, tour):
    return [points[tour[i]] for i in range(n)]


def get_loop(ordered_points, n):
    loop = ordered_points.copy()
    loop.append(ordered_points[0])

    return loop, n + 1


def get_sample_input(points_count, dimension):
    return [random.sample(range(100), dimension) for _ in range(points_count)]


def test_multiple_runs(initial_input_points, compare_loops=False):
    input_points = initial_input_points
    runs = 0
    done = False

    while not done:
        points, n, d = validate_tsp_input(input_points)
        present_tsp_input_summary(n, d)
        start_time = time.time()
        ordered_points, loop_dist = solve_tsp(points, n, d, compare_loops)
        end_time = time.time()
        runs += 1

        if get_loop_dist(ordered_points, n, d) < get_loop_dist(input_points, n, d):
            input_points = ordered_points

        present_tsp_solution(ordered_points, loop_dist, n, d)
        print("Runs:", runs)
        print("Runtime:", str(round(end_time - start_time, 3)) + "s")
        done = input("Done? Type 'exit' to quit:") == "exit"


# endregion


# region Examples


validate_solve_present_tsp(get_sample_input(16, 2))
validate_solve_present_tsp(get_sample_input(16, 3))
validate_solve_present_tsp(get_sample_input(16, 4))

test_multiple_runs(get_sample_input(24, 3), True)

# endregion
