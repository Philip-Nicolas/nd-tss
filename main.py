import random, numpy, math, copy, matplotlib.pyplot as plt


## Adapted from https://ericphanson.com/blog/2016/the-traveling-salesman-and-10-lines-of-python/

def solveTsp(pts):
    n = len(pts)
    tour = list(range(0, n))

    for temp in numpy.logspace(0, 5, num=100000)[::-1]:
        [i, j] = sorted(random.sample(range(n), 2))
        newTour = tour[:i] + tour[j:j + 1] + tour[i + 1:j] + tour[i:i + 1] + tour[j + 1:]

        oldDistance = sum(
            [math.sqrt(sum([(pts[tour[(k + 1) % n]][d] - pts[tour[k % n]][d]) ** 2 for d in [0, 1]])) for k in
             [j, j - 1, i, i - 1]])
        newDistance = sum(
            [math.sqrt(sum([(pts[newTour[(k + 1) % n]][d] - pts[newTour[k % n]][d]) ** 2 for d in [0, 1]])) for
             k in [j, j - 1, i, i - 1]])

        if math.exp((oldDistance - newDistance) / temp) > random.random():
            tour = copy.copy(newTour)

    return tour


cities = [random.sample(range(100), 2) for x in range(15)]
tour = solveTsp(cities)

plt.plot([cities[tour[i % 15]][0] for i in range(16)], [cities[tour[i % 15]][1] for i in range(16)], 'xb-')
plt.show()
