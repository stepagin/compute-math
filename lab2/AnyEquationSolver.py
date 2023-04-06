from InputManager import InputManager


class EquationSolver:
    @staticmethod
    def solve(equation):
        result = EquationSolver.Half_Division_Method(equation)
        if result is None:
            print("Не удалось найти корень уравнения.")
        else:
            print("Корень уравнения:", result)

    @staticmethod
    def Half_Division_Method(equation):

        if len(equation.get_var_list()) != 1:
            print("Для решения методом половинного деления необходимо, "
                  "чтобы в уравнении участвовало только одно неизвестное.")
            print("Неизвестные в данном уравнении:", equation.get_var_list())
            return

        k = equation.get_var_list()[0]
        a = InputManager.float_input(f"\tВведите левый край начального приближения: {k} = ")
        b = InputManager.float_input(f"\tВведите правый край начального приближения: {k} = ")

        while not (equation.calculate({k: a}) * equation.calculate({k: b}) < 0):
            print("Необходимо, чтобы значения функции на концах отрезков были разных знаков!")
            if not InputManager.yes_or_no_input("Ввести концы заново?"):
                return
            a = InputManager.float_input(f"\tВведите левый край начального приближения: {k} = ")
            b = InputManager.float_input(f"\tВведите правый край начального приближения: {k} = ")

        epsilon = 0.001
        print("Хотите ввести точность? По умолчанию epsilon равно 10^-3.")
        if InputManager.yes_or_no_input("Ввести epsilon?"):
            epsilon = InputManager.float_input("epsilon=")

        if not equation.calculate({k: a}) < 0:
            a, b = b, a
        while not abs(a - b) < epsilon:
            mid = (a + b) / 2
            if equation.calculate({k: mid}) < 0:
                a = mid
            else:
                b = mid

        return (a + b) / 2
