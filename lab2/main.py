import numpy as np

from AnyEquationSolver import EquationSolver
from EquationManager import Equation
from Exceptions import InvalidAlgebraicEquationException
from InputManager import InputManager
from PreparedEquationManager import PreparedEquation
from PreparedSystemManager import PreparedSystem


def variants_function_solver():
    result = None
    variants = ["3x^3 + 1.7x^2 − 15.42x + 6.89",
                "x • sin(x) - 1",
                "e^sin(x) • ln(|x|) - 1.4",
                "arcsin(e^(-x)) - 0.3",
                "tg(x/2 • sin(x))"]
    values = [PreparedEquation(lambda x: 3 * x ** 3 + 1.7 * x ** 2 - 15.42 * x + 6.89,
                               derivative_func=lambda x: -15.42 + 3.4 * x + 9 * x ** 2),
              PreparedEquation(lambda x: x * np.sin(x) - 1,
                               derivative_func=lambda x: np.sin(x) + x * np.cos(x)),
              PreparedEquation(lambda x: np.exp(np.sin(x)) * np.log(abs(x)) - 1.4,
                               derivative_func=lambda x: np.exp(np.sin(x)) * (
                                       abs(x) * np.log(abs(x)) * np.cos(x) + np.sign(x)) / abs(x)),
              PreparedEquation(lambda x: np.arcsin(np.exp(-x)) - 0.3,
                               derivative_func=lambda x: -np.exp(-x) / np.sqrt(1 - np.exp(-2 * x))),
              PreparedEquation(lambda x: np.tan(x / 2 * np.sin(x)),
                               derivative_func=lambda x: (np.sin(x) + x * np.cos(x)) /
                                                         (2 * np.cos(x * np.sin(x) / 2) ** 2))]

    chosen_equation = InputManager.multiple_choice_input(variants, values, "Выберите функцию:")
    try:
        result = chosen_equation.solve()
    except ValueError:
        print("Возможно, функция не определена в некоторых точках.\n"
              "Попробуйте ввести другие концы отрезка.")
    if result is None:
        print("Не удалось найти корень уравнения.")
    else:
        print("------------РЕШЕНИЕ------------")
        print("Найденный корень уравнения:", round(result, 5))
        print("Значение функции в точке: ", round(chosen_equation.calculate(result), 9))
        print("Количество итераций:", chosen_equation.iterations)
        if InputManager.yes_or_no_input("Показать график функции?"):
            chosen_equation.draw_graphic(dot_x=result, dot_y=chosen_equation.calculate(result))


def any_function_solver():
    try:
        line = InputManager.algebraic_expression_input("Введите уравнение: ")
        eq = Equation(line)
        EquationSolver.solve(eq)
    except InvalidAlgebraicEquationException:
        print("Не удалось распарсить выражение")
        print('Попробуйте не использовать знак "=".')


def system_solver():
    name1 = "┌ 0.1x^2 + x + 0.2y^2 - 0.3" + "\n" + \
            "└ 0.2x^2 + y + 0.1xy - 0.7" + "\n" + \
            "Пример корня: (0.20 0.67)"
    ps1 = PreparedSystem([lambda x, y: 0.1 * x ** 2 + x + 0.2 * y ** 2 - 0.3,
                          lambda x, y: 0.2 * x ** 2 + y + 0.1 * x * y - 0.7],
                         derivative_funcs=[lambda x, y: np.array([-0.2 * x, -0.4 * y]),
                                           lambda x, y: np.array([-0.4 * x - 0.1 * y, -0.1 * x])])
    name2 = "┌ sin(x)" + "\n" + \
            "└ xy/20 - 0.5" + "\n" + \
            "Пример корня: (6.28 1.59)"
    ps2 = PreparedSystem([lambda x, y: np.sin(x),
                          lambda x, y: x * y / 20 - 0.5],
                         derivative_funcs=[lambda x, y: np.array([np.cos(x), 0]),
                                           lambda x, y: np.array([y / 20, x / 20])])
    chosen_system = InputManager.multiple_choice_input([name1, name2], [ps1, ps2], "Выберите систему:")

    result = chosen_system.solve()
    if result is None:
        print("Не удалось найти корень системы.")
    else:
        print("------------РЕШЕНИЕ------------")
        print("Найденный корень системы:", result)
        print("Значение системы в этой точке:", chosen_system.calculate(*result))
        print("Количество итераций:", chosen_system.iterations)
        print("Вектор погрешностей:", chosen_system.get_error_rate())


if __name__ == '__main__':
    variants = ["Выбрать функцию и метод из предложенных",
                "Ввести произвольную функцию и решить её методом половинного деления",
                "Выбрать систему уравнений из предложенных и решить её методом простых итераций"]
    values = [variants_function_solver, any_function_solver, system_solver]

    chosen_variant = InputManager.multiple_choice_input(variants, values, "Чем хотите себя побаловать?")

    chosen_variant()
