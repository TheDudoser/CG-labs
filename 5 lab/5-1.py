import matplotlib
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sympy import symbols, Eq, solve

# uniform B-spline


def interpolate(t: float, degree: int, points: list, knots: list = None, weights: list = None) -> tuple[list, list]:
    n = len(points)
    d = len(points[0])  # point dimensionality

    if degree < 1:
        raise Exception('degree must be at least 1 (linear)')
    if degree > n - 1:
        raise Exception('degree must be less than or equal to point count - 1')

    if weights is None:
        # build weight vector of length [n]
        weights = [1 for _ in range(n)]

    if knots is None:
        # build knot vector of length [n + degree + 1]
        knots = [i for i in range(n + degree + 1)]
    elif len(knots) != n + degree + 1:
        raise Exception('bad knot vector length')

    domain = [degree, len(knots) - 1 - degree]

    # remap t to the domain where the spline is defined
    low = knots[domain[0]]
    high = knots[domain[1]]
    t = t * (high - low) + low

    if t < low or t > high:
        raise Exception('t выходит за границы')

    # find s (the spline segment) for the [t] value provided
    s = domain[0]
    while not (knots[s] <= t <= knots[s + 1]):
        s += 1

    # convert points to homogeneous coordinates
    vector = []
    for i in range(n):
        vector.append(list())
        for j in range(d):
            vector[i].append(points[i][j] * weights[i])
        vector[i].append(weights[i])

    # l (level) goes from 1 to the curve degree + 1
    for level in range(1, degree + 2):
        # build level l of the pyramid
        for i in range(s, s - degree - 1 + level, -1):
            alpha = (t - knots[i]) / (knots[i + degree + 1 - level] - knots[i])
            # interpolate each component
            for j in range(d + 1):
                vector[i][j] = (1 - alpha) * vector[i - 1][j] + alpha * vector[i][j]

    v = vector.copy()[: s + 1]
    x_, y_ = symbols('x y')
    for i in range(1, len(v)):
        if v[i - 1][0] == x[i - 1] or v[i - 1][1] == y[i - 1]:
            continue
        eq1 = Eq((x_ - vector[i - 1][0]) * (vector[i][1] - vector[i - 1][1]), (y_ - vector[i - 1][1]) * (
                vector[i][0] - vector[i - 1][0]))
        eq2 = Eq((x_ - x[i - 1]) * (y[i] - y[i - 1]), (y_ - y[i - 1]) * (x[i] - x[i - 1]))
        sol = solve((eq1, eq2), (x_, y_))
        x__ = sol.get(x_) if sol.get(x_) else 0
        y__ = sol.get(y_) if sol.get(y_) else 0
        # if vector[i][0] <= x__ <= x[i] and vector[i][1] <= y__ <= y[i]:
        v[i] = [x__, y__]

    # convert back to cartesian and return
    return [vector[s][i] / vector[s][d] for i in range(d)], v


"""
Реализовать интерактивную среду демонстрации
параметрических кубических кривых (выполнять интерполяцию
по нескольким точкам, использовать uniform B-spline и сплайн
Катмула-Рома). Дополнительное задание: реализовать
изменение весов точек и визуализацию рациональными
кривыми.
"""

matplotlib.use('Qt5Agg')
fig, ax = plt.subplots()
ln, = plt.plot([], [], 'g-', lw=3, label='uniform b-spline')
vectorplt, = plt.plot([], [], 'b-', lw=1)
xdata, ydata = [], []

points = [
    [0, 0],
    [0, 4],
    [4, 4],
    [4, 0],
    [8, 0],
    [12, 4],
    [14, 4],
    [14, 0]
]
degree = 2
x = [point[0] for point in points]
y = [point[1] for point in points]


def init():
    ax.set_xlim(min(x) - 1, max(x) + 1)
    ax.set_ylim(min(y) - 1, max(y) + 1)
    ax.scatter(x, y, c='r')
    ax.plot(x, y, c='black', lw=1)
    ax.grid(True)
    ax.legend(loc='best')
    return ln,


def update(t):
    if t == 0:
        xdata.clear()
        ydata.clear()
    point, vectors = interpolate(t, degree, points)
    xdata.append(point[0])
    ydata.append(point[1])
    ln.set_data(xdata, ydata)
    vectorplt.set_data([vector[0] for vector in vectors], [vector[1] for vector in vectors])
    return ln, vectorplt,


if __name__ == '__main__':
    ani = FuncAnimation(fig, update, frames=np.linspace(0.0, 1.0, 99),
                        init_func=init, blit=True, cache_frame_data=True)
    plt.show()