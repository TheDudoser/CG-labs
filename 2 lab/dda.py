import matplotlib.pyplot as plt
import PIL.Image, PIL.ImageDraw


def dda(x1, x2, y1, y2):
    plt.title("DDA Algorithm")
    plt.xlabel('X-Axis')
    plt.ylabel('Y-Axis')

    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)

    xincrement = dx / steps
    yincrement = dy / steps

    i = 0

    xcoordinates = []
    ycoordinates = []

    while i < steps:
        i += 1
        x1 += xincrement
        y1 += yincrement
        print("X1: ", x1, "Y1: ", y1)
        xcoordinates.append(x1)
        ycoordinates.append(y1)

    plt.plot(xcoordinates, ycoordinates)
    plt.show()


def bres(x1, x2, y1, y2):
    plt.title("Bresenham Algorithm")
    plt.xlabel('X-Axis')
    plt.ylabel('Y-Axis')

    x, y = x1, y1
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    gradient = dy/float(dx)

    if gradient > 1:
        dx, dy = dy, dx
        x, y = y, x
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    p = 2 * dy - dx
    print('x = %s, y= %s' % (x, y))

    xcoordinates = [x]
    ycoordinates = [y]

    for k in range(2, dx):
        if p > 0:
            y = y + 1 if y < y2 else y - 1
            p += 2 * (dy - dx)
        else:
            p += 2*dy
        x = x + 1 if x < x2 else x - 1

        print('x = %s, y= %s' % (x, y))

        xcoordinates.append(x)
        ycoordinates.append(y)

    plt.plot(xcoordinates, ycoordinates)
    plt.show()


def circle(radius):
    # plt.title("Bresenham complete circle algorithm in Python")
    # plt.xlabel('X-Axis')
    # plt.ylabel('Y-Axis')

    # init vars
    switch = 3 - (2 * radius)
    points = set()
    x = 0
    y = radius

    # first quarter/octant starts clockwise at 12 o'clock
    while x <= y:
        points.add((x,-y))
        # first quarter 2nd octant
        points.add((y,-x))
        # second quarter 3rd octant
        points.add((y,x))
        # second quarter 4.octant
        points.add((x,y))
        # third quarter 5.octant
        points.add((-x,y))
        # third quarter 6.octant
        points.add((-y,x))
        # fourth quarter 7.octant
        points.add((-y,-x))
        # fourth quarter 8.octant
        points.add((-x,-y))
        if switch < 0:
            switch = switch + (4 * x) + 6
        else:
            switch = switch + (4 * (x - y)) + 10
            y = y - 1
        x = x + 1

    return points


if __name__ == '__main__':
    # circle
    size = 1000
    radius = 400
    circle_graph = PIL.Image.new("RGB", (size, size), (255, 255, 255))
    draw = PIL.ImageDraw.Draw(circle_graph)
    p = circle(radius)
    # print the point coords
    print(p)
    for point in p:
        draw.point((size / 2 + point[0], size / 2 + point[1]), (0, 0, 0))
    circle_graph.show()

