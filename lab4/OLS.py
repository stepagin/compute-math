# OLS means Ordinary least squares

import matplotlib.pyplot as plt
import numpy as np

from series import SeriesManager

np.set_printoptions(formatter={'float_kind': "{:.2f}".format})


class Function:

    def __init__(self, ser):
        self.series = ser
        self.mse = None
        self.phi = lambda x: x * 0
        self.method_name = None

    def get_epsilon_list(self, phi_x):
        result = np.array(self.series.Y) - phi_x
        return result

    def draw_graphic(self, series=None):
        x = np.linspace(min(self.series.X), max(self.series.X), 100)
        ax = plt.subplot()
        if series is None:
            ax.scatter(self.series.X, self.series.Y, c="r")
        else:
            ax.scatter(series.X, series.Y, c="r")
        ax.plot(x, self.phi(x))
        ax.set_title(self.method_name)
        plt.show()

    def calculate(self, points):
        return self.phi(np.array(points))

    def solve(self):
        return None

    def check_series(self, series, condition=lambda x, y: x > 0 and y > 0):
        for i in range(series.n):
            if not condition(series.X[i], series.Y[i]):
                return False
        return True

class LinearFunction(Function):
    def __init__(self, series):
        self.broken_flag = False
        super().__init__(series.copy())
        self.method_name = "Линейная функция."

    def get_pearson_correlation_coefficient(self):
        X, Y, n = np.array(self.series.X), np.array(self.series.Y), self.series.n
        x_mean = sum(X) / n
        y_mean = sum(Y) / n
        result = sum([(X[i] - x_mean) * (Y[i] - y_mean) for i in range(n)])
        result /= np.sqrt(sum((X - x_mean) ** 2) * sum((Y - y_mean) ** 2))
        return result

    def define_linear_relationship(self, r):
        r = round(r, 3)
        if r == 0:
            return "отсутствует"
        elif r < 0.3:
            return "слабая"
        elif r < 0.5:
            return "умеренная"
        elif r < 0.7:
            return "заметная"
        elif r < 0.9:
            return "высокая"
        elif r < 0.99:
            return "весьма высокая"
        else:
            return "прямая"

    def get_a_b(self):
        sx = sum(self.series.X)
        sy = sum(self.series.Y)
        sxx = sum([x ** 2 for x in self.series.X])
        sxy = sum([self.series.X[i] * self.series.Y[i] for i in range(self.series.n)])
        delta = sxx * self.series.n - sx * sx
        delta1 = sxy * self.series.n - sx * sy
        delta2 = sxx * sy - sx * sxy
        a = delta1 / delta
        b = delta2 / delta
        return a, b

    def solve(self):
        a, b = self.get_a_b()
        self.phi = lambda x: a * x + b
        p = self.calculate(self.series.X)
        epsilon_list = self.get_epsilon_list(p)
        self.mse = sum([e ** 2 for e in epsilon_list]) / self.series.n
        r = self.get_pearson_correlation_coefficient()
        result = \
            f"""    Формула функции: phi(x) = ax + b
    Коэффициенты: a={round(a, 4)}, b={round(b, 4)}
    Значение функции в точках: {p.round(4)}
    Отклонения: {epsilon_list.round(4)}
    Сумма отклонений: {round(sum(epsilon_list), 4)}
    Коэффициенты: [{round(a, 4)} {round(b, 4)}]
    Среднеквадратичное отклонение: {np.sqrt(round(self.mse, 4))}
    Коэффициент корреляции: {round(r, 2)}
    Линейная зависимость: {self.define_linear_relationship(r)}
"""
        return result


class PolynomialFunction2ndDegree(Function):

    def __init__(self, series):
        self.broken_flag = False
        super().__init__(series.copy())
        self.method_name = "Полиномиальная функция 2-й степени."

    def get_solution(self):
        x = np.array(self.series.X)
        y = np.array(self.series.Y)
        sx1, sx2, sx3, sx4 = sum(x), sum(x ** 2), sum(x ** 3), sum(x ** 4)
        matrix = np.array(
            [[self.series.n, sx1, sx2],
             [sx1, sx2, sx3],
             [sx2, sx3, sx4]]
        )
        b = np.array([sum(y), sum(x * y), sum(x ** 2 * y)])
        return np.linalg.solve(matrix, b)

    def solve(self):
        solution = self.get_solution()
        self.phi = lambda x: solution[0] + solution[1] * x + solution[2] * x ** 2
        p = self.calculate(self.series.X)
        epsilon_list = self.get_epsilon_list(p)
        self.mse = sum([e ** 2 for e in epsilon_list]) / self.series.n
        result = \
            f"""    Формула функции: phi(x) = a0 + a1*x + a2*x^2
    Коэффициенты: {solution.round(4)}
    Значение функции в точках: {p.round(4)}
    Отклонения: {epsilon_list.round(4)}
    Сумма отклонений: {round(sum(epsilon_list), 4)}
    Среднеквадратичное отклонение: {np.sqrt(round(self.mse, 4))}
"""
        return result


