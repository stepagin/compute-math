import math

import numpy as np
from matplotlib import pyplot as plt

from Functions import FunctionHolder
from InputManager import InputManager


def get_n(x0, xn, h):
    return int(math.ceil(round(abs(xn - x0) / h, 3)))


def euler_method(func, x0, xn, y0, h):
    """
    Метод Эйлера
    """
    x_previous = [x0]
    y_previous = [y0]
    n = get_n(x0, xn, h)
    for i in range(n):
        x_now = x_previous[i]
        y_now = y_previous[i]
        x_previous.append(x_now + h)
        y_previous.append(y_now + h * (func(x_now, y_now) + func(x_now + h, y_now + h * func(x_now, y_now))) / 2)

    return x_previous, y_previous


def runge_kutta_method(func, x0, xn, y0, h):
    """
    Метод Рунге-Кутта 4-го порядка
    """
    x_previous = [x0]
    y_previous = [y0]
    n = get_n(x0, xn, h)
    for i in range(n):
        x_now = x_previous[i]
        y_now = y_previous[i]
        k1 = h * func(x_now, y_now)
        k2 = h * func(x_now + h / 2, y_now + k1 / 2)
        k3 = h * func(x_now + h / 2, y_now + k2 / 2)
        k4 = h * func(x_now + h, y_now + k3)
        x_previous.append(x_now + h)
        y_previous.append(y_now + (k1 + 2 * k2 + 2 * k3 + k4) / 6)
    return x_previous, y_previous


def milne_method(func, x0, xn, y0, h):
    n = get_n(x0, xn, h)
    if n < 5:
        return runge_kutta_method(func, x0, xn, y0, h)
    # y1, y2, y3 считаются методом Рунге-Кутта 4-го порядка
    x_previous, y_previous = runge_kutta_method(func, x0, x0 + 3 * h, y0, h)

    x_now = x_previous[-1]
    y_now = y_previous[-1]
    f = lambda i: func(x_previous[i], y_previous[i])
    for i in range(4, n + 1):
        x_now += h
        # этап прогноза
        y_now = y_previous[i - 4] + 4 * h * (2 * f(i - 3) - f(i - 2) + 2 * f(i - 1)) / 3
        # этап коррекции
        y_now = y_previous[i - 2] + h * (f(i - 2) + 4 * f(i - 1) + func(x_now, y_now)) / 3

        x_previous.append(x_now)
        y_previous.append(y_now)

    return x_previous, y_previous


def get_inputs():
    x0 = InputManager.float_input("Введите левый край отрезка x0 = ")
    xn = InputManager.float_input("Введите правый край отрезка xn = ")
    y0 = InputManager.float_input("Введите y(x0): ")
    h = InputManager.float_input("Введите шаг h = ")
    return x0, xn, y0, h


if __name__ == '__main__':
    """
    y' = e^sin(x) * cos(x), answer: y = e^sin(x) + C
    y' = x + 1, answer = x^2/2 + x + C
    y' = 2xy - x^2 - y^2 + 5, answer: y = 4 / (C * e^4x - 1) + x + 2
    """
    variants = ["y' = e^sin(x) * cos(x)",
                "y' = x + 1"]
    values = [FunctionHolder(lambda x, y: np.exp(np.sin(x)) * np.cos(x), lambda x, c: np.exp(np.sin(x)) + c),
              FunctionHolder(lambda x, y: x + 1, lambda x, c: x ** 2 / 2 + x + c)]
    chosen_func = InputManager.multiple_choice_input(variants, values, "Выберите ОДУ для численного решения:")

    variants = ["Метод Эйлера", "Метод Рунге-Кутта 4-го порядка", "Метод Милна"]
    values = [euler_method, runge_kutta_method, milne_method]
    chosen_method = InputManager.multiple_choice_input(variants, values, "Выберите метод для интегрирования: ")

    x0, xn, y0, h = get_inputs()
    c = y0 - chosen_func.answer(x0, 0)

    plt.title("Численное решение ОДУ")
    plt.plot(*chosen_method(chosen_func.f, x0, xn, y0, h), c='b')
    x = np.linspace(x0, xn, 50)
    plt.plot(x, chosen_func.answer(x, c), c='r')
    plt.grid(True)
    plt.show()
