from random import random

import numpy as np
from matplotlib import pyplot as plt

from InputManager import InputManager


class Integral:

    def __init__(self, func):
        self.func = func
        self.steps = 0
        self.left = None
        self.right = None
        self.iterations = 0

    def calculate(self, x):
        return self.func(x)

    def set_steps(self, steps):
        self.steps = steps

    def solve(self, left, right, method_func):
        self.left = left
        self.right = right
        try:
            steps = 4
            epsilon = InputManager.epsilon_input("Введите epsilon: ")
            while abs(method_func(self, left, right, steps / 2) - method_func(self, left, right, steps)) > epsilon \
                    and self.iterations < 19:
                steps *= 2
                self.iterations += 1
            self.set_steps(steps)
            return round(method_func(self, left, right, steps), len(str(int(1 / epsilon))))
        except Exception:
            return None

    def draw_func(self, left=None, right=None):
        if left is None or right is None:
            if self.left is None or self.right is None:
                print("Невозможно нарисовать график. Не определены концы отрезка")
            else:
                left = self.left
                right = self.right
        x_axis = np.linspace(min(left, right), max(left, right), 100)
        plt.plot(x_axis, self.calculate(x_axis))
        plt.grid(True, which='both')
        plt.axvline(x=0, color='k')
        plt.axhline(y=0, color='k')
        plt.show()
