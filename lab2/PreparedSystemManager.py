import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt

from InputManager import InputManager


class PreparedSystem:
    def __init__(self, funcs, derivative_funcs=None):
        """
        funcs: вектор функций
        derivative_funcs: матрица частных производных
        """
        self.solutions = None
        self.funcs = funcs
        self.derivative_funcs = derivative_funcs
        self.before_x_vector = []
        self.iterations = 0
        self.x_left, self.x_right = None, None
        self.y_left, self.y_right = None, None

    def calculate(self, x, y):
        return np.array([self.funcs[0](x, y), self.funcs[1](x, y)])

    def calculate_derivatives(self, *args):
        return np.array([f(*args) for f in self.derivative_funcs])

    def get_error_rate(self):
        return abs(np.array(self.before_x_vector) - self.solutions)

    def _get_sufficient_convergence_condition(self, x, y):
        return max(sum(abs(i)) for i in self.calculate_derivatives(x, y))

    def check_sufficient_convergence_condition(self, x, y):
        return self._get_sufficient_convergence_condition(x, y) < 1

    def solve(self):
        return self.Simple_Iteration_Method()

    def _enter_root_isolation(self):
        print("Введите интервал изоляции корня:")
        x_left = InputManager.float_input("\tЛевый конец отрезка по x: ")
        x_right = InputManager.float_input("\tПравый конец отрезка по x: ")
        y_left = InputManager.float_input("\tЛевый конец отрезка по y: ")
        y_right = InputManager.float_input("\tПравый конец отрезка по y: ")
        while not (self.calculate(x_left, y_left)[0] * self.calculate(x_right, y_right)[0] < 0 and
                   self.calculate(x_left, y_left)[1] * self.calculate(x_right, y_right)[1] < 0):
            if not (x_left < x_right and y_left < y_right):
                print("Значения левых концов должны быть меньше правых.")
                continue
            print("Значения функции на углах квадрата должны быть разного знака для обеих функций!")
            if InputManager.yes_or_no_input(f"Показать график системы для корректировки?"):
                self.draw_graphic(x_left, x_right, y_left, y_right)
            print("Введите другие значения концов:")
            x_left = InputManager.float_input("\tЛевый конец отрезка по x: ")
            x_right = InputManager.float_input("\tПравый конец отрезка по x: ")
            y_left = InputManager.float_input("\tЛевый конец отрезка по y: ")
            y_right = InputManager.float_input("\tПравый конец отрезка по y: ")
        self.x_left, self.x_right = min(x_left, x_right), max(x_left, x_right)
        self.y_left, self.y_right = min(y_left, y_right), max(y_left, y_right)

        return

    def draw_graphic(self, x_left=None, x_right=None, y_left=None, y_right=None):
        if None in [x_left, x_right, y_left, y_right]:
            if None in [self.x_left, self.x_right, self.y_left, self.y_right]:
                print("Невозможно нарисовать график. Не определены концы отрезка")
                return
            else:
                x_left = self.x_left
                x_right = self.x_right
                y_left = self.y_left
                y_right = self.y_right
        x = np.arange(x_left, x_right, abs(x_left - x_right) / 30)
        y = np.arange(y_left, x_right, abs(y_left - y_right) / 30)
        x, y = np.meshgrid(x, y)
        Z = self.calculate(x, y)
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        # ax.axes.set_zlim3d(-5, 5)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.plot_surface(x, y, Z[0], cmap=cm.coolwarm)
        ax.plot_surface(x, y, Z[1], cmap="plasma")
        plt.show()

    def Simple_Iteration_Method(self):
        self._enter_root_isolation()
        if InputManager.yes_or_no_input("Показать график системы на введённом квадрате?"):
            self.draw_graphic()

        x = InputManager.float_input("Введите начальное приближение по x: ")
        y = InputManager.float_input("Введите начальное приближение по y: ")
        while not (self.x_left < x < self.x_right and self.y_left < y < self.y_right):
            print("Начальное приближение должно быть внутри интервала изоляции корня!")
            x = InputManager.float_input("Введите начальное приближение по x: ")
            y = InputManager.float_input("Введите начальное приближение по y: ")

        if not self.check_sufficient_convergence_condition(x, y):
            print("Не выполняется достаточное условие сходимости итерационного процесса.")
            print("Попробуйте ввести другое начальное приближение.")
            if not InputManager.yes_or_no_input("Продолжить выполнение?"):
                return

        # lambda_x = -max(self._get_sufficient_convergence_condition(self.x_left, self.y_left),
        #                 self._get_sufficient_convergence_condition(self.x_right, self.y_right))
        lambda_x = -1
        phi_x = lambda x, y: x + self.calculate(x, y)[0] / lambda_x
        # lambda_y = -max(self._get_sufficient_convergence_condition(self.x_left, self.y_left),
        #                 self._get_sufficient_convergence_condition(self.x_right, self.y_right))
        lambda_y = -1
        phi_y = lambda x, y: y + self.calculate(x, y)[1] / lambda_y
        epsilon = 10 ** (-5)
        self.before_x_vector = [x + 100, y + 100]
        while max(abs(x - self.before_x_vector[0]),
                  abs(y - self.before_x_vector[1])) > epsilon and self.iterations <= 100000:
            self.before_x_vector[0], self.before_x_vector[1] = x, y
            x, y = phi_x(x, y), phi_y(x, y)
            self.iterations += 1
        self.solutions = np.array([x, y])
        return self.solutions
