# projectile motion without restiance
import matplotlib.pyplot as plt
import numpy as np

class TanError(Exception):
    pass


def tan(x):
    if x % (np.pi / 2) == 0:
        raise TanError


def maxHeight(A, B, C, x):
    return A * x ** 2 + B * x + C


def acceleration(gravity):
    xAcceleration = 0
    yAcceleration = -1 * gravity
    acceleration = gravity


def velocity(initialVelocity, alpha, gravity, time):
    xVelocity = initialVelocity * np.cos(alpha)
    yVelocity = initialVelocity * np.sin(alpha) - gravity * time
    velocity = np.sqrt(xVelocity ** 2 + yVelocity ** 2)
    return velocity


def projectileMotionWithoutResistance(initialVelocity, initialHeight, alpha, gravity):
    # kąty muszą być w radianach
    A = -1 * gravity / (2 * initialVelocity ** 2 * np.cos(alpha) ** 2)
    B = np.tan(alpha)
    C = initialHeight

    quadraticEquation = [A, B, C]
    roots = np.roots(quadraticEquation)
    range = max(roots)
    height = maxHeight(A, B, C, (roots[0] + roots[1]) / 2)

    x = np.linspace(0, range, 1000)
    y = (
        initialHeight
        + np.tan(alpha) * x
        - gravity * x ** 2 / (2 * initialVelocity ** 2 * np.cos(alpha) ** 2)
    )

 # `  plt.plot(x, y)
 #    plt.xlim(0, range + 0.1 * range)
 #    plt.show()

    return {"x": x, "y": y}

