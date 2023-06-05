import math
from abc import abstractmethod
from functools import lru_cache

import numpy as np
from matplotlib import pyplot as plt
from prettytable import PrettyTable

from InputManager import InputManager


def multiply(arr):
    res = 1
    for i in arr:
        res *= i
    return res


class Solver:
    def __init__(self, points):
        self.f = lambda x: 0
        self.points_x = [p[0] for p in points]
        self.points_y = [p[1] for p in points]
        self.n = len(points)

    def draw_graphics(self, plot_name=""):
        X = np.linspace(min(self.points_x), max(self.points_x), 100)
        Y = [self.f(x) for x in X]
        fig, ax = plt.subplots(1, 1)
        # ax.set_ylim([min(self.points_y) - 1, max(self.points_y) + 1])
        ax.scatter(self.points_x, self.points_y, c='r', marker='o')
        ax.plot(X, Y)
        plt.title(plot_name)
        plt.show()

    @abstractmethod
    def solve(self):
        pass


class Lagrange(Solver):

    def solve(self, draw_graphic=True):
        one_brace = lambda x, i, j: (x - self.points_x[j]) / (self.points_x[i] - self.points_x[j])
        l_i = lambda x, i: multiply([one_brace(x, i, j) if i != j else 1 for j in range(self.n)])
        L_n = lambda x: sum(np.multiply(self.points_y, [l_i(x, i) for i in range(self.n)]))
        self.f = L_n
        if draw_graphic:
            self.draw_graphics("Интерполяционный многочлен Лагранжа")


class Gaussian(Solver):

    @lru_cache
    def calculate_gaussian_delta_y(self, d, i):
        if abs(i) > len(self.points_x) // 2 or d > self.n:
            return None
        if self.n // 2 + i + d >= self.n:
            return None

        if d == 0:
            return self.points_y[i + self.n // 2]

        return self.calculate_gaussian_delta_y(d - 1, i + 1) - self.calculate_gaussian_delta_y(d - 1, i)

    @staticmethod
    @lru_cache(maxsize=None)
    def get_first_t_coefficient(t, n):
        """
        Возвращает число (в зависимости от n)
        для n = 0, n = 1, и т.д.:
        1, t, t(t-1), (t+1)t(t-1), (t+1)t(t-1)(t-2), ...
        """
        if n == 0:
            return 1
        res = 1
        for i in range((n + 1) // 2):
            res *= (t + i)
        for i in range(1, n // 2 + 1):
            res *= (t - i)
        return res / math.factorial(n)

    @staticmethod
    @lru_cache(maxsize=None)
    def get_second_t_coefficient(t, n):
        """
        1, t, (t+1)t, (t+1)t(t-1), (t+1)(t+2)t(t-1), ...
        """
        if n == 0:
            return 1
        res = 1
        for i in range((n + 1) // 2):
            res *= (t - i)
        for i in range(1, n // 2 + 1):
            res *= (t + i)
        return res / math.factorial(n)

    def solve(self):

        h = self.points_x[1] - self.points_x[0]

        for i in range(1, self.n - 1):
            if self.points_x[i] - self.points_x[i - 1] - h > 10 ** (-9):
                print("Невозможно применить метод Гаусса. Узлы не равноотстоящие.")
                return

        if len(self.points_x) % 2 == 0:
            print("Невозможно применить метод Гаусса. Количество точек должно быть нечётным.")
            return

        self.calculate_gaussian_delta_y(self.n - 1, -(self.n // 2))
        table = PrettyTable(["x_i", "y_i", "d y_i"] + [f"d^{i} y_i" for i in range(2, self.n)])
        for i in range(self.n):
            table.add_row([self.points_x[i]] + ["-" if u is None else round(u, 4) for u in
                                                [self.calculate_gaussian_delta_y(j, i - self.n // 2) for j in
                                                 range(self.n)]])
        print("Таблица конечных разностей:")
        print(table)

        center_of_section = (self.points_x[0] + self.points_x[-1]) / 2

        first_fg = lambda t: sum(
            [Gaussian.get_first_t_coefficient(t, i) * self.calculate_gaussian_delta_y(i, -(i // 2))
             for i in range(self.n)])
        second_fg = lambda t: sum(
            [Gaussian.get_second_t_coefficient(t, i) * self.calculate_gaussian_delta_y(i, (-i // 2))
             for i in range(self.n)])

        self.f = lambda x: first_fg((x - center_of_section) / h) if x < center_of_section else second_fg(
            (x - center_of_section) / h)

        if InputManager.yes_or_no_input("Показать график функции?"):
            self.draw_graphics("Интерполяционный многочлен Гаусса")

        if InputManager.yes_or_no_input("Хотите узнать значение функции в конкретной точке?"):
            x = InputManager.float_input_with_borders(self.points_x[0], self.points_x[-1],
                                                      "Введите координату x точки: ")
            t = (x - center_of_section) / h
            print("Значение функции в точке x:", self.f(x))

            # погрешность считается по формуле из лекции
            print("Оценка погрешности:", abs(self.calculate_gaussian_delta_y(self.n - 1, -(self.n // 2)) * multiply(
                [(t - i) for i in range(self.n // 2)]) / math.factorial(self.n // 2 + 1)))


class StirlingAndBessel(Solver):
    def solve(self):
        print("Интерполяция по схемам Стирлинга и Бесселя пока не реализована.")


class PreparedFunctionSolver:
    def __init__(self, f):
        self.f = f
        self.interpolated_function = lambda x: 0

    def draw_init_graphic(self):
        X = np.linspace(-5, 5, 100)
        Y = self.f(X)
        fig, ax = plt.subplots(1, 1)
        ax.plot(X, Y)
        ax.grid(True)
        plt.title("Выбранная функция")
        plt.show()

    def draw_two_graphics(self, f_second, points):
        X = np.linspace(points[0][0], points[-1][0], 100)
        Y1 = self.f(X)
        Y2 = [f_second(x) for x in X]
        fig, ax = plt.subplots(1, 1)
        ax.scatter([p[0] for p in points], [p[1] for p in points], c='r', marker='o')
        ax.plot(X, Y2, c='g')
        ax.plot(X, Y1, color=(0, 0, 0, 0.2), linestyle='-.')
        ax.grid(True)
        plt.title("Результат интерполяции:")
        plt.show()