class PolynomialFunction3rdDegree(Function):

    def __init__(self, series):
        self.broken_flag = False
        super().__init__(series.copy())
        self.method_name = "Полиномиальная функция 3-й степени."

    def get_solution(self):
        x = np.array(self.series.X)
        y = np.array(self.series.Y)
        sx1, sx2, sx3, sx4, sx5, sx6 = sum(x), sum(x ** 2), sum(x ** 3), sum(x ** 4), sum(x ** 5), sum(x ** 6)
        matrix = np.array(
            [[self.series.n, sx1, sx2, sx3],
             [sx1, sx2, sx3, sx4],
             [sx2, sx3, sx4, sx5],
             [sx3, sx4, sx5, sx6]]
        )
        b = np.array([sum(y), sum(x * y), sum(x ** 2 * y), sum(x ** 3 * y)])
        return np.linalg.solve(matrix, b)

    def solve(self):
        solution = self.get_solution()
        self.phi = lambda x: solution[0] + solution[1] * x + solution[2] * x ** 2 + solution[3] * x ** 3
        p = self.calculate(self.series.X)
        epsilon_list = self.get_epsilon_list(p)
        self.mse = sum([e ** 2 for e in epsilon_list]) / self.series.n
        result = \
            f"""    Формула функции: phi(x) = a0 + a1*x + a2*x^2 + a3*x^3
    Коэффициенты: {solution.round(4)}
    Значение функции в точках: {p.round(4)}
    Отклонения: {epsilon_list.round(4)}
    Сумма отклонений: {round(sum(epsilon_list), 4)}
    Среднеквадратичное отклонение: {round(np.sqrt(self.mse), 4)}
"""
        return result


class ExponentialFunction(Function):

    def __init__(self, series):
        ser = series.copy()
        condition = lambda x, y: y > 0
        self.broken_flag = False
        if not self.check_series(series=ser, condition=condition):
            self.broken_flag = True
            x, y = [], []
            for i in range(series.n):
                if series.Y[i] > 0:
                    x.append(series.X[i])
                    y.append(series.Y[i])
            ser.set_xy(x, y)
        super().__init__(ser)
        self.method_name = "Экспоненциальная функция."

    def solve(self):
        x = np.array(self.series.X)
        y = np.log(np.array(self.series.Y))
        ser = self.series.copy()
        ser.set_xy(x, y)

        linf = LinearFunction(ser)
        b, a = linf.get_a_b()
        a = np.exp(a)

        self.phi = lambda x: a * np.exp(b * x)
        p = self.calculate(self.series.X)
        epsilon_list = self.get_epsilon_list(p)
        self.mse = sum([e ** 2 for e in epsilon_list]) / self.series.n
        result = \
            f"""    Формула функции: phi(x) = a * exp(bx)
            Коэффициенты: a={round(a, 4)}, b={round(b, 4)}
            Значение функции в точках: {p.round(4)}
            Отклонения: {epsilon_list.round(4)}
            Сумма отклонений: {round(sum(epsilon_list), 4)}
            Среднеквадратичное отклонение: {round(np.sqrt(self.mse), 4)}
        """
        return result


class LogarithmicFunction(Function):
    def __init__(self, series):
        condition = lambda x, y: x > 0
        ser = series.copy()
        self.broken_flag = False
        if not self.check_series(series, condition):
            self.broken_flag = True
            x, y = [], []
            for i in range(series.n):
                if series.X[i] > 0:
                    x.append(series.X[i])
                    y.append(series.Y[i])
            ser = SeriesManager()
            ser.set_xy(x, y)
        super().__init__(ser)
        self.method_name = "Логарифмическая функция."

    def solve(self):
        x = np.log(np.array(self.series.X))
        y = np.array(self.series.Y)
        ser = self.series.copy()
        ser.set_xy(x, y)
        linf = LinearFunction(ser)
        a, b = linf.get_a_b()
        # a = np.exp(a)
        self.phi = lambda x: a * np.log(x) + b
        p = self.calculate(self.series.X)
        epsilon_list = self.get_epsilon_list(p)
        self.mse = sum([e ** 2 for e in epsilon_list]) / self.series.n
        result = \
            f"""    Формула функции: phi(x) = a * ln(x) + b
            Значение функции в точках: {p.round(4)}
            Отклонения: {epsilon_list.round(4)}
            Сумма отклонений: {round(sum(epsilon_list), 4)}
            Среднеквадратичное отклонение: {round(np.sqrt(self.mse), 4)}
        """
        return result


class PowerFunction(Function):

    def __init__(self, series):
        condition = lambda x, y: x > 0 and y > 0
        ser = series.copy()
        self.broken_flag = False
        if not self.check_series(series, condition):
            self.broken_flag = True
            x, y = [], []
            for i in range(series.n):
                if series.X[i] > 0 and series.Y[i] > 0:
                    x.append(series.X[i])
                    y.append(series.Y[i])
            ser = SeriesManager()
            ser.set_xy(x, y)
        super().__init__(ser)
        self.method_name = "Степенная функция."

    def solve(self):
        x = np.log(np.array(self.series.X))
        y = np.log(np.array(self.series.Y))
        ser = self.series.copy()
        ser.set_xy(x, y)
        linf = LinearFunction(ser)
        b, a = linf.get_a_b()
        a = np.exp(a)
        self.phi = lambda x: a * x ** b
        p = self.calculate(self.series.X)
        epsilon_list = self.get_epsilon_list(p)
        self.mse = sum([e ** 2 for e in epsilon_list]) / self.series.n
        result = \
            f"""    Формула функции: phi(x) = a * x^b
    Коэффициенты: a={round(a, 4)}, b={round(b, 4)}
    Значение функции в точках: {p.round(4)}
    Отклонения: {epsilon_list.round(4)}
    Сумма отклонений: {round(sum(epsilon_list), 4)}
    Среднеквадратичное отклонение: {round(np.sqrt(self.mse), 4)}
        """
        return result
