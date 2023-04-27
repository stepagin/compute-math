import numpy as np
from matplotlib import pyplot as plt

from InputManager import InputManager


class PreparedEquation:

    def __init__(self, func, derivative_func=None):
        self.func = func
        self.derivative_func = derivative_func
        self.iterations = 0

    def calculate(self, arg):
        try:
            return self.func(arg)
        except Exception:
            raise ValueError

    def solve(self):
        variants = ["Метод хорд", "Метод Ньютона", "Метод простых итераций"]
        values = [self.Chord_Method, self.Newtons_Method, self.Simple_Iteration_Method]
        chosen_method = InputManager.multiple_choice_input(variants, values, "Выберите метод решения уравнения: ")
        return chosen_method()

    def _enter_root_isolation(self):
        print("Введите интервал изоляции корня:")
        left = InputManager.float_input("\tЛевый конец отрезка: ")
        right = InputManager.float_input("\tПравый конец отрезка: ")

        while not self.calculate(left) * self.calculate(right) < 0:
            print("Значения функции на концах отрезка должны быть разного знака!")
            if InputManager.yes_or_no_input(f"Показать график функции для корректировки?"):
                self.draw_graphic(left, right)
            print("Введите другие значения концов:")
            left = InputManager.float_input("\tЛевый конец отрезка: ")
            right = InputManager.float_input("\tПравый конец отрезка: ")
        if self.calculate(left) > 0:
            # функция принимает значение > 0 на правом конце, и < 0 на левом
            # от left до right функция возрастает
            left, right = right, left
        self.left, self.right = left, right
        return left, right

    def draw_graphic(self, left=None, right=None, dot_x=None, dot_y=None):
        if left is None or right is None:
            if self.left is None or self.right is None:
                print("Невозможно нарисовать график. Не определены концы отрезка")
            else:
                left = self.left
                right = self.right
        grid = abs(left - right) / 30
        x_axis = np.linspace(min(left, right) - grid, max(left, right) + grid, 32)
        plt.plot(x_axis, self.calculate(x_axis))
        plt.grid(True, which='both')
        if (min(left, right) - grid <= 0 and 0 <= max(left, right) + grid):
            plt.axvline(x=0, color='k')
        plt.axhline(y=0, color='k')
        if dot_x is not None:
            if dot_y is None:
                dot_y = 0
            plt.plot(dot_x, dot_y, "ro")
        plt.show()

    def Chord_Method(self):
        left, right = self._enter_root_isolation()

        # основная часть решения
        epsilon = 10 ** (-8)
        x = left - self.calculate(left) * (right - left) / (self.calculate(right) - self.calculate(left))
        while abs(self.calculate(x)) > epsilon:
            x = left - self.calculate(left) * (right - left) / (self.calculate(right) - self.calculate(left))
            if self.calculate(x) > 0:
                right = x
            else:
                left = x
            self.iterations += 1

        return x

    def Simple_Iteration_Method(self):
        left, right = self._enter_root_isolation()
        halflife = -0.01 / max(abs(self.derivative_func(left)), abs(self.derivative_func(right)))
        phi = lambda x: x + halflife * self.calculate(x)
        print(f"Используемая лямбда={halflife}")

        # основная часть решения
        epsilon = 10 ** (-8)
        x = InputManager.float_input("Введите начальное приближение: ")
        while not (min(left, right) < x and x < max(left, right)):
            x = InputManager.float_input("Введите начальное приближение внутри интервала изоляции корня: ")
        try:
            self.calculate(x)
        except Exception:
            print("Невозможно посчитать значение функции в заданной точке.")
            return None


        while abs(self.calculate(x)) > epsilon and self.iterations <= 1000000:
            x = phi(x)
            self.iterations += 1
        if self.iterations == 1000000:
            return None
        return x

    def Newtons_Method(self):
        left, right = self._enter_root_isolation()
        x = InputManager.float_input("Введите начальное приближение: ")

        epsilon = 10 ** (-8)
        while abs(self.calculate(x)) > epsilon:
            x = x - self.calculate(x) / self.derivative_func(x)
            self.iterations += 1

        return x
